from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession


from app.db.dependencies import get_db
from app.users.schemas import UserCreate, UserResponse
from app.users.service import UserService


router = APIRouter(prefix="/auth", tags=["Authentication"])

service = UserService()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):

    try: 
        return await service.create_user(db, data)
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
