from fastapi import APIRouter, Depends, HTTPException, status, Query
from .schemas import *
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from .models import *
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List
from fastapi_cache.decorator import cache
from .tasks import send_mail
from decimal import Decimal

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
@cache(expire=60)
async def get_clients(client_id: int, db: AsyncSession = Depends(get_db)):
    client = await db.execute(select(Clients).where(Clients.id == client_id))
    result = client.scalars().first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Данные не найдены')
    return result


# Получение списка клиентов
@router.get('/clients-list/', response_model=List[ClientSchema])
@cache(expire=120)
async def list_of_clients(db: AsyncSession = Depends(get_db)):
    clients = await db.execute(select(Clients))
    result = clients.scalars().all()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Данные отсутствуют')
    return result


@router.post('/injuries/')
async def injuries_send(injury: InjuryBaseSchema, db: AsyncSession = Depends(get_db)):
    try:
        created_injury = Injury(message=injury.message,
                                client_id=injury.client_id)
        db.add(created_injury)
        await db.commit()
        await db.refresh(created_injury)
        return created_injury
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get('/injuries/{client_id}', response_model=List[InjurySchema])
async def injuries_list(client_id: int, db: AsyncSession = Depends(get_db)):
    try:
        injuries = await db.execute(select(Injury).options(
            selectinload(Injury.client)).where(Injury.client_id == client_id))
        result = injuries.scalars().all()
        return result
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post('/contacts-email-send/')
async def email_send(email: EmailSchema, db: AsyncSession = Depends(get_db)):
    try:
        send_mail(email.email, email.subject, email.message)
        contact = Contacts(email=email.email)
        db.add(contact)
        await db.commit()
        await db.refresh(contact)
        return contact
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Данный аккаунт уже существует')


# pagination
@router.get('/paginate-injuries/', response_model=List[ClientSchema])
async def paginate_injuries(start: int = 0, limit: int = 2, db: AsyncSession = Depends(get_db)):
    clients = await db.execute(select(Clients).offset(start).limit(limit))
    result = clients.scalars().all()
    return result


# filtration
@router.get('/property-filter/', response_model=List[PropertySchema])
async def filter_property(
        address: str = Query(None),
        city: str = Query(None),
        price: Decimal = Query(None),
        db: AsyncSession = Depends(get_db)):
    query = select(Property)

    if address:
        query = query.where(Property.address == address)
    if city:
        query = query.where(Property.city == city)
    if price:
        query = query.where(Property.price >= price)

    properties = await db.execute(query)
    result = properties.scalars().all()

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)
    return result
