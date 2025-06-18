# 使用 Python 3.11 作為基礎映像
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 設定環境變數
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONPATH=/app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 複製 requirements.txt 並安裝 Python 依賴
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt || \
    (echo "某些依賴安裝失敗，將嘗試安裝基本依賴" && \
     pip install --no-cache-dir gradio requests chromadb flask flask-restx flask-cors)

# 複製應用程式代碼
COPY . .

# 創建必要的目錄
RUN mkdir -p chroma_db selected_workflows workflows_all_1 workflows_data

# 設定權限
RUN chmod +x *.py

# 暴露端口 (GUI 服務 + API 服務)
EXPOSE 5000 7861 7862

# 創建多服務啟動腳本
RUN echo '#!/bin/bash\n\
# 檢查並啟動服務\n\
echo "檢查 Python 依賴..."\n\
python -c "import gradio, requests, chromadb, flask" || {\n\
    echo "基本依賴缺失，請檢查安裝"\n\
    exit 1\n\
}\n\
\n\
# 根據環境變數決定啟動模式\n\
SERVICE_MODE=${SERVICE_MODE:-all}\n\
\n\
case "$SERVICE_MODE" in\n\
    "api")\n\
        echo "啟動 API 服務模式 (端口 5000)..."\n\
        python n8n_workflow_api.py\n\
        ;;\n\
    "gui")\n\
        echo "啟動 GUI 服務模式..."\n\
        echo "啟動 n8n workflow scraper (端口 7861)..."\n\
        python n8n_workflow_scraper.py &\n\
        SCRAPER_PID=$!\n\
        sleep 5\n\
        echo "啟動 n8n workflow search GUI (端口 7862)..."\n\
        python n8n_workflow_search_gui.py &\n\
        SEARCH_PID=$!\n\
        echo "GUI 服務啟動完成:"\n\
        echo "- Scraper: http://0.0.0.0:7861"\n\
        echo "- Search: http://0.0.0.0:7862"\n\
        wait\n\
        ;;\n\
    "all"|*)\n\
        echo "啟動所有服務 (API + GUI)..."\n\
        echo "啟動 API 服務 (端口 5000)..."\n\
        python n8n_workflow_api.py &\n\
        API_PID=$!\n\
        sleep 3\n\
        echo "啟動 n8n workflow scraper (端口 7861)..."\n\
        python n8n_workflow_scraper.py &\n\
        SCRAPER_PID=$!\n\
        sleep 5\n\
        echo "啟動 n8n workflow search GUI (端口 7862)..."\n\
        python n8n_workflow_search_gui.py &\n\
        SEARCH_PID=$!\n\
        echo "所有服務啟動完成:"\n\
        echo "- API: http://0.0.0.0:5000 (文檔: http://0.0.0.0:5000/docs/)"\n\
        echo "- Scraper: http://0.0.0.0:7861"\n\
        echo "- Search: http://0.0.0.0:7862"\n\
        wait\n\
        ;;\n\
esac' > /app/start.sh && chmod +x /app/start.sh

# 創建備用啟動腳本
COPY start_simple.py /app/
RUN chmod +x /app/start_simple.py

# 健康檢查腳本
RUN echo '#!/bin/bash\n\
SERVICE_MODE=${SERVICE_MODE:-all}\n\
case "$SERVICE_MODE" in\n\
    "api")\n\
        curl -f http://localhost:5000/api/v1/health || exit 1\n\
        ;;\n\
    "gui")\n\
        curl -f http://localhost:7861 || curl -f http://localhost:7862 || exit 1\n\
        ;;\n\
    "all"|*)\n\
        curl -f http://localhost:5000/api/v1/health && (curl -f http://localhost:7861 || curl -f http://localhost:7862) || exit 1\n\
        ;;\n\
esac' > /app/healthcheck.sh && chmod +x /app/healthcheck.sh

# 啟動命令
CMD ["/app/start.sh"]
