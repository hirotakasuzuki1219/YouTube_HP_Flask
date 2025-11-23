# トラブルシューティング: Koyebデプロイ時の404エラー

## 問題: "The requested URL was not found on the server"

このエラーは、Reactアプリが正しくビルドされていないか、`dist/`フォルダが正しく配信されていない場合に発生します。

## 確認事項

### 1. ビルドログの確認

Koyeb Dashboardの「Logs」タブで以下を確認：

1. **Node.jsのビルドが成功しているか**
   ```
   npm install
   npm run build
   ```

2. **`dist/`フォルダが生成されているか**
   - ビルドログに `dist/` フォルダの生成が表示されているか確認

3. **エラーメッセージがないか**
   - ビルドエラーがないか確認

### 2. Koyeb Dashboardでの設定確認

**Settings → Build** で以下を確認：

- **Build Command**: `npm install && npm run build`
- **Run Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

### 3. ファイル構造の確認

ビルド後、以下のファイルが存在する必要があります：

```
dist/
  ├── index.html
  ├── assets/
  │   ├── index-[hash].js
  │   └── index-[hash].css
  └── ...
```

## 解決方法

### 方法1: ビルドコマンドの確認

Koyeb Dashboardの「Settings」→「Build」で、Build Commandが以下になっているか確認：

```bash
npm install && npm run build
```

### 方法2: 手動でビルドを確認

ローカルで以下を実行して、`dist/`フォルダが正しく生成されるか確認：

```bash
npm install
npm run build
ls -la dist/
```

`dist/index.html`が存在することを確認してください。

### 方法3: 環境変数の確認

Koyeb Dashboardの「Settings」→「Environment Variables」で以下を確認：

- `FLASK_ENV=production`
- `PORT=8080` (Koyebが自動設定)

### 方法4: ログの確認

Koyeb Dashboardの「Logs」タブで、アプリ起動時のログを確認：

- Flaskアプリが正しく起動しているか
- `dist/`フォルダが見つからないエラーがないか

## よくある問題と解決策

### 問題1: `dist/`フォルダが生成されない

**原因**: ビルドコマンドが実行されていない

**解決策**:
1. Koyeb Dashboardの「Settings」→「Build」でBuild Commandを確認
2. `npm install && npm run build` が設定されているか確認
3. デプロイを再実行

### 問題2: 静的ファイルが見つからない

**原因**: `dist/`フォルダのパスが正しくない

**解決策**:
1. `app.py`の`static_folder='dist'`が正しく設定されているか確認
2. ビルドログで`dist/`フォルダの生成を確認

### 問題3: APIエンドポイントが404になる

**原因**: ルーティングの順序が間違っている

**解決策**:
- `app.py`でAPIエンドポイントがReact SPAのルーティングより前に定義されているか確認
- 最新の`app.py`を使用しているか確認

## デバッグ方法

### 1. ビルドログを確認

Koyeb Dashboardの「Logs」タブで、ビルドプロセスの全ログを確認

### 2. 実行時ログを確認

アプリ起動時のログで、エラーメッセージを確認

### 3. 手動でデプロイを再実行

Koyeb Dashboardの「Deployments」タブで「Redeploy」をクリック

## 確認チェックリスト

- [ ] `package.json`に`build`スクリプトが定義されている
- [ ] `vite.config.js`で`outDir: 'dist'`が設定されている
- [ ] Koyeb DashboardでBuild Commandが正しく設定されている
- [ ] ビルドログで`dist/`フォルダの生成が確認できる
- [ ] `app.py`で`static_folder='dist'`が設定されている
- [ ] 環境変数`FLASK_ENV=production`が設定されている


