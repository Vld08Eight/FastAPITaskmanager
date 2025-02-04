from typing import Optional
from pydantic import BaseModel, constr
from datetime import datetime

# Базовая схема задачи
class TaskBase(BaseModel):
    title: constr(min_length=1, max_length=200)
    description: Optional[str] = None
    owner_id: int

# Схема для создания задачи
class TaskCreate(TaskBase):
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Complete project documentation",
                "description": "Write detailed documentation for the API",
                "owner_id": 0
            }
        }

# Схема для обновления задачи
class TaskUpdate(BaseModel):
    title: Optional[constr(min_length=1, max_length=200)] = None
    description: Optional[str] = None

# Схема для ответа API
class Task(TaskBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Complete project documentation",
                "description": "Write detailed documentation for the API",
                "user_id": 1,
             
            }
        }
