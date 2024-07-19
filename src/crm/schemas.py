from pydantic import BaseModel, Field, EmailStr


class ClientCreateSchema(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr | None = None


class ClientSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr