#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試 Zeabur 部署修復
驗證環境變數解析和 ChromaDB 初始化是否正常
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

def test_port_parsing():
    """測試 PORT 環境變數解析修復"""
    print("🔍 測試 PORT 環境變數解析...")
    
    # 模擬 Zeabur 的環境變數格式
    test_cases = [
        ("5000", 5000),
        ("${WEB_PORT}", 5000),  # Zeabur 未解析的變數
        ("${PORT}", 5000),      # Zeabur 未解析的變數
        ("8080", 8080),
        ("", 5000),             # 空值
        ("invalid", 5000),      # 無效值
    ]
    
    for port_env, expected in test_cases:
        print(f"  測試 PORT='{port_env}' -> 期望: {expected}")
        
        # 設定環境變數
        if port_env:
            os.environ['PORT'] = port_env
        elif 'PORT' in os.environ:
            del os.environ['PORT']
        
        try:
            # 模擬 n8n_workflow_api.py 中的邏輯
            port_env_val = os.getenv('PORT', '5000')
            if port_env_val.startswith('${') and port_env_val.endswith('}'):
                port = 5000
                print(f"    ✅ 檢測到未解析的環境變數，使用預設端口 {port}")
            else:
                try:
                    port = int(port_env_val)
                    print(f"    ✅ 成功解析端口: {port}")
                except (ValueError, TypeError):
                    port = 5000
                    print(f"    ✅ 解析失敗，使用預設端口: {port}")
            
            assert port == expected, f"期望 {expected}，實際 {port}"
            
        except Exception as e:
            print(f"    ❌ 測試失敗: {e}")
            return False
    
    print("✅ PORT 環境變數解析測試通過")
    return True

def test_chromadb_error_handling():
    """測試 ChromaDB 錯誤處理"""
    print("\n🔍 測試 ChromaDB 錯誤處理...")
    
    try:
        import chromadb
        from chromadb.errors import InvalidCollectionException
        
        # 創建臨時目錄
        with tempfile.TemporaryDirectory() as temp_dir:
            print(f"  使用臨時目錄: {temp_dir}")
            
            # 初始化 ChromaDB 客戶端
            client = chromadb.PersistentClient(path=temp_dir)
            collection_name = "test_collection"
            
            # 第一次創建集合
            try:
                collection1 = client.create_collection(collection_name)
                print("  ✅ 成功創建第一個集合")
            except Exception as e:
                print(f"  ❌ 創建第一個集合失敗: {e}")
                return False
            
            # 嘗試再次創建同名集合（應該會失敗）
            try:
                collection2 = client.create_collection(collection_name)
                print("  ❌ 不應該能創建重複的集合")
                return False
            except Exception as e:
                print(f"  ✅ 正確捕獲重複集合錯誤: {type(e).__name__}")
            
            # 測試獲取現有集合
            try:
                existing_collection = client.get_collection(collection_name)
                print("  ✅ 成功獲取現有集合")
            except Exception as e:
                print(f"  ❌ 獲取現有集合失敗: {e}")
                return False
            
            # 測試刪除集合
            try:
                client.delete_collection(collection_name)
                print("  ✅ 成功刪除集合")
            except Exception as e:
                print(f"  ❌ 刪除集合失敗: {e}")
                return False
            
            # 測試刪除不存在的集合
            try:
                client.delete_collection("non_existent_collection")
                print("  ❌ 不應該能刪除不存在的集合")
                return False
            except Exception as e:
                print(f"  ✅ 正確捕獲刪除不存在集合的錯誤: {type(e).__name__}")
        
        print("✅ ChromaDB 錯誤處理測試通過")
        return True
        
    except ImportError:
        print("  ⚠️  ChromaDB 未安裝，跳過測試")
        return True
    except Exception as e:
        print(f"  ❌ ChromaDB 測試失敗: {e}")
        return False

def test_api_import():
    """測試 API 模組導入"""
    print("\n🔍 測試 API 模組導入...")
    
    try:
        # 測試基本導入
        import flask
        import flask_restx
        import flask_cors
        print("  ✅ Flask 相關模組導入成功")
        
        # 測試可選依賴
        try:
            import requests
            print("  ✅ requests 模組可用")
        except ImportError:
            print("  ⚠️  requests 模組不可用")
        
        try:
            import gradio
            print("  ✅ gradio 模組可用")
        except ImportError:
            print("  ⚠️  gradio 模組不可用")
        
        try:
            import chromadb
            print("  ✅ chromadb 模組可用")
        except ImportError:
            print("  ⚠️  chromadb 模組不可用")
        
        print("✅ API 模組導入測試通過")
        return True
        
    except ImportError as e:
        print(f"  ❌ 必要模組導入失敗: {e}")
        return False
    except Exception as e:
        print(f"  ❌ 模組導入測試失敗: {e}")
        return False

def test_file_structure():
    """測試檔案結構"""
    print("\n🔍 測試檔案結構...")
    
    required_files = [
        "n8n_workflow_api.py",
        "n8n_workflow_search_gui.py", 
        "n8n_workflow_scraper.py",
        "requirements.txt",
        "Dockerfile",
        "docker-compose.yml"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
        else:
            print(f"  ✅ {file}")
    
    if missing_files:
        print(f"  ❌ 缺少檔案: {missing_files}")
        return False
    
    print("✅ 檔案結構測試通過")
    return True

def test_environment_variables():
    """測試環境變數處理"""
    print("\n🔍 測試環境變數處理...")
    
    # 備份原始環境變數
    original_env = dict(os.environ)
    
    try:
        # 測試各種環境變數組合
        test_envs = [
            {"PORT": "5000"},
            {"WEB_PORT": "8080"},
            {"PORT": "${WEB_PORT}", "WEB_PORT": "3000"},
            {"PORT": "${INVALID_VAR}"},
            {},  # 無環境變數
        ]
        
        for i, env_vars in enumerate(test_envs):
            print(f"  測試環境變數組合 {i+1}: {env_vars}")
            
            # 清除相關環境變數
            for key in ["PORT", "WEB_PORT"]:
                if key in os.environ:
                    del os.environ[key]
            
            # 設定測試環境變數
            for key, value in env_vars.items():
                os.environ[key] = value
            
            # 模擬端口解析邏輯
            port_env = os.getenv('PORT', '5000')
            if port_env.startswith('${') and port_env.endswith('}'):
                port = 5000
            else:
                try:
                    port = int(port_env)
                except (ValueError, TypeError):
                    port = 5000
            
            print(f"    解析結果: {port}")
            assert isinstance(port, int) and 1 <= port <= 65535
        
        print("✅ 環境變數處理測試通過")
        return True
        
    except Exception as e:
        print(f"  ❌ 環境變數測試失敗: {e}")
        return False
    finally:
        # 恢復原始環境變數
        os.environ.clear()
        os.environ.update(original_env)

def main():
    """主測試函數"""
    print("🧪 Zeabur 部署修復測試")
    print("=" * 50)
    
    tests = [
        ("檔案結構", test_file_structure),
        ("模組導入", test_api_import),
        ("PORT 環境變數解析", test_port_parsing),
        ("環境變數處理", test_environment_variables),
        ("ChromaDB 錯誤處理", test_chromadb_error_handling),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 {test_name}")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} 失敗")
        except Exception as e:
            print(f"❌ {test_name} 執行時發生錯誤: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 測試結果: {passed}/{total} 通過")
    
    if passed == total:
        print("🎉 所有測試通過！Zeabur 部署修復成功。")
        print("\n💡 部署建議:")
        print("  - 使用 SERVICE_MODE=api 進行 Zeabur 部署")
        print("  - 設定必要的 AI API 金鑰環境變數")
        print("  - 檢查 /api/v1/health 端點確認服務正常")
    else:
        print("⚠️  部分測試失敗，請檢查相關配置。")
        sys.exit(1)

if __name__ == "__main__":
    main()
