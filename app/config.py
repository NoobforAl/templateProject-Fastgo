from dotenv import load_dotenv
from pathlib import Path
import os


load_dotenv(dotenv_path=Path('../.env'))


SQLALCHEMY_DATABASE_URL: str = os.getenv(
    "DATABASE_URL") or "sqlite:///./sql_app.db"

REDIS_HOST: str = os.getenv("REDIS_URL") or "localhost"
REDIS_PORT: int = int(os.getenv("REDIS_PORT") or 6379)
REDIS_PASS: str = os.getenv("REDIS_PASS") or ""

MONGODB_URL: str = os.getenv("MONGODB_URL") or ""
