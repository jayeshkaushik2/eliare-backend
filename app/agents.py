from app.schemas.logs_schema import ErrorStatuses

def handle_error_log(log):
    print(f"processing pending log: {log}")
    return ErrorStatuses.COMPLETED.value
