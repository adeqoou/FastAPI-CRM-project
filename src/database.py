from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from src.config import settings

async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    echo=True,
    # pool_size=5,
    # max_overflow=10
)

async_session = async_sessionmaker(bind=async_engine)

Base = declarative_base()


async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session