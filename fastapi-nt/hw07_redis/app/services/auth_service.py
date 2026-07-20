from app.schemas.user import UserCreate, UserUpdate, UserLogin
from app.models.user import User
from app.core.security import hash_password, verify_password
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repo import create_user, update_user
from app.repositories.user_repo import get_user_by_email, get_user_by_id, get_user_by_username
from fastapi.exceptions import HTTPException


async def register_user(user_data: UserCreate, db: AsyncSession) -> User:
   
    user = get_user_by_email(user_data.email, db)
    if user:
        raise HTTPException(status_code=400, detail="Bu email allaqachon ro'yxatdan o'tgan")
    
    user = get_user_by_username(user_data.username, db)
    if user:
        raise HTTPException(status_code=400, detail="Bu username allaqachon ro'yxatdan o'tgan")

    hashed = hash_password(user_data.password)
    
    new_user = {
        "email": user_data.email,
        "username": user_data.username,
        "full_name": user_data.full_name,
        "password_hash": hashed,
    }
    
    return await create_user(new_user, db)

async def login_user(db: AsyncSession, user_data: UserLogin) -> User:
    user_by_email = get_user_by_email(user_data.email_or_username, db)
    if not user_by_email:
        user_by_username = get_user_by_username(user_data.email_or_username, db)
        if not user_by_username:
            raise HTTPException(status_code=401, detail="Xato ma'lumot kiritildi")    
        user = user_by_username
    user = user_by_email
    verified = verify_password(user_data.password, user.password_hash)
    if not verified:
        raise HTTPException(status_code=401, detail="Xato ma'lumot kiritildi")
    
    return user








async def update_profile(user: User, update_data: UserUpdate, db: AsyncSession) -> User:
    data = update_data.model_dump(exclude_unset=True)
    return await update_user(user, data, db)