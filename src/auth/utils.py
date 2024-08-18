from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User

from .config import auth_config
from .schemas import TokenData
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> bytes:
    return pwd_context.hash(password)


def encode_jwt(
        payload: dict,
        private_key: str = auth_config.auth_jwt.private_key_path.read_text(),
        algorithm: str = auth_config.auth_jwt.algorithm
):
    encoded = jwt.encode(payload, private_key, algorithm=algorithm)
    return encoded


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({'exp': expire})
    encoded_jwt = encode_jwt(to_encode)
    return encoded_jwt


def decode_access_token(token: str, credentials_exception):
    try:
        public_key = auth_config.auth_jwt.public_key_path.read_text()
        algorithm = auth_config.auth_jwt.algorithm
        payload = jwt.decode(token, public_key, algorithms=[algorithm])
        username: str = payload.get('sub')

        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.exceptions.PyJWTError:
        raise credentials_exception
    return token_data


async def authenticate_user(db: AsyncSession, username: str, password: str):
    result = await db.execute(select(User).where(User.username == username))
    user = result.scalars().first()

    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
