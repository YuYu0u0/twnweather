# 使用 Python Slim 基礎映像
FROM python:3.11.9-slim-bookworm

# 設定環境變數
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 設定工作目錄
WORKDIR /twnweather

# 複製所有檔案進容器
COPY . .

# 安裝系統套件（例如 psycopg2 需要）
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 使用 gunicorn 作為入口點（Cloud Run 預期長時間執行的 HTTP server）
CMD ["gunicorn", "web.wsgi:application", "--bind", "0.0.0.0:$PORT", "--workers=2"]
