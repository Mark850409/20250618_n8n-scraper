#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
n8n Workflow Scraper with Gradio GUI
功能：透過 Gradio 介面下載 n8n workflows
"""

import requests
import json
import os
import time
import gradio as gr
from typing import Tuple, List, Dict, Any
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class N8nWorkflowScraper:
    """n8n Workflow 下載器"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def get_workflows_list(self, rows: int, category: str, page: int) -> List[str]:
        """
        取得 workflows 列表

        Args:
            rows: 每頁筆數
            category: Workflow 類別 (如果是「全部」則不帶 category 參數)
            page: 起始頁數

        Returns:
            List[str]: workflow IDs 列表
        """
        # 如果選擇「全部」，則不帶 category 參數
        if category == "全部":
            url = f"https://n8n.io/api/product-api/workflows/search?rows={rows}&page={page}"
        else:
            url = f"https://n8n.io/api/product-api/workflows/search?rows={rows}&category={category}&page={page}"
        
        try:
            logger.info(f"正在請求 workflows 列表: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # 提取 workflow IDs
            workflow_ids = []
            if 'workflows' in data:
                for workflow in data['workflows']:
                    if 'id' in workflow:
                        workflow_ids.append(str(workflow['id']))
            
            logger.info(f"找到 {len(workflow_ids)} 個 workflows")
            return workflow_ids
            
        except requests.exceptions.RequestException as e:
            logger.error(f"請求 workflows 列表失敗: {e}")
            raise Exception(f"無法取得 workflows 列表: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析失敗: {e}")
            raise Exception(f"回應格式錯誤: {e}")
        except Exception as e:
            logger.error(f"未知錯誤: {e}")
            raise Exception(f"取得 workflows 列表時發生錯誤: {e}")
    
    def download_workflow(self, workflow_id: str) -> bool:
        """
        下載單個 workflow
        
        Args:
            workflow_id: workflow ID
            
        Returns:
            bool: 是否下載成功
        """
        url = f"https://api.n8n.io/api/workflows/templates/{workflow_id}"
        filename = f"{workflow_id}.json"
        
        try:
            logger.info(f"正在下載 workflow: {workflow_id}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # 檢查回應是否為 JSON
            try:
                full_response = response.json()
            except json.JSONDecodeError:
                logger.warning(f"Workflow {workflow_id} 回應不是有效的 JSON")
                return False

            # 只取得 workflow 節點下的內容
            if 'workflow' in full_response:
                workflow_data = full_response['workflow']
            else:
                logger.warning(f"Workflow {workflow_id} 回應中沒有找到 'workflow' 節點")
                # 如果沒有 workflow 節點，保存整個回應
                workflow_data = full_response

            # 儲存檔案
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(workflow_data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"成功下載並儲存: {filename}")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"下載 workflow {workflow_id} 失敗: {e}")
            return False
        except Exception as e:
            logger.error(f"儲存 workflow {workflow_id} 失敗: {e}")
            return False
    
    def scrape_workflows(self, rows: int, category: str, page: int) -> Tuple[str, str]:
        """
        主要的爬取功能
        
        Args:
            rows: 每頁筆數
            category: Workflow 類別
            page: 起始頁數
            
        Returns:
            Tuple[str, str]: (狀態訊息, 詳細結果)
        """
        try:
            # 驗證輸入參數
            if rows <= 0 or page < 1:
                return "❌ 錯誤", "參數錯誤：rows 必須大於 0，page 必須大於等於 1"
            
            if not category.strip():
                return "❌ 錯誤", "參數錯誤：category 不能為空"
            
            # 建立下載目錄
            category_name = "all" if category == "全部" else category
            download_dir = f"workflows_{category_name}_{page}"
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
            
            # 切換到下載目錄
            original_dir = os.getcwd()
            os.chdir(download_dir)
            
            try:
                # 取得 workflows 列表
                workflow_ids = self.get_workflows_list(rows, category, page)
                
                if not workflow_ids:
                    return "⚠️ 警告", "沒有找到任何 workflows"
                
                # 下載每個 workflow
                success_count = 0
                failed_count = 0
                results = []
                
                for i, workflow_id in enumerate(workflow_ids, 1):
                    results.append(f"[{i}/{len(workflow_ids)}] 正在處理 workflow: {workflow_id}")
                    
                    if self.download_workflow(workflow_id):
                        success_count += 1
                        results.append(f"✅ 成功下載: {workflow_id}.json")
                    else:
                        failed_count += 1
                        results.append(f"❌ 下載失敗: {workflow_id}")
                    
                    # 延遲 1 秒
                    if i < len(workflow_ids):  # 最後一個不需要延遲
                        time.sleep(1)
                
                # 生成結果報告
                status = f"✅ 完成" if failed_count == 0 else f"⚠️ 部分完成"
                summary = f"總共處理 {len(workflow_ids)} 個 workflows\n"
                summary += f"成功下載: {success_count} 個\n"
                summary += f"下載失敗: {failed_count} 個\n"
                summary += f"檔案儲存位置: {os.path.abspath('.')}\n\n"
                summary += "詳細結果:\n" + "\n".join(results)
                
                return status, summary
                
            finally:
                # 恢復原始目錄
                os.chdir(original_dir)
                
        except Exception as e:
            logger.error(f"爬取過程發生錯誤: {e}")
            return "❌ 錯誤", f"執行過程中發生錯誤: {str(e)}"

def create_gradio_interface():
    """建立 Gradio 介面"""
    scraper = N8nWorkflowScraper()

    def process_request(rows, category, page):
        """處理使用者請求"""
        return scraper.scrape_workflows(rows, category, page)

    # 建立 Gradio 介面 - 使用相容性更好的 Interface
    interface = gr.Interface(
        fn=process_request,
        inputs=[
            gr.Number(
                label="每頁筆數 (rows)",
                value=10,
                minimum=1,
                maximum=100
            ),
            gr.Dropdown(
                label="Workflow 類別 (category)",
                choices=[
                    "全部",
                    "AI",
                    "SecOps",
                    "Sales",
                    "IT Ops",
                    "Marketing",
                    "Engineering",
                    "DevOps",
                    "Building Blocks",
                    "Design",
                    "Finance",
                    "HR",
                    "Other",
                    "Product",
                    "Support"
                ],
                value="全部"
            ),
            gr.Number(
                label="起始頁數 (page)",
                value=1,
                minimum=1
            )
        ],
        outputs=[
            gr.Textbox(label="執行狀態"),
            gr.Textbox(label="詳細結果", lines=15)
        ],
        title="🔧 n8n Workflow 下載器",
        description="""
        透過此工具可以批量下載 n8n workflows

        ## 📝 使用說明
        1. **每頁筆數**: 設定要下載的 workflow 數量 (1-100)
        2. **Workflow 類別**: 從下拉選單選擇要搜尋的類別 (選擇「全部」可下載所有類別)
        3. **起始頁數**: 設定從第幾頁開始 (預設從第 1 頁開始)
        4. 點擊「Submit」按鈕執行
        5. 下載的檔案會儲存在 `workflows_{類別}_{頁數}` 資料夾中

        ## 📂 可用類別
        全部 (不限類別), AI, SecOps, Sales, IT Ops, Marketing, Engineering, DevOps, Building Blocks, Design, Finance, HR, Other, Product, Support

        ## ⚠️ 注意事項
        - 選擇「全部」時會下載所有類別的 workflows
        - 每次請求間會自動延遲 1 秒，避免過度請求
        - 請確保網路連線穩定
        - 大量下載時請耐心等待
        """,
        allow_flagging="never"
    )

    return interface

if __name__ == "__main__":
    # 建立並啟動 Gradio 介面
    interface = create_gradio_interface()
    try:
        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            share=False,
            debug=False,
            inbrowser=False,
            quiet=True
        )
    except Exception as e:
        logger.error(f"Gradio 啟動失敗: {e}")
        print(f"❌ Gradio 啟動失敗: {e}")
        print("嘗試使用備用配置...")
        try:
            interface.launch(
                server_name="127.0.0.1",
                server_port=7860,
                share=False,
                debug=False,
                inbrowser=False,
                quiet=True
            )
        except Exception as e2:
            logger.error(f"備用配置也失敗: {e2}")
            print(f"❌ 無法啟動應用: {e2}")
