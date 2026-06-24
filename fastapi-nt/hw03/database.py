from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session


DATABASE_URL = 'postgresql://postgres:7799@localhost:5432/fastapi02_db'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autoflush = False, 
    autocommit = False,
    bind = engine

)

Base = declarative_base()


def get_db():
    db= SessionLocal()
    try:
        yield db

    finally:
        db.close()