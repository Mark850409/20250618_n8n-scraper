# n8n Workflow 智能搜尋與教學生成系統

基於 LangChain + ChromaDB 的向量搜尋引擎，幫助您快速找到相關的 n8n 工作流程並生成詳細教學。

## 🚀 功能特色

- **智能語意搜尋**: 使用向量搜尋技術，支援中文語意查詢
- **自動索引建立**: 自動掃描並索引所有 workflow JSON 檔案
- **詳細結果展示**: 顯示相似度、工作流程名稱、節點結構等資訊
- **教學自動生成**: 自動產生詳細的 Markdown 教學文件
- **互動式介面**: 友善的命令列互動介面

## 📋 系統需求

- Python 3.8+
- 至少 4GB RAM（用於 Embedding 模型）
- 網路連線（首次下載模型時需要）

## 🔧 安裝步驟

1. 安裝依賴套件：
   ```bash
   pip install -r requirements_search.txt
   ```

2. 確保您的 workflow JSON 檔案在當前目錄或子目錄中

3. 執行程式：
   ```bash
   python n8n_workflow_search.py
   ```

## 🎯 使用方法

### 1. 啟動程式
```bash
python n8n_workflow_search.py
```

### 2. 輸入需求描述
程式會提示您輸入想要實作的工作流程描述，例如：
- "每天早上寄出氣象通知"
- "監控伺服器異常發 Discord 警告"
- "定時備份資料庫並發送報告"

### 3. 查看搜尋結果
系統會顯示最相似的 3 個工作流程，包含：
- 相似度分數
- 工作流程名稱
- 節點結構
- 功能描述

### 4. 選擇並儲存
選擇您想要的工作流程編號，系統會：
- 複製 JSON 檔案到 `selected_workflows/` 目錄
- 生成詳細的教學 Markdown 檔案

## 📁 檔案結構

```
n8n-scraper/
├── n8n_workflow_search.py      # 主程式
├── requirements_search.txt     # 依賴套件
├── README_search.md           # 使用說明
├── chroma_db/                 # 向量資料庫（自動生成）
├── selected_workflows/        # 選中的工作流程（自動生成）
│   ├── workflow_xxxx.json    # 工作流程 JSON 檔案
│   └── workflow_xxxx_教學.md  # 自動生成的教學檔案
└── workflows_*/               # 原始 workflow 檔案目錄
```

## 🔍 搜尋範例

### 輸入範例
```
🔍 請輸入您的需求描述: 每天定時發送天氣預報到 Discord
```

### 輸出範例
```
🔍 正在匹配最相近的工作流程...
📝 搜尋關鍵字：每天定時發送天氣預報到 Discord
================================================================================

[1] 來源檔案：workflow_3040.json
🧠 相似度：0.8234
🔧 工作流程名稱：Daily Weather Notification
📌 標籤：workflow
📝 自定標籤：Daily Weather Notification
📖 描述：每日天氣預報自動發送系統，整合氣象 API 並發送到 Discord 頻道

🧩 Workflow 結構：

Trigger：Schedule Trigger（n8n-nodes-base.scheduleTrigger）
Weather API（n8n-nodes-base.httpRequest）
Discord Notification（n8n-nodes-base.discord）
```

## 🛠️ 技術架構

- **向量搜尋**: ChromaDB + HuggingFace Embeddings
- **語言模型**: sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
- **資料處理**: LangChain Document Processing
- **介面**: 命令列互動介面

## ⚠️ 注意事項

1. **首次執行**: 第一次執行時會下載 Embedding 模型，需要網路連線
2. **記憶體需求**: Embedding 模型需要約 500MB 記憶體
3. **檔案格式**: 確保 JSON 檔案格式正確且包含 workflow 結構
4. **中文支援**: 完全支援繁體中文搜尋和輸出

## 🐛 故障排除

### 常見問題

1. **找不到 JSON 檔案**
   - 確保 workflow JSON 檔案在當前目錄或子目錄中
   - 檢查檔案名稱是否以 .json 結尾

2. **記憶體不足**
   - 關閉其他應用程式釋放記憶體
   - 考慮使用較小的 Embedding 模型

3. **搜尋結果不準確**
   - 嘗試使用更具體的關鍵字
   - 重新建立向量索引（刪除 chroma_db 目錄）

## 📝 更新日誌

### v1.0.0
- 初始版本
- 支援向量搜尋和教學生成
- 繁體中文介面
- 自動索引建立

## 📄 授權

此專案僅供學習和研究使用。
