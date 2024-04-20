from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

match_routes = APIRouter(
    tags=["matches"]
)


class Match(BaseModel):
    passengerRouteId: str
    contact: str
    name: str


@match_routes.get("/matches", response_model=List[Match])
async def get_matches_by_route(passenger_route_id: str):
    matches = []
    return matches
