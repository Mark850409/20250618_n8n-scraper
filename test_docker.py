#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Docker 配置測試腳本
驗證 Docker Compose 配置是否正確
"""

import subprocess
import sys
import json
import yaml

def run_command(command, capture_output=True):
    """執行命令並返回結果"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=capture_output, 
            text=True,
            timeout=30
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "命令執行超時"
    except Exception as e:
        return False, "", str(e)

def test_docker_compose_syntax():
    """測試 Docker Compose 語法"""
    print("🔍 測試 Docker Compose 語法...")
    
    success, stdout, stderr = run_command("docker-compose config")
    if success:
        print("✅ Docker Compose 語法正確")
        return True
    else:
        print(f"❌ Docker Compose 語法錯誤: {stderr}")
        return False

def test_profiles():
    """測試不同的 profiles"""
    profiles = ["api", "gui", "ollama"]
    
    print("🔍 測試 Docker Compose Profiles...")
    
    for profile in profiles:
        print(f"  測試 profile: {profile}")
        success, stdout, stderr = run_command(f"docker-compose --profile {profile} config")
        if success:
            print(f"  ✅ Profile '{profile}' 配置正確")
        else:
            print(f"  ❌ Profile '{profile}' 配置錯誤: {stderr}")
            return False
    
    return True

def test_dockerfile_syntax():
    """測試 Dockerfile 語法"""
    print("🔍 測試 Dockerfile 語法...")
    
    success, stdout, stderr = run_command("docker build --dry-run .")
    if success:
        print("✅ Dockerfile 語法正確")
        return True
    else:
        # Docker build --dry-run 可能不被支援，嘗試其他方法
        success, stdout, stderr = run_command("docker build -t test-image --no-cache .", capture_output=False)
        if success:
            print("✅ Dockerfile 可以成功建構")
            # 清理測試映像
            run_command("docker rmi test-image")
            return True
        else:
            print(f"❌ Dockerfile 建構失敗: {stderr}")
            return False

def check_required_files():
    """檢查必要的檔案是否存在"""
    print("🔍 檢查必要檔案...")
    
    required_files = [
        "Dockerfile",
        "docker-compose.yml",
        "requirements.txt",
        "n8n_workflow_api.py",
        "n8n_workflow_search_gui.py",
        "n8n_workflow_scraper.py"
    ]
    
    missing_files = []
    for file in required_files:
        try:
            with open(file, 'r'):
                pass
        except FileNotFoundError:
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 缺少必要檔案: {', '.join(missing_files)}")
        return False
    else:
        print("✅ 所有必要檔案都存在")
        return True

def check_docker_availability():
    """檢查 Docker 是否可用"""
    print("🔍 檢查 Docker 環境...")
    
    # 檢查 Docker
    success, stdout, stderr = run_command("docker --version")
    if not success:
        print("❌ Docker 未安裝或不可用")
        return False
    
    print(f"✅ Docker 版本: {stdout.strip()}")
    
    # 檢查 Docker Compose
    success, stdout, stderr = run_command("docker-compose --version")
    if not success:
        print("❌ Docker Compose 未安裝或不可用")
        return False
    
    print(f"✅ Docker Compose 版本: {stdout.strip()}")
    
    # 檢查 Docker 是否運行
    success, stdout, stderr = run_command("docker info")
    if not success:
        print("❌ Docker 服務未運行")
        return False
    
    print("✅ Docker 服務正在運行")
    return True

def analyze_compose_config():
    """分析 Docker Compose 配置"""
    print("🔍 分析 Docker Compose 配置...")
    
    try:
        with open("docker-compose.yml", 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        services = config.get('services', {})
        print(f"📊 發現 {len(services)} 個服務:")
        
        for service_name, service_config in services.items():
            ports = service_config.get('ports', [])
            profiles = service_config.get('profiles', ['default'])
            
            print(f"  - {service_name}")
            print(f"    端口: {ports}")
            print(f"    Profiles: {profiles}")
        
        return True
        
    except Exception as e:
        print(f"❌ 分析配置時發生錯誤: {e}")
        return False

def main():
    """主測試函數"""
    print("🐳 Docker 配置測試開始")
    print("=" * 50)
    
    tests = [
        ("檢查必要檔案", check_required_files),
        ("檢查 Docker 環境", check_docker_availability),
        ("測試 Docker Compose 語法", test_docker_compose_syntax),
        ("測試 Profiles", test_profiles),
        ("分析配置", analyze_compose_config),
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
        print("🎉 所有測試通過！Docker 配置正確。")
        print("\n💡 使用建議:")
        print("  - 預設模式: docker-compose up -d")
        print("  - API 模式: docker-compose --profile api up -d")
        print("  - GUI 模式: docker-compose --profile gui up -d")
        print("  - 包含 Ollama: docker-compose --profile ollama up -d")
    else:
        print("⚠️  部分測試失敗，請檢查配置。")
        sys.exit(1)

if __name__ == "__main__":
    main()
