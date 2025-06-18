# n8n Workflow 智能搜尋與教學生成系統

一個基於 LangChain + ChromaDB 的 n8n 工作流程智能搜尋系統，現在新增了 AI 教學生成功能！

## 🆕 新功能：雙頁籤介面

### 🔍 第一個頁籤：n8n Workflow 智能搜尋
- 基於向量相似度的智能搜尋
- 自然語言查詢工作流程
- 自動生成工作流程教學文件
- 支援工作流程儲存和管理

### 🤖 第二個頁籤：n8n Workflow 教學生成
- **全新功能**：AI 驅動的節點教學生成
- 支援三種 AI 提供商：OpenAI、Gemini、Ollama
- 即時回答 n8n 節點設定問題
- 專業的繁體中文教學內容

## 🚀 功能特色

- **雙頁籤介面**: 搜尋與教學生成分離，使用更直觀
- **智能搜尋**: 基於向量相似度的語義搜尋
- **AI 教學**: 支援多種 AI 模型的即時教學生成
- **暗色主題**: 護眼的深色介面設計
- **自動索引**: 每次啟動自動更新工作流程索引
- **教學文件**: 自動生成詳細的設定步驟說明

## 📋 系統需求

- Python 3.7+
- 網路連線

## 🔧 安裝步驟

1. 克隆或下載此專案
2. 安裝依賴套件：
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 使用方法

### 1. 設定 AI 服務（新功能）
複製並編輯 `.env` 檔案：

```env
# 選擇 AI 提供商：openai, gemini, ollama
AI_PROVIDER=openai

# OpenAI 設定
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo

# 其他設定
MAX_TOKENS=2000
TEMPERATURE=0.7
```

詳細設定請參考 `AI_SETUP_GUIDE.md`

### 2. 啟動應用程式
```bash
python n8n_workflow_search_gui.py
```

### 3. 開啟瀏覽器
訪問 http://localhost:7862

### 4. 使用雙頁籤功能

#### 🔍 智能搜尋頁籤
1. 輸入自然語言描述，例如：
   - "每天早上寄出氣象通知"
   - "監控伺服器異常發 Discord 警告"
   - "Telegram Bot 自動回覆"
2. 點擊「搜尋工作流程」
3. 從結果中選擇合適的工作流程
4. 點擊「儲存選中的工作流程」生成教學文件

#### 🤖 AI 教學生成頁籤
1. 輸入具體問題，例如：
   - "OpenWeather 節點該如何設定？"
   - "如何設定 Telegram Bot 自動回覆？"
   - "Discord Webhook 節點的參數設定"
2. 點擊「生成教學」
3. 獲得詳細的設定指導

## 📁 檔案結構

```
n8n-scraper/
├── n8n_workflow_search_gui.py    # 主程式（含雙頁籤介面）
├── .env                          # AI 設定檔案
├── AI_SETUP_GUIDE.md            # AI 設定指南
├── test_ai_tutorial.py          # AI 功能測試腳本
├── requirements.txt             # 依賴套件
├── README.md                    # 說明文件
├── selected_workflows/          # 儲存的工作流程
├── chroma_db/                   # 向量資料庫
└── *.json                       # n8n 工作流程檔案
```

## 🔍 API 端點

程式會使用以下 API 端點：

1. **搜尋 workflows**:
   ```
   https://n8n.io/api/product-api/workflows/search?rows={rows}&category={category}&page={page}
   ```

2. **下載 workflow 詳細資料**:
   ```
   https://api.n8n.io/api/workflows/templates/{workflowID}
   ```

## ⚠️ 注意事項

- 每次請求間會自動延遲 1 秒，避免對伺服器造成過大負擔
- 請確保網路連線穩定
- 大量下載時請耐心等待
- 如果遇到網路錯誤，程式會自動跳過並繼續下載其他檔案

## 🐛 故障排除

### 常見問題

1. **無法連接到伺服器**
   - 檢查網路連線
   - 確認防火牆設定

2. **下載失敗**
   - 檢查 workflow ID 是否正確
   - 確認 API 端點是否可用

3. **JSON 解析錯誤**
   - 可能是 API 回傳格式異常
   - 程式會自動跳過並繼續處理其他檔案

## �️ 技術架構

- **前端**：Gradio（暗色主題）
- **搜尋引擎**：LangChain + ChromaDB
- **AI 整合**：OpenAI、Gemini、Ollama
- **向量模型**：sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

## 🔧 AI 提供商選擇

1. **OpenAI**（推薦）
   - 高品質回應
   - 快速回應時間
   - 需要 API 金鑰

2. **Gemini**
   - 免費額度較高
   - Google 生態系整合
   - 需要 API 金鑰

3. **Ollama**
   - 完全本地運行
   - 無需 API 金鑰
   - 需要本地安裝

## 📚 相關資源

- [n8n 官方文檔](https://docs.n8n.io/)
- [n8n 社群範例](https://n8n.io/workflows/)
- [節點參考文檔](https://docs.n8n.io/integrations/)

## �📝 更新日誌

### v2.0.0（最新）
- 🆕 新增雙頁籤介面設計
- 🤖 新增 AI 教學生成功能
- 🔧 支援 OpenAI、Gemini、Ollama 三種 AI 提供商
- 🎨 全新暗色主題介面
- 📖 智能工作流程搜尋與教學文件生成

### v1.0.0
- 初始版本
- 支援批量下載 n8n workflows
- Gradio 圖形介面
- 完整錯誤處理機制

## 📄 授權

MIT License - 此專案僅供學習和研究使用，請遵守相關服務的使用條款。
