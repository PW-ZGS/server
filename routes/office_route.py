from fastapi import FastAPI
from pydantic import BaseModel

from .models import Location
from typing import List
from fastapi import APIRouter

office_router = APIRouter(
    tags=["office"]
)

offices = [
    {"officeId": "1", "name": "Main Office", "location": {"latitude": 52.196774, "longitude": 21.017593}},
    {"officeId": "2", "name": "Branch Office", "location": {"latitude": 51.107748, "longitude": 17.068012}},
]


class Office(BaseModel):
    officeId: str
    name: str
    location: Location


@office_router.get("/offices", response_model=List[Office])
def get_offices():
    return [Office(**office) for office in offices]
