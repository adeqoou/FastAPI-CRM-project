from pydantic import BaseModel, Field, EmailStr, condecimal
from src.auth.schemas import UserSchema
from datetime import datetime


class ClientCreateSchema(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr | None = None


class ClientSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr


class InjuryBaseSchema(BaseModel):
    message: str
    client_id: int


class InjurySchema(InjuryBaseSchema):
    id: int
    created_at: datetime
    updated_at: datetime | None = None
    client: ClientSchema
    user: UserSchema | None = None


class EmailSchema(BaseModel):
    email: str = EmailStr
    subject: str
    message: str


class PropertySchema(BaseModel):
    id: int
    address: str | None
    city: str | None
    price: condecimal(max_digits=10, decimal_places=2) | None