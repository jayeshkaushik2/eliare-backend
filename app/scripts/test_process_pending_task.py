from app.schemas.database import *
from app.schemas.logs_schema import *
from app.schemas.users_schema import *
from app.tasks import *

from app.tasks import task_process_pending_error_logs

async def run_test():
    # Properly use the asynccontextmanager with 'async with'
    async with lifespan():
        # At this point, db_container.db is initialized
        print("Lifespan active, executing task...")

        # Since your celery task might be synchronous (standard def) or asynchronous (async def),
        # call it appropriately. If it's a standard synchronous Celery task:
        result = task_process_pending_error_logs(n=1)
        print("Task result:", result)


# If you are in modern IPython, you can just await this directly in the prompt:
await run_test()