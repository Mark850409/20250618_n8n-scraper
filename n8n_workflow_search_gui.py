#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
n8n Workflow 智能搜尋與教學生成系統 - Gradio GUI 版本
基於 LangChain + ChromaDB 的向量搜尋引擎，提供網頁介面
"""

import os
import json
import shutil
import gradio as gr
from typing import List, Dict, Any, Tuple
from datetime import datetime
import chromadb
import requests
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 可選依賴的導入
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    logger.warning("python-dotenv 未安裝，將跳過 .env 文件載入")

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("openai 套件未安裝，OpenAI 功能將不可用")

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("google-generativeai 套件未安裝，Gemini 功能將不可用")

try:
    from langchain_huggingface import HuggingFaceEmbeddings
    LANGCHAIN_HUGGINGFACE_AVAILABLE = True
except ImportError:
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        LANGCHAIN_HUGGINGFACE_AVAILABLE = True
    except ImportError:
        LANGCHAIN_HUGGINGFACE_AVAILABLE = False
        logger.warning("HuggingFace embeddings 未安裝，將使用簡單文字搜尋")

try:
    from langchain_community.vectorstores import Chroma
    from langchain_core.documents import Document
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    logger.warning("langchain 套件未安裝，將使用簡單文字搜尋")

# 載入環境變數
if DOTENV_AVAILABLE:
    load_dotenv()

class AITutorialGenerator:
    """AI 教學生成器"""

    def __init__(self):
        """初始化 AI 教學生成器"""
        self.provider = os.getenv('AI_PROVIDER', 'openai').lower()
        self.max_tokens = int(os.getenv('MAX_TOKENS', '2000'))
        self.temperature = float(os.getenv('TEMPERATURE', '0.7'))
        self.available = False

        # 初始化對應的 AI 服務
        self.init_ai_service()

    def init_ai_service(self):
        """初始化 AI 服務"""
        try:
            if self.provider == 'openai':
                if not OPENAI_AVAILABLE:
                    logger.error("OpenAI 套件未安裝，無法使用 OpenAI 服務")
                    return

                api_key = os.getenv('OPENAI_API_KEY')
                if not api_key:
                    logger.error("未設定 OPENAI_API_KEY")
                    return

                base_url = os.getenv('OPENAI_BASE_URL', 'https://api.openai.com/v1')
                self.model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
                self.openai_client = OpenAI(api_key=api_key, base_url=base_url)
                self.available = True
                logger.info(f"已初始化 OpenAI 服務，模型：{self.model}")

            elif self.provider == 'gemini':
                if not GEMINI_AVAILABLE:
                    logger.error("Gemini 套件未安裝，無法使用 Gemini 服務")
                    return

                api_key = os.getenv('GEMINI_API_KEY')
                if api_key:
                    genai.configure(api_key=api_key)
                    self.model = os.getenv('GEMINI_MODEL', 'gemini-pro')
                    self.available = True
                    logger.info(f"已初始化 Gemini 服務，模型：{self.model}")
                else:
                    logger.error("未設定 GEMINI_API_KEY")

            elif self.provider == 'ollama':
                self.base_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
                self.model = os.getenv('OLLAMA_MODEL', 'llama2')
                self.available = True
                logger.info(f"已初始化 Ollama 服務，模型：{self.model}")

            else:
                logger.error(f"不支援的 AI 提供商：{self.provider}")

        except Exception as e:
            logger.error(f"初始化 AI 服務時發生錯誤：{e}")
            self.available = False

    def generate_tutorial(self, question: str) -> str:
        """
        生成 n8n 節點教學

        Args:
            question: 用戶問題

        Returns:
            str: 生成的教學內容
        """
        if not self.available:
            return """❌ AI 教學生成功能不可用

可能的原因：
1. 缺少必要的 AI 套件 (openai, google-generativeai)
2. 未設定 API 金鑰
3. AI 服務初始化失敗

請檢查環境變數設定或安裝必要的依賴套件。"""

        try:
            # 構建提示詞
            prompt = self.build_prompt(question)

            # 根據提供商調用對應的 API
            if self.provider == 'openai':
                return self.call_openai(prompt)
            elif self.provider == 'gemini':
                return self.call_gemini(prompt)
            elif self.provider == 'ollama':
                return self.call_ollama(prompt)
            else:
                return "❌ 不支援的 AI 提供商"

        except Exception as e:
            logger.error(f"生成教學時發生錯誤：{e}")
            return f"❌ 生成教學時發生錯誤：{str(e)}"

    def build_prompt(self, question: str) -> str:
        """構建提示詞"""
        return f"""你是一個專業的 n8n 工作流程自動化專家。請根據用戶的問題，提供詳細、實用的 n8n 節點設定教學。

用戶問題：{question}

請按照以下格式回答：

## 📋 節點概述
簡要介紹相關節點的功能和用途

## 🛠️ 詳細設定步驟
提供逐步的設定指南，包括：
1. 如何添加節點
2. 必要的參數設定
3. 認證設定（如果需要）
4. 測試方法

## 💡 實用範例
提供一個具體的使用場景和設定範例

## ⚠️ 注意事項
列出常見問題和解決方案

## 🔗 相關資源
提供相關的官方文檔連結

請用繁體中文回答，內容要詳細且實用。"""

    def call_openai(self, prompt: str) -> str:
        """調用 OpenAI API"""
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一個專業的 n8n 工作流程自動化專家，擅長提供詳細的技術教學。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"調用 OpenAI API 時發生錯誤：{e}")
            return f"❌ OpenAI API 調用失敗：{str(e)}"

    def call_gemini(self, prompt: str) -> str:
        """調用 Gemini API"""
        try:
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=self.max_tokens,
                    temperature=self.temperature
                )
            )
            return response.text
        except Exception as e:
            logger.error(f"調用 Gemini API 時發生錯誤：{e}")
            return f"❌ Gemini API 調用失敗：{str(e)}"

    def call_ollama(self, prompt: str) -> str:
        """調用 Ollama API"""
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": self.temperature,
                        "num_predict": self.max_tokens
                    }
                }
            )
            response.raise_for_status()
            return response.json()['response']
        except Exception as e:
            logger.error(f"調用 Ollama API 時發生錯誤：{e}")
            return f"❌ Ollama API 調用失敗：{str(e)}"

class N8nWorkflowSearcherGUI:
    """n8n Workflow 搜尋與教學生成系統 - GUI 版本"""
    
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
        self.embeddings = None

        if LANGCHAIN_HUGGINGFACE_AVAILABLE:
            try:
                self.embeddings = HuggingFaceEmbeddings(
                    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
                    model_kwargs={'device': 'cpu'}
                )
                logger.info("成功載入 HuggingFace Embedding 模型")
            except Exception as e:
                logger.warning(f"無法載入 HuggingFace 模型，使用簡單的文字匹配: {e}")
                self.embeddings = None
        else:
            logger.info("HuggingFace embeddings 不可用，使用簡單文字搜尋模式")
        
        # 初始化 ChromaDB
        self.chroma_client = chromadb.PersistentClient(path=chroma_db_path)
        self.collection_name = "n8n_workflows"

        # 儲存搜尋結果供後續使用
        self.current_results = []

        # 簡單搜尋模式的資料儲存
        self.simple_workflows = []

        # 初始化向量資料庫
        self.vectorstore = None
        self.init_vectorstore()
    
    def init_vectorstore(self):
        """初始化向量資料庫"""
        if self.embeddings is None:
            logger.info("使用簡單文字搜尋模式")
            self.vectorstore = None
            self.build_simple_index()
            return

        try:
            # 每次啟動都重新建立索引以確保資料是最新的
            logger.info("重新掃描並建立向量資料庫索引...")

            # 先清除現有的 collection（如果存在）
            try:
                self.chroma_client.delete_collection(self.collection_name)
                logger.info("已清除舊的向量資料庫")
            except Exception:
                logger.info("沒有找到舊的向量資料庫，將建立新的")

            # 重新建立索引
            self.build_index()

        except Exception as e:
            logger.error(f"初始化向量資料庫時發生錯誤: {e}")
            logger.info("建立新的向量資料庫...")
            self.build_index()

    def build_simple_index(self):
        """建立簡單的文字搜尋索引"""
        logger.info("重新掃描並建立簡單搜尋索引...")

        # 清空現有索引
        self.simple_workflows = []

        # 掃描所有 JSON 檔案
        json_files = []
        for root, _, files in os.walk(self.workflows_dir):
            for file in files:
                if file.endswith('.json') and not file.startswith('.'):
                    json_files.append(os.path.join(root, file))

        logger.info(f"找到 {len(json_files)} 個 JSON 檔案")

        # 使用字典來去重，以檔案路徑為鍵
        workflows_dict = {}

        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    workflow_data = json.load(f)

                # 提取工作流程資訊
                workflow_info = self.extract_workflow_info(workflow_data, os.path.basename(json_file))
                workflow_info['file_path'] = json_file

                # 使用檔案路徑作為唯一鍵來去重
                workflows_dict[json_file] = workflow_info

            except Exception as e:
                logger.warning(f"處理檔案 {json_file} 時發生錯誤: {e}")
                continue

        # 將去重後的工作流程轉換為列表
        self.simple_workflows = list(workflows_dict.values())
        logger.info(f"成功建立簡單搜尋索引，包含 {len(self.simple_workflows)} 筆資料")

        # 調試：顯示前幾個工作流程的資訊和檢查重複
        logger.info("檢查工作流程列表是否有重複...")
        file_paths = [w['file_path'] for w in self.simple_workflows]
        unique_paths = set(file_paths)
        if len(file_paths) != len(unique_paths):
            logger.warning(f"發現重複項目！總數: {len(file_paths)}, 唯一數: {len(unique_paths)}")
            # 找出重複的路徑
            from collections import Counter
            path_counts = Counter(file_paths)
            duplicates = [path for path, count in path_counts.items() if count > 1]
            logger.warning(f"重複的檔案路徑: {duplicates}")
        else:
            logger.info("工作流程列表無重複項目")

        for i, workflow in enumerate(self.simple_workflows[:3]):
            logger.info(f"工作流程 {i+1}: {workflow['name']}")
            logger.info(f"  檔案路徑: {workflow['file_path']}")
            logger.info(f"  描述: {workflow['description'][:100]}...")
            logger.info(f"  節點類型 (前5個): {workflow['node_types'][:5]}")
            logger.info(f"  所有節點類型: {workflow['node_types']}")
    
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
        
        # 節點資料直接在根層級
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
        if not LANGCHAIN_AVAILABLE:
            logger.warning("LangChain 不可用，跳過向量索引建立")
            return

        logger.info("開始掃描 workflow 檔案...")

        documents = []

        # 掃描所有 JSON 檔案
        json_files = []
        for root, _, files in os.walk(self.workflows_dir):
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
                    'node_structure': str(workflow_info['node_structure']),
                    'node_count': workflow_info['node_count'],
                    'file_path': json_file
                }
                documents.append(Document(page_content=doc_content, metadata=doc_metadata))

            except Exception as e:
                logger.warning(f"處理檔案 {json_file} 時發生錯誤: {e}")
                continue

        if documents:
            try:
                # 建立向量資料庫
                self.vectorstore = Chroma.from_documents(
                    documents=documents,
                    embedding=self.embeddings,
                    collection_name=self.collection_name,
                    persist_directory=self.chroma_db_path
                )
                logger.info(f"成功建立向量索引，包含 {len(documents)} 筆資料")

            except Exception as e:
                error_msg = str(e).lower()
                if "already exists" in error_msg or "collection" in error_msg:
                    logger.info(f"集合已存在，嘗試載入現有集合: {e}")
                    try:
                        # 嘗試載入現有的向量資料庫
                        self.vectorstore = Chroma(
                            collection_name=self.collection_name,
                            embedding_function=self.embeddings,
                            persist_directory=self.chroma_db_path
                        )
                        logger.info("成功載入現有向量資料庫")
                    except Exception as load_error:
                        logger.error(f"載入現有向量資料庫失敗: {load_error}")
                        # 嘗試重置並重新建立
                        try:
                            logger.info("嘗試重置向量資料庫...")
                            self.chroma_client.delete_collection(self.collection_name)
                            self.vectorstore = Chroma.from_documents(
                                documents=documents,
                                embedding=self.embeddings,
                                collection_name=self.collection_name,
                                persist_directory=self.chroma_db_path
                            )
                            logger.info(f"重置後成功建立向量索引，包含 {len(documents)} 筆資料")
                        except Exception as reset_error:
                            logger.error(f"重置向量資料庫失敗: {reset_error}")
                            raise
                else:
                    logger.error(f"建立向量資料庫時發生未知錯誤: {e}")
                    raise
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
        if self.vectorstore is None:
            # 使用簡單文字搜尋
            return self.simple_text_search(query, top_k)

        try:
            # 執行相似度搜尋
            results = self.vectorstore.similarity_search_with_score(query, k=top_k)

            search_results = []
            for doc, score in results:
                # 取得 metadata
                metadata = doc.metadata
                # ChromaDB 使用餘弦距離，距離越小相似度越高
                if score <= 1.0:
                    similarity = 1.0 - score
                else:
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

    def simple_text_search(self, query: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        """
        簡單的文字搜尋

        Args:
            query: 搜尋查詢
            top_k: 回傳前 N 筆結果

        Returns:
            List: 搜尋結果列表，包含 (metadata, similarity_score)
        """
        logger.info(f"執行簡單文字搜尋，查詢：'{query}'，資料庫包含 {len(self.simple_workflows)} 筆資料")

        query_lower = query.lower()
        search_results = []
        seen_workflows = set()  # 用於去重

        # 將查詢分解為關鍵字
        query_keywords = [kw.strip() for kw in query_lower.split() if kw.strip()]

        for workflow in self.simple_workflows:
            # 使用檔案路徑作為唯一標識符來避免重複
            workflow_id = workflow['file_path']
            if workflow_id in seen_workflows:
                continue

            # 計算文字匹配度
            score = 0.0

            # 檢查名稱匹配
            name_lower = workflow['name'].lower()
            for keyword in query_keywords:
                if keyword in name_lower:
                    score += 0.5

            # 檢查描述匹配
            desc_lower = workflow['description'].lower()
            for keyword in query_keywords:
                if keyword in desc_lower:
                    score += 0.3

            # 檢查節點類型匹配（避免重複計分）
            node_type_matches = set()
            for node_type in workflow['node_types']:
                node_type_lower = node_type.lower()
                for keyword in query_keywords:
                    if keyword in node_type_lower and keyword not in node_type_matches:
                        score += 0.2
                        node_type_matches.add(keyword)

            # 檢查檔案名匹配
            filename_lower = workflow['filename'].lower()
            for keyword in query_keywords:
                if keyword in filename_lower:
                    score += 0.1

            # 特殊關鍵字匹配（避免重複計分）
            special_matches = {
                'telegram': ['telegram'],
                'bot': ['telegram', 'bot'],
                'discord': ['discord'],
                'email': ['email', 'mail'],
                'weather': ['weather', 'openweathermap'],
                'schedule': ['schedule', 'trigger'],
                'http': ['http', 'request'],
                'api': ['http', 'api'],
                'notification': ['discord', 'telegram', 'email'],
                '通知': ['discord', 'telegram', 'email'],
                '機器人': ['telegram', 'bot'],
                '天氣': ['weather', 'openweathermap'],
                '排程': ['schedule', 'trigger'],
                '定時': ['schedule', 'trigger'],
                '自動回覆': ['telegram', 'bot'],
                '回覆': ['telegram', 'bot']
            }

            special_score_added = set()
            for keyword in query_keywords:
                if keyword in special_matches:
                    for match_type in special_matches[keyword]:
                        if match_type not in special_score_added:
                            for node_type in workflow['node_types']:
                                if match_type.lower() in node_type.lower():
                                    score += 0.4
                                    special_score_added.add(match_type)
                                    break

            # 如果有任何匹配，加入結果
            if score > 0:
                search_results.append((workflow, score))
                seen_workflows.add(workflow_id)
                logger.info(f"找到匹配：{workflow['name']} (分數: {score:.2f})")

        # 按相似度排序（高到低）
        search_results.sort(key=lambda x: x[1], reverse=True)

        # 確保返回足夠的結果，如果不足則補充其他工作流程
        if len(search_results) < top_k:
            # 創建一個去重的工作流程列表
            unique_workflows = []
            seen_paths = set()
            for workflow in self.simple_workflows:
                if workflow['file_path'] not in seen_paths:
                    unique_workflows.append(workflow)
                    seen_paths.add(workflow['file_path'])

            for workflow in unique_workflows:
                if len(search_results) >= top_k:
                    break
                workflow_id = workflow['file_path']
                if workflow_id not in seen_workflows:
                    search_results.append((workflow, 0.0))
                    seen_workflows.add(workflow_id)
                    logger.info(f"補充結果：{workflow['name']} (分數: 0.00)")

        logger.info(f"搜尋完成，找到 {len(search_results)} 個結果")
        return search_results[:top_k]

    def format_search_results(self, results: List[Tuple[Dict[str, Any], float]], query: str) -> str:
        """
        格式化搜尋結果為 HTML 顯示

        Args:
            results: 搜尋結果
            query: 原始查詢

        Returns:
            str: 格式化的 HTML 結果
        """
        if not results:
            return "❌ 沒有找到相關的工作流程，請嘗試其他關鍵字"

        html_content = f"""
        <div style="font-family: Arial, sans-serif;">
            <h3>🔍 搜尋結果</h3>
            <p><strong>搜尋關鍵字：</strong>{query}</p>
            <p><strong>找到 {len(results)} 個相關工作流程</strong></p>
            <hr>
        """

        for i, (metadata, similarity) in enumerate(results, 1):
            # 解析節點結構
            node_structure_str = metadata.get('node_structure', '[]')
            try:
                import ast
                if isinstance(node_structure_str, str):
                    node_structure = ast.literal_eval(node_structure_str)
                else:
                    node_structure = node_structure_str
            except:
                node_structure = []

            # 顯示節點結構（前10個）
            nodes_display = ""
            for j, node in enumerate(node_structure[:10]):
                if j == 0:
                    nodes_display += f"<li><strong>Trigger：</strong>{node}</li>"
                else:
                    nodes_display += f"<li>{node}</li>"

            if len(node_structure) > 10:
                nodes_display += f"<li><em>... 還有 {len(node_structure) - 10} 個節點</em></li>"

            html_content += f"""
            <div style="border: 1px solid #ddd; padding: 15px; margin: 10px 0; border-radius: 5px;">
                <h4>[{i}] {metadata['name']}</h4>
                <p><strong>🧠 相似度：</strong>{similarity:.4f}</p>
                <p><strong>📁 來源檔案：</strong>{metadata['filename']}</p>
                <p><strong>📖 描述：</strong>{metadata['description']}</p>
                <p><strong>🧩 Workflow 結構：</strong></p>
                <ul style="margin-left: 20px;">
                    {nodes_display}
                </ul>
            </div>
            """

        html_content += "</div>"
        return html_content

    def search_and_display(self, query: str, top_k: int = 5) -> Tuple[str, gr.update]:
        """
        執行搜尋並返回結果，同時更新下拉選單

        Args:
            query: 搜尋查詢
            top_k: 回傳前 N 筆結果

        Returns:
            Tuple: (搜尋結果HTML, 更新的下拉選單)
        """
        if not query.strip():
            return "請輸入搜尋關鍵字", gr.update(choices=[], value=None)

        # 執行搜尋
        self.current_results = self.search_workflows(query, top_k)

        # 格式化結果
        html_results = self.format_search_results(self.current_results, query)

        # 準備下拉選單選項
        if self.current_results:
            choices = [f"[{i}] {metadata['name']}" for i, (metadata, _) in enumerate(self.current_results, 1)]
            dropdown_update = gr.update(choices=choices, value=None, visible=True)
        else:
            dropdown_update = gr.update(choices=[], value=None, visible=False)

        return html_results, dropdown_update

    def save_selected_workflow(self, selected_workflow: str) -> tuple[str, str]:
        """
        儲存選中的工作流程並返回教學文件內容

        Args:
            selected_workflow: 選中的工作流程（格式：[1] 工作流程名稱）

        Returns:
            tuple: (儲存結果訊息, 教學文件內容)
        """
        if not selected_workflow or not self.current_results:
            return "❌ 請先搜尋並選擇一個工作流程", ""

        try:
            # 解析選擇的索引
            index = int(selected_workflow.split(']')[0].replace('[', '')) - 1

            if index < 0 or index >= len(self.current_results):
                return "❌ 選擇的工作流程索引無效", ""

            metadata, _ = self.current_results[index]

            # 儲存工作流程
            success, tutorial_content = self.save_workflow_files(metadata)

            if success:
                save_message = f"✅ 成功儲存工作流程「{metadata['name']}」！\n📁 檔案已儲存到 selected_workflows/ 目錄"
                return save_message, tutorial_content
            else:
                return "❌ 儲存工作流程時發生錯誤", ""

        except Exception as e:
            logger.error(f"儲存工作流程時發生錯誤: {e}")
            return f"❌ 儲存失敗：{str(e)}", ""

    def save_workflow_files(self, metadata: Dict[str, Any]) -> tuple[bool, str]:
        """
        儲存工作流程檔案（JSON 和 Markdown）

        Args:
            metadata: 工作流程 metadata

        Returns:
            tuple: (是否儲存成功, 教學內容)
        """
        try:
            source_file = metadata['file_path']
            original_filename = metadata['filename']
            workflow_name = metadata['name']

            # 清理檔案名稱中的特殊字元
            safe_workflow_name = self.sanitize_filename(workflow_name)
            safe_original_name = os.path.splitext(original_filename)[0]

            # 複製 JSON 檔案到 selected_workflows 目錄
            new_json_filename = f"workflow_{safe_original_name}.json"
            dest_json = os.path.join(self.selected_dir, new_json_filename)
            shutil.copy2(source_file, dest_json)

            # 生成教學 Markdown 檔案
            tutorial_filename = f"workflow_{safe_workflow_name}.md"
            tutorial_path = os.path.join(self.selected_dir, tutorial_filename)

            tutorial_content = self.generate_tutorial_markdown(metadata, source_file)

            with open(tutorial_path, 'w', encoding='utf-8') as f:
                f.write(tutorial_content)

            logger.info(f"成功儲存工作流程：JSON={dest_json}, MD={tutorial_path}")
            return True, tutorial_content

        except Exception as e:
            logger.error(f"儲存工作流程檔案時發生錯誤: {e}")
            return False, ""

    def sanitize_filename(self, filename: str) -> str:
        """清理檔案名稱，移除不合法的字元"""
        import re
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'[🤖🚘📲💡🔧📌📝📖🧩]', '', filename)
        filename = filename.strip()
        if len(filename) > 50:
            filename = filename[:50]
        return filename

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

    def generate_use_cases(self, nodes: List[Dict[str, Any]]) -> str:
        """根據節點類型生成使用場景建議"""
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
        """生成延伸應用建議"""
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
                    main_params = list(parameters.keys())[:3]
                    for param in main_params:
                        steps.append(f"   - **{param}**: 根據需求設定此參數")
                steps.append("3. 測試節點確保設定正確")

            steps.append("")  # 添加空行分隔

        if not steps:
            return ""

        return f"""## 🛠️ 詳細設定步驟

{chr(10).join(steps)}"""

def create_gradio_interface():
    """創建 Gradio 介面"""

    # 初始化搜尋系統和 AI 教學生成器
    searcher = N8nWorkflowSearcherGUI()
    ai_generator = AITutorialGenerator()

    # 創建 Gradio 介面
    with gr.Blocks(
        title="n8n Workflow 智能搜尋與教學生成系統",
        theme=gr.themes.Base(
            primary_hue="blue",
            secondary_hue="gray",
            neutral_hue="slate"
        ).set(
            body_background_fill="*neutral_950",
            body_text_color="*neutral_100",
            background_fill_primary="*neutral_900",
            background_fill_secondary="*neutral_800",
            border_color_primary="*neutral_700",
            block_background_fill="*neutral_900",
            block_border_color="*neutral_700",
            input_background_fill="*neutral_800",
            input_border_color="*neutral_600",
            button_primary_background_fill="*primary_600",
            button_primary_background_fill_hover="*primary_700",
            button_secondary_background_fill="*neutral_700",
            button_secondary_background_fill_hover="*neutral_600"
        ),
        css="""
        .gradio-container {
            max-width: 1200px !important;
            background-color: #0f172a !important;
            color: #f1f5f9 !important;
        }
        .search-results {
            max-height: 600px;
            overflow-y: auto;
            background-color: #1e293b !important;
            border: 1px solid #475569 !important;
            border-radius: 8px;
            padding: 15px;
        }
        .tutorial-content {
            max-height: 800px;
            overflow-y: auto;
            border: 1px solid #475569 !important;
            border-radius: 8px;
            padding: 20px;
            background-color: #1e293b !important;
            color: #f1f5f9 !important;
        }
        .tutorial-content h1 {
            color: #60a5fa !important;
            border-bottom: 2px solid #3b82f6 !important;
            padding-bottom: 10px;
        }
        .tutorial-content h2 {
            color: #94a3b8 !important;
            margin-top: 25px;
        }
        .tutorial-content h3 {
            color: #cbd5e1 !important;
            margin-top: 20px;
        }
        .tutorial-content code {
            background-color: #374151 !important;
            color: #fbbf24 !important;
            padding: 2px 4px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
        }
        .tutorial-content ul, .tutorial-content ol {
            color: #e2e8f0 !important;
        }
        .tutorial-content li {
            margin-bottom: 5px;
        }
        .tutorial-content p {
            color: #e2e8f0 !important;
            line-height: 1.6;
        }
        .tutorial-content strong {
            color: #fbbf24 !important;
        }
        .tutorial-content em {
            color: #a78bfa !important;
        }
        /* 修復搜尋結果的顯示 */
        .search-results h3, .search-results h4 {
            color: #60a5fa !important;
        }
        .search-results p {
            color: #e2e8f0 !important;
        }
        .search-results strong {
            color: #fbbf24 !important;
        }
        .search-results ul, .search-results li {
            color: #cbd5e1 !important;
        }
        /* 輸入框和按鈕樣式 */
        .gr-textbox, .gr-dropdown {
            background-color: #374151 !important;
            border-color: #6b7280 !important;
            color: #f9fafb !important;
        }
        .gr-button {
            background-color: #4f46e5 !important;
            border-color: #4f46e5 !important;
            color: white !important;
        }
        .gr-button:hover {
            background-color: #4338ca !important;
        }
        """
    ) as demo:

        gr.Markdown("""
        # 🤖 n8n Workflow 智能搜尋與教學生成系統

        專業的 n8n 工作流程搜尋與 AI 教學生成平台
        """)

        # 創建頁籤
        with gr.Tabs():
            # 第一個頁籤：工作流程搜尋
            with gr.TabItem("🔍 n8n Workflow 智能搜尋"):
                gr.Markdown("""
                ## 💡 使用說明
                1. 在下方輸入框中描述您想要實作的工作流程
                2. 點擊「搜尋」按鈕查找相關的工作流程
                3. 從搜尋結果中選擇合適的工作流程
                4. 點擊「儲存選中的工作流程」生成教學文件

                ### 📝 搜尋範例：
                - 每天早上寄出氣象通知
                - 監控伺服器異常發 Discord 警告
                - 定時備份資料庫並發送報告
                - Telegram Bot 自動回覆
                """)

                with gr.Row():
                    with gr.Column(scale=3):
                        # 搜尋輸入
                        search_input = gr.Textbox(
                            label="🔍 請描述您想要實作的工作流程",
                            placeholder="例如：每天早上寄出氣象通知",
                            lines=2
                        )

                        # 搜尋按鈕
                        search_btn = gr.Button("🔍 搜尋工作流程", variant="primary", size="lg")

                    with gr.Column(scale=1):
                        # 結果數量選擇
                        top_k = gr.Slider(
                            minimum=1,
                            maximum=10,
                            value=5,
                            step=1,
                            label="顯示結果數量",
                            info="最多顯示幾個搜尋結果"
                        )

                # 搜尋結果顯示
                search_results = gr.HTML(
                    label="搜尋結果",
                    elem_classes=["search-results"]
                )

                # 工作流程選擇下拉選單
                workflow_dropdown = gr.Dropdown(
                    label="📥 選擇要儲存的工作流程",
                    choices=[],
                    visible=False,
                    interactive=True
                )

                # 儲存按鈕
                save_btn = gr.Button("💾 儲存選中的工作流程", variant="secondary", visible=False)

                # 儲存結果顯示
                save_result = gr.Textbox(
                    label="儲存結果",
                    visible=False,
                    interactive=False
                )

                # 教學文件顯示
                tutorial_display = gr.Markdown(
                    label="📖 工作流程教學文件",
                    visible=False,
                    elem_classes=["tutorial-content"]
                )

            # 第二個頁籤：AI 教學生成
            with gr.TabItem("🤖 n8n Workflow 教學生成"):
                gr.Markdown("""
                ## 🎓 AI 教學生成說明
                透過大語言模型為您提供專業的 n8n 節點設定教學與指導

                ### 💡 使用方式：
                1. 在下方輸入您的問題或需要了解的節點
                2. 選擇 AI 模型（已在 .env 檔案中設定）
                3. 點擊「生成教學」獲得詳細的設定指導

                ### 📝 問題範例：
                - OpenWeather 節點該如何設定？
                - 如何設定 Telegram Bot 自動回覆？
                - Discord Webhook 節點的參數設定
                - Google Sheets 節點如何連接和操作？
                - HTTP Request 節點的認證設定
                """)

                with gr.Row():
                    with gr.Column(scale=4):
                        # 問題輸入
                        question_input = gr.Textbox(
                            label="🤔 請輸入您的問題",
                            placeholder="例如：OpenWeather 節點該如何設定？",
                            lines=3
                        )

                    with gr.Column(scale=1):
                        # AI 模型資訊顯示
                        ai_info = gr.Markdown(
                            f"""
                            **🤖 當前 AI 設定**
                            - 提供商：{ai_generator.provider.upper()}
                            - 模型：{getattr(ai_generator, 'model', 'N/A')}
                            - 最大 Token：{ai_generator.max_tokens}
                            - 溫度：{ai_generator.temperature}

                            *設定可在 .env 檔案中修改*
                            """
                        )

                # 生成按鈕
                generate_btn = gr.Button("🎓 生成教學", variant="primary", size="lg")

                # 教學內容顯示
                tutorial_output = gr.Markdown(
                    label="📚 AI 生成的教學內容",
                    elem_classes=["tutorial-content"]
                )

        # 事件處理
        def on_search(query, k):
            html_results, dropdown_update = searcher.search_and_display(query, k)

            # 根據是否有結果來決定顯示哪些元件
            if searcher.current_results:
                return (
                    html_results,
                    dropdown_update,
                    gr.update(visible=True),  # save_btn
                    gr.update(visible=False), # save_result
                    gr.update(visible=False)  # tutorial_display
                )
            else:
                return (
                    html_results,
                    dropdown_update,
                    gr.update(visible=False), # save_btn
                    gr.update(visible=False), # save_result
                    gr.update(visible=False)  # tutorial_display
                )

        def on_save(selected_workflow):
            if not selected_workflow:
                return (
                    gr.update(value="❌ 請先選擇一個工作流程", visible=True),
                    gr.update(visible=False)
                )

            save_message, tutorial_content = searcher.save_selected_workflow(selected_workflow)

            if tutorial_content:
                return (
                    gr.update(value=save_message, visible=True),
                    gr.update(value=tutorial_content, visible=True)
                )
            else:
                return (
                    gr.update(value=save_message, visible=True),
                    gr.update(visible=False)
                )

        # AI 教學生成事件處理
        def on_generate_tutorial(question):
            if not question.strip():
                return "❌ 請輸入您的問題"

            try:
                # 顯示載入中的訊息
                loading_message = "🤖 AI 正在生成教學內容，請稍候..."

                # 生成教學內容
                tutorial_content = ai_generator.generate_tutorial(question)

                return tutorial_content

            except Exception as e:
                logger.error(f"生成教學時發生錯誤: {e}")
                return f"❌ 生成教學時發生錯誤：{str(e)}"

        # 綁定事件
        search_btn.click(
            fn=on_search,
            inputs=[search_input, top_k],
            outputs=[search_results, workflow_dropdown, save_btn, save_result, tutorial_display]
        )

        # 支援 Enter 鍵搜尋
        search_input.submit(
            fn=on_search,
            inputs=[search_input, top_k],
            outputs=[search_results, workflow_dropdown, save_btn, save_result, tutorial_display]
        )

        save_btn.click(
            fn=on_save,
            inputs=[workflow_dropdown],
            outputs=[save_result, tutorial_display]
        )

        # 綁定 AI 教學生成事件
        generate_btn.click(
            fn=on_generate_tutorial,
            inputs=[question_input],
            outputs=[tutorial_output]
        )

        # 支援 Enter 鍵生成教學
        question_input.submit(
            fn=on_generate_tutorial,
            inputs=[question_input],
            outputs=[tutorial_output]
        )

        # 頁腳資訊
        gr.Markdown("""
        ---
        ### 📚 相關資源
        - [n8n 官方文檔](https://docs.n8n.io/)
        - [n8n 社群範例](https://n8n.io/workflows/)
        - [節點參考文檔](https://docs.n8n.io/integrations/)

        *由 n8n Workflow 智能搜尋系統提供支援*
        """)

    return demo

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

        # 創建並啟動 Gradio 介面
        demo = create_gradio_interface()

        # 啟動介面
        try:
            demo.launch(
                server_name="0.0.0.0",  # 允許外部訪問
                server_port=7862,       # 使用不同端口避免衝突
                share=False,            # 不創建公開連結
                debug=False,            # 生產環境關閉 debug
                show_error=True,        # 顯示錯誤訊息
                inbrowser=False,        # 不自動開啟瀏覽器
                quiet=True              # 減少輸出訊息
            )
        except Exception as e:
            logger.error(f"Gradio 啟動失敗: {e}")
            print(f"❌ Gradio 啟動失敗: {e}")
            print("嘗試使用備用配置...")
            try:
                demo.launch(
                    server_name="127.0.0.1",  # 僅本地訪問
                    server_port=7862,
                    share=False,
                    debug=False,
                    inbrowser=False,
                    quiet=True
                )
            except Exception as e2:
                logger.error(f"備用配置也失敗: {e2}")
                print(f"❌ 無法啟動應用: {e2}")

    except Exception as e:
        logger.error(f"啟動應用程式時發生錯誤: {e}")
        print(f"❌ 啟動失敗：{e}")

if __name__ == "__main__":
    main()
