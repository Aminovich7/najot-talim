from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from books import crud, schema
from db import get_db
from users.permissions import get_current_active_user

router = APIRouter(prefix="/comments", tags=["comments"])


@router.get("/list", response_model=list[schema.CommentRead])
def list_comments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    book_id: int | None = None,
    db: Session = Depends(get_db),
):
    return crud.get_comments(db=db, skip=skip, limit=limit, book_id=book_id)


@router.get("/mine", response_model=list[schema.CommentRead])
def my_comments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return crud.get_comments(db=db, skip=skip, limit=limit, user_id=current_user.id)


@router.get("/detail/{comment_id}", response_model=schema.CommentRead)
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    comment = crud.get_comment(db=db, comment_id=comment_id)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment


@router.post("/create", response_model=schema.CommentRead, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment_in: schema.CommentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    book = crud.get_book(db=db, book_id=comment_in.book_id)
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
    return crud.create_comment(db=db, comment_in=comment_in, current_user=current_user)


@router.patch("/update/{comment_id}", response_model=schema.CommentRead)
def update_comment(
    comment_id: int,
    comment_in: schema.CommentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    comment = crud.get_comment(db=db, comment_id=comment_id)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    if comment_in.book_id is not None:
        book = crud.get_book(db=db, book_id=comment_in.book_id)
        if book is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    return crud.update_comment(db=db, comment_id=comment_id, comment_in=comment_in, current_user=current_user)


@router.delete("/delete/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    comment = crud.delete_comment(db=db, comment_id=comment_id, current_user=current_user)
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
