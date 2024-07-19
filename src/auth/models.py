from sqlalchemy import Column, String, Integer, Boolean, Enum as SqlEnum
from src.database import Base
from enum import Enum
from sqlalchemy.orm import relationship


class UserRole(Enum):
    REALTOR = 'realtor'
    MANAGER = 'manager' 


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column(String(length=100), unique=True, nullable=False)
    first_name = Column(String(length=100))
    last_name = Column(String(length=100))
    email = Column(String(length=255), unique=True)
    password = Column(String)
    is_superuser = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    role = Column(SqlEnum(UserRole), default=UserRole.REALTOR, nullable=False)

    deals = relationship('Deals', back_populates='user')
    injury = relationship('Injury', back_populates='user')
