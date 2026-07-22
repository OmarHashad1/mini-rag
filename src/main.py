from fastapi import FastAPI
from routes import base_router, data_router
from configs import get_settings
from contextlib import asynccontextmanager
from pymongo import AsyncMongoClient
from beanie import init_beanie
from models import Chunk, Project, Asset
import logging

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    Settings = get_settings()
    client = AsyncMongoClient(Settings.MONGO_URI)
    await init_beanie(
        database=client[Settings.DB_NAME], document_models=[Chunk, Project, Asset]
    )
    logger.info("Connected to MongoDB")
    yield
    await client.close()
    logger.info("MongoDB connection closed")


app = FastAPI(lifespan=lifespan)


app.include_router(base_router)
app.include_router(data_router)
