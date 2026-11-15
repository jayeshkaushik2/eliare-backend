from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

# ------------------- Mongo DB connect -------------------


# A global dictionary or class can hold the client container
class MongoDBContainer:
    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None


db_container = MongoDBContainer()


def get_mongo_db() -> AsyncIOMotorDatabase:
    return db_container.db
