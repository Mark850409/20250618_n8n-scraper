# n8n Workflow 智能搜尋與教學生成系統 - AI 設定指南

## 🤖 AI 教學生成功能設定

本系統支援三種 AI 提供商，您可以根據需求選擇其中一種：

### 1. OpenAI (推薦)

**設定步驟：**
1. 前往 [OpenAI API](https://platform.openai.com/api-keys) 申請 API 金鑰
2. 在 `.env` 檔案中設定：
   ```
   AI_PROVIDER=openai
   OPENAI_API_KEY=your_actual_api_key_here
   OPENAI_MODEL=gpt-3.5-turbo
   ```

**優點：**
- 回應品質高
- 支援繁體中文
- 回應速度快

### 2. Google Gemini

**設定步驟：**
1. 前往 [Google AI Studio](https://makersuite.google.com/app/apikey) 申請 API 金鑰
2. 在 `.env` 檔案中設定：
   ```
   AI_PROVIDER=gemini
   GEMINI_API_KEY=your_actual_api_key_here
   GEMINI_MODEL=gemini-pro
   ```

**優點：**
- 免費額度較高
- 支援繁體中文
- Google 生態系整合

### 3. Ollama (本地部署)

**設定步驟：**
1. 安裝 [Ollama](https://ollama.ai/)
2. 下載模型：`ollama pull llama2`
3. 在 `.env` 檔案中設定：
   ```
   AI_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama2
   ```

**優點：**
- 完全本地運行
- 無需 API 金鑰
- 資料隱私性高

## 🔧 其他設定參數

```env
# 最大回應長度
MAX_TOKENS=2000

# 創意程度 (0.0-1.0)
TEMPERATURE=0.7
```

## 📝 使用範例

設定完成後，您可以在「n8n Workflow 教學生成」頁籤中詢問：

- "OpenWeather 節點該如何設定？"
- "如何設定 Telegram Bot 自動回覆？"
- "Discord Webhook 節點的參數設定"
- "Google Sheets 節點如何連接和操作？"

## ⚠️ 注意事項

1. **API 金鑰安全**：請勿將 API 金鑰提交到版本控制系統
2. **費用控制**：OpenAI 和 Gemini 為付費服務，請注意使用量
3. **網路連線**：OpenAI 和 Gemini 需要網路連線，Ollama 可離線使用
4. **回應品質**：不同模型的回應品質可能有差異，建議先測試

## 🚀 快速開始

1. 複製 `.env.example` 為 `.env`（如果有的話）
2. 根據選擇的 AI 提供商設定對應的 API 金鑰
3. 重新啟動應用程式
4. 在「n8n Workflow 教學生成」頁籤中開始使用

## 🔍 故障排除

**問題：顯示 "❌ OpenAI API 調用失敗"**
- 檢查 API 金鑰是否正確
- 確認網路連線正常
- 檢查 API 額度是否足夠

**問題：回應內容不完整**
- 增加 `MAX_TOKENS` 值
- 降低 `TEMPERATURE` 值以獲得更穩定的回應

**問題：Ollama 連接失敗**
- 確認 Ollama 服務已啟動
- 檢查模型是否已下載
- 確認端口設定正確
