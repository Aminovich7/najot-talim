from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from db import get_db
from models import User
from schemas import UserCreate, Token
from security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)

router = APIRouter()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    
    result = await db.execute(
        select(User).where(
            (User.username == user_in.username) | (User.email == user_in.email)
        )
    )
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Bu username yoki email allaqachon mavjud",
        )

    new_user = User(
        username=user_in.username,
        email=user_in.email,
        password=hash_password(user_in.password),
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return {"msg": 'User created', 
            'username':new_user.username}
    


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username yoki parol noto'g'ri",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Foydalanuvchi faol emas"
        )

    token_payload = {"sub": user.id}
    access_token = create_access_token(token_payload)
    refresh_token = create_refresh_token(token_payload)

    return {
        'msg': 'Signin',
        'status':status.HTTP_200_OK,
        'tokens' : Token(access_token=access_token, refresh_token=refresh_token)
    }

@router.post("/refresh", response_model=Token)
async def refresh_access_token(refresh_token: str):
    payload = decode_token(refresh_token)
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token yaroqsiz yoki muddati o'tgan",
        )

    user_id = payload.get("sub")
    token_payload = {"sub": user_id}
    new_access_token = create_access_token(token_payload)
    new_refresh_token = create_refresh_token(token_payload)

    return Token(access_token=new_access_token, refresh_token=new_refresh_token)


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Tizimga kirish tasdiqlanmadi",
    )

    payload = decode_token(token)
    if payload is None or payload.get("type") != "access":
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise credentials_exception

    return user


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user