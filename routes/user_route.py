from uuid import uuid4, UUID

from fastapi import Body
from pydantic import BaseModel, Field
from fastapi import APIRouter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.credentials import POSTGRE_CONNECTION
from common.models import UserEntity
from fastapi.responses import JSONResponse

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


@user_router.post("/", response_model=CreateUserResponse)
def create_user(user: User = Body(...)):
    engine = create_engine(POSTGRE_CONNECTION)
    sesion_maker = sessionmaker(engine)
    session = sesion_maker()
    user = UserEntity(id=user.user_id,name=str(user.name), contact=user.contact)
    try:
        session.add(user)
        session.commit()
    except Exception as e:
        print(e)
    content = {"user_id": str(user.id)}
    return JSONResponse(status_code=200, content=content)

@user_router.get("/validation", response_model=ValidateUserResponse)
def validate_user(userId: UUID):
    engine = create_engine(POSTGRE_CONNECTION)
    sesion_maker = sessionmaker(engine)
    session = sesion_maker()
    try:
        entity = session.query(UserEntity).filter_by(id=str(userId)).one()
        content = {"name":entity.name,
               "contact":entity.contact}
        return JSONResponse(status_code=200, content=content)
    except Exception as e:
        return JSONResponse(status_code=404, content="User not found")

