from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from .models import PassengerRoute

passenger_routes: dict[str, PassengerRoute] = {}


class DeleteResponse(BaseModel):
    pass


passenger_route_router = APIRouter(
    prefix="/passenger_routes",
    tags=["passenger_routes"]
)


@passenger_route_router.get("/{passenger_route_id}", response_model=PassengerRoute)
def get_passenger_route(passenger_route_id: str):
    passenger_route = passenger_routes.get(passenger_route_id)
    if passenger_route is None:
        return {"detail": f"Passenger route with ID {passenger_route_id} not found"}, 404
    return passenger_route


@passenger_route_router.delete("/{passenger_route_id}", status_code=204)
def delete_passenger_route(passenger_route_id: str):
    if passenger_route_id in passenger_routes:
        del passenger_routes[passenger_route_id]
    else:
        return {"detail": f"Passenger route with ID {passenger_route_id} not found"}, 404
    return DeleteResponse()


@passenger_route_router.get("/by-users/{user_id}", response_model=List[PassengerRoute])
def get_passenger_routes_by_user(user_id: str):
    filtered_routes = []
    for route in passenger_routes.values():
        if route.userId == user_id or user_id is None:
            filtered_routes.append(route)
    return filtered_routes
