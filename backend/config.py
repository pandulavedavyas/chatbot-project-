import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), '..', 'database.db')
