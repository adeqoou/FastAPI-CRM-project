from pydantic import BaseModel
from pathlib import Path
from pydantic_settings import BaseSettings
import os

BASE_DIR = Path(__file__).parent.parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / 'certs/jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs/jwt-public.pem'
    algorithm: str = 'RS256'


class AuthConfig(BaseSettings):
    auth_jwt: AuthJWT = AuthJWT()

    SECRET_KEY: str = os.getenv('SECRET_KEY')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


auth_config = AuthConfig()