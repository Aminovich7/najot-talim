from sqlalchemy.orm import Session

from books.models import Book, Comment, Saved
from books.schema import (
    BookCreate,
    BookUpdate,
    CommentCreate,
    CommentUpdate,
    SavedCreate,
    SavedUpdate,
)


def _dump_model(model, **kwargs):
    dump = getattr(model, "model_dump", None)
    if dump is not None:
        return dump(**kwargs)
    return model.dict(**kwargs)


def get_books(db: Session, skip: int = 0, limit: int = 100) -> list[Book]:
    return db.query(Book).offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int) -> Book | None:
    return db.query(Book).filter(Book.id == book_id).first()


def create_book(db: Session, book_in: BookCreate) -> Book:
    book = Book(**_dump_model(book_in))
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def update_book(db: Session, book_id: int, book_in: BookUpdate) -> Book | None:
    book = get_book(db, book_id)
    if book is None:
        return None

    for field, value in _dump_model(book_in, exclude_unset=True).items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int) -> Book | None:
    book = get_book(db, book_id)
    if book is None:
        return None

    db.delete(book)
    db.commit()
    return book


def get_comments(db: Session, skip: int = 0, limit: int = 100) -> list[Comment]:
    return db.query(Comment).offset(skip).limit(limit).all()


def get_comment(db: Session, comment_id: int) -> Comment | None:
    return db.query(Comment).filter(Comment.id == comment_id).first()


def create_comment(db: Session, comment_in: CommentCreate) -> Comment:
    comment = Comment(**_dump_model(comment_in))
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def update_comment(db: Session, comment_id: int, comment_in: CommentUpdate) -> Comment | None:
    comment = get_comment(db, comment_id)
    if comment is None:
        return None

    for field, value in _dump_model(comment_in, exclude_unset=True).items():
        setattr(comment, field, value)

    db.commit()
    db.refresh(comment)
    return comment


def delete_comment(db: Session, comment_id: int) -> Comment | None:
    comment = get_comment(db, comment_id)
    if comment is None:
        return None

    db.delete(comment)
    db.commit()
    return comment


def get_saved_items(db: Session, skip: int = 0, limit: int = 100) -> list[Saved]:
    return db.query(Saved).offset(skip).limit(limit).all()


def get_saved_item(db: Session, saved_id: int) -> Saved | None:
    return db.query(Saved).filter(Saved.id == saved_id).first()


def create_saved_item(db: Session, saved_in: SavedCreate) -> Saved:
    saved = Saved(**_dump_model(saved_in))
    db.add(saved)
    db.commit()
    db.refresh(saved)
    return saved


def update_saved_item(db: Session, saved_id: int, saved_in: SavedUpdate) -> Saved | None:
    saved = get_saved_item(db, saved_id)
    if saved is None:
        return None

    for field, value in _dump_model(saved_in, exclude_unset=True).items():
        setattr(saved, field, value)

    db.commit()
    db.refresh(saved)
    return saved


def delete_saved_item(db: Session, saved_id: int) -> Saved | None:
    saved = get_saved_item(db, saved_id)
    if saved is None:
        return None

    db.delete(saved)
    db.commit()
    return saved
