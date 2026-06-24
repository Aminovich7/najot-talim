
from sqlalchemy import create_engine
from sqlalchemy. orm import sessionmaker, declarative_base


engine = create_engine('postgresql://postgres:7799@localhost:5432/bookshop_db')
                       
Base = declarative_base()

SessionLocal = sessionmaker(
    autoflush=False, 
    autocommit=False, 
    bind=engine
    )

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session. close()