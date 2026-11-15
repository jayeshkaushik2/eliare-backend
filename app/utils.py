from app.schemas.logs_schema import *
from motor.motor_asyncio import AsyncIOMotorDatabase
from kafka import KafkaProducer, KafkaConsumer
import uuid
from app.settings import settings
import json
from app.constants import KafkaTopics
import json

bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS

producer = KafkaProducer(bootstrap_servers=bootstrap_servers)
# consumer = KafkaConsumer(topic, bootstrap_servers=bootstrap_servers)


def create_error_log_api_handler(db: AsyncIOMotorDatabase, payload: ErrorLogCreate):
    try:
        error_log_dict = payload.model_dump()
        error_log_dict["status"] = ErrorStatuses.PENDING.value

        if not error_log_dict.get("error_dt"):
            error_log_dict["error_dt"] = datetime.now()
        result = db.error_logs.insert_one(error_log_dict)

        instance = db.error_logs.find_one({"_id": result.inserted_id})

        return ErrorRespStatus.SUCCESS.value, instance
    except Exception as e:
        return ErrorRespStatus.FAILED.value, str(e)


def send_error_log_to_kafka(data: dict):
    topic = KafkaTopics.ERROR_LOGS
    future = producer.send(
        topic=topic,
        value=json.dumps(data).encode(encoding="utf-8"),
    )
    result = None
    try:
        result = future.get(timeout=60)
    except Exception as e:
        print("Unable to send error logs", str(e))
    finally:
        return result
