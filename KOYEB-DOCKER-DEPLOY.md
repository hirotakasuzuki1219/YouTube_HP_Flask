# Koyeb Dockerデプロイ手順

## Dockerを使う利点

1. **確実なビルド**: Node.jsとPythonの両方を1つのDockerfileで管理
2. **環境の一貫性**: ローカルと本番環境で同じ環境を再現
3. **ビルドパックの問題を回避**: 複数のビルドパックの順序や設定の問題を回避
4. **無料版でも利用可能**: Koyebの無料版（Hobbyプラン）でもDockerは使用可能

## デプロイ手順

### 1. Koyeb Dashboardでの設定

1. **アプリを選択** → **Settings** → **Build**

2. **Build Type** を **Dockerfile** に変更

3. **Dockerfile** が自動的に検出されます

4. **環境変数の設定**（Settings → Environment Variables）:
   ```
   ADMIN_PASSWORD=your-secure-password-here
   SECRET_KEY=your-secret-key-here
   FLASK_ENV=production
   PORT=8080
   ```

### 2. GitHubにプッシュ

```bash
git add Dockerfile .dockerignore
git commit -m "Add Dockerfile for Koyeb deployment"
git push origin main
```

### 3. 自動デプロイ

Koyebが自動的に：
1. Dockerfileを検出
2. Dockerイメージをビルド
3. コンテナを起動

## Dockerfileの説明

### マルチステージビルド

1. **frontend-builderステージ**:
   - Node.js 18を使用
   - Reactアプリをビルド
   - `dist/`フォルダを生成

2. **最終ステージ**:
   - Python 3.11を使用
   - Flaskアプリを実行
   - ビルドされた`dist/`フォルダをコピー

### ビルドプロセス

1. Node.jsの依存関係をインストール
2. Reactアプリをビルド（`npm run build`）
3. Pythonの依存関係をインストール
4. ビルドされたReactアプリをFlaskアプリにコピー
5. GunicornでFlaskアプリを起動

## ローカルでのテスト

### Dockerイメージをビルド

```bash
docker build -t youtube-hp .
```

### コンテナを実行

```bash
docker run -p 8080:8080 \
  -e ADMIN_PASSWORD=your-password \
  -e SECRET_KEY=your-secret-key \
  -e FLASK_ENV=production \
  youtube-hp
```

### ブラウザで確認

http://localhost:8080 にアクセス

## トラブルシューティング

### ビルドが失敗する場合

1. **ログを確認**: Koyeb Dashboardの「Logs」タブでエラーを確認
2. **ローカルでテスト**: `docker build`でローカルでビルドをテスト
3. **Dockerfileの確認**: パスやコマンドが正しいか確認

### アプリが起動しない場合

1. **ポート番号の確認**: `PORT`環境変数が8080に設定されているか
2. **ログを確認**: コンテナのログでエラーメッセージを確認
3. **環境変数の確認**: 必要な環境変数が設定されているか

## ビルドパック vs Docker

### ビルドパックを使う場合
- ✅ 設定が簡単
- ✅ Koyebが自動検出
- ❌ 複数のビルドパック（Node.js + Python）の順序が複雑
- ❌ ビルドプロセスの制御が難しい

### Dockerを使う場合
- ✅ ビルドプロセスを完全に制御
- ✅ ローカルと本番環境の一貫性
- ✅ 複数の言語/ツールを扱いやすい
- ✅ デバッグが容易
- ❌ Dockerfileの作成が必要

## 推奨

**このプロジェクトの場合、Dockerを使うことを推奨します。**

理由：
1. Node.jsとPythonの両方が必要
2. ReactアプリのビルドとFlaskアプリの実行を1つのプロセスで管理できる
3. ビルドパックで発生していた問題を回避できる
4. 無料版でも利用可能

