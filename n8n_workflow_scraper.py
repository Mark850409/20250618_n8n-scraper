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
from typing import Tuple, List
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
        
    def get_workflows_list(self, rows: int, category: str) -> Tuple[List[str], int]:
        """
        取得所有 workflows 列表 (完整分頁)

        Args:
            rows: 每頁筆數
            category: Workflow 類別 (如果是「全部」則不帶 category 參數)

        Returns:
            Tuple[List[str], int]: (所有 workflow IDs 列表, 總筆數)
        """
        all_workflow_ids = []
        total_workflows = 0
        current_page = 1

        try:
            # 先取得第一頁來獲取總筆數
            if category == "全部":
                url = f"https://n8n.io/api/product-api/workflows/search?rows={rows}&page={current_page}"
            else:
                url = f"https://n8n.io/api/product-api/workflows/search?rows={rows}&category={category}&page={current_page}"

            logger.info(f"正在請求第一頁 workflows 列表: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            data = response.json()

            # 取得總筆數
            if 'totalWorkflows' in data:
                total_workflows = data['totalWorkflows']
            elif 'total' in data:
                total_workflows = data['total']
            else:
                # 如果沒有總筆數資訊，嘗試從當前頁面推估
                if 'workflows' in data and len(data['workflows']) == rows:
                    logger.warning("無法取得總筆數，將逐頁爬取直到沒有更多資料")
                    total_workflows = -1  # 標記為未知
                else:
                    total_workflows = len(data.get('workflows', []))

            # 計算總頁數
            if total_workflows > 0:
                total_pages = (total_workflows + rows - 1) // rows  # 向上取整
                logger.info(f"總共有 {total_workflows} 個 workflows，分為 {total_pages} 頁")
            else:
                total_pages = -1  # 未知頁數，需要逐頁爬取
                logger.info("總頁數未知，將逐頁爬取")

            # 處理第一頁的資料
            if 'workflows' in data:
                for workflow in data['workflows']:
                    if 'id' in workflow:
                        all_workflow_ids.append(str(workflow['id']))

            logger.info(f"第 {current_page} 頁找到 {len(data.get('workflows', []))} 個 workflows")

            # 如果總頁數已知，爬取剩餘頁面
            if total_pages > 1:
                for page in range(2, total_pages + 1):
                    # 延遲 2-3 秒避免被識別為機器人
                    time.sleep(2.5)

                    if category == "全部":
                        url = f"https://n8n.io/api/product-api/workflows/search?rows={rows}&page={page}"
                    else:
                        url = f"https://n8n.io/api/product-api/workflows/search?rows={rows}&category={category}&page={page}"

                    logger.info(f"正在請求第 {page} 頁 workflows 列表: {url}")
                    response = self.session.get(url, timeout=30)
                    response.raise_for_status()

                    page_data = response.json()

                    if 'workflows' in page_data:
                        page_workflow_ids = []
                        for workflow in page_data['workflows']:
                            if 'id' in workflow:
                                page_workflow_ids.append(str(workflow['id']))

                        all_workflow_ids.extend(page_workflow_ids)
                        logger.info(f"第 {page} 頁找到 {len(page_workflow_ids)} 個 workflows")

                        # 如果這一頁沒有資料，提前結束
                        if not page_workflow_ids:
                            logger.info(f"第 {page} 頁沒有資料，停止爬取")
                            break

            # 如果總頁數未知，繼續逐頁爬取直到沒有更多資料
            elif total_pages == -1:
                current_page = 2
                while True:
                    # 延遲 2-3 秒避免被識別為機器人
                    time.sleep(2.5)

                    if category == "全部":
                        url = f"https://n8n.io/api/product-api/workflows/search?rows={rows}&page={current_page}"
                    else:
                        url = f"https://n8n.io/api/product-api/workflows/search?rows={rows}&category={category}&page={current_page}"

                    logger.info(f"正在請求第 {current_page} 頁 workflows 列表: {url}")
                    response = self.session.get(url, timeout=30)
                    response.raise_for_status()

                    page_data = response.json()

                    if 'workflows' in page_data and page_data['workflows']:
                        page_workflow_ids = []
                        for workflow in page_data['workflows']:
                            if 'id' in workflow:
                                page_workflow_ids.append(str(workflow['id']))

                        if page_workflow_ids:
                            all_workflow_ids.extend(page_workflow_ids)
                            logger.info(f"第 {current_page} 頁找到 {len(page_workflow_ids)} 個 workflows")
                            current_page += 1
                        else:
                            logger.info(f"第 {current_page} 頁沒有有效資料，停止爬取")
                            break
                    else:
                        logger.info(f"第 {current_page} 頁沒有 workflows 資料，停止爬取")
                        break

                # 更新實際總筆數
                total_workflows = len(all_workflow_ids)

            logger.info(f"完成所有頁面爬取，總共找到 {len(all_workflow_ids)} 個 workflows")
            return all_workflow_ids, total_workflows

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
    
    def scrape_workflows(self, rows: int, category: str) -> Tuple[str, str]:
        """
        主要的爬取功能 - 自動爬取所有頁面

        Args:
            rows: 每頁筆數
            category: Workflow 類別

        Returns:
            Tuple[str, str]: (狀態訊息, 詳細結果)
        """
        try:
            # 驗證輸入參數
            if rows <= 0:
                return "❌ 錯誤", "參數錯誤：rows 必須大於 0"

            if not category.strip():
                return "❌ 錯誤", "參數錯誤：category 不能為空"

            # 建立下載目錄
            category_name = "all" if category == "全部" else category
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            download_dir = f"workflows_{category_name}_{timestamp}"
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)

            # 切換到下載目錄
            original_dir = os.getcwd()
            os.chdir(download_dir)

            try:
                # 取得所有 workflows 列表
                logger.info("開始取得 workflows 列表...")
                workflow_ids, total_workflows = self.get_workflows_list(rows, category)

                if not workflow_ids:
                    return "⚠️ 警告", "沒有找到任何 workflows"

                logger.info(f"準備下載 {len(workflow_ids)} 個 workflows")

                # 下載每個 workflow
                success_count = 0
                failed_count = 0
                results = []

                results.append(f"📊 爬取統計資訊:")
                results.append(f"   - 總筆數: {total_workflows}")
                results.append(f"   - 每頁筆數: {rows}")
                results.append(f"   - 類別: {category}")
                results.append(f"   - 實際取得: {len(workflow_ids)} 個 workflows")
                results.append("")
                results.append("🔄 開始下載 workflows...")
                results.append("")

                for i, workflow_id in enumerate(workflow_ids, 1):
                    results.append(f"[{i}/{len(workflow_ids)}] 正在處理 workflow: {workflow_id}")

                    if self.download_workflow(workflow_id):
                        success_count += 1
                        results.append(f"✅ 成功下載: {workflow_id}.json")
                    else:
                        failed_count += 1
                        results.append(f"❌ 下載失敗: {workflow_id}")

                    # 延遲 1 秒避免過度請求
                    if i < len(workflow_ids):  # 最後一個不需要延遲
                        time.sleep(1)

                    # 每下載 10 個顯示一次進度
                    if i % 10 == 0:
                        progress = (i / len(workflow_ids)) * 100
                        results.append(f"📈 進度: {progress:.1f}% ({i}/{len(workflow_ids)})")

                # 生成結果報告
                status = f"✅ 完成" if failed_count == 0 else f"⚠️ 部分完成"

                results.append("")
                results.append("=" * 50)
                results.append("📋 最終統計報告")
                results.append("=" * 50)
                results.append(f"總共處理: {len(workflow_ids)} 個 workflows")
                results.append(f"成功下載: {success_count} 個")
                results.append(f"下載失敗: {failed_count} 個")
                results.append(f"成功率: {(success_count/len(workflow_ids)*100):.1f}%")
                results.append(f"檔案儲存位置: {os.path.abspath('.')}")

                summary = "\n".join(results)

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

    def process_request(rows, category):
        """處理使用者請求"""
        return scraper.scrape_workflows(rows, category)

    # 建立 Gradio 介面 - 使用相容性更好的 Interface
    interface = gr.Interface(
        fn=process_request,
        inputs=[
            gr.Number(
                label="每頁筆數 (rows)",
                value=20,
                minimum=1,
                maximum=100,
                info="建議設定 20-50，數值越大單次請求時間越長但總請求次數越少"
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
                value="全部",
                info="選擇要下載的 workflow 類別，「全部」會下載所有類別"
            )
        ],
        outputs=[
            gr.Textbox(label="執行狀態"),
            gr.Textbox(label="詳細結果", lines=20)
        ],
        title="🔧 n8n Workflow 完整下載器",
        description="""
        透過此工具可以**完整下載**指定類別的所有 n8n workflows

        ## 📝 使用說明
        1. **每頁筆數**: 設定每次 API 請求的 workflow 數量 (1-100)
           - 建議值：20-50 (平衡請求效率與穩定性)
           - 數值越大：單次請求時間越長，但總請求次數越少
        2. **Workflow 類別**: 從下拉選單選擇要搜尋的類別
           - 選擇「全部」可下載所有類別的 workflows
        3. 點擊「Submit」按鈕開始執行
        4. 系統會**自動計算總頁數**並**完整爬取所有頁面**
        5. 下載的檔案會儲存在 `workflows_{類別}_{時間戳記}` 資料夾中

        ## 📂 可用類別
        全部 (不限類別), AI, SecOps, Sales, IT Ops, Marketing, Engineering, DevOps, Building Blocks, Design, Finance, HR, Other, Product, Support

        ## 🚀 新功能特色
        - ✅ **完整分頁爬取**: 自動取得總筆數並計算頁數，確保下載所有 workflows
        - ✅ **智慧延遲機制**: 頁面間延遲 2.5 秒，workflow 下載間延遲 1 秒，避免被識別為機器人
        - ✅ **進度追蹤**: 即時顯示爬取進度和統計資訊
        - ✅ **錯誤處理**: 完善的錯誤處理和重試機制
        - ✅ **時間戳記命名**: 避免資料夾名稱衝突

        ## ⚠️ 注意事項
        - 選擇「全部」時會下載**所有類別**的 workflows，數量可能很大
        - 系統會自動延遲請求，避免過度請求被封鎖
        - 請確保網路連線穩定，大量下載時請耐心等待
        - 下載時間取決於 workflows 總數量和網路速度
        """,

    )

    return interface

if __name__ == "__main__":
    # 建立並啟動 Gradio 介面
    interface = create_gradio_interface()
    try:
        interface.launch(
            server_name="0.0.0.0",
            server_port=7861,
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
                server_port=7861,
                share=False,
                debug=False,
                inbrowser=False,
                quiet=True
            )
        except Exception as e2:
            logger.error(f"備用配置也失敗: {e2}")
            print(f"❌ 無法啟動應用: {e2}")
