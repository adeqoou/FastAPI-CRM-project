from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import *
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from .models import *
from sqlalchemy import select
from typing import List

router = APIRouter()


# Регистрация клиентов
@router.post('/clients/', response_model=ClientCreateSchema)
async def create_clients(clients: ClientCreateSchema, db: AsyncSession = Depends(get_db)):
    try:
        client = Clients(first_name=clients.first_name,
                         last_name=clients.last_name,
                         email=clients.email)
        db.add(client)
        await db.commit()
        await db.refresh(client)
        return client
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# Получение клиента по id
@router.get('/clients/{client_id}', response_model=ClientSchema)
async def get_clients(client_id: int, db: AsyncSession = Depends(get_db)):
    client = await db.execute(select(Clients).where(Clients.id == client_id))
    result = client.scalars().first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Данные не найдены')
    return result


# Получение списка клиентов
@router.get('/clients-list/', response_model=List[ClientSchema])
async def list_of_clients(db: AsyncSession = Depends(get_db)):
    clients = await db.execute(select(Clients))
    result = clients.scalars().all()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Данные отсутствуют')
    return result