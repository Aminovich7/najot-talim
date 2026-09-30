from sqlalchemy import Column, String, Integer
from database import Base


class Watch(Base):
    __tablename__ = 'watches'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    country = Column(String)
