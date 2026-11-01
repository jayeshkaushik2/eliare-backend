from dotenv import load_dotenv
import os

# loading .env variables
load_dotenv()

class Settings:
    DEBUG = os.getenv("DEBUG", "False")
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
    RDS_DATABASE_URL = os.getenv("RDS_DATABASE_URL")

    # AI keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")

settings = Settings()