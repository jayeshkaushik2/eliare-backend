from fastapi import FastAPI
from app.schemas import UserDetail, UsersList, UserCreate
from app.apis import user_apis, log_apis
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
import asyncio
from app.constants import KafkaTopics
import json
from contextlib import asynccontextmanager
from app.settings import settings
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from app.schemas.database import db_container

MONGO_URI = settings.MONGO_URI
DB_NAME = settings.MONGO_DB_NAME

KAFKA_BOOTSTRAP_SERVERS = settings.KAFKA_BOOTSTRAP_SERVERS
KAFKA_TOPIC = KafkaTopics.ERROR_LOGS

kafka_producer: AIOKafkaProducer = None


async def setup_kafka_consumer():
    """Background Kafka consumer task."""
    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset="earliest",
    )

    # Start the consumer
    await consumer.start()
    print("Kafka Consumer started successfully.")

    try:
        async for msg in consumer:
            try:
                # Deserialize and process event payload
                payload = json.loads(msg.value.decode("utf-8"))
                print(f"Consumed event from partition {msg.partition}: {payload}")
                # TODO: Add your business/processing logic here

            except Exception as e:
                print(f"Error parsing message: {e}")
    except asyncio.CancelledError:
        print("Consumer task is being cancelled...")
    finally:
        await consumer.stop()
        print("Kafka Consumer stopped.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ==========================
    # --- STARTUP LOGIC ---
    # ==========================
    
    # 1. Connect to MongoDB
    db_container.client = AsyncIOMotorClient(MONGO_URI)
    db_container.db = db_container.client[DB_NAME]
    print(f"Successfully connected to MongoDB {DB_NAME}!")

    # 2. Initialize Kafka Producer
    print("Initializing Kafka Producer...")
    global kafka_producer
    kafka_producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS)
    await kafka_producer.start()
    print("Kafka Producer started successfully.")

    # 3. Spin up the background Kafka consumer task
    consumer_task = asyncio.create_task(setup_kafka_consumer())

    yield  # --- APP IS RUNNING AND HANDLING REQUESTS ---

    # ==========================
    # --- SHUTDOWN LOGIC ---
    # ==========================
    
    print("Shutting down components...")

    # 1. Stop the Kafka Producer
    if kafka_producer:
        await kafka_producer.stop()
        print("Kafka Producer stopped.")

    # 2. Cancel the background consumer task and wait for it to clean up
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        pass

    # 3. Close MongoDB connection
    db_container.client.close()
    print("MongoDB connection closed.")


app = FastAPI(lifespan=lifespan)
app.include_router(prefix="/api", router=user_apis.router)
app.include_router(prefix="/api", router=log_apis.router)