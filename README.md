# YouTubeHP - React SPA

家族世界一周の記録を共有するReactベースのSPAアプリケーションです。

## セットアップ

### 1. 依存関係のインストール

#### バックエンド（Flask）
```bash
pip install -r requirements.txt
```

#### フロントエンド（React）
```bash
npm install
```

### 2. 開発環境での実行

#### バックエンドサーバーを起動
```bash
python app.py
```
Flaskサーバーが `http://localhost:5000` で起動します。

#### フロントエンド開発サーバーを起動（別のターミナル）
```bash
npm run dev
```
React開発サーバーが `http://localhost:3000` で起動します。

### 3. 本番環境用のビルド

#### Reactアプリをビルド
```bash
npm run build
```

ビルドされたファイルは `dist/` ディレクトリに生成されます。

#### 本番環境でFlaskサーバーを起動
```bash
python app.py
```

Flaskサーバーが `dist/` ディレクトリからReactアプリを配信します。

## 技術スタック

### フロントエンド
- React 18
- React Router DOM
- Framer Motion（アニメーション）
- Leaflet（地図表示）
- Vite（ビルドツール）

### バックエンド
- Flask
- SQLAlchemy
- Flask-CORS

## プロジェクト構造

```
.
├── app.py                 # Flaskバックエンド
├── src/                   # Reactソースコード
│   ├── components/        # Reactコンポーネント
│   ├── pages/            # ページコンポーネント
│   ├── App.jsx           # メインアプリコンポーネント
│   └── main.jsx          # エントリーポイント
├── dist/                  # ビルドされたReactアプリ（生成される）
├── static/                # 静的ファイル
├── templates/             # 旧テンプレート（使用されない）
├── package.json           # Node.js依存関係
├── vite.config.js        # Vite設定
└── requirements.txt       # Python依存関係
```

## 認証機能

管理ページ（`/admin`）は認証が必要です。

### パスワードの設定

環境変数 `ADMIN_PASSWORD` でパスワードを設定できます。設定しない場合、デフォルトは `admin123` です。

```bash
# Windows (PowerShell)
$env:ADMIN_PASSWORD="your-secure-password"

# Linux/Mac
export ADMIN_PASSWORD="your-secure-password"
```

**本番環境では必ず環境変数で強力なパスワードを設定してください。**

### ログイン方法

1. 管理ページ（`/admin`）にアクセス
2. ログインページが表示されるので、パスワードを入力
3. ログイン後、管理画面で旅行地点の追加・編集・削除が可能

## APIエンドポイント

### 公開エンドポイント
- `GET /api/travels` - すべての旅行地点を取得

### 認証が必要なエンドポイント
- `POST /api/travels` - 新しい旅行地点を追加
- `PUT /api/travels/<id>` - 旅行地点を更新
- `DELETE /api/travels/<id>` - 旅行地点を削除

### 認証エンドポイント
- `POST /api/login` - ログイン
- `POST /api/logout` - ログアウト
- `GET /api/check-auth` - 認証状態の確認

