from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.auth.utils import hash_password, authenticate_user, create_access_token, decode_access_token
from .schemas import *
from .models import User
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy import select, update
from datetime import timedelta
from src.auth.config import auth_config
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# Регистрация пользователей
@router.post('/register/')
async def registration(user: UserCreate, db: AsyncSession = Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = User(username=user.username,
                   first_name=user.first_name,
                   last_name=user.last_name,
                   email=user.email,
                   role=user.role,
                   password=hashed_password,
                   is_superuser=user.is_superuser)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return {'username': db_user.username}


# Авторизация пользователей по токену
@router.post('/login/', response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    user = await authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Неверный логин или пароль',
            headers={'WWW-Authenticate': 'Bearer'}
        )
    access_token_expires = timedelta(minutes=auth_config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.username},
        expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'Bearer'}


# Получение текущего пользователя
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exceptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Не удалось получить данные о текущем пользователе',
        headers={'WWW-Authenticate': 'Bearer'}
    )
    try:
        token_data = decode_access_token(token, credentials_exceptions)
        logger.info('Decoded: %s', token_data)
    except Exception as e:
        logger.error('Failed: %s', e)
        raise credentials_exceptions

    result = await db.execute(select(User).where(User.username == token_data.username))
    user = result.scalars().first()

    if user is None:
        raise credentials_exceptions
    return user


# Профиль пользователя
@router.get('/profile/', response_model=UserSchema)
async def users_profile(current_user: UserSchema = Depends(get_current_user)):
    return current_user


@router.put('/profile-change/')
async def change_profile(user_id: int, update_schema: UserSchema, db: AsyncSession = Depends(get_db)):
    query = (
        update(User).where(User.id == user_id)
        .values(**update_schema).execution_options(syncronize_session='fetch')
    )
    await db.execute(query)

    updated_profile = await db.execute(select(User).where(User.id == user_id))
    user = updated_profile.scalars().one_or_none()

    await db.commit()

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return user
