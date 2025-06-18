# The Ultimate Beginner's Guide to an AI-Powered Telegram Assistant (PDF, Brave search & Google Suite) - 工作流程教學

## 📋 基本資訊

- **工作流程名稱**: The Ultimate Beginner's Guide to an AI-Powered Telegram Assistant (PDF, Brave search & Google Suite)
- **工作流程 ID**: ALajUsJPZXlb0D1x
- **節點數量**: 79
- **來源檔案**: 4525.json
- **生成時間**: 2025-06-18 20:22:34

## 📖 工作流程描述

The Ultimate Beginner's Guide to an AI-Powered Telegram Assistant (PDF, Brave search & Google Suite)；工作流程包含 79 個節點；節點類型：n8n-nodes-base.stickyNote、n8n-nodes-base.telegramTrigger、n8n-nodes-base.telegram、n8n-nodes-base.set、@n8n/n8n-nodes-langchain.openAi；包含觸發器；包含HTTP請求

## 🛠️ 詳細設定步驟

### 步驟 1：設定 Sticky Note12
1. 拖曳「Sticky Note12」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **content**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 2：設定 Listen for incoming events
1. 拖曳「Telegram Trigger」節點到工作流程畫布上
2. 設定 Telegram Bot 觸發器：
3. 在憑證管理中設定 Telegram Bot Token

### 步驟 3：設定 Download voice file
1. 拖曳「Telegram」節點到工作流程畫布上
2. 設定 Telegram 訊息發送：
3. 在憑證管理中設定 Telegram Bot Token

### 步驟 4：設定 Combine content and set properties
1. 拖曳「Set」節點到工作流程畫布上
2. 設定資料處理：
3. 測試節點確保資料處理正確

### 步驟 5：設定 Convert audio to text
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 6：設定 Send Typing action
1. 拖曳「Telegram」節點到工作流程畫布上
2. 設定 Telegram 訊息發送：
3. 在憑證管理中設定 Telegram Bot Token

### 步驟 7：設定 Sticky Note13
1. 拖曳「Sticky Note13」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **content**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 8：設定 Sticky Note14
1. 拖曳「Sticky Note14」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **content**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 9：設定 Sticky Note15
1. 拖曳「Sticky Note15」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **content**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 10：設定 Sticky Note16
1. 拖曳「Sticky Note16」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **content**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 11：設定 Call Replicate API
1. 拖曳「HTTP Request」節點到工作流程畫布上
2. 點擊節點，然後設定：
3. 測試節點確保 API 請求正常運作

### 步驟 12：設定 Send AI Voice Response via Telegram
1. 拖曳「Telegram」節點到工作流程畫布上
2. 設定 Telegram 訊息發送：
3. 在憑證管理中設定 Telegram Bot Token

### 步驟 13：設定 Download Replicate Audio
1. 拖曳「HTTP Request」節點到工作流程畫布上
2. 點擊節點，然後設定：
3. 測試節點確保 API 請求正常運作

### 步驟 14：設定 Google Gemini Chat Model
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 15：設定 Send AI Text Response (Chat)
1. 拖曳「Telegram」節點到工作流程畫布上
2. 設定 Telegram 訊息發送：
3. 在憑證管理中設定 Telegram Bot Token

### 步驟 16：設定 Send Brave Search Results via Telegram
1. 拖曳「Telegram」節點到工作流程畫布上
2. 設定 Telegram 訊息發送：
3. 在憑證管理中設定 Telegram Bot Token

### 步驟 17：設定 Think
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 18：設定 Calculator
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 19：設定 Date & Time
1. 拖曳「Date & Time」節點到工作流程畫布上
2. 點擊節點進行設定：
3. 測試節點確保設定正確

### 步驟 20：設定 Brave Search 2
1. 拖曳「Brave Search 2」節點到工作流程畫布上
2. 點擊節點進行設定：
3. 測試節點確保設定正確

### 步驟 21：設定 Brave Search
1. 拖曳「Brave Search」節點到工作流程畫布上
2. 點擊節點進行設定：
3. 測試節點確保設定正確

### 步驟 22：設定 Google Calendar Create Event
1. 拖曳「Google Calendar Create Event」節點到工作流程畫布上
2. 點擊節點進行設定：
3. 測試節點確保設定正確

### 步驟 23：設定 Google Calendar Next Holiday
1. 拖曳「Google Calendar Next Holiday」節點到工作流程畫布上
2. 點擊節點進行設定：
3. 測試節點確保設定正確

### 步驟 24：設定 Question and Answer Chain
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 25：設定 Vector Store Retriever
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 26：設定 Qdrant Vector Store1
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 27：設定 Embeddings OpenAI1
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 28：設定 Sticky Note1
1. 拖曳「Sticky Note1」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **content**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 29：設定 Gemini for RAG Answer
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 30：設定 Send RAG Answer via Telegram
1. 拖曳「Telegram」節點到工作流程畫布上
2. 設定 Telegram 訊息發送：
3. 在憑證管理中設定 Telegram Bot Token

### 步驟 31：設定 Refresh collection
1. 拖曳「HTTP Request」節點到工作流程畫布上
2. 點擊節點，然後設定：
3. 測試節點確保 API 請求正常運作

### 步驟 32：設定 Search PDFs
1. 拖曳「Search PDFs」節點到工作流程畫布上
2. 點擊節點進行設定：
3. 測試節點確保設定正確

### 步驟 33：設定 Send PDF Search Results via Telegram
1. 拖曳「Telegram」節點到工作流程畫布上
2. 設定 Telegram 訊息發送：
3. 在憑證管理中設定 Telegram Bot Token

### 步驟 34：設定 Send Qdrant Indexing Confirmation
1. 拖曳「Telegram」節點到工作流程畫布上
2. 設定 Telegram 訊息發送：
3. 在憑證管理中設定 Telegram Bot Token

### 步驟 35：設定 Mistral Upload
1. 拖曳「HTTP Request」節點到工作流程畫布上
2. 點擊節點，然後設定：
3. 測試節點確保 API 請求正常運作

### 步驟 36：設定 Mistral Signed URL
1. 拖曳「HTTP Request」節點到工作流程畫布上
2. 點擊節點，然後設定：
3. 測試節點確保 API 請求正常運作

### 步驟 37：設定 Mistral DOC OCR
1. 拖曳「HTTP Request」節點到工作流程畫布上
2. 點擊節點，然後設定：
3. 測試節點確保 API 請求正常運作

### 步驟 38：設定 Loop Over Items
1. 拖曳「Loop Over Items」節點到工作流程畫布上
2. 點擊節點進行設定：
3. 測試節點確保設定正確

### 步驟 39：設定 Embeddings OpenAI
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 40：設定 Default Data Loader
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 41：設定 Token Splitter
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 42：設定 Code
1. 拖曳「Code」節點到工作流程畫布上
2. 設定 JavaScript 程式碼：
   - **JavaScript Code**: 輸入自定義的處理邏輯
3. 測試程式碼確保邏輯正確

### 步驟 43：設定 Wait
1. 拖曳「Wait」節點到工作流程畫布上
2. 設定等待時間：
3. 根據需要調整等待時間

### 步驟 44：設定 Qdrant Vector Store
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 45：設定 Set page
1. 拖曳「Set」節點到工作流程畫布上
2. 設定資料處理：
3. 測試節點確保資料處理正確

### 步驟 46：設定 Get PDF
1. 拖曳「Get PDF」節點到工作流程畫布上
2. 點擊節點進行設定：
3. 測試節點確保設定正確

### 步驟 47：設定 Sticky Note2
1. 拖曳「Sticky Note2」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **content**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 48：設定 Sticky Note3
1. 拖曳「Sticky Note3」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **content**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 49：設定 Sticky Note4
1. 拖曳「Sticky Note4」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **content**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 50：設定 Sticky Note5
1. 拖曳「Sticky Note5」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **content**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 51：設定 AI Agent1
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 52：設定 Determine content type1
1. 拖曳「Switch」節點到工作流程畫布上
2. 設定條件分支：
3. 測試各個分支路徑

### 步驟 53：設定 Google Gemini Chat Model1
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 54：設定 Think1
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 55：設定 Calculator1
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 56：設定 Date & Time1
1. 拖曳「Date & Time1」節點到工作流程畫布上
2. 點擊節點進行設定：
3. 測試節點確保設定正確

### 步驟 57：設定 Brave Search1
1. 拖曳「Brave Search1」節點到工作流程畫布上
2. 點擊節點進行設定：
3. 測試節點確保設定正確

### 步驟 58：設定 Google Calendar Create Event1
1. 拖曳「Google Calendar Create Event1」節點到工作流程畫布上
2. 點擊節點進行設定：
3. 測試節點確保設定正確

### 步驟 59：設定 Google Calendar Next Holiday1
1. 拖曳「Google Calendar Next Holiday1」節點到工作流程畫布上
2. 點擊節點進行設定：
3. 測試節點確保設定正確

### 步驟 60：設定 AI Agent3
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 61：設定 Window Buffer Memory2
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 62：設定 Help Responder1
1. 拖曳「Telegram」節點到工作流程畫布上
2. 設定 Telegram 訊息發送：
3. 在憑證管理中設定 Telegram Bot Token

### 步驟 63：設定 Window Buffer Memory
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 64：設定 Airbnb MCP
1. 拖曳「Airbnb MCP」節點到工作流程畫布上
2. 點擊節點進行設定：
3. 測試節點確保設定正確

### 步驟 65：設定 Airbnb Tools
1. 拖曳「Airbnb Tools」節點到工作流程畫布上
2. 點擊節點進行設定：
3. 測試節點確保設定正確

### 步驟 66：設定 Airbnb MCP1
1. 拖曳「Airbnb MCP1」節點到工作流程畫布上
2. 點擊節點進行設定：
3. 測試節點確保設定正確

### 步驟 67：設定 Airbnb Tools1
1. 拖曳「Airbnb Tools1」節點到工作流程畫布上
2. 點擊節點進行設定：
3. 測試節點確保設定正確

### 步驟 68：設定 Google Drive
1. 拖曳「Google Drive」節點到工作流程畫布上
2. 點擊節點進行設定：
3. 測試節點確保設定正確

### 步驟 69：設定 Google Docs
1. 拖曳「Google Docs」節點到工作流程畫布上
2. 點擊節點進行設定：
3. 測試節點確保設定正確

### 步驟 70：設定 Google Drive1
1. 拖曳「Google Drive1」節點到工作流程畫布上
2. 點擊節點進行設定：
3. 測試節點確保設定正確

### 步驟 71：設定 Google Drive2
1. 拖曳「Google Drive2」節點到工作流程畫布上
2. 點擊節點進行設定：
3. 測試節點確保設定正確

### 步驟 72：設定 Edit Fields
1. 拖曳「Set」節點到工作流程畫布上
2. 設定資料處理：
3. 測試節點確保資料處理正確

### 步驟 73：設定 Send Invoice PDF via Telegram
1. 拖曳「Telegram」節點到工作流程畫布上
2. 設定 Telegram 訊息發送：
3. 在憑證管理中設定 Telegram Bot Token

### 步驟 74：設定 Sticky Note
1. 拖曳「Sticky Note」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **content**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 75：設定 Sticky Note6
1. 拖曳「Sticky Note6」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **content**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 76：設定 Google Calendar 2
1. 拖曳「Google Calendar 2」節點到工作流程畫布上
2. 點擊節點進行設定：
3. 測試節點確保設定正確

### 步驟 77：設定 Send Birthday List via Telegram
1. 拖曳「Telegram」節點到工作流程畫布上
2. 設定 Telegram 訊息發送：
3. 在憑證管理中設定 Telegram Bot Token

### 步驟 78：設定 Sticky Note7
1. 拖曳「Sticky Note7」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **content**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 79：設定 Sticky Note8
1. 拖曳「Sticky Note8」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **content**: 根據需求設定此參數
3. 測試節點確保設定正確


## 💡 建議用途與延伸應用

### 適用場景
- API 資料整合與同步
- 第三方服務整合

### 延伸應用建議
- 添加錯誤處理和重試機制
- 整合更多通知管道（如 LINE、WeChat）
- 加入資料持久化存儲
- 實作條件分支處理不同情況
- 添加日誌記錄和監控功能

## 🔧 設定注意事項

1. **認證設定**: 請確保所有需要認證的節點都已正確設定 API 金鑰或認證資訊
2. **觸發條件**: 檢查觸發器的設定是否符合您的需求
3. **錯誤處理**: 建議為關鍵節點添加錯誤處理邏輯
4. **測試執行**: 在正式使用前，請先進行測試執行

## 📚 相關資源

- [n8n 官方文檔](https://docs.n8n.io/)
- [n8n 社群範例](https://n8n.io/workflows/)
- [節點參考文檔](https://docs.n8n.io/integrations/)

---
*此教學檔案由 n8n Workflow 智能搜尋系統自動生成*
