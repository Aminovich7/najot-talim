from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = 'postgres://postgres:7799localhost:5432/fastapi02_db'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autoflush = False, 
    autocommit = False,
    bind = engine

)

Base = declarative_base()
