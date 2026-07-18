import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from config import Config
from database import init_db
from routes.chat import chat_bp
from routes.conversation import conversation_bp

STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

app = Flask(__name__, static_folder=STATIC_DIR, static_url_path='')
app.config.from_object(Config)

CORS(app)

app.register_blueprint(chat_bp)
app.register_blueprint(conversation_bp)

with app.app_context():
    init_db()


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path and os.path.exists(os.path.join(STATIC_DIR, path)):
        return send_from_directory(STATIC_DIR, path)
    return send_from_directory(STATIC_DIR, 'index.html')


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
