import uuid
from datetime import datetime
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.responses import JSONResponse

from common.credentials import POSTGRE_CONNECTION
from common.models import RouteEntity, DriverRouteEntity, PassengerRouteEntity
from .models import PassengerRoute, Location, PassengerRouteInput

passenger_routes: dict[str, PassengerRoute] = {
    'acb': PassengerRoute(passengerRouteId='def',
                          startPoint=Location(latitude=12.34, longitude=54.34),
                          endPoint=Location(latitude=19.34, longitude=90.34)
                          ),
    'qwe': PassengerRoute(passengerRouteId='rty',
                          startPoint=Location(latitude=15.34, longitude=57.34),
                          endPoint=Location(latitude=17.34, longitude=65.34)
                          )
}


class DeleteResponse(BaseModel):
    pass


passenger_route_router = APIRouter(
    prefix="/passenger_routes",
    tags=["passenger_routes"]
)


@passenger_route_router.post("/to")
def create_driver_route_to(route_data: PassengerRouteInput):
    route_id = uuid.uuid4()
    route = RouteEntity(
        id=route_id,
        directions_text="-1",
        latitude=route_data.startPoint.latitude,
        longitude=route_data.startPoint.longitude,
        office_id=route_data.officeId,
        owner_id=route_data.userId)
    driver_route = PassengerRouteEntity(date_from=datetime.now(),
                                        date_to=datetime.now(),
                                        max_distance=500,
                                        route_id=route.id
                                        )
    passenger_routes[route_data.userId] = driver_route
    engine = create_engine(POSTGRE_CONNECTION)
    session_maker = sessionmaker(engine)
    session = session_maker()
    try:
        session.add(route)
        session.commit()
        session.add(driver_route)
        session.commit()
        return JSONResponse(status_code=200, content={"routeId": f"{route_id}"})
    except Exception as e:
        return JSONResponse(status_code=404, content="Not valid data, check if user exists")


@passenger_route_router.get("/{passengerRouteId}", response_model=PassengerRoute)
def get_passenger_route(passengerRouteId: str):
    return PassengerRoute(passengerRouteId='rty',
                          startPoint=Location(latitude=15.34, longitude=57.34),
                          endPoint=Location(latitude=17.34, longitude=65.34)
                          )

    for (userId, route) in passenger_routes.items():
        if passengerRouteId == route.passengerRouteId:
            return route
    return {"detail": f"Passenger route with ID {passengerRouteId} not found"}, 404


@passenger_route_router.delete("/{passengerRouteId}", status_code=204)
def delete_passenger_route(passengerRouteId: str):
    if passengerRouteId in passenger_routes:
        del passenger_routes[passengerRouteId]
    else:
        return {"detail": f"Passenger route with ID {passengerRouteId} not found"}, 404
    return DeleteResponse()


@passenger_route_router.get("/by-users/{user_id}", response_model=List[PassengerRoute])
def get_passenger_routes_by_user(user_id: str):
    return [PassengerRoute(passengerRouteId='rty',
                           startPoint=Location(latitude=15.34, longitude=57.34),
                           endPoint=Location(latitude=17.34, longitude=65.34)
                           )]
    filtered_routes = []
    for (userId, route) in passenger_routes.items():
        if userId == user_id:
            filtered_routes.append(route)
    return filtered_routes
