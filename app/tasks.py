from app.celery_worker import app
from app.schemas.database import get_mongo_db
from app.schemas.logs_schema import ErrorStatuses
from app import agents
from pymongo import MongoClient
from app.settings import settings

sync_client = MongoClient(settings.MONGO_URI)
sync_db = sync_client[settings.MONGO_DB_NAME]

@app.task
def task_process_pending_error_logs(n: int = 10):
    # processing n number of error logs at a time
    pending_error_logs = list(
        sync_db.error_logs.find({"status": ErrorStatuses.PENDING.value}).limit(n)
    )

    for log in pending_error_logs:
        new_status = agents.handle_error_log(log=log)
        sync_db.error_logs.update_one(
            {"_id": log["_id"]},
            {"$set": {"status": new_status}},
        )

@app.task
def task_process_failed_error_logs(n: int = 10):
    ...

@app.task
def task_process_sub_completed_error_logs(n: int = 10):
    # Raise prs for completed error_logs
    ...
