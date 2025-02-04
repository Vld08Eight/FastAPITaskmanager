from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.api.v1.deps import get_current_user 
from app.crud.crud_task import task_crud

router = APIRouter(prefix='/tasks', tags=['task'])



@router.get('/')
async def get_all_tasks(db: Annotated[AsyncSession, Depends(get_db)], get_user: Annotated[dict, Depends(get_current_user)]):
    return task_crud.get_all_user_tasks(get_user.id)
   
@router.get('/{task_id}')
async def get_task_by_id(db: Annotated[AsyncSession, Depends(get_db)], get_user: Annotated[dict, Depends(get_current_user)], task_id: int):
    return task_crud.get_task(db, get_user.id, task_id)


@router.post('/')
async def create_task(db: Annotated[AsyncSession, Depends(get_db)], create_task: TaskCreate, get_user: Annotated[dict, Depends(get_current_user)]):
    create_task.owner_id = get_user.id
    task_crud.create(db, create_task)
    return HTTPException (
        status_code=status.HTTP_200_OK
    )

@router.put('/{task_id}')
async def update_task(db: Annotated[AsyncSession, Depends(get_db)], get_user: Annotated[dict, Depends(get_current_user)], task: TaskUpdate, task_id: int):
    return task_crud.update(db, task_crud.get_task(db, get_user.id, task_id), )

@router.delete('/{task_id}')
async def delete_task(db: Annotated[AsyncSession, Depends(get_db)], get_user: Annotated[dict, Depends(get_current_user)], task_id: int):
    if task_crud.delete(db, task_id):
        return HTTPException (
        status_code=status.HTTP_200_OK,
        detail='task {task_id} delete'
    )