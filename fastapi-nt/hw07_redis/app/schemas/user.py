from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
import re
from sqlalchemy.dialects.postgresql import UUID
import uuid



USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9_]+$")
FULL_NAME_PATTERN = re.compile(r"^[a-zA-Zа-яА-ЯёЁ\s\-]+$")


def validate_username_format(value: str) -> str:
    if not USERNAME_PATTERN.match(value):
        raise ValueError("Username faqat lotin harflari, raqamlar va '_' belgisidan iborat bo'lishi kerak")
    return value


def validate_full_name_format(value: str) -> str:
    if not FULL_NAME_PATTERN.match(value):
        raise ValueError("Full name faqat harflar, bo'shliq va defisdan iborat bo'lishi kerak")
    return value

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=32)
    full_name: str = Field(min_length=2, max_length=100)
    password: str = Field(min_length=8, max_length=72)
    confirm_password: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        return validate_username_format(value)  

    @field_validator("full_name")
    @classmethod
    def validate_full_name(cls, value: str) -> str:
        return validate_full_name_format(value)
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not re.search(r"[A-Z]", value):
            raise ValueError("Parolda kamida bitta katta harf bo'lishi kerak")
        if not re.search(r"[a-z]", value):
            raise ValueError("Parolda kamida bitta kichik harf bo'lishi kerak")
        if not re.search(r"\d", value):
            raise ValueError("Parolda kamida bitta raqam bo'lishi kerak")
        return value
    
    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Parollar mos emas! ")
        return self
    

class UserLogin(BaseModel):
    email_or_username : str
    password : str


class UserUpdate(BaseModel):
    username: str | None = Field(default=None, min_length=3, max_length=32)
    full_name: str | None = Field(default=None, min_length=2, max_length=100)

    @field_validator("username")
    @classmethod
    def check_username(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return validate_username_format(value)

    @field_validator("full_name")
    @classmethod
    def check_full_name(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return validate_full_name_format(value)
    

class UserOut(BaseModel):
    id: uuid.UUID
    email: EmailStr
    username: str
    full_name: str
    is_verified: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }