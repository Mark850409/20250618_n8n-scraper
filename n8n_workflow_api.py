#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
n8n Workflow API Server
結合 Flask OpenAPI 的 n8n 工作流程搜尋與爬取 API 服務
整合了 n8n_workflow_search_gui.py 和 n8n_workflow_scraper.py 的功能
"""

import os
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime

from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields, Namespace
from flask_cors import CORS
from marshmallow import Schema, fields as ma_fields, ValidationError

# 導入現有的功能模組
import sys
sys.path.append('.')

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 可選依賴的導入
try:
    from dotenv import load_dotenv
    load_dotenv()
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    logger.warning("python-dotenv 未安裝，將跳過 .env 文件載入")

# 創建 Flask 應用
app = Flask(__name__)
app.config['RESTX_MASK_SWAGGER'] = False
CORS(app)

# 創建 API 實例
api = Api(
    app,
    version='1.0',
    title='n8n Workflow API',
    description='n8n 工作流程搜尋與爬取 API 服務',
    doc='/docs/',
    prefix='/api/v1'
)

# 創建命名空間
search_ns = Namespace('search', description='工作流程搜尋相關 API')
scraper_ns = Namespace('scraper', description='工作流程爬取相關 API')
tutorial_ns = Namespace('tutorial', description='AI 教學生成相關 API')

api.add_namespace(search_ns)
api.add_namespace(scraper_ns)
api.add_namespace(tutorial_ns)

# API 模型定義
search_request_model = api.model('SearchRequest', {
    'query': fields.String(required=True, description='搜尋關鍵字', example='telegram bot'),
    'top_k': fields.Integer(required=False, default=5, description='返回結果數量', example=5)
})

search_response_model = api.model('SearchResponse', {
    'success': fields.Boolean(description='是否成功'),
    'message': fields.String(description='回應訊息'),
    'total_results': fields.Integer(description='總結果數'),
    'results': fields.List(fields.Raw, description='搜尋結果列表')
})

scraper_request_model = api.model('ScraperRequest', {
    'rows': fields.Integer(required=False, default=20, description='每頁筆數', example=20),
    'category': fields.String(required=False, default='全部', description='工作流程類別', example='AI')
})

scraper_response_model = api.model('ScraperResponse', {
    'success': fields.Boolean(description='是否成功'),
    'message': fields.String(description='回應訊息'),
    'status': fields.String(description='執行狀態'),
    'details': fields.String(description='詳細結果')
})

tutorial_request_model = api.model('TutorialRequest', {
    'question': fields.String(required=True, description='問題或節點名稱', example='如何設定 Telegram Bot 節點？')
})

tutorial_response_model = api.model('TutorialResponse', {
    'success': fields.Boolean(description='是否成功'),
    'message': fields.String(description='回應訊息'),
    'tutorial_content': fields.String(description='生成的教學內容')
})

save_workflow_request_model = api.model('SaveWorkflowRequest', {
    'workflow_index': fields.Integer(required=True, description='工作流程索引 (從搜尋結果中選擇)', example=0)
})

save_workflow_response_model = api.model('SaveWorkflowResponse', {
    'success': fields.Boolean(description='是否成功'),
    'message': fields.String(description='回應訊息'),
    'tutorial_content': fields.String(description='生成的教學內容')
})

# 全域變數儲存搜尋系統和爬取器實例
searcher = None
scraper = None
ai_generator = None
current_search_results = []

def initialize_services():
    """初始化服務"""
    global searcher, scraper, ai_generator
    
    try:
        # 動態導入搜尋功能
        from n8n_workflow_search_gui import N8nWorkflowSearcherGUI, AITutorialGenerator
        searcher = N8nWorkflowSearcherGUI()
        ai_generator = AITutorialGenerator()
        logger.info("成功初始化搜尋系統和 AI 教學生成器")
    except Exception as e:
        logger.error(f"初始化搜尋系統失敗: {e}")
        searcher = None
        ai_generator = None
    
    try:
        # 動態導入爬取功能
        from n8n_workflow_scraper import N8nWorkflowScraper
        scraper = N8nWorkflowScraper()
        logger.info("成功初始化爬取系統")
    except Exception as e:
        logger.error(f"初始化爬取系統失敗: {e}")
        scraper = None

# 搜尋相關 API
@search_ns.route('/workflows')
class WorkflowSearch(Resource):
    @search_ns.expect(search_request_model)
    @search_ns.marshal_with(search_response_model)
    def post(self):
        """搜尋工作流程"""
        global current_search_results
        
        if not searcher:
            return {
                'success': False,
                'message': '搜尋系統未初始化',
                'total_results': 0,
                'results': []
            }, 500
        
        try:
            data = request.get_json()
            query = data.get('query', '')
            top_k = data.get('top_k', 5)
            
            if not query.strip():
                return {
                    'success': False,
                    'message': '搜尋關鍵字不能為空',
                    'total_results': 0,
                    'results': []
                }, 400
            
            # 執行搜尋
            search_results = searcher.search_workflows(query, top_k)
            current_search_results = search_results  # 儲存搜尋結果供後續使用
            
            # 格式化結果
            formatted_results = []
            for i, (metadata, similarity) in enumerate(search_results):
                formatted_results.append({
                    'index': i,
                    'name': metadata.get('name', 'Unknown'),
                    'filename': metadata.get('filename', 'Unknown'),
                    'description': metadata.get('description', ''),
                    'similarity_score': round(similarity, 4),
                    'node_count': metadata.get('node_count', 0),
                    'workflow_id': metadata.get('workflow_id', 'N/A')
                })
            
            return {
                'success': True,
                'message': f'找到 {len(search_results)} 個相關工作流程',
                'total_results': len(search_results),
                'results': formatted_results
            }
            
        except Exception as e:
            logger.error(f"搜尋工作流程時發生錯誤: {e}")
            return {
                'success': False,
                'message': f'搜尋失敗: {str(e)}',
                'total_results': 0,
                'results': []
            }, 500

@search_ns.route('/workflows/save')
class SaveWorkflow(Resource):
    @search_ns.expect(save_workflow_request_model)
    @search_ns.marshal_with(save_workflow_response_model)
    def post(self):
        """儲存選中的工作流程並生成教學文件"""
        global current_search_results
        
        if not searcher:
            return {
                'success': False,
                'message': '搜尋系統未初始化',
                'tutorial_content': ''
            }, 500
        
        if not current_search_results:
            return {
                'success': False,
                'message': '沒有可用的搜尋結果，請先執行搜尋',
                'tutorial_content': ''
            }, 400
        
        try:
            data = request.get_json()
            workflow_index = data.get('workflow_index')
            
            if workflow_index is None or workflow_index < 0 or workflow_index >= len(current_search_results):
                return {
                    'success': False,
                    'message': f'無效的工作流程索引，請選擇 0 到 {len(current_search_results)-1} 之間的值',
                    'tutorial_content': ''
                }, 400
            
            # 取得選中的工作流程
            metadata, _ = current_search_results[workflow_index]
            
            # 儲存工作流程並生成教學
            success, tutorial_content = searcher.save_workflow_files(metadata)
            
            if success:
                return {
                    'success': True,
                    'message': f'成功儲存工作流程「{metadata["name"]}」到 selected_workflows/ 目錄',
                    'tutorial_content': tutorial_content
                }
            else:
                return {
                    'success': False,
                    'message': '儲存工作流程時發生錯誤',
                    'tutorial_content': ''
                }, 500
                
        except Exception as e:
            logger.error(f"儲存工作流程時發生錯誤: {e}")
            return {
                'success': False,
                'message': f'儲存失敗: {str(e)}',
                'tutorial_content': ''
            }, 500

# 爬取相關 API
@scraper_ns.route('/workflows')
class WorkflowScraper(Resource):
    @scraper_ns.expect(scraper_request_model)
    @scraper_ns.marshal_with(scraper_response_model)
    def post(self):
        """爬取 n8n 工作流程"""
        if not scraper:
            return {
                'success': False,
                'message': '爬取系統未初始化',
                'status': '錯誤',
                'details': '爬取系統未初始化，請檢查系統配置'
            }, 500

        try:
            data = request.get_json()
            rows = data.get('rows', 20)
            category = data.get('category', '全部')

            # 驗證參數
            if rows <= 0 or rows > 100:
                return {
                    'success': False,
                    'message': '參數錯誤：rows 必須在 1-100 之間',
                    'status': '錯誤',
                    'details': 'rows 參數超出允許範圍'
                }, 400

            # 執行爬取
            status, details = scraper.scrape_workflows(rows, category)

            success = not status.startswith('❌')

            return {
                'success': success,
                'message': f'爬取任務完成，狀態：{status}',
                'status': status,
                'details': details
            }

        except Exception as e:
            logger.error(f"爬取工作流程時發生錯誤: {e}")
            return {
                'success': False,
                'message': f'爬取失敗: {str(e)}',
                'status': '錯誤',
                'details': f'執行過程中發生錯誤: {str(e)}'
            }, 500

@scraper_ns.route('/categories')
class WorkflowCategories(Resource):
    def get(self):
        """取得可用的工作流程類別"""
        categories = [
            "全部", "AI", "SecOps", "Sales", "IT Ops", "Marketing",
            "Engineering", "DevOps", "Building Blocks", "Design",
            "Finance", "HR", "Other", "Product", "Support"
        ]

        return {
            'success': True,
            'message': '成功取得類別列表',
            'categories': categories
        }

# AI 教學生成相關 API
@tutorial_ns.route('/generate')
class TutorialGenerator(Resource):
    @tutorial_ns.expect(tutorial_request_model)
    @tutorial_ns.marshal_with(tutorial_response_model)
    def post(self):
        """生成 AI 教學內容"""
        if not ai_generator:
            return {
                'success': False,
                'message': 'AI 教學生成系統未初始化',
                'tutorial_content': ''
            }, 500

        try:
            data = request.get_json()
            question = data.get('question', '')

            if not question.strip():
                return {
                    'success': False,
                    'message': '問題不能為空',
                    'tutorial_content': ''
                }, 400

            # 生成教學內容
            tutorial_content = ai_generator.generate_tutorial(question)

            # 檢查是否生成成功
            if tutorial_content.startswith('❌'):
                return {
                    'success': False,
                    'message': 'AI 教學生成失敗',
                    'tutorial_content': tutorial_content
                }, 500

            return {
                'success': True,
                'message': '成功生成 AI 教學內容',
                'tutorial_content': tutorial_content
            }

        except Exception as e:
            logger.error(f"生成 AI 教學時發生錯誤: {e}")
            return {
                'success': False,
                'message': f'生成教學失敗: {str(e)}',
                'tutorial_content': ''
            }, 500

@tutorial_ns.route('/config')
class TutorialConfig(Resource):
    def get(self):
        """取得 AI 教學生成器配置資訊"""
        if not ai_generator:
            return {
                'success': False,
                'message': 'AI 教學生成系統未初始化',
                'config': {}
            }, 500

        config = {
            'provider': ai_generator.provider,
            'model': getattr(ai_generator, 'model', 'N/A'),
            'max_tokens': ai_generator.max_tokens,
            'temperature': ai_generator.temperature,
            'available': ai_generator.available
        }

        return {
            'success': True,
            'message': '成功取得 AI 配置資訊',
            'config': config
        }

# 健康檢查和系統資訊 API
@api.route('/health')
class HealthCheck(Resource):
    def get(self):
        """系統健康檢查"""
        status = {
            'api_server': True,
            'search_system': searcher is not None,
            'scraper_system': scraper is not None,
            'ai_generator': ai_generator is not None and ai_generator.available if ai_generator else False,
            'timestamp': datetime.now().isoformat()
        }

        all_healthy = all(status.values())

        return {
            'success': all_healthy,
            'message': '系統狀態正常' if all_healthy else '部分系統異常',
            'status': status
        }, 200 if all_healthy else 206

@api.route('/info')
class SystemInfo(Resource):
    def get(self):
        """取得系統資訊"""
        info = {
            'name': 'n8n Workflow API',
            'version': '1.0.0',
            'description': 'n8n 工作流程搜尋與爬取 API 服務',
            'endpoints': {
                'search': '/api/v1/search/workflows',
                'save': '/api/v1/search/workflows/save',
                'scraper': '/api/v1/scraper/workflows',
                'categories': '/api/v1/scraper/categories',
                'tutorial': '/api/v1/tutorial/generate',
                'config': '/api/v1/tutorial/config',
                'health': '/api/v1/health',
                'docs': '/docs/'
            },
            'features': [
                '智能工作流程搜尋',
                '批量工作流程爬取',
                'AI 教學內容生成',
                '工作流程教學文件生成',
                'RESTful API 介面',
                'OpenAPI 文檔支援'
            ]
        }

        return {
            'success': True,
            'message': '系統資訊',
            'info': info
        }

# 初始化服務
initialize_services()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'

    logger.info(f"啟動 n8n Workflow API 服務於 port {port}")
    logger.info(f"API 文檔可在 http://localhost:{port}/docs/ 查看")
    logger.info("可用的 API 端點:")
    logger.info("  - POST /api/v1/search/workflows - 搜尋工作流程")
    logger.info("  - POST /api/v1/search/workflows/save - 儲存工作流程")
    logger.info("  - POST /api/v1/scraper/workflows - 爬取工作流程")
    logger.info("  - GET  /api/v1/scraper/categories - 取得類別列表")
    logger.info("  - POST /api/v1/tutorial/generate - 生成 AI 教學")
    logger.info("  - GET  /api/v1/tutorial/config - 取得 AI 配置")
    logger.info("  - GET  /api/v1/health - 健康檢查")
    logger.info("  - GET  /api/v1/info - 系統資訊")

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
