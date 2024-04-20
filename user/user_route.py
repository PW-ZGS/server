from fastapi import APIRouter

user_router = APIRouter(
    prefix = "/user",
    tags=["user"]

)

class
@user_router.get("/")
def get_user():
    return "1"