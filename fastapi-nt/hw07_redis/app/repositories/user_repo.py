import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User
from sqlalchemy import select


async def create_user(user_data: dict, db: AsyncSession) -> User:
    user = User(**user_data)   
    
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user

async def get_user_by_id( user_id: uuid.UUID, db:AsyncSession) -> User | None:
    query = select(User).where(User.id == user_id)

    result = await db.execute(query)
    return result.scalar_one_or_none()

    
async def get_user_by_email( user_email: str, db:AsyncSession) -> User | None:
    query = select(User).where(User.email == user_email)

    result = await db.execute(query)
    return result.scalar_one_or_none()


async def get_user_by_username(username: str, db:AsyncSession) -> User | None:
    query = select(User).where(User.username == username)

    result = await db.execute(query)
    return result.scalar_one_or_none()


async def update_user(user: User, update_data: dict, db: AsyncSession) -> User:
    for key, value in update_data.items():
        setattr(user, key, value)
        
    await db.commit()
    await db.refresh(user)
    
    return user

async def delete_user(user: User, db: AsyncSession) -> None:
    await db.delete(user)
    await db.commit()