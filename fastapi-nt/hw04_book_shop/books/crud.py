from fastapi import HTTPException, status
from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

from books.models import Author, Book, Category, Comment, Saved
from books.schema import (
    BookCreate,
    BookUpdate,
    CommentCreate,
    CommentUpdate,
    SavedCreate,
    SavedUpdate,
)
from users.models import User


def _dump_model(model, **kwargs):
    dump = getattr(model, "model_dump", None)
    if dump is not None:
        return dump(**kwargs)
    return model.dict(**kwargs)


def _require_owner(owner_id: int | None, current_user: User, resource_name: str) -> None:
    if owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"You do not own this {resource_name}",
        )


def get_books(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: str | None = None,
    owner_id: int | None = None,
    author_id: int | None = None,
    category_id: int | None = None,
    has_image: bool | None = None,
    sort_by: str = "created_at",
    order: str = "desc",
) -> list[Book]:
    query = db.query(Book)

    if search:
        term = f"%{search.strip()}%"
        query = query.outerjoin(Book.author).outerjoin(Book.category).filter(
            or_(
                Book.title.ilike(term),
                Book.desc.ilike(term),
                Author.fullname.ilike(term),
                Category.title.ilike(term),
            )
        )

    if owner_id is not None:
        query = query.filter(Book.owner_id == owner_id)

    if author_id is not None:
        query = query.filter(Book.author_id == author_id)

    if category_id is not None:
        query = query.filter(Book.category_id == category_id)

    if has_image is True:
        query = query.filter(Book.image.isnot(None))
    elif has_image is False:
        query = query.filter(Book.image.is_(None))

    sort_columns = {
        "created_at": Book.created_at,
        "title": Book.title,
        "id": Book.id,
    }
    sort_column = sort_columns.get(sort_by, Book.created_at)
    query = query.order_by(asc(sort_column) if order.lower() == "asc" else desc(sort_column))

    return query.offset(skip).limit(limit).all()


def get_book(db: Session, book_id: int) -> Book | None:
    return db.query(Book).filter(Book.id == book_id).first()


def create_book(db: Session, book_in: BookCreate, current_user: User) -> Book:
    book = Book(**_dump_model(book_in), owner_id=current_user.id)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def update_book(db: Session, book_id: int, book_in: BookUpdate, current_user: User) -> Book | None:
    book = get_book(db, book_id)
    if book is None:
        return None
    _require_owner(book.owner_id, current_user, "book")

    for field, value in _dump_model(book_in, exclude_unset=True).items():
        setattr(book, field, value)

    db.commit()
    db.refresh(book)
    return book


def delete_book(db: Session, book_id: int, current_user: User) -> Book | None:
    book = get_book(db, book_id)
    if book is None:
        return None
    _require_owner(book.owner_id, current_user, "book")

    db.delete(book)
    db.commit()
    return book


def get_comments(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    book_id: int | None = None,
    user_id: int | None = None,
) -> list[Comment]:
    query = db.query(Comment)
    if book_id is not None:
        query = query.filter(Comment.book_id == book_id)
    if user_id is not None:
        query = query.filter(Comment.user_id == user_id)
    return query.offset(skip).limit(limit).all()


def get_comment(db: Session, comment_id: int) -> Comment | None:
    return db.query(Comment).filter(Comment.id == comment_id).first()


def create_comment(db: Session, comment_in: CommentCreate, current_user: User) -> Comment:
    comment = Comment(**_dump_model(comment_in), user_id=current_user.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def update_comment(db: Session, comment_id: int, comment_in: CommentUpdate, current_user: User) -> Comment | None:
    comment = get_comment(db, comment_id)
    if comment is None:
        return None
    _require_owner(comment.user_id, current_user, "comment")

    for field, value in _dump_model(comment_in, exclude_unset=True).items():
        setattr(comment, field, value)

    db.commit()
    db.refresh(comment)
    return comment


def delete_comment(db: Session, comment_id: int, current_user: User) -> Comment | None:
    comment = get_comment(db, comment_id)
    if comment is None:
        return None
    _require_owner(comment.user_id, current_user, "comment")

    db.delete(comment)
    db.commit()
    return comment


def get_saved_items(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    user_id: int | None = None,
) -> list[Saved]:
    query = db.query(Saved)
    if user_id is not None:
        query = query.filter(Saved.user_id == user_id)
    return query.offset(skip).limit(limit).all()


def get_saved_item(db: Session, saved_id: int) -> Saved | None:
    return db.query(Saved).filter(Saved.id == saved_id).first()


def get_saved_item_by_user_and_book(db: Session, user_id: int, book_id: int) -> Saved | None:
    return (
        db.query(Saved)
        .filter(Saved.user_id == user_id, Saved.book_id == book_id)
        .first()
    )


def create_saved_item(db: Session, saved_in: SavedCreate, current_user: User) -> Saved:
    saved = Saved(**_dump_model(saved_in), user_id=current_user.id)
    db.add(saved)
    db.commit()
    db.refresh(saved)
    return saved


def update_saved_item(db: Session, saved_id: int, saved_in: SavedUpdate, current_user: User) -> Saved | None:
    saved = get_saved_item(db, saved_id)
    if saved is None:
        return None
    _require_owner(saved.user_id, current_user, "saved item")

    for field, value in _dump_model(saved_in, exclude_unset=True).items():
        setattr(saved, field, value)

    db.commit()
    db.refresh(saved)
    return saved


def delete_saved_item(db: Session, saved_id: int, current_user: User) -> Saved | None:
    saved = get_saved_item(db, saved_id)
    if saved is None:
        return None
    _require_owner(saved.user_id, current_user, "saved item")

    db.delete(saved)
    db.commit()
    return saved
