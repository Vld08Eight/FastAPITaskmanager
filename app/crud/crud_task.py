from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from typing import Annotated

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

class CRUDTask:
    async def get_task(db: Annotated[AsyncSession, Depends(get_db)], user_id: int):
        query = select(Task).where(Task.owner_id == user_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_all_user_tasks(db: Annotated[AsyncSession, Depends(get_db)], user_id: int):
        tasks = db.scalars(select(Task).where(Task.owner_id == user_id))
        if not tasks:
            raise HTTPException(
                status_code=status.HTTP_204_NO_CONTENT,
                detail='there are no tasks'
            )
        return tasks.all()

    async def create(db: Annotated[AsyncSession, Depends(get_db)], task: TaskCreate):
        db_obj = Task(
            title=task.title,
            description=task.description,
            owner_id=task.owner_id
        )
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
        
    async def update(
        self, 
        db: AsyncSession, 
        db_obj: Task, 
        obj_in: TaskUpdate
    ) -> Task:
        update_data = obj_in.dict(exclude_unset=True)
        
        # Обновляем только разрешенные поля
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def delete(self, db: AsyncSession, task_id: int) -> bool:
        query = select(Task).where(Task.id == task_id)
        result = await db.execute(query)
        task = result.scalar_one_or_none()
        if task:
            await db.delete(rask)
            await db.commit()
            return True
        return False

task_crud = CRUDTask()