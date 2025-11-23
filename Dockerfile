# マルチステージビルド: Node.jsでReactアプリをビルド
FROM node:18-alpine AS frontend-builder

WORKDIR /app

# package.jsonとpackage-lock.jsonをコピー
COPY package*.json ./

# 依存関係をインストール（開発依存関係も含む）
RUN npm ci

# ソースコードをコピー（必要なファイルのみ）
COPY index.html .
COPY vite.config.js .
COPY src ./src

# Reactアプリをビルド
RUN npm run build

# ビルド結果を確認
RUN ls -la dist/ || (echo "Build failed: dist directory not found" && exit 1)
RUN test -f dist/index.html || (echo "Build failed: index.html not found" && exit 1)

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

# ポートを公開（Koyebは8000ポートを使用）
EXPOSE 8000

# 環境変数を設定
ENV PORT=8000
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# アプリを起動（Koyebのデフォルトポート8000を使用）
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120", "app:app"]


