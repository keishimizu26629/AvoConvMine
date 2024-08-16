FROM python:3.12.4-slim

ENV LANG C.UTF-8
ENV TZ Asia/Tokyo

WORKDIR /app
# WORKDIR /

# 必要なパッケージのインストール
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# pip のアップグレード
RUN pip install --no-cache-dir --upgrade pip

# pip installs
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

ENV PYTHONPATH=/app

# FastAPIの起動
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
