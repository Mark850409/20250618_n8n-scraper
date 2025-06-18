#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
n8n Workflow API 使用範例
展示如何使用 Flask OpenAPI 服務的各種功能
"""

import requests
import json
import time

# API 基礎 URL
BASE_URL = "http://localhost:5000/api/v1"

def test_health_check():
    """測試系統健康檢查"""
    print("=== 測試系統健康檢查 ===")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"錯誤: {e}")
    print()

def test_system_info():
    """測試系統資訊"""
    print("=== 測試系統資訊 ===")
    try:
        response = requests.get(f"{BASE_URL}/info")
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"錯誤: {e}")
    print()

def test_workflow_search():
    """測試工作流程搜尋"""
    print("=== 測試工作流程搜尋 ===")
    try:
        # 搜尋 Telegram Bot 相關的工作流程
        search_data = {
            "query": "telegram bot",
            "top_k": 3
        }
        
        response = requests.post(
            f"{BASE_URL}/search/workflows",
            json=search_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"狀態碼: {response.status_code}")
        result = response.json()
        print(f"成功: {result.get('success')}")
        print(f"訊息: {result.get('message')}")
        print(f"總結果數: {result.get('total_results')}")
        
        if result.get('results'):
            print("搜尋結果:")
            for i, workflow in enumerate(result['results']):
                print(f"  [{i}] {workflow['name']}")
                print(f"      相似度: {workflow['similarity_score']}")
                print(f"      描述: {workflow['description'][:100]}...")
                print()
        
        return result.get('results', [])
        
    except Exception as e:
        print(f"錯誤: {e}")
        return []

def test_save_workflow(search_results):
    """測試儲存工作流程"""
    print("=== 測試儲存工作流程 ===")
    
    if not search_results:
        print("沒有搜尋結果可以儲存")
        return
    
    try:
        # 儲存第一個搜尋結果
        save_data = {
            "workflow_index": 0
        }
        
        response = requests.post(
            f"{BASE_URL}/search/workflows/save",
            json=save_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"狀態碼: {response.status_code}")
        result = response.json()
        print(f"成功: {result.get('success')}")
        print(f"訊息: {result.get('message')}")
        
        if result.get('tutorial_content'):
            print("教學內容 (前 500 字元):")
            print(result['tutorial_content'][:500] + "...")
        
    except Exception as e:
        print(f"錯誤: {e}")
    print()

def test_get_categories():
    """測試取得工作流程類別"""
    print("=== 測試取得工作流程類別 ===")
    try:
        response = requests.get(f"{BASE_URL}/scraper/categories")
        print(f"狀態碼: {response.status_code}")
        result = response.json()
        print(f"成功: {result.get('success')}")
        print(f"可用類別: {result.get('categories')}")
    except Exception as e:
        print(f"錯誤: {e}")
    print()

def test_scrape_workflows():
    """測試爬取工作流程 (小量測試)"""
    print("=== 測試爬取工作流程 ===")
    try:
        # 只爬取少量 AI 類別的工作流程進行測試
        scrape_data = {
            "rows": 5,  # 只爬取 5 個
            "category": "AI"
        }
        
        print("開始爬取 (這可能需要一些時間)...")
        response = requests.post(
            f"{BASE_URL}/scraper/workflows",
            json=scrape_data,
            headers={"Content-Type": "application/json"},
            timeout=300  # 5 分鐘超時
        )
        
        print(f"狀態碼: {response.status_code}")
        result = response.json()
        print(f"成功: {result.get('success')}")
        print(f"狀態: {result.get('status')}")
        print(f"訊息: {result.get('message')}")
        
        if result.get('details'):
            print("詳細結果 (前 1000 字元):")
            print(result['details'][:1000] + "...")
        
    except Exception as e:
        print(f"錯誤: {e}")
    print()

def test_ai_tutorial_config():
    """測試 AI 教學生成器配置"""
    print("=== 測試 AI 教學生成器配置 ===")
    try:
        response = requests.get(f"{BASE_URL}/tutorial/config")
        print(f"狀態碼: {response.status_code}")
        result = response.json()
        print(f"成功: {result.get('success')}")
        print(f"配置: {json.dumps(result.get('config', {}), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"錯誤: {e}")
    print()

def test_ai_tutorial_generation():
    """測試 AI 教學生成"""
    print("=== 測試 AI 教學生成 ===")
    try:
        tutorial_data = {
            "question": "如何設定 Telegram Bot 節點來接收和回覆訊息？"
        }
        
        print("正在生成 AI 教學內容...")
        response = requests.post(
            f"{BASE_URL}/tutorial/generate",
            json=tutorial_data,
            headers={"Content-Type": "application/json"},
            timeout=60  # 1 分鐘超時
        )
        
        print(f"狀態碼: {response.status_code}")
        result = response.json()
        print(f"成功: {result.get('success')}")
        print(f"訊息: {result.get('message')}")
        
        if result.get('tutorial_content'):
            print("AI 生成的教學內容 (前 800 字元):")
            print(result['tutorial_content'][:800] + "...")
        
    except Exception as e:
        print(f"錯誤: {e}")
    print()

def main():
    """主測試函數"""
    print("🚀 開始測試 n8n Workflow API")
    print("=" * 50)
    
    # 基礎測試
    test_health_check()
    test_system_info()
    
    # 搜尋功能測試
    search_results = test_workflow_search()
    test_save_workflow(search_results)
    
    # 爬取功能測試
    test_get_categories()
    
    # 注意：爬取測試可能需要較長時間，可以選擇跳過
    user_input = input("是否要測試工作流程爬取功能？(y/N): ")
    if user_input.lower() == 'y':
        test_scrape_workflows()
    else:
        print("跳過工作流程爬取測試")
        print()
    
    # AI 教學生成測試
    test_ai_tutorial_config()
    
    # 注意：AI 教學生成需要配置 API 金鑰
    user_input = input("是否要測試 AI 教學生成功能？(y/N): ")
    if user_input.lower() == 'y':
        test_ai_tutorial_generation()
    else:
        print("跳過 AI 教學生成測試")
        print()
    
    print("🎉 測試完成！")
    print("💡 提示：")
    print("   - 確保 API 服務正在運行 (python n8n_workflow_api.py)")
    print("   - 如需使用 AI 功能，請設定相應的 API 金鑰")
    print("   - 完整的 API 文檔可在 http://localhost:5000/docs/ 查看")

if __name__ == "__main__":
    main()
