# Zeabur 部署指南

## 📋 概述

本項目包含兩個 Gradio 應用程式：
- **端口 7860**: n8n Workflow Scraper - 用於抓取 n8n 工作流程
- **端口 7862**: n8n Workflow Search GUI - 用於搜尋和生成教學

## 🚀 Zeabur 部署步驟

### 1. 準備工作

1. 確保您的代碼已推送到 GitHub 倉庫
2. 登入 [Zeabur](https://zeabur.com) 控制台

### 2. 創建新項目

1. 在 Zeabur 控制台點擊「New Project」
2. 選擇您的 GitHub 倉庫
3. Zeabur 會自動檢測到 `Dockerfile` 並開始構建

### 3. 配置環境變數 (可選)

如果您需要使用 AI 教學生成功能，請在 Zeabur 控制台設定以下環境變數：

```
AI_PROVIDER=openai
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
MAX_TOKENS=2000
TEMPERATURE=0.7
```

### 4. 端口配置

Zeabur 會自動檢測並暴露以下端口：
- `7860` - n8n Workflow Scraper
- `7862` - n8n Workflow Search GUI

### 5. 域名設定

部署完成後，Zeabur 會為每個端口提供一個域名：
- `https://your-app-7860.zeabur.app` - Scraper 介面
- `https://your-app-7862.zeabur.app` - Search 介面

## 🔧 本地測試

在部署到 Zeabur 之前，您可以在本地測試：

```bash
# 使用 Docker Compose
docker-compose up --build

# 或直接使用 Docker
docker build -t n8n-scraper .
docker run -p 7860:7860 -p 7862:7862 n8n-scraper
```

訪問：
- http://localhost:7860 - Scraper 介面
- http://localhost:7862 - Search 介面

## 📁 數據持久化

以下目錄會被持久化保存：
- `chroma_db/` - 向量資料庫
- `selected_workflows/` - 選中的工作流程
- `workflows_all_1/` - 抓取的工作流程數據

## ⚠️ 注意事項

1. **資源使用**: 向量搜尋功能需要較多記憶體，建議使用 Zeabur 的 Pro 方案
2. **AI API**: 如需使用 AI 教學生成功能，請確保設定正確的 API 金鑰
3. **網路延遲**: 首次啟動可能需要下載模型，請耐心等待
4. **數據備份**: 重要數據請定期備份

## 🐛 故障排除

### 應用無法啟動
- 檢查 Zeabur 控制台的構建日誌
- 確認 `requirements.txt` 中的依賴版本
- 如果依賴安裝失敗，系統會自動回退到最小化依賴

### 依賴安裝問題
如果遇到 "No module named 'openai'" 等錯誤：
1. 系統會自動使用簡化模式運行
2. AI 教學生成功能將不可用，但基本搜尋功能仍可正常使用
3. 可以手動安裝缺失的依賴：`pip install openai google-generativeai`

### 端口無法訪問
- 確認 Zeabur 已正確檢測到端口 7860 和 7862
- 檢查防火牆設定
- 查看容器日誌確認服務是否正常啟動

### AI 功能無法使用
- 檢查環境變數是否正確設定
- 確認 API 金鑰有效且有足夠額度
- 如果 AI 套件未安裝，會顯示相應錯誤訊息

### 向量搜尋功能異常
- 如果 LangChain 或 HuggingFace 套件未安裝，系統會自動切換到簡單文字搜尋
- 簡單文字搜尋功能完全可用，只是搜尋精度可能較低

### 本地測試建議
在部署前建議先本地測試：
```bash
# 測試最小化依賴
pip install -r requirements-minimal.txt
python start_simple.py

# 測試完整功能
pip install -r requirements.txt
python n8n_workflow_search_gui.py
```

## 📞 支援

如遇到問題，請檢查：
1. Zeabur 控制台的應用日誌
2. GitHub Issues
3. 項目文檔
