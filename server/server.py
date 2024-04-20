from uuid import uuid4, UUID

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from fastapi import APIRouter

app = FastAPI()


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


@app.post("/users", response_model=CreateUserResponse)
async def create_user(user: User = Body(...)):
    users[user.user_id] = user
    return user


@app.get("/users/validation", response_model=ValidateUserResponse)
async def validate_user(user_id: UUID):
    user = users.get(user_id)
    if user:
        return user
    else:
        return {"detail": "User not found"}, 404


# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
