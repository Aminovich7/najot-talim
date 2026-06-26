from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from books import crud, schema
from db import get_db
from users.permissions import get_current_active_user

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/list", response_model=list[schema.CategoryRead])
def list_categories(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return crud.get_categories(db=db, skip=skip, limit=limit)


@router.get("/detail/{category_id}", response_model=schema.CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category(db=db, category_id=category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.get("/{category_id}/books", response_model=list[schema.BookRead])
def category_books(
    category_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: str | None = None,
    has_image: bool | None = None,
    sort_by: Literal["created_at", "title", "id"] = "created_at",
    order: Literal["asc", "desc"] = "desc",
    db: Session = Depends(get_db),
):
    category = crud.get_category(db=db, category_id=category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return crud.get_books(
        db=db,
        skip=skip,
        limit=limit,
        search=search,
        category_id=category_id,
        has_image=has_image,
        sort_by=sort_by,
        order=order,
    )


@router.post("/create", response_model=schema.CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(
    category_in: schema.CategoryCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_active_user),
):
    return crud.create_category(db=db, title=category_in.title)


@router.patch("/update/{category_id}", response_model=schema.CategoryRead)
def update_category(
    category_id: int,
    category_in: schema.CategoryUpdate,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_active_user),
):
    if category_in.title is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="title is required")
    category = crud.update_category(db=db, category_id=category_id, title=category_in.title)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    return category


@router.delete("/delete/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_active_user),
):
    category = crud.delete_category(db=db, category_id=category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
