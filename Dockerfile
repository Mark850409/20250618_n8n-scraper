# 使用 Python 3.11 作為基礎映像
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 設定環境變數
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

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
     pip install --no-cache-dir gradio requests chromadb)

# 複製應用程式代碼
COPY . .

# 創建必要的目錄
RUN mkdir -p chroma_db selected_workflows workflows_all_1

# 設定權限
RUN chmod +x *.py

# 暴露端口
EXPOSE 7860 7862

# 創建啟動腳本
RUN echo '#!/bin/bash\n\
# 檢查並啟動服務\n\
echo "檢查 Python 依賴..."\n\
python -c "import gradio, requests, chromadb" || {\n\
    echo "基本依賴缺失，請檢查安裝"\n\
    exit 1\n\
}\n\
\n\
echo "啟動 n8n workflow scraper (端口 7860)..."\n\
python n8n_workflow_scraper.py &\n\
SCRAPER_PID=$!\n\
\n\
# 等待一下確保第一個服務啟動\n\
sleep 5\n\
\n\
echo "啟動 n8n workflow search GUI (端口 7862)..."\n\
python n8n_workflow_search_gui.py &\n\
SEARCH_PID=$!\n\
\n\
echo "服務啟動完成:"\n\
echo "- Scraper: http://0.0.0.0:7860"\n\
echo "- Search: http://0.0.0.0:7862"\n\
\n\
# 等待所有背景程序\n\
wait' > /app/start.sh && chmod +x /app/start.sh

# 創建備用啟動腳本
COPY start_simple.py /app/
RUN chmod +x /app/start_simple.py

# 啟動命令
CMD ["/app/start.sh"]
