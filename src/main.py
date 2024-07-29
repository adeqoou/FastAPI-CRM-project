from fastapi import FastAPI
import uvicorn
from src.auth import router as auth_router
from src.crm import router as crm_router
from src.chat import router as chat_router
from src.admin import init_admin

from fastapi_cache import FastAPICache
from redis import asyncio as aioredis
from fastapi_cache.backends.redis import RedisBackend

app = FastAPI()

app.include_router(auth_router.router, prefix='/api/v1')
app.include_router(crm_router.router, prefix='/api/v1')
app.include_router(chat_router.router)

init_admin(app)


@app.on_event('startup')
async def startup():
    redis = aioredis.from_url('redis://localhost')
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
