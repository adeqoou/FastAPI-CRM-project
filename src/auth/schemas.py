from pydantic import BaseModel, EmailStr, ConfigDict, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    first_name: str
    last_name: str
    email: EmailStr
    password: bytes
    role: str | None = None
    is_superuser: bool = False


class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    username: str = Field(min_length=1, max_length=30)
    email: EmailStr | None = None
    is_active: bool = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    # scopes: list[str] = []
