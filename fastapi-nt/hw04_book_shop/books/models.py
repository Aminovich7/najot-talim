from db import Base
from sqlalchemy import Column, String, Integer, Text, ForeignKey, func, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship

class Author(Base):
    __tablename__ = 'authors'
    
    id = Column(Integer, primary_key=True)
    fullname = Column(String(120))
    created_at = Column(DateTime, default=func.now)
    
    books = relationship('Book', back_populates='author')


class Category(Base):
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(120))
    created_at = Column(DateTime, default=func.now)
    
    books = relationship('Book', back_populates='category')


class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(120))
    image = Column(String(120), nullable=True)
    desc = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True, index=True)
    author_id = Column(Integer, ForeignKey('authors.id', ondelete='CASCADE'))
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'))
    created_at = Column(DateTime, default=func.now)

    
    author = relationship('Author', back_populates='books')
    category = relationship('Category', back_populates='books')
    owner = relationship('User', back_populates='books')
    comments = relationship('Comment', back_populates='book', cascade='all, delete-orphan')
    saved_items = relationship('Saved', back_populates='book', cascade='all, delete-orphan')
    
class Comment (Base) :
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True)
    sumary = Column(String(128))
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='comments')
    book = relationship('Book', back_populates='comments')

class Saved(Base) :
    __tablename__ = 'saveds'
    __table_args__ = (
        UniqueConstraint('user_id', 'book_id', name='uq_saveds_user_book'),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=True, index=True)
    book_id = Column(Integer, ForeignKey('books.id', ondelete='CASCADE'))
    user = relationship('User', back_populates='saved_items')
    book = relationship('Book', back_populates='saved_items')
