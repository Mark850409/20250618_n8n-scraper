# n8n Workflow API 服務

結合 Flask OpenAPI 的 n8n 工作流程搜尋與爬取 API 服務，整合了原有的 GUI 功能並提供 RESTful API 介面。

## 🚀 功能特色

- **智能工作流程搜尋**: 基於 LangChain + ChromaDB 的向量搜尋引擎
- **批量工作流程爬取**: 支援完整分頁爬取，自動計算總頁數
- **AI 教學內容生成**: 支援 OpenAI、Gemini、Ollama 多種 AI 模型
- **工作流程教學文件生成**: 自動生成詳細的設定教學
- **RESTful API 介面**: 標準的 REST API 設計
- **OpenAPI 文檔支援**: 自動生成 Swagger 文檔
- **健康檢查**: 系統狀態監控

## 📦 安裝依賴

```bash
pip install -r requirements.txt
```

## 🔧 環境設定

創建 `.env` 檔案並設定 AI 服務參數（可選）：

```env
# AI 服務設定 (可選)
AI_PROVIDER=openai  # 可選: openai, gemini, ollama
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo

# Gemini 設定
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-pro

# Ollama 設定
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# API 服務設定
PORT=5000
DEBUG=False
```

## 🚀 啟動服務

```bash
python n8n_workflow_api.py
```

服務將在 `http://localhost:5000` 啟動，API 文檔可在 `http://localhost:5000/docs/` 查看。

## 📚 API 端點

### 系統資訊

- `GET /api/v1/health` - 系統健康檢查
- `GET /api/v1/info` - 取得系統資訊

### 工作流程搜尋

- `POST /api/v1/search/workflows` - 搜尋工作流程
- `POST /api/v1/search/workflows/save` - 儲存選中的工作流程

### 工作流程爬取

- `POST /api/v1/scraper/workflows` - 爬取工作流程
- `GET /api/v1/scraper/categories` - 取得可用類別

### AI 教學生成

- `POST /api/v1/tutorial/generate` - 生成 AI 教學內容
- `GET /api/v1/tutorial/config` - 取得 AI 配置資訊

## 💡 使用範例

### 1. 搜尋工作流程

```bash
curl -X POST "http://localhost:5000/api/v1/search/workflows" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "telegram bot",
    "top_k": 5
  }'
```

### 2. 儲存工作流程

```bash
curl -X POST "http://localhost:5000/api/v1/search/workflows/save" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_index": 0
  }'
```

### 3. 爬取工作流程

```bash
curl -X POST "http://localhost:5000/api/v1/scraper/workflows" \
  -H "Content-Type: application/json" \
  -d '{
    "rows": 20,
    "category": "AI"
  }'
```

### 4. 生成 AI 教學

```bash
curl -X POST "http://localhost:5000/api/v1/tutorial/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "如何設定 Telegram Bot 節點？"
  }'
```

## 🧪 測試

運行測試範例：

```bash
python api_usage_examples.py
```

## 📖 API 文檔

啟動服務後，可在以下位置查看完整的 API 文檔：

- Swagger UI: `http://localhost:5000/docs/`
- OpenAPI JSON: `http://localhost:5000/swagger.json`

## 🔍 API 回應格式

所有 API 都遵循統一的回應格式：

```json
{
  "success": true,
  "message": "操作成功",
  "data": { ... }
}
```

### 搜尋工作流程回應範例

```json
{
  "success": true,
  "message": "找到 3 個相關工作流程",
  "total_results": 3,
  "results": [
    {
      "index": 0,
      "name": "Telegram Bot Auto Reply",
      "filename": "telegram_bot.json",
      "description": "自動回覆 Telegram 訊息的機器人",
      "similarity_score": 0.8542,
      "node_count": 5,
      "workflow_id": "12345"
    }
  ]
}
```

### 爬取工作流程回應範例

```json
{
  "success": true,
  "message": "爬取任務完成，狀態：✅ 完成",
  "status": "✅ 完成",
  "details": "📊 爬取統計資訊:\n   - 總筆數: 50\n   - 每頁筆數: 20\n..."
}
```

## 🛠️ 開發說明

### 專案結構

```
n8n-scraper/
├── n8n_workflow_api.py          # Flask API 主程式
├── n8n_workflow_search_gui.py   # 搜尋功能模組
├── n8n_workflow_scraper.py      # 爬取功能模組
├── api_usage_examples.py        # API 使用範例
├── requirements.txt             # 依賴套件
└── API_README.md               # API 說明文檔
```

### 擴展功能

要添加新的 API 端點，可以：

1. 在對應的 Namespace 中添加新的 Resource 類別
2. 定義請求和回應的資料模型
3. 實作業務邏輯
4. 更新文檔

## ⚠️ 注意事項

1. **AI 功能**: 需要設定對應的 API 金鑰才能使用 AI 教學生成功能
2. **爬取限制**: 大量爬取時請注意 API 限制，系統已內建延遲機制
3. **資源使用**: 向量搜尋功能需要較多記憶體，建議在有足夠資源的環境中運行
4. **網路連線**: 爬取和 AI 功能需要穩定的網路連線

## 🤝 整合現有功能

此 API 服務完全整合了原有的 GUI 功能：

- `n8n_workflow_search_gui.py` 的搜尋和 AI 教學功能
- `n8n_workflow_scraper.py` 的批量爬取功能
- 保持所有原有的功能特性和偏好設定

可以同時使用 GUI 版本和 API 版本，它們共享相同的核心功能。
