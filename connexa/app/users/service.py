from sqlalchemy.ext.asyncio import AsyncSession
from app.common.security import password_hasher
from app.users import repository
from app.users.models import User
from app.users.schemas import UserCreate


class UserService:
    async def create_user(self, db:AsyncSession, data: UserCreate)-> User:

        if await repository.get_by_email(db, data.email):
            raise ValueError("Email already exists")

        if await repository.get_by_username(db, data.username):
            raise ValueError("Username already exists")

        hashed_password = password_hasher.hash(data.password)

        user = User(
            email=data.email,
            username=data.username,
            full_name=data.full_name,
            password_hash=hashed_password,
        )

        return await repository.create(db, user)
