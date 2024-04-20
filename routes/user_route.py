from uuid import uuid4, UUID

from fastapi import Body
from pydantic import BaseModel, Field
from fastapi import APIRouter

user_router = APIRouter(
    prefix="/user",
    tags=["user"]
)


class User(BaseModel):
    name: str
    contact: str
    user_id: UUID = Field(default_factory=uuid4)


class CreateUserResponse(BaseModel):
    user_id: UUID


class ValidateUserResponse(BaseModel):
    name: str
    contact: str


users = {}  # In-memory user storage (replace with database)


@user_router.post("/users", response_model=CreateUserResponse)
def create_user(user: User = Body(...)):
    users[user.user_id] = user
    return user


@user_router.get("/users/validation", response_model=ValidateUserResponse)
def validate_user(user_id: UUID):
    user = users.get(user_id)
    if user:
        return user
    else:
        return {"detail": "User not found"}, 404
