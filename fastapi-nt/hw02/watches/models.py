from sqlalchemy import Column, String, Boolean, Integer
from database import Base


class Watch(Base):
    __tablename__ = 'watches'
    id = Column(String, primary_key=True)
    name = Column(String)
    country = Column(String)
