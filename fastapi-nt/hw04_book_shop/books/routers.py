from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from books import crud, schema
from db import get_db

router = APIRouter(prefix="/books", tags=["books"])


@router.get("/list", response_model=list[schema.BookRead])
def list_books(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_books(db=db, skip=skip, limit=limit)


@router.get("/detail/{book_id}", response_model=schema.BookRead)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.get_book(db=db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.post("/create", response_model=schema.BookRead, status_code=status.HTTP_201_CREATED)
def create_book(book_in: schema.BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db=db, book_in=book_in)


@router.patch("/update/{book_id}", response_model=schema.BookRead)
def update_book(book_id: int, book_in: schema.BookUpdate, db: Session = Depends(get_db)):
    book = crud.update_book(db=db, book_id=book_id, book_in=book_in)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return book


@router.delete("/delete/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = crud.delete_book(db=db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
