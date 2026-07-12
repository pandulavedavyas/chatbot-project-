from flask import Flask
from flask_cors import CORS
from config import Config
from database import init_db
from routes.chat import chat_bp
from routes.conversation import conversation_bp

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)

app.register_blueprint(chat_bp)
app.register_blueprint(conversation_bp)

with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(debug=Config.DEBUG, port=Config.PORT)
