from app.schemas.logs_schema import ErrorLogCreate, ErrorLogDetail, ErrorStatuses, ErrorLogsList
from fastapi import APIRouter, HTTPException, status
from app.schemas.database import get_mongo_db
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/v1/logs", tags=["logs"])

def error_log_helper(error_log):
    return {
        "id": str(error_log["_id"]),
        "message": error_log["message"],
        "error_dt": error_log["error_dt"],
        "status": error_log["status"],
    }

async def create_error_log_api_handler(payload: ErrorLogCreate):
    db = get_mongo_db()
    try:
        error_log_dict = payload.model_dump()
        error_log_dict["status"] = ErrorStatuses.PENDING.value

        if not error_log_dict.get("error_dt"):
            error_log_dict["error_dt"] = datetime.now()
        result = await db.error_logs.insert_one(error_log_dict)
        instance = await db.error_logs.find_one({"_id": result.inserted_id})
        return error_log_helper(instance)

    except Exception as e:
        print(e)
        raise HTTPException(detail="Failed to create error log enter", status_code=status.HTTP_400_BAD_REQUEST)

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
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid ID format"
        )
    # 2. Query the database
    error_log = await db.error_logs.find_one({"_id": obj_id})
    
    if not error_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="error_log not found"
        )
    return error_log_helper(error_log)

# ---------------------- APIs ----------------------

@router.post("/create/", response_model=ErrorLogDetail, status_code=status.HTTP_201_CREATED)
async def create_error_log_api(payload: ErrorLogCreate):
    result = await create_error_log_api_handler(payload)
    return result

@router.get("/", response_model=ErrorLogsList, status_code=status.HTTP_200_OK)
async def list_error_logs_api():
    result = await list_error_logs_api_handler()
    return result

@router.get("/{pk}/", response_model=ErrorLogDetail, status_code=status.HTTP_200_OK)
async def error_log_detail_api(pk):
    result = await error_log_detail_api_handler(pk=pk)
    return result
