from app.schemas.logs_schema import (
    ErrorLogCreate,
    ErrorLogDetail,
    ErrorStatuses,
    ErrorLogsList,
    ErrorLogCreateResp,
    ErrorRespStatus,
)
from fastapi import APIRouter, HTTPException, status
from app.schemas.database import get_mongo_db
from datetime import datetime
from bson import ObjectId
from app.tasks import task_register_error_log
from app.utils import send_error_log_to_kafka

router = APIRouter(prefix="/v1/logs", tags=["logs"])


def error_log_helper(error_log):
    return {
        "id": str(error_log["_id"]),
        "message": error_log["message"],
        "error_dt": error_log["error_dt"],
        "status": error_log["status"],
    }


async def list_error_logs_api_handler():
    db = get_mongo_db()
    error_logs = await db.error_logs.find().to_list(length=None)
    return [error_log_helper(error_log) for error_log in error_logs]


async def error_log_detail_api_handler(pk):
    db = get_mongo_db()
    try:
        obj_id = ObjectId(pk)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID format"
        )
    # 2. Query the database
    error_log = await db.error_logs.find_one({"_id": obj_id})

    if not error_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="error_log not found"
        )
    return error_log_helper(error_log)


# ---------------------- APIs ----------------------


@router.post(
    "/create/", response_model=ErrorLogCreateResp, status_code=status.HTTP_201_CREATED
)
async def create_error_log_api(payload: ErrorLogCreate):
    result = send_error_log_to_kafka(payload.model_dump())
    return {"status_code": ErrorRespStatus.SUCCESS.value if result else ErrorRespStatus.FAILED.value}


@router.get("/", response_model=ErrorLogsList, status_code=status.HTTP_200_OK)
async def list_error_logs_api():
    result = await list_error_logs_api_handler()
    return result


@router.get("/{pk}/", response_model=ErrorLogDetail, status_code=status.HTTP_200_OK)
async def error_log_detail_api(pk):
    result = await error_log_detail_api_handler(pk=pk)
    return result
