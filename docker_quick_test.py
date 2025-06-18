#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Docker 快速測試腳本
"""

import yaml
import os

def test_compose_file():
    """測試 docker-compose.yml 文件"""
    print("🔍 測試 docker-compose.yml 文件...")
    
    try:
        with open('docker-compose.yml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        print("✅ YAML 語法正確")
        
        # 檢查服務
        services = config.get('services', {})
        print(f"📊 發現 {len(services)} 個服務:")
        
        for service_name, service_config in services.items():
            ports = service_config.get('ports', [])
            profiles = service_config.get('profiles', ['預設'])
            environment = service_config.get('environment', [])
            
            print(f"  🔧 {service_name}:")
            print(f"     端口: {ports}")
            print(f"     Profiles: {profiles}")
            print(f"     環境變數數量: {len(environment)}")
        
        return True
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        return False

def test_dockerfile():
    """測試 Dockerfile"""
    print("\n🔍 測試 Dockerfile...")
    
    try:
        with open('Dockerfile', 'r', encoding='utf-8') as f:
            content = f.read()
        
        print("✅ Dockerfile 可讀取")
        
        # 檢查關鍵指令
        required_instructions = ['FROM', 'WORKDIR', 'COPY', 'RUN', 'EXPOSE', 'CMD']
        found_instructions = []
        
        for instruction in required_instructions:
            if instruction in content:
                found_instructions.append(instruction)
        
        print(f"📊 找到指令: {found_instructions}")
        
        if len(found_instructions) >= 5:
            print("✅ Dockerfile 結構完整")
            return True
        else:
            print("⚠️  Dockerfile 可能不完整")
            return False
            
    except Exception as e:
        print(f"❌ 錯誤: {e}")
        return False

def check_required_files():
    """檢查必要文件"""
    print("\n🔍 檢查必要文件...")
    
    required_files = [
        'docker-compose.yml',
        'Dockerfile',
        'requirements.txt',
        'n8n_workflow_api.py',
        'n8n_workflow_search_gui.py',
        'n8n_workflow_scraper.py'
    ]
    
    missing_files = []
    existing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            existing_files.append(file)
        else:
            missing_files.append(file)
    
    print(f"✅ 存在的文件 ({len(existing_files)}):")
    for file in existing_files:
        print(f"   - {file}")
    
    if missing_files:
        print(f"❌ 缺少的文件 ({len(missing_files)}):")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ 所有必要文件都存在")
    return True

def main():
    """主函數"""
    print("🐳 Docker 配置快速測試")
    print("=" * 40)
    
    tests = [
        check_required_files,
        test_dockerfile,
        test_compose_file
    ]
    
    passed = 0
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 40)
    print(f"📊 測試結果: {passed}/{len(tests)} 通過")
    
    if passed == len(tests):
        print("🎉 基本配置測試通過！")
        print("\n💡 使用方式:")
        print("  預設 (所有服務): docker-compose up -d")
        print("  僅 API:         docker-compose --profile api up -d")
        print("  僅 GUI:         docker-compose --profile gui up -d")
        print("  包含 Ollama:    docker-compose --profile ollama up -d")
    else:
        print("⚠️  部分測試失敗")

if __name__ == "__main__":
    main()
