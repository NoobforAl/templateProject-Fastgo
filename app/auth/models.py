from sqlalchemy import Column, Integer, String
from sqlalchemy import Enum

from app.database import Base

import enum


class UserOwner(enum.Enum):
    admin = "admin"
    user = "user"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    owner = Column(Enum(UserOwner), nullable=False)
