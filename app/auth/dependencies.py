from .config import PASSWORD_SECRET_HASH
from sqlalchemy.orm import Session
from typing import Generator

from passlib.context import CryptContext
from app.database import SessionLocal

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    plain_password += PASSWORD_SECRET_HASH
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    password += PASSWORD_SECRET_HASH
    return pwd_context.hash(password)
