from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db import get_db
from users import crud, schema
from users.security import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, get_current_user

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
def profile(current_user=Depends(get_current_user)):
    return current_user
