from flask import Flask, render_template
import os

# load_dotenv()

app = Flask(__name__)

# --- ルート ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route("/map")
def map_page():
    return render_template("map.html")

# if __name__ == '__main__':
#     app.run(debug=True)

if __name__ == "__main__":
    app.run()
