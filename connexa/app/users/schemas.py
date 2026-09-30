from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):

    email: EmailStr
    username: str = Field(min_length=3, max_length=32)
    full_name: str = Field(min_length=2, max_length=100)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=100)


class UserResponse(UserBase):
    id: UUID
    is_verified: bool
    

    model_config=ConfigDict(from_attributes=True)


    
