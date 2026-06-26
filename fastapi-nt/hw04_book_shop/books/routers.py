from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from books import crud, schema
from db import get_db
from users.permissions import get_current_active_user

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/list", response_model=list[schema.BookRead])
def list_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: str | None = None,
    owner_id: int | None = None,
    author_id: int | None = None,
    category_id: int | None = None,
    has_image: bool | None = None,
    sort_by: Literal["created_at", "title", "id"] = "created_at",
    order: Literal["asc", "desc"] = "desc",
    db: Session = Depends(get_db),
):
    return crud.get_books(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        owner_id=owner_id,
        author_id=author_id,
        category_id=category_id,
        has_image=has_image,
        sort_by=sort_by,
        order=order,
    )


@router.get("/mine", response_model=list[schema.BookRead])
def my_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: str | None = None,
    author_id: int | None = None,
    category_id: int | None = None,
    has_image: bool | None = None,
    sort_by: Literal["created_at", "title", "id"] = "created_at",
    order: Literal["asc", "desc"] = "desc",
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return crud.get_books(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        owner_id=current_user.id,
        author_id=author_id,
        category_id=category_id,
        has_image=has_image,
        sort_by=sort_by,
        order=order,
    )


@router.get("/detail/{book_id}", response_model=schema.BookRead)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db=db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.get("/{book_id}/comments", response_model=list[schema.CommentRead])
def book_comments(
    book_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    book = crud.get_book(db=db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return crud.get_comments(db=db, skip=skip, limit=limit, book_id=book_id)


@router.get("/{book_id}/saved-by-me", response_model=schema.SavedRead)
def saved_by_me(
    book_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    book = crud.get_book(db=db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    saved_item = crud.get_saved_item_by_user_and_book(
        db=db,
        user_id=current_user.id,
        book_id=book_id,
    )
    if saved_item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book is not saved by current user")
    return saved_item


@router.post("/create", response_model=schema.BookRead, status_code=status.HTTP_201_CREATED)
def create_book(
    book_in: schema.BookCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return crud.create_book(db=db, book_in=book_in, current_user=current_user)


@router.patch("/update/{book_id}", response_model=schema.BookRead)
def update_book(
    book_id: int,
    book_in: schema.BookUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    book = crud.update_book(db=db, book_id=book_id, book_in=book_in, current_user=current_user)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.delete("/delete/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    book = crud.delete_book(db=db, book_id=book_id, current_user=current_user)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
