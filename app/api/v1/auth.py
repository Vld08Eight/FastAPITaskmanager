from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.security import create_access_token, create_refresh_token
from app.crud.crud_user import user_crud
from app.schemas.user import UserCreate
from app.db.base import get_db
from app.core.security import get_password_hash, verify_password
from app.core.settings import settings
router = APIRouter(prefix='/auth', tags=['auth'])

@router.post("/register")
async def register(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    user = await user_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="User with this email already exists"
        )
    user = await user_crud.create(db, obj_in=user_in)
    return user


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    # Используем email для входа (username в форме - это email)
    user = await user_crud.get_by_email(db, email=form_data.username.lower())
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    access_token = create_access_token(
        subject=user.email, 
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return {"access_token": access_token, "token_type": "bearer"}