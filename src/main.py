from fastapi import FastAPI
from async_generator import asynccontextmanager
from base import engine, Base
from websocket.websocket import router
from chat.router import chat_router
import models
import uvicorn
import logging.config
from authentication.router import router as auth_router
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logging.config.fileConfig(
    os.path.join(BASE_DIR, 'logging.conf'),
    disable_existing_loggers=False
    )

logger = logging.getLogger(f"chatapp.{__name__}")
logger.info("Logging is initialized")


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)
    yield
    

app = FastAPI(lifespan=lifespan)

app.include_router(router)
app.include_router(chat_router)
app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run(app)