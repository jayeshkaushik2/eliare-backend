from pydantic import BaseModel

COLLECTION_NAME = "users"

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str
    is_active: bool = True

class UserDetail(BaseModel):
    id: str
    username: str
    email: str
    is_active: bool = True

UsersList = list[UserDetail]
