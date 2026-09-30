from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from books import crud, schema
from db import get_db
from users.permissions import get_current_active_user

router = APIRouter(prefix="/saved", tags=["saved"])


@router.get("/list", response_model=list[schema.SavedRead])
def list_saved(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return crud.get_saved_items(db=db, skip=skip, limit=limit, user_id=current_user.id)


@router.post("/create", response_model=schema.SavedRead, status_code=status.HTTP_201_CREATED)
def create_saved(
    saved_in: schema.SavedCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    book = crud.get_book(db=db, book_id=saved_in.book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    existing = crud.get_saved_item_by_user_and_book(
        db=db,
        user_id=current_user.id,
        book_id=saved_in.book_id,
    )
    if existing is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book already saved")

    return crud.create_saved_item(db=db, saved_in=saved_in, current_user=current_user)


@router.delete("/delete/{saved_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_saved(
    saved_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    saved = crud.delete_saved_item(db=db, saved_id=saved_id, current_user=current_user)
    if saved is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Saved item not found")
