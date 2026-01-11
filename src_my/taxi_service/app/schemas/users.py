# taxi_service/app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional

# Схема для создания пользователя
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: Optional[str] = None

# Схема для ответа с данными пользователя (без пароля)
class UserRead(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool

    class Config:
        orm_mode = True

# Схема для логина
class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Схема для JWT токена
class Token(BaseModel):
    access_token: str
    token_type: str
