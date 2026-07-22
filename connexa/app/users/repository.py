from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User


async def get_by_email(db: AsyncSession, email: str ) -> User | None:
    result = await db.execute(
        select(User).where(User.email == email)
    )
    return result.scalar_one_or_none()




async def get_by_usernam(db: AsyncSession, username: str ) -> User | None:
    result = await db.execute(
        select(User).where(User.username == username)
    )
    return result.scalar_one_or_none()


async def create(db: AsyncSession, user: User) -> User | None:

    db.add(User)
    await db.commit()
    await db.refresh(User)

    response = {
        'msg': f'{User.username} created successfully'
    }
    return response