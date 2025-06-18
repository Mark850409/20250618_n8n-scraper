#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
n8n Workflow API 啟動腳本
提供便捷的啟動選項和配置檢查
"""

import os
import sys
import subprocess
import argparse
import logging
from pathlib import Path

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_dependencies():
    """檢查必要的依賴是否已安裝"""
    required_packages = [
        'flask',
        'flask_restx',
        'flask_cors',
        'requests',
        'gradio'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"缺少必要的依賴套件: {', '.join(missing_packages)}")
        logger.info("請執行: pip install -r requirements.txt")
        return False
    
    logger.info("✅ 所有必要依賴已安裝")
    return True

def check_files():
    """檢查必要的檔案是否存在"""
    required_files = [
        'n8n_workflow_api.py',
        'n8n_workflow_search_gui.py',
        'n8n_workflow_scraper.py',
        'requirements.txt'
    ]
    
    missing_files = []
    
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        logger.error(f"缺少必要的檔案: {', '.join(missing_files)}")
        return False
    
    logger.info("✅ 所有必要檔案存在")
    return True

def create_directories():
    """創建必要的目錄"""
    directories = [
        'selected_workflows',
        'chroma_db',
        'workflows_data'
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        logger.info(f"📁 確保目錄存在: {directory}")

def check_env_config():
    """檢查環境變數配置"""
    logger.info("🔧 檢查環境變數配置...")
    
    # 檢查 .env 檔案
    env_file = Path('.env')
    if env_file.exists():
        logger.info("✅ 找到 .env 檔案")
        try:
            from dotenv import load_dotenv
            load_dotenv()
            logger.info("✅ 成功載入 .env 檔案")
        except ImportError:
            logger.warning("⚠️  python-dotenv 未安裝，無法載入 .env 檔案")
    else:
        logger.info("ℹ️  未找到 .env 檔案，將使用預設配置")
    
    # 檢查 AI 配置
    ai_provider = os.getenv('AI_PROVIDER', 'openai')
    logger.info(f"🤖 AI 提供商: {ai_provider}")
    
    if ai_provider == 'openai':
        if os.getenv('OPENAI_API_KEY'):
            logger.info("✅ OpenAI API 金鑰已設定")
        else:
            logger.warning("⚠️  OpenAI API 金鑰未設定，AI 功能將不可用")
    
    elif ai_provider == 'gemini':
        if os.getenv('GEMINI_API_KEY'):
            logger.info("✅ Gemini API 金鑰已設定")
        else:
            logger.warning("⚠️  Gemini API 金鑰未設定，AI 功能將不可用")
    
    elif ai_provider == 'ollama':
        ollama_url = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')
        logger.info(f"🦙 Ollama 服務 URL: {ollama_url}")

def start_api_server(port=5000, debug=False):
    """啟動 API 服務"""
    logger.info(f"🚀 啟動 n8n Workflow API 服務...")
    logger.info(f"📡 服務端口: {port}")
    logger.info(f"🐛 除錯模式: {'開啟' if debug else '關閉'}")
    
    # 設定環境變數
    os.environ['PORT'] = str(port)
    os.environ['DEBUG'] = str(debug).lower()
    
    try:
        # 啟動 API 服務
        subprocess.run([sys.executable, 'n8n_workflow_api.py'], check=True)
    except KeyboardInterrupt:
        logger.info("👋 服務已停止")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ 服務啟動失敗: {e}")
        sys.exit(1)

def start_gui_server(port=7860):
    """啟動 GUI 服務"""
    logger.info(f"🖥️  啟動 Gradio GUI 服務...")
    logger.info(f"📡 服務端口: {port}")
    
    try:
        # 啟動 GUI 服務
        subprocess.run([sys.executable, 'n8n_workflow_search_gui.py'], check=True)
    except KeyboardInterrupt:
        logger.info("👋 GUI 服務已停止")
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ GUI 服務啟動失敗: {e}")
        sys.exit(1)

def start_both_servers():
    """同時啟動 API 和 GUI 服務"""
    import threading
    import time
    
    logger.info("🚀 同時啟動 API 和 GUI 服務...")
    
    # 啟動 API 服務的執行緒
    api_thread = threading.Thread(
        target=start_api_server,
        kwargs={'port': 5000, 'debug': False}
    )
    api_thread.daemon = True
    api_thread.start()
    
    # 等待一下讓 API 服務啟動
    time.sleep(3)
    
    # 啟動 GUI 服務
    start_gui_server(7860)

def main():
    """主函數"""
    parser = argparse.ArgumentParser(description='n8n Workflow API 啟動腳本')
    parser.add_argument('--mode', choices=['api', 'gui', 'both'], default='api',
                       help='啟動模式: api (僅API), gui (僅GUI), both (同時啟動)')
    parser.add_argument('--port', type=int, default=5000,
                       help='API 服務端口 (預設: 5000)')
    parser.add_argument('--debug', action='store_true',
                       help='啟用除錯模式')
    parser.add_argument('--skip-checks', action='store_true',
                       help='跳過依賴和檔案檢查')
    
    args = parser.parse_args()
    
    print("🤖 n8n Workflow API 啟動腳本")
    print("=" * 50)
    
    # 執行檢查
    if not args.skip_checks:
        if not check_files():
            sys.exit(1)
        
        if not check_dependencies():
            sys.exit(1)
    
    # 創建必要目錄
    create_directories()
    
    # 檢查環境配置
    check_env_config()
    
    print("=" * 50)
    
    # 根據模式啟動服務
    if args.mode == 'api':
        start_api_server(args.port, args.debug)
    elif args.mode == 'gui':
        start_gui_server(7860)
    elif args.mode == 'both':
        start_both_servers()
    
    logger.info("🎉 啟動完成！")
    logger.info("💡 提示:")
    logger.info("   - API 文檔: http://localhost:5000/docs/")
    logger.info("   - GUI 介面: http://localhost:7860/")
    logger.info("   - 健康檢查: http://localhost:5000/api/v1/health")

if __name__ == '__main__':
    main()
