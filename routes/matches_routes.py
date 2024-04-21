from typing import List

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.credentials import POSTGRE_CONNECTION
from common.models import RouteMatchEntity

match_routes = APIRouter(
    tags=["matches"]
)


class Match(BaseModel):
    passengerRouteId: str
    contact: str
    name: str
    link: str


def convert_route_match_to_match(route_match: RouteMatchEntity) -> Match:
    passenger_route = route_match.passenger_route
    driver_route = route_match.driver_route

    contact = passenger_route.route.owner.contact
    name = passenger_route.route.owner.name

    return Match(
        passengerRouteId=str(route_match.passenger_route_id),
        contact=contact,
        name=name,
        link=f'http://18.199.107.206:30490/html/{str(route_match.id)}.html'
    )


@match_routes.get("/matches", response_model=List[Match])
def get_matches_by_route(passengerRouteId: str):

    return [
        Match(passengerRouteId='nvdivnw3u', contact='ajajaj@gmail.com', name='Simon', link='http://18.199.107.206:30490/html/map.html'),
        Match(passengerRouteId='ndsadvdivnw3u', contact='ajajaj2@gmail.com', name='Simon2', link='http://18.199.107.206:30490/html/map.html')
    ]

    engine = create_engine(POSTGRE_CONNECTION)
    sesion_maker = sessionmaker(engine)
    session = sesion_maker()

    try:
        route_matches = session.query(RouteMatchEntity).filter(
            RouteMatchEntity.passenger_route_id == passengerRouteId
        ).all()

        matches = [convert_route_match_to_match(route_match) for route_match in route_matches]

        return matches

    finally:
        session.close()
