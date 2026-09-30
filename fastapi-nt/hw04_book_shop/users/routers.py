from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from books import crud as book_crud
from books import schema as book_schema
from db import get_db
from users import crud, schema
from users.permissions import get_current_active_user
from users.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=schema.UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: schema.UserRegister, db: Session = Depends(get_db)):
    if crud.get_user_by_username(db, user_in.username) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")
    if crud.get_user_by_email(db, user_in.email) is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
    return crud.create_user(db=db, user_in=user_in)


@router.post("/login", response_model=schema.Token)
def login(login_in: schema.UserLogin, db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, login_in.username, login_in.password)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return schema.Token(access_token=access_token)


@router.get("/profile", response_model=schema.UserRead)
def profile(current_user=Depends(get_current_active_user)):
    return current_user


@router.get("/me/comments", response_model=list[book_schema.CommentRead])
def my_comments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return book_crud.get_comments(db=db, skip=skip, limit=limit, user_id=current_user.id)


@router.get("/me/saved", response_model=list[book_schema.SavedRead])
def my_saved(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return book_crud.get_saved_items(db=db, skip=skip, limit=limit, user_id=current_user.id)


@router.put("/profile-update", response_model=schema.UserRead)
def update_profile(
    user_in: schema.UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    if user_in.username and user_in.username != current_user.username:
        existing_user = crud.get_user_by_username(db, user_in.username)
        if existing_user is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    if user_in.email and user_in.email != current_user.email:
        existing_user = crud.get_user_by_email(db, user_in.email)
        if existing_user is not None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    return crud.update_user(db, current_user, user_in)


@router.post("/change-password", response_model=schema.Message)
def change_password(
    payload: schema.ChangePassword,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    if not crud.authenticate_user(db, current_user.username, payload.current_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")

    crud.change_password(db, current_user, payload.new_password)
    return schema.Message(detail="Password updated successfully")


@router.post("/refresh", response_model=schema.Token)
def refresh_token(current_user=Depends(get_current_active_user)):
    access_token = create_access_token(data={"sub": str(current_user.id)})
    return schema.Token(access_token=access_token)


@router.delete("/profile-delete", response_model=schema.Message)
def delete_profile(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    crud.delete_user(db, current_user)
    return schema.Message(detail="Account deleted successfully")


@router.post("/logout", response_model=schema.Message)
def logout():
    return schema.Message(detail="Logout successful. Discard the access token on the client.")
