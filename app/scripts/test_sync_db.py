from app.schemas.utils import *

res = get_mongo_document(
    "error_logs", 
    _id="6aea34761f84657314abdbf6"
    # load=True,
    # status="PENDING",
)

print("RES: ", res)