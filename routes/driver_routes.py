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
        session.close()
        content = {"routeId": str(route_id)}
        return JSONResponse(status_code=200, content=content)
    except Exception as e:
        return JSONResponse(status_code=404, content="Not valid data, check if user exists")


@driver_route.get("/by-users/{userId}", response_model=List[DriverRoute])
def get_driver_routes_by_user(userId: str):
    engine = create_engine(POSTGRE_CONNECTION)
    session_maker = sessionmaker(engine)
    session = session_maker()
    try:
        filtered_entities = session.query(RouteEntity).filter(RouteEntity.owner_id == userId).all()
        filtered_entities = [{"routeId":str(entity.id), "startPoint":{"latitude":float(entity.latitude),"longitude":float(entity.longitude)}, "endPoint":{"latitude":float(entity.office.latitude),"longitude":float(entity.office.longitude)}} for entity in filtered_entities]
        session.close()
        return JSONResponse(status_code=200, content=filtered_entities)
    except Exception as e:
        return JSONResponse(status_code=404, content="Entities not found")


@driver_route.get("/{route_id}", response_model=DriverRoute)
def get_driver_route(route_id: str):
    engine = create_engine(POSTGRE_CONNECTION)
    session_maker = sessionmaker(engine)
    session = session_maker()
    try:
        entity = session.query(RouteEntity).filter(RouteEntity.id == route_id).one()
        content = {"routeId": str(entity.id),
                              "startPoint": {"latitude": float(entity.latitude), "longitude": float(entity.longitude)},
                              "endPoint": {"latitude": float(entity.office.latitude),
                                           "longitude": float(entity.office.longitude)}}
        session.close()
        return JSONResponse(status_code=200, content=content)
    except Exception as e:
        return JSONResponse(status_code=404, content="Entities not found")


@driver_route.delete("/{route_id}", status_code=204)
def delete_driver_route(route_id: str):
    engine = create_engine(POSTGRE_CONNECTION)
    session_maker = sessionmaker(engine)
    session = session_maker()
    route_to_delete = session.query(RouteEntity).filter(RouteEntity.id == route_id).one()
    session.delete(route_to_delete)
    session.commit()
    session.close()
    # return JSONResponse(status_code=204,content="DriverRoute deleted successfully")


@driver_route.post("/{route_id}", response_model=BaseModel)
def modify_passenger_count(route_id: str, body: ModifyPassengerCount = Body(...)):
    engine = create_engine(POSTGRE_CONNECTION)
    session_maker = sessionmaker(engine)
    session = session_maker()
    driver_route = session.query(DriverRouteEntity).filter_by(route_id=route_id).get(1)
    driver_route.passenger_count = driver_route.passenger_count+1
    content = {"updatedPassengerCount": driver_route.passenger_count}
    session.commit()
    session.close()
    return JSONResponse(status_code=200,content=content)

