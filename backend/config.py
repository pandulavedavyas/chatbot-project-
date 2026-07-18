import os
from dotenv import load_dotenv

load_dotenv(override=False)

class Config:
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    if os.getenv('VERCEL'):
        DATABASE_PATH = os.path.join('/tmp', 'database.db')
    else:
        DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'database.db')
    PORT = int(os.getenv('PORT', '5000'))
    DEBUG = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    MAX_MESSAGE_LENGTH = 10000
