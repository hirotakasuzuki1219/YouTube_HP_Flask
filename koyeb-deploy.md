# Koyebへのデプロイ手順（GitHub連携）

## 前提条件

1. Koyebアカウントを作成済み
2. GitHubリポジトリにコードをプッシュ済み
3. KoyebでGitHubリポジトリを連携済み

## Koyeb Dashboardでの設定

### 1. アプリの設定を開く

Koyeb Dashboardでアプリを選択し、「Settings」→「Build」に移動

### 2. ビルド設定

**Build Command:**
```bash
npm install && npm run build
```

**Run Command:**
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

**Buildpack:**
- 自動検出を使用（Node.jsとPythonの両方を検出）

または、手動で設定する場合：
1. **Primary Buildpack**: `heroku/nodejs` または `heroku/python`
2. Koyebは自動的に両方のビルドパックを検出して使用します

### 3. 環境変数の設定

「Settings」→「Environment Variables」で以下を設定：

#### 必須の環境変数

```
ADMIN_PASSWORD=your-secure-password-here
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
```

#### オプションの環境変数

```
PORT=8080
DATABASE_URL=sqlite:///instance/travels.db
```

### 4. ビルド順序の確認

Koyebは以下の順序でビルドします：
1. Node.jsの依存関係をインストール（`npm install`）
2. Reactアプリをビルド（`npm run build`）
3. Pythonの依存関係をインストール（`pip install -r requirements.txt`）
4. アプリを起動（`gunicorn`）

## デプロイの流れ

1. **GitHubにコードをプッシュ**
   ```bash
   git add .
   git commit -m "Update for Koyeb deployment"
   git push origin main
   ```

2. **Koyebが自動的にデプロイ**
   - GitHubにプッシュすると、Koyebが自動的に検出
   - ビルドが開始される
   - ビルド完了後、自動的にデプロイ

3. **デプロイの確認**
   - Koyeb Dashboardの「Deployments」タブで確認
   - 「Logs」タブでビルドログと実行ログを確認

## トラブルシューティング

### ビルドが失敗する場合

1. **ログを確認**
   - Koyeb Dashboardの「Logs」タブでエラーを確認

2. **よくある問題**
   - `dist/` ディレクトリが存在しない
     → `npm run build` が実行されているか確認
   - Node.jsのバージョンが合わない
     → `package.json` に `engines` を追加（後述）

3. **ビルドコマンドの確認**
   - Build Commandが正しく設定されているか確認
   - `npm install && npm run build` が実行されているか

### アプリが起動しない場合

1. **ポート番号の確認**
   - Koyebは自動的に `PORT` 環境変数を設定
   - `app.py` で `os.environ.get("PORT", 5000)` を使用していることを確認

2. **ログを確認**
   - 「Logs」タブでエラーメッセージを確認

### 環境変数が反映されない場合

1. **環境変数の再設定**
   - 「Settings」→「Environment Variables」で再設定
   - デプロイを再実行

## package.jsonの推奨設定

Node.jsのバージョンを指定する場合：

```json
{
  "engines": {
    "node": "18.x",
    "npm": "9.x"
  }
}
```

## 本番環境での注意事項

1. **パスワード**: 必ず強力なパスワードを設定
2. **SECRET_KEY**: ランダムな文字列を使用（下記参照）
3. **HTTPS**: Koyebは自動的にHTTPSを提供
4. **データベース**: SQLiteは一時的なデータに適しています。永続化が必要な場合はPostgreSQLなどを検討

## SECRET_KEYの生成方法

```bash
# Pythonで生成
python -c "import secrets; print(secrets.token_hex(24))"

# または
python -c "import os; print(os.urandom(24).hex())"
```

生成された文字列を `SECRET_KEY` 環境変数に設定してください。

## カスタムドメインの設定

1. Koyeb Dashboardでアプリを選択
2. 「Settings」→「Domains」に移動
3. カスタムドメインを追加

## 自動デプロイの設定

デフォルトで、GitHubのmainブランチにプッシュすると自動的にデプロイされます。

特定のブランチのみをデプロイしたい場合：
1. 「Settings」→「Build」に移動
2. 「Branch」でブランチを指定
