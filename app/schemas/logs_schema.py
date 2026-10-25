from pydantic import BaseModel
from datetime import datetime
from enum import Enum

COLLECTION_NAME = "error_logs"


class ErrorStatuses(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    FAILED = "FAILED"
    SUB_COMPLETED = "SUB_COMPLETED"
    COMPLETED = "COMPLETED"


class ErrorLogCreate(BaseModel):
    message: str
    error_json: dict
    error_dt: datetime | None = None
    status: str | None = None

class ErrorLogDetail(BaseModel):
    id: str
    message: str
    error_dt: datetime
    status: str

ErrorLogsList = list[ErrorLogDetail]

class GitPrCreate(BaseModel):
    error_log_id: str
    pr_link: str
    # branching flow
    checkout_from: str
    branch_name: str
    raised_for: str
    # to store commit ids and messages
    commits: dict
