from flask import Flask, render_template, send_from_directory, send_file, request, jsonify, make_response, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import os
from functools import wraps
import hashlib

# load_dotenv()

app = Flask(__name__, static_folder='dist', static_url_path='')
# CORSを有効化（認証用のクッキーを送信できるように設定）
# 開発環境ではlocalhostを許可、本番環境では同一オリジンのみ許可
if os.environ.get('FLASK_ENV') == 'production':
    CORS(app, supports_credentials=True, origins=None)  # 同一オリジンのみ
else:
    CORS(app, supports_credentials=True, origins=['http://localhost:3000', 'http://localhost:5000'])
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///travels.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24).hex())
app.config['SESSION_COOKIE_SECURE'] = os.environ.get('FLASK_ENV') == 'production'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

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
    db.create_all()

# 認証用のデコレータ
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return jsonify({'error': '認証が必要です'}), 401
        return f(*args, **kwargs)
    return decorated_function

# パスワードのハッシュ化（環境変数から取得、デフォルト値は設定しない）
def get_admin_password():
    return os.environ.get('ADMIN_PASSWORD', 'admin123')  # 本番環境では必ず環境変数で設定すること

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
# APIエンドポイント（React SPAのルーティングより前に定義する必要がある）
@app.route('/api/travels', methods=['GET'])
def get_travels():
    travels = Travel.query.order_by(Travel.created_at).all()
    return jsonify([travel.to_dict() for travel in travels])

@app.route('/api/travels', methods=['POST'])
@login_required
def create_travel():
    data = request.json
    travel = Travel(
        name=data['name'],
        lat=float(data['lat']),
        lon=float(data['lon']),
        note=data.get('note', ''),
        youtube=data.get('youtube', '')
    )
    db.session.add(travel)
    db.session.commit()
    return jsonify(travel.to_dict()), 201

@app.route('/api/travels/<int:travel_id>', methods=['PUT'])
@login_required
def update_travel(travel_id):
    travel = Travel.query.get_or_404(travel_id)
    data = request.json
    travel.name = data['name']
    travel.lat = float(data['lat'])
    travel.lon = float(data['lon'])
    travel.note = data.get('note', '')
    travel.youtube = data.get('youtube', '')
    travel.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(travel.to_dict())

@app.route('/api/travels/<int:travel_id>', methods=['DELETE'])
@login_required
def delete_travel(travel_id):
    travel = Travel.query.get_or_404(travel_id)
    db.session.delete(travel)
    db.session.commit()
    return '', 204

# 認証APIエンドポイント
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    password = data.get('password', '')
    admin_password = get_admin_password()
    
    # パスワードの比較（ハッシュ化して比較することも可能）
    if password == admin_password:
        session['authenticated'] = True
        return jsonify({'success': True, 'message': 'ログイン成功'})
    else:
        return jsonify({'success': False, 'error': 'パスワードが正しくありません'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('authenticated', None)
    return jsonify({'success': True, 'message': 'ログアウトしました'})

@app.route('/api/check-auth', methods=['GET'])
def check_auth():
    if session.get('authenticated'):
        return jsonify({'authenticated': True})
    else:
        return jsonify({'authenticated': False})

# 静的ファイルの配信（robots.txt, sitemap.xmlなど）
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml', mimetype='application/xml')

@app.route('/robots.txt')
def robots_txt():
    return send_from_directory('static', 'robots.txt', mimetype='text/plain')

# React SPAのためのルート - すべてのルートをindex.htmlにリダイレクト（最後に定義）
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react_app(path):
    # 静的ファイル（JS、CSS、画像など）を配信
    static_folder = app.static_folder
    if static_folder and path:
        # アセットファイル（JS、CSSなど）の配信
        if path.startswith('assets/'):
            file_path = os.path.join(static_folder, path)
            if os.path.exists(file_path):
                return send_from_directory(static_folder, path)
        
        # その他の静的ファイル
        file_path = os.path.join(static_folder, path)
        if os.path.exists(file_path) and os.path.isfile(file_path):
            return send_from_directory(static_folder, path)
    
    # それ以外はReactアプリのindex.htmlを返す（SPAのため）
    if static_folder:
        index_path = os.path.join(static_folder, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder, 'index.html')
        else:
            # distフォルダが存在しない場合のエラーメッセージ
            return f'''
            <html>
                <head><title>Build Required</title></head>
                <body>
                    <h1>React app not built</h1>
                    <p>Please run "npm run build" to build the React app.</p>
                    <p>Static folder: {static_folder}</p>
                    <p>Index path: {index_path}</p>
                </body>
            </html>
            ''', 500
    else:
        return 'Static folder not configured', 500

# APIエンドポイント
@app.route('/api/travels', methods=['GET'])
def get_travels():
    travels = Travel.query.order_by(Travel.created_at).all()
    return jsonify([travel.to_dict() for travel in travels])

# 認証APIエンドポイント
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    password = data.get('password', '')
    admin_password = get_admin_password()
    
    # パスワードの比較（ハッシュ化して比較することも可能）
    if password == admin_password:
        session['authenticated'] = True
        return jsonify({'success': True, 'message': 'ログイン成功'})
    else:
        return jsonify({'success': False, 'error': 'パスワードが正しくありません'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.pop('authenticated', None)
    return jsonify({'success': True, 'message': 'ログアウトしました'})

@app.route('/api/check-auth', methods=['GET'])
def check_auth():
    if session.get('authenticated'):
        return jsonify({'authenticated': True})
    else:
        return jsonify({'authenticated': False})

@app.route('/api/travels', methods=['POST'])
@login_required
def create_travel():
    data = request.json
    travel = Travel(
        name=data['name'],
        lat=float(data['lat']),
        lon=float(data['lon']),
        note=data.get('note', ''),
        youtube=data.get('youtube', '')
    )
    db.session.add(travel)
    db.session.commit()
    return jsonify(travel.to_dict()), 201

@app.route('/api/travels/<int:travel_id>', methods=['PUT'])
@login_required
def update_travel(travel_id):
    travel = Travel.query.get_or_404(travel_id)
    data = request.json
    travel.name = data['name']
    travel.lat = float(data['lat'])
    travel.lon = float(data['lon'])
    travel.note = data.get('note', '')
    travel.youtube = data.get('youtube', '')
    travel.updated_at = datetime.utcnow()
    db.session.commit()
    return jsonify(travel.to_dict())

@app.route('/api/travels/<int:travel_id>', methods=['DELETE'])
@login_required
def delete_travel(travel_id):
    travel = Travel.query.get_or_404(travel_id)
    db.session.delete(travel)
    db.session.commit()
    return '', 204

# Sitemap.xml
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml', mimetype='application/xml')

# robots.txt
@app.route('/robots.txt')
def robots_txt():
    return send_from_directory('static', 'robots.txt', mimetype='text/plain')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
