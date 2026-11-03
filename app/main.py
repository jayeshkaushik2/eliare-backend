from fastapi import FastAPI
from app.schemas import UserDetail, UsersList, UserCreate
from app.schemas.database import lifespan
from app.apis import user_apis, log_apis
from app.settings import settings

app = FastAPI(lifespan=lifespan)
app.include_router(prefix="/api", router=user_apis.router)
app.include_router(prefix="/api", router=log_apis.router)

@app.get("/")
async def root():
    return {"message": "Hello World", "version": settings.VERSION}