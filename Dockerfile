FROM python:3.9-slim

ENV LANG C.UTF-8
ENV TZ Asia/Tokyo

WORKDIR /app

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

COPY . /app

# FastAPIの起動
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
