# Koyebへのデプロイ手順（GitHub連携）

## 概要

このプロジェクトは既にKoyebでGitHubを介してデプロイされています。
GitHubにプッシュするだけで自動的にデプロイされます。

## デプロイの流れ

1. **コードを変更**
2. **GitHubにプッシュ**
   ```bash
   git add .
   git commit -m "Update"
   git push origin main
   ```
3. **Koyebが自動的にデプロイ**
   - GitHubにプッシュすると、Koyebが自動的に検出
   - ビルドが開始される
   - ビルド完了後、自動的にデプロイ

## Koyeb Dashboardでの設定確認

### ビルド設定

「Settings」→「Build」で以下を確認：

**Build Command:**
```bash
npm install && npm run build
```

**Run Command:**
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

### 環境変数の設定

「Settings」→「Environment Variables」で以下を設定：

#### 必須の環境変数

- `ADMIN_PASSWORD`: 管理画面のパスワード（強力なパスワードを設定）
- `SECRET_KEY`: Flaskのセッション用の秘密鍵

#### オプションの環境変数

- `FLASK_ENV`: `production`（本番環境用）
- `PORT`: Koyebが自動設定（通常は8080）
- `DATABASE_URL`: データベースURL（SQLiteの場合は設定不要）

## SECRET_KEYの生成方法

```bash
# Pythonで生成
python -c "import secrets; print(secrets.token_hex(24))"
```

生成された文字列を `SECRET_KEY` 環境変数に設定してください。

## ビルドプロセス

Koyebは以下の順序でビルドします：

1. **Node.jsの依存関係をインストール**
   - `npm install` を実行
   - `package.json` から依存関係をインストール

2. **Reactアプリをビルド**
   - `npm run build` を実行
   - `dist/` ディレクトリにビルド結果が生成される

3. **Pythonの依存関係をインストール**
   - `pip install -r requirements.txt` を実行

4. **アプリを起動**
   - `gunicorn app:app` でFlaskアプリを起動
   - `dist/` ディレクトリからReactアプリを配信

## トラブルシューティング

### ビルドが失敗する場合

1. **ログを確認**
   - Koyeb Dashboardの「Logs」タブでエラーを確認

2. **よくある問題**
   - `dist/` ディレクトリが存在しない
     → `npm run build` が実行されているか確認
   - Node.jsのバージョンが合わない
     → `package.json` に `engines` を追加

3. **ビルドコマンドの確認**
   - Build Commandが正しく設定されているか確認

### アプリが起動しない場合

1. **ポート番号の確認**
   - Koyebは自動的に `PORT` 環境変数を設定
   - `app.py` で `os.environ.get("PORT", 5000)` を使用していることを確認

2. **ログを確認**
   - 「Logs」タブでエラーメッセージを確認

### 環境変数が反映されない場合

1. **環境変数の再設定**
   - 「Settings」→「Environment Variables」で再設定
   - デプロイを再実行（「Deployments」タブから「Redeploy」）

## 本番環境での注意事項

1. **パスワード**: 必ず強力なパスワードを設定
2. **SECRET_KEY**: ランダムな文字列を使用
3. **HTTPS**: Koyebは自動的にHTTPSを提供
4. **データベース**: SQLiteは一時的なデータに適しています。永続化が必要な場合はPostgreSQLなどを検討

## カスタムドメインの設定

1. Koyeb Dashboardでアプリを選択
2. 「Settings」→「Domains」に移動
3. カスタムドメインを追加

