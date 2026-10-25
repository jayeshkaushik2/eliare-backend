from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from ..settings import settings

# ------------------- Mongo DB connect -------------------

MONGO_URI = settings.MONGO_URI 
DB_NAME = settings.MONGO_DB_NAME

# A global dictionary or class can hold the client container
class MongoDBContainer:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

db_container = MongoDBContainer()

@asynccontextmanager
async def lifespan(*args, **kwargs):
    # This runs when the server starts
    db_container.client = AsyncIOMotorClient(MONGO_URI)
    db_container.db = db_container.client[DB_NAME]
    print(f"Successfully connected to MongoDB {DB_NAME}!")
    yield
    db_container.client.close()
    print("MongoDB connection closed.")

def get_mongo_db() -> AsyncIOMotorDatabase:
    return db_container.db
