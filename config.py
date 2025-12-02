import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Use Railway MySQL if available; fallback to local for development
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "SQLALCHEMY_DATABASE_URI",
        f"mysql+pymysql://root:{os.getenv('MYSQL_PASSWORD')}@localhost/sumsafari"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "default_secret_key")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
