# Zeabur 部署指南

本文檔說明如何將 n8n Workflow API 服務部署到 Zeabur 平台。

## 🚀 快速部署

### 方法一：GitHub 連接部署（推薦）

1. **準備 GitHub 倉庫**
   ```bash
   git add .
   git commit -m "準備 Zeabur 部署"
   git push origin main
   ```

2. **連接到 Zeabur**
   - 登入 [Zeabur](https://zeabur.com/)
   - 創建新專案
   - 選擇 "Deploy from GitHub"
   - 選擇您的倉庫

3. **配置環境變數**
   在 Zeabur 專案設定中添加以下環境變數：
   ```
   SERVICE_MODE=api
   AI_PROVIDER=openai
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_MODEL=gpt-3.5-turbo
   MAX_TOKENS=2000
   TEMPERATURE=0.7
   ```

### 方法二：Docker 部署

1. **使用 Docker Compose**
   ```bash
   docker-compose --profile api up -d
   ```

2. **或使用單一服務**
   ```bash
   docker build -t n8n-workflow-api .
   docker run -p 5000:5000 -e SERVICE_MODE=api n8n-workflow-api
   ```

## 🔧 環境變數配置

### 必要環境變數

| 變數名 | 說明 | 預設值 | 範例 |
|--------|------|--------|------|
| `SERVICE_MODE` | 服務模式 | `all` | `api`, `gui`, `all` |
| `PORT` | API 服務端口 | `5000` | `5000` |

### AI 服務配置（可選）

#### OpenAI 配置
```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-your-openai-api-key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo
```

#### Gemini 配置
```env
AI_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-pro
```

#### Ollama 配置
```env
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2
```

#### 通用 AI 參數
```env
MAX_TOKENS=2000
TEMPERATURE=0.7
```

## 📋 部署模式

### 1. API 模式（推薦用於 Zeabur）
```env
SERVICE_MODE=api
```
- 僅啟動 REST API 服務
- 端口：5000
- 適合生產環境和 API 整合

### 2. GUI 模式
```env
SERVICE_MODE=gui
```
- 僅啟動 Gradio GUI 服務
- 端口：7861 (Scraper), 7862 (Search)
- 適合演示和開發

### 3. 完整模式
```env
SERVICE_MODE=all
```
- 啟動所有服務（API + GUI）
- 端口：5000, 7861, 7862
- 適合開發和測試環境

## 🛠️ Zeabur 特殊配置

### 端口配置
Zeabur 會自動設定 `PORT` 或 `WEB_PORT` 環境變數，系統已自動處理：

```bash
# 系統會自動處理這些情況：
PORT=${WEB_PORT}     # Zeabur 動態端口
PORT=5000            # 固定端口
```

### 健康檢查
API 提供健康檢查端點：
```
GET /api/v1/health
```

### 資料持久化
建議在 Zeabur 中配置 Volume 來持久化以下目錄：
- `/app/chroma_db` - 向量資料庫
- `/app/selected_workflows` - 儲存的工作流程
- `/app/workflows_data` - 爬取的資料

## 📊 監控與日誌

### API 端點監控
- 健康檢查：`GET /api/v1/health`
- 系統資訊：`GET /api/v1/info`
- API 文檔：`GET /docs/`

### 日誌查看
在 Zeabur 控制台中可以查看即時日誌：
- 應用啟動日誌
- API 請求日誌
- 錯誤日誌

## 🔍 故障排除

### 常見問題

1. **端口衝突**
   ```
   錯誤：Port 5000 is already in use
   解決：Zeabur 會自動分配端口，無需手動設定
   ```

2. **環境變數解析錯誤**
   ```
   錯誤：ValueError: invalid literal for int() with base 10: '${WEB_PORT}'
   解決：系統已自動處理 Zeabur 環境變數格式
   ```

3. **ChromaDB 集合已存在**
   ```
   錯誤：table collections already exists
   解決：系統會自動處理集合衝突，重新載入或重置資料庫
   ```

4. **記憶體不足**
   ```
   錯誤：Out of memory
   解決：在 Zeabur 中升級到更高記憶體的方案
   ```

### 除錯步驟

1. **檢查服務狀態**
   ```bash
   curl https://your-app.zeabur.app/api/v1/health
   ```

2. **查看系統資訊**
   ```bash
   curl https://your-app.zeabur.app/api/v1/info
   ```

3. **檢查 API 文檔**
   ```
   https://your-app.zeabur.app/docs/
   ```

## 🚀 部署最佳實踐

### 1. 環境分離
- **開發環境**：使用 `SERVICE_MODE=all`
- **測試環境**：使用 `SERVICE_MODE=api`
- **生產環境**：使用 `SERVICE_MODE=api`

### 2. 安全配置
- 設定強密碼的 API 金鑰
- 使用 HTTPS（Zeabur 自動提供）
- 定期更新依賴套件

### 3. 效能優化
- 使用 API 模式減少資源使用
- 配置適當的記憶體限制
- 啟用 Zeabur 的 CDN 加速

### 4. 監控設定
- 設定健康檢查
- 配置日誌收集
- 設定錯誤警告

## 📚 相關資源

- [Zeabur 官方文檔](https://zeabur.com/docs)
- [Docker 部署指南](./DOCKER_USAGE.md)
- [API 使用說明](./API_README.md)
- [n8n 官方文檔](https://docs.n8n.io/)

## 🎯 部署檢查清單

部署前請確認：

- [ ] GitHub 倉庫已更新
- [ ] 環境變數已設定
- [ ] AI API 金鑰已配置（如需要）
- [ ] 服務模式已選擇
- [ ] 健康檢查端點可訪問
- [ ] API 文檔可正常載入
- [ ] 核心功能測試通過

部署後驗證：

- [ ] 服務正常啟動
- [ ] API 端點回應正常
- [ ] 搜尋功能正常
- [ ] AI 教學生成正常（如已配置）
- [ ] 日誌無錯誤訊息

現在您的 n8n Workflow API 服務已準備好部署到 Zeabur！
