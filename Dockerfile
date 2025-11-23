# マルチステージビルド: Node.jsでReactアプリをビルド
FROM node:18-alpine AS frontend-builder

WORKDIR /app

# package.jsonとpackage-lock.jsonをコピー
COPY package*.json ./

# 依存関係をインストール
RUN npm ci --only=production=false

# ソースコードをコピー
COPY . .

# Reactアプリをビルド
RUN npm run build

# Python環境でFlaskアプリを実行
FROM python:3.11-slim

WORKDIR /app

# システムの依存関係をインストール
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Pythonの依存関係をインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ビルドされたReactアプリをコピー
COPY --from=frontend-builder /app/dist ./dist

# Flaskアプリとその他のファイルをコピー
COPY app.py .
COPY static ./static

# instanceディレクトリを作成（データベース用）
RUN mkdir -p instance

# ポートを公開
EXPOSE 8080

# 環境変数を設定
ENV PORT=8080
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# アプリを起動
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "--timeout", "120", "app:app"]

