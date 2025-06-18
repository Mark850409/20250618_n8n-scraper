# Telegram ChatBot with multiple sessions - 工作流程教學

## 📋 基本資訊

- **工作流程名稱**: Telegram ChatBot with multiple sessions
- **工作流程 ID**: A7dRnMf9WybO8O02
- **節點數量**: 38
- **來源檔案**: 3798.json
- **生成時間**: 2025-06-18 12:10:39

## 📖 工作流程描述

Telegram ChatBot with multiple sessions；工作流程包含 38 個節點；節點類型：@n8n/n8n-nodes-langchain.lmChatOpenAi、@n8n/n8n-nodes-langchain.memoryBufferWindow、n8n-nodes-base.telegramTrigger、n8n-nodes-base.switch、n8n-nodes-base.googleSheets；包含觸發器

## 🛠️ 詳細設定步驟

### 步驟 1：設定 OpenAI Chat Model
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
   - **Model**: 選擇「gpt-4o-mini」
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 2：設定 Simple Memory
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 3：設定 Get message
1. 拖曳「Telegram Trigger」節點到工作流程畫布上
2. 設定 Telegram Bot 觸發器：
   - **Updates**: 選擇「message」來接收訊息
3. 在憑證管理中設定 Telegram Bot Token

### 步驟 4：設定 Command or text?
1. 拖曳「Switch」節點到工作流程畫布上
2. 設定條件分支：
   - **Rules**: 設定判斷條件和對應的輸出路徑
3. 測試各個分支路徑

### 步驟 5：設定 Get session
1. 拖曳「Google Sheets」節點到工作流程畫布上
2. 設定 Google Sheets 操作：
   - **Document ID**: 輸入 Google Sheets 文件 ID
   - **Sheet Name**: 選擇要操作的工作表
3. 在憑證管理中設定 Google Sheets OAuth2 認證

### 步驟 6：設定 Disable previous session
1. 拖曳「Google Sheets」節點到工作流程畫布上
2. 設定 Google Sheets 操作：
   - **Operation**: 選擇「update」
   - **Document ID**: 輸入 Google Sheets 文件 ID
   - **Sheet Name**: 選擇要操作的工作表
3. 在憑證管理中設定 Google Sheets OAuth2 認證

### 步驟 7：設定 Set new session
1. 拖曳「Google Sheets」節點到工作流程畫布上
2. 設定 Google Sheets 操作：
   - **Operation**: 選擇「append」
   - **Document ID**: 輸入 Google Sheets 文件 ID
   - **Sheet Name**: 選擇要操作的工作表
3. 在憑證管理中設定 Google Sheets OAuth2 認證

### 步驟 8：設定 Session activated
1. 拖曳「Telegram」節點到工作流程畫布上
2. 設定 Telegram 訊息發送：
   - **Text**: 設定要發送的訊息內容
   - **Chat ID**: 設定目標聊天室 ID
3. 在憑證管理中設定 Telegram Bot Token

### 步驟 9：設定 Send response
1. 拖曳「Telegram」節點到工作流程畫布上
2. 設定 Telegram 訊息發送：
   - **Text**: 設定要發送的訊息內容
   - **Chat ID**: 設定目標聊天室 ID
3. 在憑證管理中設定 Telegram Bot Token

### 步驟 10：設定 Update database
1. 拖曳「Google Sheets」節點到工作流程畫布上
2. 設定 Google Sheets 操作：
   - **Operation**: 選擇「append」
   - **Document ID**: 輸入 Google Sheets 文件 ID
   - **Sheet Name**: 選擇要操作的工作表
3. 在憑證管理中設定 Google Sheets OAuth2 認證

### 步驟 11：設定 Sticky Note
1. 拖曳「Sticky Note」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **color**: 根據需求設定此參數
   - **width**: 根據需求設定此參數
   - **height**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 12：設定 Summarization Chain
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 13：設定 OpenAI Chat Model1
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
   - **Model**: 選擇「gpt-4o-mini」
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 14：設定 OpenAI Chat Model2
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
   - **Model**: 選擇「gpt-4o-mini」
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 15：設定 Basic LLM Chain
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
   - **Text**: 設定輸入文本
   - **Messages**: 設定對話訊息
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 16：設定 Get message1
1. 拖曳「Set」節點到工作流程畫布上
2. 設定資料處理：
   - **Assignments**: 設定要修改或新增的資料欄位
3. 測試節點確保資料處理正確

### 步驟 17：設定 Set to expire
1. 拖曳「Google Sheets」節點到工作流程畫布上
2. 設定 Google Sheets 操作：
   - **Operation**: 選擇「update」
   - **Document ID**: 輸入 Google Sheets 文件 ID
   - **Sheet Name**: 選擇要操作的工作表
3. 在憑證管理中設定 Google Sheets OAuth2 認證

### 步驟 18：設定 Exist?
1. 拖曳「Exist?」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **options**: 根據需求設定此參數
   - **conditions**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 19：設定 OK
1. 拖曳「Telegram」節點到工作流程畫布上
2. 設定 Telegram 訊息發送：
   - **Text**: 設定要發送的訊息內容
   - **Chat ID**: 設定目標聊天室 ID
3. 在憑證管理中設定 Telegram Bot Token

### 步驟 20：設定 KO
1. 拖曳「Telegram」節點到工作流程畫布上
2. 設定 Telegram 訊息發送：
   - **Text**: 設定要發送的訊息內容
   - **Chat ID**: 設定目標聊天室 ID
3. 在憑證管理中設定 Telegram Bot Token

### 步驟 21：設定 Trim resume
1. 拖曳「Code」節點到工作流程畫布上
2. 設定 JavaScript 程式碼：
   - **JavaScript Code**: 輸入自定義的處理邏輯
3. 測試程式碼確保邏輯正確

### 步驟 22：設定 Get session1
1. 拖曳「Google Sheets」節點到工作流程畫布上
2. 設定 Google Sheets 操作：
   - **Document ID**: 輸入 Google Sheets 文件 ID
   - **Sheet Name**: 選擇要操作的工作表
3. 在憑證管理中設定 Google Sheets OAuth2 認證

### 步驟 23：設定 Prompt + Resume
1. 拖曳「Code」節點到工作流程畫布上
2. 設定 JavaScript 程式碼：
   - **JavaScript Code**: 輸入自定義的處理邏輯
3. 測試程式碼確保邏輯正確

### 步驟 24：設定 Send summary
1. 拖曳「Telegram」節點到工作流程畫布上
2. 設定 Telegram 訊息發送：
   - **Text**: 設定要發送的訊息內容
   - **Chat ID**: 設定目標聊天室 ID
3. 在憑證管理中設定 Telegram Bot Token

### 步驟 25：設定 Get message2
1. 拖曳「Set」節點到工作流程畫布上
2. 設定資料處理：
   - **Assignments**: 設定要修改或新增的資料欄位
3. 測試節點確保資料處理正確

### 步驟 26：設定 Trim question
1. 拖曳「Code」節點到工作流程畫布上
2. 設定 JavaScript 程式碼：
   - **JavaScript Code**: 輸入自定義的處理邏輯
3. 測試程式碼確保邏輯正確

### 步驟 27：設定 Set new current session
1. 拖曳「Google Sheets」節點到工作流程畫布上
2. 設定 Google Sheets 操作：
   - **Operation**: 選擇「update」
   - **Document ID**: 輸入 Google Sheets 文件 ID
   - **Sheet Name**: 選擇要操作的工作表
3. 在憑證管理中設定 Google Sheets OAuth2 認證

### 步驟 28：設定 Response + Text
1. 拖曳「Google Sheets」節點到工作流程畫布上
2. 設定 Google Sheets 操作：
   - **Document ID**: 輸入 Google Sheets 文件 ID
   - **Sheet Name**: 選擇要操作的工作表
3. 在憑證管理中設定 Google Sheets OAuth2 認證

### 步驟 29：設定 fullText
1. 拖曳「Code」節點到工作流程畫布上
2. 設定 JavaScript 程式碼：
   - **JavaScript Code**: 輸入自定義的處理邏輯
3. 測試程式碼確保邏輯正確

### 步驟 30：設定 Send answer
1. 拖曳「Telegram」節點到工作流程畫布上
2. 設定 Telegram 訊息發送：
   - **Text**: 設定要發送的訊息內容
   - **Chat ID**: 設定目標聊天室 ID
3. 在憑證管理中設定 Telegram Bot Token

### 步驟 31：設定 Send current session
1. 拖曳「Telegram」節點到工作流程畫布上
2. 設定 Telegram 訊息發送：
   - **Text**: 設定要發送的訊息內容
   - **Chat ID**: 設定目標聊天室 ID
3. 在憑證管理中設定 Telegram Bot Token

### 步驟 32：設定 Sticky Note1
1. 拖曳「Sticky Note1」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **width**: 根據需求設定此參數
   - **height**: 根據需求設定此參數
   - **content**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 33：設定 Sticky Note2
1. 拖曳「Sticky Note2」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **width**: 根據需求設定此參數
   - **height**: 根據需求設定此參數
   - **content**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 34：設定 Sticky Note3
1. 拖曳「Sticky Note3」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **width**: 根據需求設定此參數
   - **height**: 根據需求設定此參數
   - **content**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 35：設定 Sticky Note4
1. 拖曳「Sticky Note4」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **width**: 根據需求設定此參數
   - **height**: 根據需求設定此參數
   - **content**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 36：設定 Sticky Note5
1. 拖曳「Sticky Note5」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **width**: 根據需求設定此參數
   - **height**: 根據需求設定此參數
   - **content**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 37：設定 Sticky Note6
1. 拖曳「Sticky Note6」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **width**: 根據需求設定此參數
   - **height**: 根據需求設定此參數
   - **content**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 38：設定 Telegram Chatbot
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
   - **Text**: 設定輸入文本
3. 在憑證管理中設定相應的 API 金鑰


## 💡 建議用途與延伸應用

### 適用場景
- 通用自動化工作流程

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
