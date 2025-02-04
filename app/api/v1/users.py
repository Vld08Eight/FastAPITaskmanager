from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated
from sqlalchemy import insert
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.crud.crud_user import user_crud
from app.core import security
from app.api.v1.deps import get_current_user 


router = APIRouter(prefix='/users', tags=['user'])



@router.get('/')
async def get_all_users(db: Annotated[AsyncSession, Depends(get_db)],get_user: Annotated[dict, Depends(get_current_user)]):
    if get_user.is_superuser:
        result = await db.execute(select(User).where(User.is_active == True))
        users = result.scalars().all()
        return users
    else:
        raise HTTPException (
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED
        )

@router.get('/')
async def get_user_by_id(db: Annotated[AsyncSession, Depends(get_db)],get_user: Annotated[dict, Depends(get_current_user)], user_id: int):
    if get_user.is_superuser == True or get_user.id == user_id:
        return user_crud.get(db, user_id)    
    else: 
        raise HTTPException (
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED
        )

@router.get('/')
async def get_user_by_email(db: Annotated[AsyncSession, Depends(get_db)],get_user: Annotated[dict, Depends(get_current_user)], email: str):
    if get_user.is_superuser == True or get_user.email == email:
        return user_crud.get_by_email(db, email)
    else:
        raise HTTPException (
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED
        )

@router.get('/')
async def get_user_by_username(db: Annotated[AsyncSession, Depends(get_db)],get_user: Annotated[dict, Depends(get_current_user)], username: str):
    if get_user.is_superuser == True or get_user.username == username:
        return user_crud.get_by_username(db, username)
    else:
        raise HTTPException (
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED
        )

@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user(db: Annotated[AsyncSession, Depends(get_db)], create_user: UserCreate):
    user = await user_crud.create(db, create_user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User could not be created"
        )
    return user
    

@router.put('/')
async def update_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    user: UserUpdate
):
    if current_user.username != user.username:
        raise HTTPException(status_code=403, detail="You can only update your own profile")

    updated_user = await user_crud.update(db, current_user, user)
    return updated_user


@router.delete('/')
async def delete_user(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)]
):
    return user_crud.delete(db, current_user.id)
