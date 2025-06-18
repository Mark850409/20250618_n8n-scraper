#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
簡化版啟動腳本 - 僅啟動基本功能
當某些依賴缺失時使用此腳本
"""

import os
import sys
import subprocess
import time
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_dependencies():
    """檢查依賴套件"""
    missing_deps = []
    
    try:
        import gradio
        logger.info("✓ Gradio 可用")
    except ImportError:
        missing_deps.append("gradio")
    
    try:
        import requests
        logger.info("✓ Requests 可用")
    except ImportError:
        missing_deps.append("requests")
    
    try:
        import chromadb
        logger.info("✓ ChromaDB 可用")
    except ImportError:
        missing_deps.append("chromadb")
    
    # 可選依賴
    try:
        import openai
        logger.info("✓ OpenAI 可用")
    except ImportError:
        logger.warning("⚠ OpenAI 套件未安裝，AI 功能將不可用")
    
    try:
        from langchain_community.embeddings import HuggingFaceEmbeddings
        logger.info("✓ LangChain 可用")
    except ImportError:
        logger.warning("⚠ LangChain 套件未安裝，將使用簡單文字搜尋")
    
    if missing_deps:
        logger.error(f"缺少必要依賴: {', '.join(missing_deps)}")
        logger.error("請執行: pip install " + " ".join(missing_deps))
        return False
    
    return True

def start_scraper():
    """啟動 n8n workflow scraper"""
    try:
        logger.info("啟動 n8n Workflow Scraper (端口 7860)...")
        process = subprocess.Popen([
            sys.executable, "n8n_workflow_scraper.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    except Exception as e:
        logger.error(f"啟動 scraper 失敗: {e}")
        return None

def start_search_gui():
    """啟動 n8n workflow search GUI"""
    try:
        logger.info("啟動 n8n Workflow Search GUI (端口 7862)...")
        process = subprocess.Popen([
            sys.executable, "n8n_workflow_search_gui.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    except Exception as e:
        logger.error(f"啟動 search GUI 失敗: {e}")
        return None

def main():
    """主函數"""
    logger.info("=== n8n Workflow 系統啟動 ===")
    
    # 檢查依賴
    if not check_dependencies():
        logger.error("依賴檢查失敗，請安裝缺少的套件")
        return
    
    # 創建必要目錄
    os.makedirs("chroma_db", exist_ok=True)
    os.makedirs("selected_workflows", exist_ok=True)
    os.makedirs("workflows_all_1", exist_ok=True)
    
    processes = []
    
    try:
        # 啟動 scraper
        scraper_process = start_scraper()
        if scraper_process:
            processes.append(("Scraper", scraper_process))
            time.sleep(3)  # 等待啟動
        
        # 啟動 search GUI
        search_process = start_search_gui()
        if search_process:
            processes.append(("Search GUI", search_process))
        
        if not processes:
            logger.error("沒有成功啟動任何服務")
            return
        
        logger.info("=== 服務啟動完成 ===")
        logger.info("可用服務:")
        if scraper_process:
            logger.info("- n8n Workflow Scraper: http://localhost:7860")
        if search_process:
            logger.info("- n8n Workflow Search: http://localhost:7862")
        
        logger.info("按 Ctrl+C 停止所有服務")
        
        # 等待所有進程
        while True:
            time.sleep(1)
            # 檢查進程是否還在運行
            for name, process in processes:
                if process.poll() is not None:
                    logger.warning(f"{name} 進程已結束")
    
    except KeyboardInterrupt:
        logger.info("收到停止信號，正在關閉服務...")
        
        # 終止所有進程
        for name, process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
                logger.info(f"已停止 {name}")
            except subprocess.TimeoutExpired:
                process.kill()
                logger.warning(f"強制終止 {name}")
            except Exception as e:
                logger.error(f"停止 {name} 時發生錯誤: {e}")
    
    except Exception as e:
        logger.error(f"運行時發生錯誤: {e}")
    
    finally:
        logger.info("所有服務已停止")

if __name__ == "__main__":
    main()
