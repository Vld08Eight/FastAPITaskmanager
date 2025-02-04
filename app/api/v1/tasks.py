from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate
from app.api.v1.deps import get_current_user 

router = APIRouter(prefix='/tasks', tags=['task'])



@router.get('/')
async def get_all_tasks(db: Annotated[AsyncSession, Depends(get_db)], get_user: Annotated[dict, Depends(get_current_user)]):
    result = await db.execute(select(Task).where(Task.is_active == True, Task.owner_id == get_user.id))
    tasks = result.scalars().all()
    return tasks

    
@router.post('/')
async def create_task(db: Annotated[AsyncSession, Depends(get_db)], create_task: TaskCreate, get_user: Annotated[dict, Depends(get_current_user)]):
    await db.execute(insert(Task).values(
        title=create_task.title,
        description=create_task.description,
        owner_id=get_user.id
        ))
    await db.commit()
    
    
@router.delete('/')
async def delete_task(db: Annotated[AsyncSession, Depends(get_db)], get_user: Annotated[dict, Depends(get_current_user)], task_id: int):
    task_delete = await db.scalar(select(Task).where(task_id == Task.id))
    task_delete.is_active = False
    await db.commit()
    return HTTPException (
        status_code=status.HTTP_200_OK
    )