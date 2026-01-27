import os
from dotenv import load_dotenv

# Load .env file ONLY for local development
load_dotenv()

class Config:
    ENV = os.environ.get("FLASK_ENV", "development")

    if ENV == "production":
        # PythonAnywhere (online)
        SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    else:
        # Local (VS Code)
        SQLALCHEMY_DATABASE_URI = (
            f"mysql+pymysql://root:{os.getenv('MYSQL_PASSWORD')}@localhost:3306/sumsafari"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_key")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
