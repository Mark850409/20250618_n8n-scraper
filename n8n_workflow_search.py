#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
n8n Workflow 智能搜尋與教學生成系統
基於 LangChain + ChromaDB 的向量搜尋引擎
"""

import os
import json
import shutil
from typing import List, Dict, Any, Tuple
from datetime import datetime
import chromadb
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class N8nWorkflowSearcher:
    """n8n Workflow 搜尋與教學生成系統"""
    
    def __init__(self, workflows_dir: str = ".", chroma_db_path: str = "./chroma_db"):
        """
        初始化搜尋系統
        
        Args:
            workflows_dir: workflow JSON 檔案所在目錄
            chroma_db_path: ChromaDB 資料庫路徑
        """
        self.workflows_dir = workflows_dir
        self.chroma_db_path = chroma_db_path
        self.selected_dir = "selected_workflows"
        
        # 建立必要目錄
        os.makedirs(self.selected_dir, exist_ok=True)
        os.makedirs(chroma_db_path, exist_ok=True)
        
        # 初始化 Embedding 模型
        logger.info("正在初始化 Embedding 模型...")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        # 初始化 ChromaDB
        self.chroma_client = chromadb.PersistentClient(path=chroma_db_path)
        self.collection_name = "n8n_workflows"
        
        # 初始化向量資料庫
        self.vectorstore = None
        self.init_vectorstore()
    
    def init_vectorstore(self):
        """初始化向量資料庫"""
        try:
            # 嘗試載入現有的向量資料庫
            self.vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=self.embeddings,
                persist_directory=self.chroma_db_path
            )
            
            # 檢查是否有資料
            collection = self.chroma_client.get_collection(self.collection_name)
            count = collection.count()
            
            if count == 0:
                logger.info("向量資料庫為空，開始建立索引...")
                self.build_index()
            else:
                logger.info(f"載入現有向量資料庫，包含 {count} 筆資料")
                
        except Exception as e:
            logger.info("建立新的向量資料庫...")
            self.build_index()
    
    def extract_workflow_info(self, workflow_data: Dict[str, Any], filename: str) -> Dict[str, Any]:
        """
        從 workflow JSON 中提取關鍵資訊
        
        Args:
            workflow_data: workflow JSON 資料
            filename: 檔案名稱
            
        Returns:
            Dict: 提取的工作流程資訊
        """
        # 基本資訊
        workflow_id = workflow_data.get('id', 'unknown')
        workflow_name = workflow_data.get('name', 'Unnamed Workflow')
        
        # 節點資料直接在根層級（因為我們已經只保存 workflow 內容）
        nodes = workflow_data.get('nodes', [])
        
        # 提取節點結構
        node_structure = []
        for node in nodes:
            node_name = node.get('name', 'Unknown Node')
            node_type = node.get('type', 'unknown')
            node_structure.append(f"{node_name}（{node_type}）")
        
        # 生成描述文字（用於搜尋）
        description_parts = [
            workflow_name,
            f"工作流程包含 {len(nodes)} 個節點",
            "節點類型：" + "、".join([node.get('type', 'unknown') for node in nodes[:5]])
        ]
        
        # 根據節點類型推測功能
        node_types = [node.get('type', '') for node in nodes]
        if any('trigger' in nt.lower() for nt in node_types):
            description_parts.append("包含觸發器")
        if any('http' in nt.lower() for nt in node_types):
            description_parts.append("包含HTTP請求")
        if any('email' in nt.lower() for nt in node_types):
            description_parts.append("包含郵件功能")
        if any('discord' in nt.lower() for nt in node_types):
            description_parts.append("包含Discord通知")
        if any('schedule' in nt.lower() for nt in node_types):
            description_parts.append("包含定時排程")
        
        return {
            'id': workflow_id,
            'name': workflow_name,
            'filename': filename,
            'description': "；".join(description_parts),
            'node_structure': node_structure,
            'node_count': len(nodes),
            'node_types': node_types,
            'raw_data': workflow_data
        }
    
    def build_index(self):
        """建立向量資料庫索引"""
        logger.info("開始掃描 workflow 檔案...")
        
        documents = []
        
        # 掃描所有 JSON 檔案
        json_files = []
        for root, dirs, files in os.walk(self.workflows_dir):
            for file in files:
                if file.endswith('.json') and not file.startswith('.'):
                    json_files.append(os.path.join(root, file))
        
        logger.info(f"找到 {len(json_files)} 個 JSON 檔案")
        
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    workflow_data = json.load(f)
                
                # 提取工作流程資訊
                workflow_info = self.extract_workflow_info(workflow_data, os.path.basename(json_file))
                
                # 建立文檔內容（用於向量搜尋）
                doc_content = f"""
                工作流程名稱：{workflow_info['name']}
                描述：{workflow_info['description']}
                節點結構：{'; '.join(workflow_info['node_structure'][:10])}
                """
                
                # 建立 Document 並包含 metadata
                doc_metadata = {
                    'filename': workflow_info['filename'],
                    'workflow_id': str(workflow_info['id']),
                    'name': workflow_info['name'],
                    'description': workflow_info['description'],
                    'node_structure': str(workflow_info['node_structure']),  # 轉為字串
                    'node_count': workflow_info['node_count'],
                    'file_path': json_file
                }
                documents.append(Document(page_content=doc_content, metadata=doc_metadata))
                
            except Exception as e:
                logger.warning(f"處理檔案 {json_file} 時發生錯誤: {e}")
                continue
        
        if documents:
            # 建立向量資料庫
            self.vectorstore = Chroma.from_documents(
                documents=documents,
                embedding=self.embeddings,
                collection_name=self.collection_name,
                persist_directory=self.chroma_db_path
            )
            
            logger.info(f"成功建立向量索引，包含 {len(documents)} 筆資料")
        else:
            logger.error("沒有找到有效的 workflow 檔案")
    
    def search_workflows(self, query: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """
        搜尋相似的工作流程
        
        Args:
            query: 搜尋查詢
            top_k: 回傳前 N 筆結果
            
        Returns:
            List: 搜尋結果列表，包含 (metadata, similarity_score)
        """
        if not self.vectorstore:
            logger.error("向量資料庫未初始化")
            return []
        
        try:
            # 執行相似度搜尋
            results = self.vectorstore.similarity_search_with_score(query, k=top_k)

            search_results = []
            for doc, score in results:
                # 取得 metadata
                metadata = doc.metadata
                # ChromaDB 使用餘弦距離，距離越小相似度越高
                # 將距離轉換為相似度分數 (0-1)
                if score <= 1.0:
                    similarity = 1.0 - score  # 距離轉相似度
                else:
                    # 處理可能的異常距離值
                    similarity = 1.0 / (1.0 + score)

                # 確保相似度在合理範圍內
                similarity = max(0.0, min(1.0, similarity))
                search_results.append((metadata, similarity))

            # 按相似度排序（高到低）
            search_results.sort(key=lambda x: x[1], reverse=True)

            return search_results
            
        except Exception as e:
            logger.error(f"搜尋時發生錯誤: {e}")
            return []

    def display_search_results(self, results: List[Tuple[Dict[str, Any], float]], query: str):
        """
        顯示搜尋結果

        Args:
            results: 搜尋結果
            query: 原始查詢
        """
        print(f"\n🔍 正在匹配最相近的工作流程...")
        print(f"📝 搜尋關鍵字：{query}")
        print("=" * 80)

        if not results:
            print("❌ 沒有找到相關的工作流程")
            return

        for i, (metadata, similarity) in enumerate(results, 1):
            print(f"\n[{i}] 來源檔案：{metadata['filename']}")
            print(f"🧠 相似度：{similarity:.4f}")
            print(f"🔧 工作流程名稱：{metadata['name']}")
            print(f"📌 標籤：workflow")
            print(f"📝 自定標籤：{metadata['name']}")
            print(f"📖 描述：{metadata['description']}")
            print(f"\n🧩 Workflow 結構：")
            print()

            # 顯示節點結構
            node_structure_str = metadata.get('node_structure', '[]')
            try:
                # 嘗試解析字串為列表
                import ast
                if isinstance(node_structure_str, str):
                    node_structure = ast.literal_eval(node_structure_str)
                else:
                    node_structure = node_structure_str
            except:
                node_structure = []

            for j, node in enumerate(node_structure[:10]):  # 最多顯示10個節點
                if j == 0:
                    print(f"Trigger：{node}")
                else:
                    print(f"{node}")

            if len(node_structure) > 10:
                print(f"... 還有 {len(node_structure) - 10} 個節點")

            print()

    def generate_tutorial_markdown(self, metadata: Dict[str, Any], file_path: str) -> str:
        """
        生成教學說明 Markdown 檔案

        Args:
            metadata: 工作流程 metadata
            file_path: 原始 JSON 檔案路徑

        Returns:
            str: 生成的 Markdown 內容
        """
        # 讀取原始 JSON 檔案以獲取詳細資訊
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                workflow_data = json.load(f)
        except Exception as e:
            logger.error(f"讀取檔案 {file_path} 失敗: {e}")
            workflow_data = {}

        # 節點資料直接在根層級
        nodes = workflow_data.get('nodes', [])

        # 生成 Markdown 內容
        markdown_content = f"""# {metadata['name']} - 工作流程教學

## 📋 基本資訊

- **工作流程名稱**: {metadata['name']}
- **工作流程 ID**: {metadata.get('workflow_id', 'N/A')}
- **節點數量**: {metadata.get('node_count', 0)}
- **來源檔案**: {metadata['filename']}
- **生成時間**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📖 工作流程描述

{metadata['description']}

"""

        # 生成詳細設定步驟
        setup_steps = self.generate_setup_steps(nodes)

        # 添加建議用途
        markdown_content += f"""{setup_steps}

## 💡 建議用途與延伸應用

### 適用場景
{self.generate_use_cases(nodes)}

### 延伸應用建議
{self.generate_extensions(nodes)}

## 🔧 設定注意事項

1. **認證設定**: 請確保所有需要認證的節點都已正確設定 API 金鑰或認證資訊
2. **觸發條件**: 檢查觸發器的設定是否符合您的需求
3. **錯誤處理**: 建議為關鍵節點添加錯誤處理邏輯
4. **測試執行**: 在正式使用前，請先進行測試執行

## 📚 相關資源

- [n8n 官方文檔](https://docs.n8n.io/)
- [n8n 社群範例](https://n8n.io/workflows/)
- [節點參考文檔](https://docs.n8n.io/integrations/)

---
*此教學檔案由 n8n Workflow 智能搜尋系統自動生成*
"""

        return markdown_content

    def sanitize_filename(self, filename: str) -> str:
        """
        清理檔案名稱，移除不合法的字元

        Args:
            filename: 原始檔案名稱

        Returns:
            str: 清理後的檔案名稱
        """
        import re
        # 移除或替換不合法的檔案名稱字元
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'[🤖🚘📲💡🔧📌📝📖🧩]', '', filename)  # 移除 emoji
        filename = filename.strip()
        # 限制長度
        if len(filename) > 50:
            filename = filename[:50]
        return filename

    def get_node_description(self, node_type: str) -> str:
        """
        根據節點類型回傳功能描述

        Args:
            node_type: 節點類型

        Returns:
            str: 節點功能描述
        """
        descriptions = {
            'n8n-nodes-base.scheduleTrigger': '定時觸發器，可設定定期執行的時間排程',
            'n8n-nodes-base.httpRequest': 'HTTP 請求節點，用於發送 GET/POST 等 HTTP 請求',
            'n8n-nodes-base.webhook': 'Webhook 觸發器，接收外部 HTTP 請求觸發工作流程',
            'n8n-nodes-base.emailSend': '郵件發送節點，用於發送電子郵件通知',
            'n8n-nodes-base.discord': 'Discord 整合節點，可發送訊息到 Discord 頻道',
            'n8n-nodes-base.slack': 'Slack 整合節點，可發送訊息到 Slack 頻道',
            'n8n-nodes-base.telegram': 'Telegram Bot 節點，可發送訊息到 Telegram',
            'n8n-nodes-base.code': '程式碼執行節點，可執行 JavaScript 程式碼',
            'n8n-nodes-base.function': '函數節點，執行自定義 JavaScript 函數',
            'n8n-nodes-base.if': '條件判斷節點，根據條件決定執行路徑',
            'n8n-nodes-base.switch': '分支節點，根據不同條件執行不同路徑',
            'n8n-nodes-base.merge': '合併節點，將多個資料流合併',
            'n8n-nodes-base.set': '設定節點，用於設定或修改資料',
            'n8n-nodes-base.wait': '等待節點，暫停工作流程執行一段時間',
            'n8n-nodes-base.stickyNote': '便利貼節點，用於添加註解和說明',
            '@n8n/n8n-nodes-langchain.chainLlm': 'LangChain LLM 節點，整合大型語言模型',
        }

        return descriptions.get(node_type, '自定義節點，請參考 n8n 文檔了解詳細功能')

    def generate_use_cases(self, nodes: List[Dict[str, Any]]) -> str:
        """
        根據節點類型生成使用場景建議

        Args:
            nodes: 節點列表

        Returns:
            str: 使用場景描述
        """
        node_types = [node.get('type', '') for node in nodes]
        use_cases = []

        if any('schedule' in nt.lower() for nt in node_types):
            use_cases.append("- 定期自動化任務（如每日報告、定時備份）")

        if any('http' in nt.lower() for nt in node_types):
            use_cases.append("- API 資料整合與同步")
            use_cases.append("- 第三方服務整合")

        if any('email' in nt.lower() for nt in node_types):
            use_cases.append("- 自動化郵件通知系統")
            use_cases.append("- 報告與警告發送")

        if any('discord' in nt.lower() or 'slack' in nt.lower() for nt in node_types):
            use_cases.append("- 團隊協作通知")
            use_cases.append("- 系統監控警告")

        if any('webhook' in nt.lower() for nt in node_types):
            use_cases.append("- 即時事件響應")
            use_cases.append("- 外部系統整合觸發")

        return "\n".join(use_cases) if use_cases else "- 通用自動化工作流程"

    def generate_extensions(self, nodes: List[Dict[str, Any]]) -> str:
        """
        生成延伸應用建議

        Args:
            nodes: 節點列表

        Returns:
            str: 延伸應用建議
        """
        extensions = [
            "- 添加錯誤處理和重試機制",
            "- 整合更多通知管道（如 LINE、WeChat）",
            "- 加入資料持久化存儲",
            "- 實作條件分支處理不同情況",
            "- 添加日誌記錄和監控功能"
        ]

        return "\n".join(extensions)

    def generate_setup_steps(self, nodes: List[Dict[str, Any]]) -> str:
        """
        根據實際節點生成詳細的設定步驟

        Args:
            nodes: 節點列表

        Returns:
            str: 設定步驟說明
        """
        steps = []
        step_count = 1

        # 分析工作流程的實際結構，生成對應的操作步驟
        for i, node in enumerate(nodes, 1):
            node_name = node.get('name', f'節點 {i}')
            node_type = node.get('type', 'unknown')
            parameters = node.get('parameters', {})

            steps.append(f"### 步驟 {step_count}：設定 {node_name}")
            step_count += 1

            # 根據節點類型生成具體的設定步驟
            if 'trigger' in node_type.lower():
                if 'schedule' in node_type.lower():
                    steps.append("1. 在工作流程的畫布上，拖曳「Schedule Trigger」節點")
                    steps.append("2. 點擊節點，並設定觸發頻率：")
                    steps.append("   - **Mode**: 選擇「Every Day」")
                    steps.append("   - **Time**: 設定您希望觸發的時間，例如「08:00」")
                    steps.append("3. 點擊「Execute Node」來測試這個節點，確保它能正常運作")
                elif 'telegram' in node_type.lower():
                    steps.append("1. 拖曳「Telegram Trigger」節點到工作流程畫布上")
                    steps.append("2. 設定 Telegram Bot 觸發器：")
                    if 'updates' in parameters:
                        updates = parameters.get('updates', [])
                        if 'message' in updates:
                            steps.append("   - **Updates**: 選擇「message」來接收訊息")
                        if 'callback_query' in updates:
                            steps.append("   - **Updates**: 選擇「callback_query」來接收按鈕回調")
                    steps.append("3. 在憑證管理中設定 Telegram Bot Token")
                elif 'webhook' in node_type.lower():
                    steps.append("1. 拖曳「Webhook」節點到工作流程畫布上")
                    steps.append("2. 設定 Webhook 參數：")
                    steps.append("   - **HTTP Method**: 選擇適當的方法（GET/POST）")
                    steps.append("   - **Path**: 設定 webhook 路徑")
                    steps.append("3. 儲存並啟用工作流程以獲得 webhook URL")
                elif 'gmail' in node_type.lower():
                    steps.append("1. 拖曳「Gmail Trigger」節點到工作流程畫布上")
                    steps.append("2. 設定 Gmail 觸發器：")
                    steps.append("   - **Event**: 選擇觸發事件（如新郵件）")
                    steps.append("3. 在憑證管理中設定 Gmail OAuth2 認證")

            elif 'httpRequest' in node_type:
                steps.append("1. 拖曳「HTTP Request」節點到工作流程畫布上")
                steps.append("2. 點擊節點，然後設定：")
                if 'method' in parameters:
                    method = parameters.get('method', 'GET')
                    steps.append(f"   - **Method**: 選擇「{method}」")
                if 'url' in parameters:
                    steps.append("   - **URL**: 輸入 API 端點 URL")
                if 'sendHeaders' in parameters or 'headerParameters' in parameters:
                    steps.append("   - **Headers**: 設定必要的請求標頭")
                if 'sendBody' in parameters:
                    steps.append("   - **Body**: 設定請求主體內容")
                steps.append("3. 測試節點確保 API 請求正常運作")

            elif 'telegram' in node_type.lower() and 'trigger' not in node_type.lower():
                steps.append("1. 拖曳「Telegram」節點到工作流程畫布上")
                steps.append("2. 設定 Telegram 訊息發送：")
                if 'text' in parameters:
                    steps.append("   - **Text**: 設定要發送的訊息內容")
                if 'chatId' in parameters:
                    steps.append("   - **Chat ID**: 設定目標聊天室 ID")
                if 'resource' in parameters and parameters.get('resource') == 'file':
                    steps.append("   - **Resource**: 選擇「file」來下載檔案")
                    if 'fileId' in parameters:
                        steps.append("   - **File ID**: 設定要下載的檔案 ID")
                steps.append("3. 在憑證管理中設定 Telegram Bot Token")

            elif 'googleSheets' in node_type:
                steps.append("1. 拖曳「Google Sheets」節點到工作流程畫布上")
                steps.append("2. 設定 Google Sheets 操作：")
                if 'operation' in parameters:
                    operation = parameters.get('operation', 'read')
                    steps.append(f"   - **Operation**: 選擇「{operation}」")
                if 'documentId' in parameters:
                    steps.append("   - **Document ID**: 輸入 Google Sheets 文件 ID")
                if 'sheetName' in parameters:
                    steps.append("   - **Sheet Name**: 選擇要操作的工作表")
                steps.append("3. 在憑證管理中設定 Google Sheets OAuth2 認證")

            elif 'code' in node_type:
                steps.append("1. 拖曳「Code」節點到工作流程畫布上")
                steps.append("2. 設定 JavaScript 程式碼：")
                steps.append("   - **JavaScript Code**: 輸入自定義的處理邏輯")
                steps.append("3. 測試程式碼確保邏輯正確")

            elif 'set' in node_type:
                steps.append("1. 拖曳「Set」節點到工作流程畫布上")
                steps.append("2. 設定資料處理：")
                if 'assignments' in parameters:
                    steps.append("   - **Assignments**: 設定要修改或新增的資料欄位")
                steps.append("3. 測試節點確保資料處理正確")

            elif 'switch' in node_type:
                steps.append("1. 拖曳「Switch」節點到工作流程畫布上")
                steps.append("2. 設定條件分支：")
                if 'rules' in parameters:
                    steps.append("   - **Rules**: 設定判斷條件和對應的輸出路徑")
                steps.append("3. 測試各個分支路徑")

            elif 'wait' in node_type:
                steps.append("1. 拖曳「Wait」節點到工作流程畫布上")
                steps.append("2. 設定等待時間：")
                if 'amount' in parameters:
                    amount = parameters.get('amount', 1)
                    steps.append(f"   - **Amount**: 設定等待時間為 {amount} 秒")
                steps.append("3. 根據需要調整等待時間")

            elif 'merge' in node_type:
                steps.append("1. 拖曳「Merge」節點到工作流程畫布上")
                steps.append("2. 設定資料合併方式：")
                if 'mode' in parameters:
                    mode = parameters.get('mode', 'append')
                    steps.append(f"   - **Mode**: 選擇「{mode}」合併模式")
                steps.append("3. 連接多個輸入節點到此合併節點")

            elif 'splitOut' in node_type:
                steps.append("1. 拖曳「Split Out」節點到工作流程畫布上")
                steps.append("2. 設定資料分割：")
                if 'fieldToSplitOut' in parameters:
                    field = parameters.get('fieldToSplitOut', '')
                    steps.append(f"   - **Field to Split Out**: 設定要分割的欄位「{field}」")
                steps.append("3. 測試資料分割結果")

            elif 'langchain' in node_type.lower():
                steps.append("1. 拖曳 LangChain 相關節點到工作流程畫布上")
                steps.append("2. 設定 AI 模型參數：")
                if 'model' in parameters:
                    model = parameters.get('model', {})
                    if isinstance(model, dict) and 'value' in model:
                        steps.append(f"   - **Model**: 選擇「{model['value']}」")
                if 'text' in parameters:
                    steps.append("   - **Text**: 設定輸入文本")
                if 'messages' in parameters:
                    steps.append("   - **Messages**: 設定對話訊息")
                steps.append("3. 在憑證管理中設定相應的 API 金鑰")

            else:
                # 通用設定步驟
                steps.append(f"1. 拖曳「{node_name}」節點到工作流程畫布上")
                steps.append("2. 點擊節點進行設定：")
                if parameters:
                    main_params = list(parameters.keys())[:3]  # 顯示前3個主要參數
                    for param in main_params:
                        steps.append(f"   - **{param}**: 根據需求設定此參數")
                steps.append("3. 測試節點確保設定正確")

            steps.append("")  # 添加空行分隔

        if not steps:
            return ""

        return f"""## 🛠️ 詳細設定步驟

{chr(10).join(steps)}"""

    def save_selected_workflow(self, metadata: Dict[str, Any], index: int = 0) -> bool:
        """
        儲存選中的工作流程

        Args:
            metadata: 工作流程 metadata
            index: 選擇的索引

        Returns:
            bool: 是否儲存成功
        """
        try:
            source_file = metadata['file_path']
            original_filename = metadata['filename']
            workflow_name = metadata['name']

            # 清理檔案名稱中的特殊字元
            safe_workflow_name = self.sanitize_filename(workflow_name)
            safe_original_name = os.path.splitext(original_filename)[0]  # 移除 .json 副檔名

            # 複製 JSON 檔案到 selected_workflows 目錄，使用新的命名格式
            new_json_filename = f"workflow_{safe_original_name}.json"
            dest_json = os.path.join(self.selected_dir, new_json_filename)
            shutil.copy2(source_file, dest_json)

            # 生成教學 Markdown 檔案，使用工作流程名稱
            tutorial_filename = f"workflow_{safe_workflow_name}.md"
            tutorial_path = os.path.join(self.selected_dir, tutorial_filename)

            tutorial_content = self.generate_tutorial_markdown(metadata, source_file)

            with open(tutorial_path, 'w', encoding='utf-8') as f:
                f.write(tutorial_content)

            print(f"\n✅ 成功儲存工作流程！")
            print(f"📁 JSON 檔案：{dest_json}")
            print(f"📚 教學檔案：{tutorial_path}")

            return True

        except Exception as e:
            logger.error(f"儲存工作流程時發生錯誤: {e}")
            print(f"❌ 儲存失敗：{e}")
            return False

    def interactive_search(self):
        """
        互動式搜尋介面
        """
        print("=" * 80)
        print("🤖 n8n Workflow 智能搜尋與教學生成系統")
        print("=" * 80)
        print("💡 請描述您想要實作的工作流程，例如：")
        print("   • 每天早上寄出氣象通知")
        print("   • 監控伺服器異常發 Discord 警告")
        print("   • 定時備份資料庫並發送報告")
        print("=" * 80)

        while True:
            try:
                # 取得使用者輸入
                query = input("\n🔍 請輸入您的需求描述（輸入 'quit' 結束）: ").strip()

                if query.lower() in ['quit', 'exit', '退出', 'q']:
                    print("👋 感謝使用！")
                    break

                if not query:
                    print("❌ 請輸入有效的描述")
                    continue

                # 執行搜尋
                print(f"\n🔍 正在搜尋相關工作流程...")
                results = self.search_workflows(query, top_k=5)

                if not results:
                    print("❌ 沒有找到相關的工作流程，請嘗試其他關鍵字")
                    continue

                # 顯示搜尋結果
                self.display_search_results(results, query)

                # 讓使用者選擇
                while True:
                    try:
                        choice = input(f"\n📥 請選擇要儲存的工作流程編號 (1-{len(results)})，或輸入 'back' 重新搜尋: ").strip()

                        if choice.lower() in ['back', 'b', '返回']:
                            break

                        choice_idx = int(choice) - 1
                        if 0 <= choice_idx < len(results):
                            metadata, _ = results[choice_idx]  # similarity 不需要使用

                            # 確認儲存
                            confirm = input(f"確定要儲存「{metadata['name']}」嗎？(y/n): ").strip().lower()
                            if confirm in ['y', 'yes', '是', 'ok']:
                                if self.save_selected_workflow(metadata, choice_idx + 1):
                                    print("\n🎉 工作流程已成功儲存到 selected_workflows/ 目錄")
                                break
                            else:
                                print("❌ 已取消儲存")
                        else:
                            print(f"❌ 請輸入 1-{len(results)} 之間的數字")

                    except ValueError:
                        print("❌ 請輸入有效的數字")
                    except KeyboardInterrupt:
                        print("\n👋 程式已中斷")
                        return

            except KeyboardInterrupt:
                print("\n👋 程式已中斷")
                break
            except Exception as e:
                logger.error(f"執行過程中發生錯誤: {e}")
                print(f"❌ 發生錯誤：{e}")

def main():
    """主程式入口"""
    try:
        # 檢查是否有 workflow 檔案
        current_dir = "."
        json_files = []
        for _, _, files in os.walk(current_dir):
            for file in files:
                if file.endswith('.json') and not file.startswith('.'):
                    json_files.append(file)

        if not json_files:
            print("❌ 在當前目錄中沒有找到 JSON 檔案")
            print("💡 請確保您的 workflow JSON 檔案在當前目錄或子目錄中")
            return

        print(f"📁 找到 {len(json_files)} 個 JSON 檔案")

        # 初始化搜尋系統
        searcher = N8nWorkflowSearcher()

        # 開始互動式搜尋
        searcher.interactive_search()

    except Exception as e:
        logger.error(f"程式執行失敗: {e}")
        print(f"❌ 程式執行失敗：{e}")

if __name__ == "__main__":
    main()
