from flask import Flask, send_from_directory, request
from flask_cors import CORS
import os

# load_dotenv()

app = Flask(__name__, static_folder='dist', static_url_path='')
# CORSを有効化
if os.environ.get('FLASK_ENV') == 'production':
    CORS(app)
else:
    CORS(app, origins=['http://localhost:3000', 'http://localhost:5000'])

# セキュリティヘッダーを追加するミドルウェア
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    
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

@app.route('/test')
def empty_page():
    return send_from_directory('static', 'test.html', mimetype='text/html')

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
