import uuid
from typing import List

from fastapi import Body, APIRouter
from pydantic import BaseModel, Field

from .models import RouteInput, DriverRoute

routes: dict[str, DriverRoute] = {}


class CreateRouteResponse(BaseModel):
    routeId: str


class ModifyPassengerCount(BaseModel):
    operation: str = Field(..., description="Operation to perform (inc or dec)")


driver_route_router = APIRouter(
    prefix="/driver_routes",
    tags=["driver_routes"]
)


@driver_route_router.post("/to", response_model=CreateRouteResponse)
def create_driver_route_to(route_data: RouteInput):
    route_id = str(uuid.uuid4())
    route = DriverRoute(
        routeId=route_id,
        startPoint=None,
        endPoint=route_data.startPoint,
        **route_data.dict(exclude_unset=True),
    )
    routes[route_id] = route
    return CreateRouteResponse(routeId=route_id)


@driver_route_router.get("/by-users/{userId}", response_model=List[DriverRoute])
def get_driver_routes_by_user(user_id: str):
    filtered_routes = []
    for route in routes.values():
        if route.userId == user_id or user_id is None:
            filtered_routes.append(route)
    return filtered_routes


@driver_route_router.get("/{route_id}", response_model=DriverRoute)
def get_driver_route(route_id: str):
    route = routes.get(route_id)
    if route is None:
        return {"detail": f"Driver route with ID {route_id} not found"}, 404
    return route


@driver_route_router.delete("/{route_id}", status_code=204)
def delete_driver_route(route_id: str):
    if route_id in routes:
        del routes[route_id]
    else:
        return {"detail": f"Driver route with ID {route_id} not found"}, 404


@driver_route_router.post("/{route_id}/modify-passenger-count", response_model=BaseModel)
def modify_passenger_count(route_id: str, body: ModifyPassengerCount = Body(...)):
    route = routes.get(route_id)
    if route is None:
        return {"detail": f"Driver route with ID {route_id} not found"}, 404

    if body.operation == "inc":
        route.availableSeats += 1
    elif body.operation == "dec" and route.availableSeats > 0:
        route.availableSeats -= 1
    else:
        return {"detail": "Cannot decrease passenger count below zero"}, 400

    return {"updatedPassengerCount": route.availableSeats}

