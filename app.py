from flask import Flask, render_template, send_from_directory, send_file
import os

# load_dotenv()

app = Flask(__name__)

# --- ルート ---
@app.route('/')
def home():
    return render_template('index.html')

# @app.route("/map")
# def map_page():
#     return render_template("map.html")

# Google Search Console用の検証ファイル
@app.route('/google486f7934b3f48a0a.html')
def google_verification():
    file_path = os.path.join(app.static_folder, 'google486f7934b3f48a0a.html')
    return send_file(file_path, mimetype='text/html')

# Sitemap.xml
@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('static', 'sitemap.xml', mimetype='application/xml')

# robots.txt
@app.route('/robots.txt')
def robots_txt():
    return send_from_directory('static', 'robots.txt', mimetype='text/plain')

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
