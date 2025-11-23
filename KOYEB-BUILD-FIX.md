# Koyebビルド問題の解決方法

## 問題: `dist/`フォルダが生成されない

Koyeb Dashboardで以下を確認・設定してください。

## 解決方法

### 1. Koyeb Dashboardでの設定確認

**Settings → Build** で以下を確認：

#### Build Command
```bash
npm install && npm run build
```

#### Run Command
```bash
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

### 2. ビルドパックの設定

Koyebは自動的にNode.jsとPythonのビルドパックを検出しますが、明示的に設定する場合：

1. **Settings → Build** に移動
2. **Buildpacks** セクションで以下を確認：
   - `heroku/nodejs` または `heroku/python` が検出されているか
   - 両方のビルドパックが使用されているか

### 3. ビルドログの確認

Koyeb Dashboardの「Logs」タブで以下を確認：

1. **ビルドフェーズ**で以下が実行されているか：
   ```
   npm install
   npm run build
   ```

2. **`dist/`フォルダの生成確認**：
   - ビルドログに `dist/` フォルダの生成が表示されているか
   - エラーメッセージがないか

### 4. 代替方法: ビルドスクリプトを使用

もし上記で解決しない場合、`build.sh`を使用する方法：

**Build Command:**
```bash
chmod +x build.sh && ./build.sh
```

ただし、Koyebでは通常、`npm install && npm run build`で十分です。

### 5. 環境変数の確認

**Settings → Environment Variables** で以下を確認：

- `NODE_ENV=production` (オプション)
- `FLASK_ENV=production`

## デバッグ手順

### ステップ1: ビルドログを確認

1. Koyeb Dashboardの「Logs」タブを開く
2. ビルドフェーズのログを確認
3. 以下が表示されているか確認：
   ```
   npm install
   npm run build
   dist/ フォルダの生成
   ```

### ステップ2: ビルドコマンドを確認

「Settings」→「Build」で、Build Commandが以下になっているか確認：
```bash
npm install && npm run build
```

### ステップ3: 再デプロイ

1. 「Deployments」タブで「Redeploy」をクリック
2. または、GitHubに空のコミットをプッシュ：
   ```bash
   git commit --allow-empty -m "Trigger rebuild"
   git push origin main
   ```

## よくある問題

### 問題1: ビルドコマンドが実行されない

**原因**: Build Commandが設定されていない

**解決策**: 「Settings」→「Build」でBuild Commandを設定

### 問題2: Node.jsのビルドパックが検出されない

**原因**: `package.json`が正しく認識されていない

**解決策**: 
- `package.json`がリポジトリのルートにあることを確認
- ビルドパックを明示的に設定

### 問題3: ビルドは成功するが`dist/`フォルダが見つからない

**原因**: ビルドとランタイムの分離

**解決策**: 
- ビルドログで`dist/`フォルダの生成を確認
- ランタイムログで`dist/`フォルダの存在を確認

## 確認チェックリスト

- [ ] Build Commandが `npm install && npm run build` になっている
- [ ] Run Commandが `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120` になっている
- [ ] ビルドログで `npm install` が実行されている
- [ ] ビルドログで `npm run build` が実行されている
- [ ] ビルドログで `dist/` フォルダの生成が確認できる
- [ ] ビルドエラーがない
- [ ] `package.json` がリポジトリのルートにある
- [ ] `vite.config.js` が存在し、`outDir: 'dist'` が設定されている


