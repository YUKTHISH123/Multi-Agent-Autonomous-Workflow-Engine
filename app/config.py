import os
from pathlib import Path
from dotenv import load_dotenv

# Resolve project root path and load .env explicitly
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "agent_engine")

if not GROQ_API_KEY:
    raise ValueError(
        f"GROQ_API_KEY is missing or empty. Please check your .env file at {env_path}"
    )