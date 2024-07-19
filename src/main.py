from fastapi import FastAPI
import uvicorn
from src.auth import router as auth_router
from src.crm import router as crm_router

app = FastAPI()

app.include_router(auth_router.router, prefix='/api/v1')
app.include_router(crm_router.router, prefix='/api/v1')

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
