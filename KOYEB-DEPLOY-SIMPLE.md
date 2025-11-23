# Koyebデプロイ手順（簡単版）

## ローカルでDockerをテストする必要はありません

Koyebは自動的にDockerfileを検出してビルドするため、ローカルでDockerをインストールする必要はありません。

## デプロイ手順

### 1. GitHubにプッシュ

```bash
git add Dockerfile .dockerignore
git commit -m "Add Dockerfile for Koyeb deployment"
git push origin main
```

### 2. Koyeb Dashboardでの設定

1. **アプリを選択** → **Settings** → **Build**

2. **Build Type** を **Dockerfile** に変更
   - Koyebが自動的にDockerfileを検出します

3. **環境変数の設定**（Settings → Environment Variables）:
   ```
   ADMIN_PASSWORD=your-secure-password-here
   SECRET_KEY=生成されたランダムな文字列（下記参照）
   FLASK_ENV=production
   PORT=8080
   ```

### 3. 自動デプロイ

GitHubにプッシュすると、Koyebが自動的に：
- Dockerfileを検出
- Dockerイメージをビルド
- コンテナを起動

## SECRET_KEYの生成

### 方法1: Pythonで生成（推奨）

```bash
python -c "import secrets; print(secrets.token_hex(24))"
```

### 方法2: オンラインツール

- ランダム文字列生成ツールを使用（32文字以上推奨）

## 重要な注意事項

### SECRET_KEYについて

現在の`.env`ファイルの`SECRET_KEY=hirotaka1219`は**非常に弱い**です。

**問題点：**
- 推測されやすい
- 短すぎる
- 個人情報を含んでいる

**推奨：**
- 最低32文字以上のランダムな文字列を使用
- 個人情報を含めない
- 本番環境では必ず強力なパスワードを使用

### セキュリティのベストプラクティス

1. **SECRET_KEY**: ランダムな文字列（32文字以上）
2. **ADMIN_PASSWORD**: 強力なパスワード
3. **環境変数で管理**: コードに直接書かない

## トラブルシューティング

### Dockerがインストールされていない場合

**問題ありません！** ローカルでDockerをテストする必要はありません。

Koyebが自動的に：
- Dockerfileを検出
- クラウド上でビルド
- デプロイ

### ローカルでテストしたい場合

Docker Desktopをインストール：
1. https://www.docker.com/products/docker-desktop からダウンロード
2. インストール後、PowerShellを再起動
3. `docker --version` で確認

ただし、**Koyebにデプロイするだけなら不要**です。

## 次のステップ

1. **SECRET_KEYを生成**:
   ```bash
   python -c "import secrets; print(secrets.token_hex(24))"
   ```

2. **Koyeb Dashboardで環境変数を設定**

3. **GitHubにプッシュ**:
   ```bash
   git add .
   git commit -m "Add Dockerfile"
   git push origin main
   ```

4. **Koyebが自動的にデプロイ**

以上です！ローカルでDockerをテストする必要はありません。

