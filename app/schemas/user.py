from typing import Optional, List
from pydantic import BaseModel, EmailStr, constr
from datetime import datetime

# Базовая схема пользователя
class UserBase(BaseModel):
    email: EmailStr
    username: constr(min_length=3, max_length=50)
    full_name: Optional[str] = None
    is_active: Optional[bool] = True

# Схема для создания пользователя
class UserCreate(UserBase):
    password: constr(min_length=8, max_length=100)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "username": "johndoe",
                "full_name": "John Doe",
                "password": "strongpassword123"
            }
        }

# Схема для обновления пользователя
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[constr(min_length=3, max_length=50)] = None
    full_name: Optional[str] = None
    password: Optional[constr(min_length=8, max_length=100)] = None

