# Crunchbase Startup Activity Monitor - 工作流程教學

## 📋 基本資訊

- **工作流程名稱**: Crunchbase Startup Activity Monitor
- **工作流程 ID**: wqZWgW8ymv4cC0Dk
- **節點數量**: 12
- **來源檔案**: 4732.json
- **生成時間**: 2025-06-18 12:09:42

## 📖 工作流程描述

Crunchbase Startup Activity Monitor；工作流程包含 12 個節點；節點類型：@n8n/n8n-nodes-langchain.lmChatOpenAi、@n8n/n8n-nodes-langchain.outputParserStructured、n8n-nodes-base.manualTrigger、n8n-nodes-base.httpRequest、n8n-nodes-base.set；包含觸發器；包含HTTP請求

## 🛠️ 詳細設定步驟

### 步驟 1：設定 OpenAI Chat Model
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
   - **Model**: 選擇「gpt-4o-mini」
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 2：設定 Structured Output Parser
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 3：設定 Trigger Manual Test

### 步驟 4：設定 Fetch Crunchbase Updates
1. 拖曳「HTTP Request」節點到工作流程畫布上
2. 點擊節點，然後設定：
   - **URL**: 輸入 API 端點 URL
   - **Headers**: 設定必要的請求標頭
3. 測試節點確保 API 請求正常運作

### 步驟 5：設定 Extract Company Details
1. 拖曳「Set」節點到工作流程畫布上
2. 設定資料處理：
   - **Assignments**: 設定要修改或新增的資料欄位
3. 測試節點確保資料處理正確

### 步驟 6：設定 Summarizer Agent
1. 拖曳 LangChain 相關節點到工作流程畫布上
2. 設定 AI 模型參數：
   - **Text**: 設定輸入文本
3. 在憑證管理中設定相應的 API 金鑰

### 步驟 7：設定 Send Email with Summary
1. 拖曳「Send Email with Summary」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **sendTo**: 根據需求設定此參數
   - **message**: 根據需求設定此參數
   - **options**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 8：設定 Sticky Note
1. 拖曳「Sticky Note」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **color**: 根據需求設定此參數
   - **width**: 根據需求設定此參數
   - **height**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 9：設定 Sticky Note1
1. 拖曳「Sticky Note1」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **color**: 根據需求設定此參數
   - **width**: 根據需求設定此參數
   - **height**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 10：設定 Sticky Note2
1. 拖曳「Sticky Note2」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **color**: 根據需求設定此參數
   - **width**: 根據需求設定此參數
   - **height**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 11：設定 Sticky Note9
1. 拖曳「Sticky Note9」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **color**: 根據需求設定此參數
   - **width**: 根據需求設定此參數
   - **height**: 根據需求設定此參數
3. 測試節點確保設定正確

### 步驟 12：設定 Sticky Note4
1. 拖曳「Sticky Note4」節點到工作流程畫布上
2. 點擊節點進行設定：
   - **color**: 根據需求設定此參數
   - **width**: 根據需求設定此參數
   - **height**: 根據需求設定此參數
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
