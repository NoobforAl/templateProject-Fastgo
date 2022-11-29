from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine

from app.config import REDIS_HOST, REDIS_PORT, REDIS_PASS
from app.config import SQLALCHEMY_DATABASE_URL
from app.config import MONGODB_URL
from app.log.logger import log

from pymongo import MongoClient, errors
from redis import Redis, ConnectionError

'''
* Sql Setup
'''
engine: Engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal: sessionmaker = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


'''
* Redis
'''
try:
    redis = Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS, db=1)
    redis.ping()
except ConnectionError:
    log.error("can't connect to redis database! "
              "database is off! ")

'''
* MongoDB
'''
try:
    mongo = MongoClient(MONGODB_URL)
    mongo.server_info()
except errors.ServerSelectionTimeoutError:
    log.error("can't connect to MongoClient database!")
    raise
