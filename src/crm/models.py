from sqlalchemy import (
    Column, String, Integer, ForeignKey,
    Float, DECIMAL, Text, DateTime, Enum as SqlEnum
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.database import Base
from enum import Enum


class Clients(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = Column(String(length=100), nullable=False)
    last_name = Column(String(length=100), nullable=False)
    email = Column(String(length=100), nullable=True)

    injury = relationship('Injury', back_populates='client')
    deals = relationship('Deals', back_populates='client')


class Property(Base):
    __tablename__ = 'property'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    address = Column(String(length=120))
    city = Column(String(length=100))
    bedrooms = Column(Integer, nullable=True)
    bathrooms = Column(Integer, nullable=True)
    square_feet = Column(Float)
    price = Column(DECIMAL(10, 2))
    description = Column(Text, nullable=True)

    images = relationship('PropertyImage', back_populates='property')
    deals = relationship('Deals', back_populates='property')


class PropertyImage(Base):
    __tablename__ = 'property_image'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    image = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    property_id = Column(Integer, ForeignKey('property.id'), nullable=False)

    property = relationship('Property', back_populates='images')


class DealsChoices(Enum):
    SALE = 1, 'sale'
    RENT = 2, 'rent'


class DealStatus(Enum):
    ISSUED = 'Оформлено'
    COMPLETED = 'Завершено'
    DRAFT = 'Черновик'


class Deals(Base):
    __tablename__ = 'deals'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deal_type = Column(SqlEnum(DealsChoices), nullable=False)
    status = Column(SqlEnum(DealStatus), nullable=False, default=DealStatus.DRAFT)
    property_id = Column(Integer, ForeignKey('property.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)

    user = relationship('User', back_populates='deals')
    property = relationship('Property', back_populates='deals')
    client = relationship('Clients', back_populates='deals')


class Injury(Base):
    __tablename__ = 'injury'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    message = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)

    user = relationship('User', back_populates='injury')
    client = relationship('Clients', back_populates='injury')

