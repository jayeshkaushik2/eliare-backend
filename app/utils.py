from app.schemas.logs_schema import *
from motor.motor_asyncio import AsyncIOMotorDatabase 


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




def write_log_to_cache():
    ...