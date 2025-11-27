from flask import Flask, render_template, send_from_directory, send_file, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os

# load_dotenv()

app = Flask(__name__, static_folder='dist', static_url_path='')
# CORSを有効化
if os.environ.get('FLASK_ENV') == 'production':
    CORS(app)
else:
    CORS(app, origins=['http://localhost:3000', 'http://localhost:5000'])
# データベースのパスを設定（instance/ディレクトリに保存）
instance_dir = os.path.join(os.getcwd(), 'instance')
os.makedirs(instance_dir, exist_ok=True, mode=0o755)
db_path = os.path.join(instance_dir, 'travels.db')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', f'sqlite:///{db_path}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# データベースモデル
class Travel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    lat = db.Column(db.Float, nullable=False)
    lon = db.Column(db.Float, nullable=False)
    note = db.Column(db.Text)
    youtube = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'lat': self.lat,
            'lon': self.lon,
            'note': self.note,
            'youtube': self.youtube
        }

# データベース初期化
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        # テーブルが既に存在する場合は無視
        print(f"Database initialization: {e}")

# セキュリティヘッダーを追加するミドルウェア
@app.after_request
def set_security_headers(response):
    # セキュリティヘッダーを設定
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    
    # CSP (Content Security Policy) - Reactアプリ用に調整
    csp = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://unpkg.com; "
        "style-src 'self' 'unsafe-inline' https://unpkg.com; "
        "img-src 'self' data: https:; "
        "font-src 'self' data:; "
        "connect-src 'self' http://localhost:5000; "
        "frame-src 'self' https://www.youtube.com; "
        "frame-ancestors 'none';"
    )
    response.headers['Content-Security-Policy'] = csp
    
    # HTTPSの強制（本番環境の場合）
    if os.environ.get('FLASK_ENV') == 'production':
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    return response

# --- ルート ---
# APIエンドポイントは削除（ハードコードデータを使用するため）

# 静的ファイルの配信（robots.txt, sitemap.xmlなど）
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml', mimetype='application/xml')

@app.route('/robots.txt')
def robots_txt():
    return send_from_directory('static', 'robots.txt', mimetype='text/plain')

# React SPAのためのルート - すべてのルートをindex.htmlにリダイレクト（最後に定義）
@app.route('/', defaults={'path': ''}, methods=['GET', 'HEAD'])
@app.route('/<path:path>', methods=['GET', 'HEAD'])
def serve_react_app(path):
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"=== serve_react_app called with path: '{path}' ===")
    logger.info(f"Request method: {request.method}")
    logger.info(f"Request path: {request.path}")
    
    # APIエンドポイントは除外（既に定義されている）
    if path.startswith('api/'):
        logger.warning(f"Path '{path}' is API endpoint, returning 404")
        return '', 404
    
    # sitemap.xmlとrobots.txtも除外（既に定義されている）
    if path in ['sitemap.xml', 'robots.txt']:
        logger.warning(f"Path '{path}' is static file, returning 404")
        return '', 404
    
    static_folder = app.static_folder
    logger.info(f"Static folder: {static_folder}")
    
    # 静的ファイル（assets/配下のJS、CSSなど）を配信
    if static_folder and path and path.startswith('assets/'):
        file_path = os.path.join(static_folder, path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            logger.info(f"Serving static file: {path}")
            return send_from_directory(static_folder, path)
    
    # それ以外はReactアプリのindex.htmlを返す（SPAのため）
    # /admin, /login, /map などのルートはすべてindex.htmlにリダイレクト
    if static_folder:
        index_path = os.path.join(static_folder, 'index.html')
        logger.info(f"Index path: {index_path}, exists: {os.path.exists(index_path)}")
        if os.path.exists(index_path):
            try:
                logger.info(f"Serving index.html for path: '{path}'")
                return send_from_directory(static_folder, 'index.html')
            except Exception as e:
                logger.error(f"Error serving index.html: {e}")
                # エラーが発生した場合のフォールバック
                with open(index_path, 'r', encoding='utf-8') as f:
                    return f.read()
        else:
            logger.error(f"index.html not found at {index_path}")
            # ディレクトリの内容を確認
            if os.path.exists(static_folder):
                logger.error(f"Contents of static_folder: {os.listdir(static_folder)}")
    
    # フォールバック
    logger.error(f"React app not found. Static folder: {static_folder}")
    return 'React app not found. Please build the app.', 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
