# Docker 部署使用說明

本專案現在支援多種 Docker 部署模式，您可以根據需求選擇不同的服務組合。

## 🚀 快速開始

### 預設模式 (推薦)
啟動所有服務 (API + GUI)：
```bash
docker-compose up -d
```

這將啟動：
- **API 服務**: http://localhost:5000 (文檔: http://localhost:5000/docs/)
- **Scraper GUI**: http://localhost:7861
- **Search GUI**: http://localhost:7862

## 📋 可用的部署模式

### 1. 完整服務模式 (預設)
```bash
# 啟動所有服務
docker-compose up -d

# 或明確指定 profile
docker-compose --profile all up -d
```

**包含服務**:
- ✅ REST API 服務 (端口 5000)
- ✅ 工作流程爬取 GUI (端口 7861)
- ✅ 智能搜尋 GUI (端口 7862)

### 2. 僅 API 服務模式
```bash
docker-compose --profile api up -d
```

**包含服務**:
- ✅ REST API 服務 (端口 5000)
- ❌ GUI 服務

**適用場景**: 
- 僅需要 API 介面
- 整合到其他系統
- 生產環境部署

### 3. 僅 GUI 服務模式
```bash
docker-compose --profile gui up -d
```

**包含服務**:
- ❌ API 服務
- ✅ 工作流程爬取 GUI (端口 7861)
- ✅ 智能搜尋 GUI (端口 7862)

**適用場景**:
- 僅需要圖形介面
- 傳統使用方式

### 4. 包含 Ollama 的完整服務
```bash
docker-compose --profile all-with-ollama up -d
```

**包含服務**:
- ✅ 所有上述服務
- ✅ 本地 Ollama AI 服務 (端口 11434)

## 🔧 環境變數配置

創建 `.env` 檔案來配置服務：

```env
# AI 服務配置
AI_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-3.5-turbo

# Gemini 配置
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-pro

# Ollama 配置
OLLAMA_BASE_URL=http://ollama:11434
OLLAMA_MODEL=llama2

# API 參數
MAX_TOKENS=2000
TEMPERATURE=0.7
```

## 📊 服務狀態檢查

### 檢查所有服務狀態
```bash
docker-compose ps
```

### 查看服務日誌
```bash
# 查看所有服務日誌
docker-compose logs -f

# 查看特定服務日誌
docker-compose logs -f n8n-scraper-all
docker-compose logs -f n8n-api
docker-compose logs -f n8n-gui
```

### 健康檢查
```bash
# API 健康檢查
curl http://localhost:5000/api/v1/health

# GUI 服務檢查
curl http://localhost:7861
curl http://localhost:7862
```

## 🛠️ 常用操作

### 重新建構映像
```bash
docker-compose build --no-cache
```

### 更新服務
```bash
# 停止服務
docker-compose down

# 拉取最新代碼並重新建構
git pull
docker-compose build

# 重新啟動
docker-compose up -d
```

### 清理資源
```bash
# 停止並移除容器
docker-compose down

# 移除映像
docker-compose down --rmi all

# 清理所有相關資源 (包含 volumes)
docker-compose down -v --rmi all
```

## 📁 資料持久化

以下目錄會自動掛載到主機，確保資料持久化：

- `./chroma_db/` - 向量資料庫
- `./selected_workflows/` - 儲存的工作流程
- `./workflows_data/` - 爬取的工作流程資料

## 🌐 Zeabur 部署

針對 Zeabur 平台的特殊配置：

```bash
# 使用環境變數指定端口
PORT=5000 docker-compose --profile api up -d
```

或在 Zeabur 中設定環境變數：
- `SERVICE_MODE=api`
- `PORT=5000`

## 🔍 故障排除

### 常見問題

1. **端口衝突**
   ```bash
   # 檢查端口使用情況
   netstat -tulpn | grep :5000
   netstat -tulpn | grep :7861
   netstat -tulpn | grep :7862
   ```

2. **記憶體不足**
   ```bash
   # 增加 Docker 記憶體限制
   docker-compose up -d --memory=4g
   ```

3. **權限問題**
   ```bash
   # 修復目錄權限
   sudo chown -R $USER:$USER ./chroma_db ./selected_workflows ./workflows_data
   ```

### 重置環境
```bash
# 完全重置 (會刪除所有資料)
docker-compose down -v
sudo rm -rf chroma_db selected_workflows workflows_data
docker-compose up -d
```

## 📚 進階配置

### 自定義 Dockerfile
如需自定義配置，可以修改 `Dockerfile` 中的環境變數或依賴。

### 負載平衡
對於生產環境，建議使用 nginx 或其他負載平衡器：

```yaml
# docker-compose.prod.yml 範例
version: '3.8'
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - n8n-api
```

## 🎯 使用建議

- **開發環境**: 使用完整服務模式 (`docker-compose up -d`)
- **生產環境**: 使用 API 模式 (`docker-compose --profile api up -d`)
- **演示環境**: 使用 GUI 模式 (`docker-compose --profile gui up -d`)
- **AI 開發**: 使用包含 Ollama 的模式 (`docker-compose --profile all-with-ollama up -d`)

現在您可以根據需求靈活選擇部署模式！
