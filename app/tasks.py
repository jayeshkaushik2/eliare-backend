from app.celery_worker import app
from app.schemas.database import get_mongo_db
from app.schemas.logs_schema import ErrorStatuses
from app import agents
from pymongo import MongoClient
from app.settings import settings
from app.utils import create_error_log_api_handler

sync_client = MongoClient(settings.MONGO_URI)
sync_db = sync_client[settings.MONGO_DB_NAME]


@app.task
def task_register_error_log(payload: dict):
    create_error_log_api_handler(sync_db, payload)


@app.task
def task_single_pending_error_log(log_id: str):
    log = sync_db.error_logs.find_one({"_id": log_id})
    new_status = agents.handle_error_log(log=log)
    sync_db.error_logs.update_one(
        {"_id": log["_id"]},
        {"$set": {"status": new_status}},
    )


@app.task
def task_process_pending_error_logs(n: int = 10):
    """
    Task scheduler to process pending error logs in batches of n.
    This function fetches n pending error logs from the database and processes each one by calling the `task_single_pending_error_log` task for each log. The status of each log is updated based on the result of the processing.
    """
    # processing n number of error logs at a time
    pending_error_logs = list(
        sync_db.error_logs.find({"status": ErrorStatuses.PENDING.value}).limit(n)
    )
    for log in pending_error_logs:
        task_single_pending_error_log.delay(log_id=str(log["_id"]))


@app.task
def task_process_failed_error_logs(n: int = 10): ...


@app.task
def task_process_sub_completed_error_logs(n: int = 10):
    # Raise prs for completed error_logs
    ...
