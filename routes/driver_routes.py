import uuid
from typing import List

from fastapi import Body, APIRouter
from pydantic import BaseModel, Field
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.responses import JSONResponse

from common.credentials import POSTGRE_CONNECTION
from common.models import RouteEntity, DriverRouteEntity
from .models import RouteInput, DriverRoute

routes: dict[str, DriverRoute] = {}


class CreateRouteResponse(BaseModel):
    routeId: str


class ModifyPassengerCount(BaseModel):
    operation: str = Field(..., description="Operation to perform (inc or dec)")


driver_route = APIRouter(
    prefix="/driver_routes",
    tags=["driver_routes"]
)


@driver_route.post("/to")
def create_driver_route_to(route_data: RouteInput):
    route_id = uuid.uuid4()
    route = RouteEntity(
                id = route_id,
                directions_text="-1",
                latitude=route_data.startPoint.latitude,
                longitude=route_data.startPoint.longitude,
                office_id=route_data.officeId,
                owner_id=route_data.userId)
    driver_route = DriverRouteEntity(start_time=route_data.fromTime,
                                     max_capacity=route_data.availableSeats,
                                     route_id=route.id)
    engine = create_engine(POSTGRE_CONNECTION)
    session_maker = sessionmaker(engine)
    session = session_maker()
    try:
        session.add(route)
        session.commit()
        session.add(driver_route)
        session.commit()
        return JSONResponse(status_code=200, content="Added")
    except Exception as e:
        return JSONResponse(status_code=404, content="Not valid data, check if user exists")



@driver_route.get("/by-users/{userId}", response_model=List[DriverRoute])
def get_driver_routes_by_user(user_id: str):
    filtered_routes = []
    for route in routes.values():
        if route.userId == user_id or user_id is None:
            filtered_routes.append(route)
    return filtered_routes


@driver_route.get("/{route_id}", response_model=DriverRoute)
def get_driver_route(route_id: str):
    route = routes.get(route_id)
    if route is None:
        return {"detail": f"Driver route with ID {route_id} not found"}, 404
    return route


@driver_route.delete("/{route_id}", status_code=204)
def delete_driver_route(route_id: str):
    if route_id in routes:
        del routes[route_id]
    else:
        return {"detail": f"Driver route with ID {route_id} not found"}, 404


@driver_route.post("/{route_id}/modify-passenger-count", response_model=BaseModel)
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

