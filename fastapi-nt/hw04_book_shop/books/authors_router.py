from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from books import crud, schema
from db import get_db
from users.permissions import get_current_active_user

router = APIRouter(prefix="/authors", tags=["authors"])


@router.get("/list", response_model=list[schema.AuthorRead])
def list_authors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud.get_authors(db=db, skip=skip, limit=limit)


@router.get("/detail/{author_id}", response_model=schema.AuthorRead)
def get_author(author_id: int, db: Session = Depends(get_db)):
    author = crud.get_author(db=db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return author


@router.get("/{author_id}/books", response_model=list[schema.BookRead])
def author_books(
    author_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: str | None = None,
    has_image: bool | None = None,
    sort_by: Literal["created_at", "title", "id"] = "created_at",
    order: Literal["asc", "desc"] = "desc",
    db: Session = Depends(get_db),
):
    author = crud.get_author(db=db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return crud.get_books(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        author_id=author_id,
        has_image=has_image,
        sort_by=sort_by,
        order=order,
    )


@router.post("/create", response_model=schema.AuthorRead, status_code=status.HTTP_201_CREATED)
def create_author(
    author_in: schema.AuthorCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_active_user),
):
    return crud.create_author(db=db, fullname=author_in.fullname)


@router.patch("/update/{author_id}", response_model=schema.AuthorRead)
def update_author(
    author_id: int,
    author_in: schema.AuthorUpdate,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_active_user),
):
    if author_in.fullname is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="fullname is required")
    author = crud.update_author(db=db, author_id=author_id, fullname=author_in.fullname)
    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
    return author


@router.delete("/delete/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_author(
    author_id: int,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_active_user),
):
    author = crud.delete_author(db=db, author_id=author_id)
    if author is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Author not found")
