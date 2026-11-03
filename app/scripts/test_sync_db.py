from app.schemas.utils import *
from app.agents import *

res = get_mongo_document(
    "error_logs", 
    _id="6aea34761f84657314abdbf6"
    # load=True,
    # status="PENDING",
)
print("RES: ", res)

agent = Agent("gemini", "gemini-flash-latest")
print(agent)
print(agent.fix_log_error(error_log=res))