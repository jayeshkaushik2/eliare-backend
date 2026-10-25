from app.schemas.users_schema import UserCreate, UsersList, UserDetail
from fastapi import APIRouter, HTTPException, status
from app.schemas.database import get_mongo_db
from bson import ObjectId
from passlib.context import CryptContext

router = APIRouter(prefix="/v1/users", tags=["users"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def user_helper(user) -> dict:
    """Helper to convert MongoDB document to response format"""
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "email": user["email"],
        "is_active": user.get("is_active", True),
    }

async def create_user_api_handler(payload: UserCreate):
    if payload.confirm_password != payload.password:
        raise HTTPException(detail="Password doesn't match", status=status.HTTP_400_BAD_REQUEST)

    db = get_mongo_db()
    existing_user = await db.users.find_one({"$or": [{"username": payload.username}, {"email": payload.email}]})

    if existing_user:
        raise HTTPException(detail="User already exist", status_code=status.HTTP_400_BAD_REQUEST)

    userdict = payload.model_dump(exclude={"confirm_password"})
    # TODO need to hash the password before storing it in the database
    # userdict["password"] = hash_password(userdict["password"])
    userdict["password"] = userdict["password"]
    result = await db.users.insert_one(userdict)
    user = await db.users.find_one({"_id": result.inserted_id})
    return user_helper(user)

async def list_users_api_handler():
    db = get_mongo_db()
    users = await db.users.find().to_list(length=None)
    return [user_helper(user) for user in users]

async def user_detail_api_handler(pk):
    db = get_mongo_db()
    try:
        obj_id = ObjectId(pk)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Invalid user ID format"
        )
    # 2. Query the database
    user = await db.users.find_one({"_id": obj_id})
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    return user_helper(user)

# ---------------------- APIs ----------------------

@router.post("/create/", response_model=UserDetail, status_code=status.HTTP_201_CREATED)
async def create_user_api(payload: UserCreate):
    result = await create_user_api_handler(payload=payload)
    return result

@router.get("/", response_model=UsersList, status_code=status.HTTP_200_OK)
async def list_users_api():
    result = await list_users_api_handler()
    return result

@router.get("/{pk}/", response_model=UserDetail, status_code=status.HTTP_200_OK)
async def user_detail_api(pk):
    result = await user_detail_api_handler(pk=pk)
    return result
