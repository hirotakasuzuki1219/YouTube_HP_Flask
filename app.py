from flask import Flask, render_template, send_from_directory, send_file, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from functools import wraps

# load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///travels.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(24).hex())
app.config['SESSION_COOKIE_SECURE'] = True
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

# セキュリティヘッダーを追加するミドルウェア
@app.after_request
def set_security_headers(response):
    # セキュリティヘッダーを設定
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
    
    # CSP (Content Security Policy) - 必要に応じて調整
    csp = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline' https://unpkg.com; "
        "style-src 'self' 'unsafe-inline' https://unpkg.com; "
        "img-src 'self' data: https:; "
        "font-src 'self' data:; "
        "connect-src 'self'; "
        "frame-src 'self' https://www.youtube.com; "
        "frame-ancestors 'none';"
    )
    response.headers['Content-Security-Policy'] = csp
    
    # HTTPSの強制（本番環境の場合）
    if os.environ.get('FLASK_ENV') == 'production':
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    
    return response

# --- ルート ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route("/map")
def map_page():
    return render_template("map.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")

# APIエンドポイント
@app.route('/api/travels', methods=['GET'])
def get_travels():
    travels = Travel.query.order_by(Travel.created_at).all()
    return jsonify([travel.to_dict() for travel in travels])

@app.route('/api/travels', methods=['POST'])
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
