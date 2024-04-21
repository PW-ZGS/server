import webbrowser
from dataclasses import dataclass

import folium
from routingpy import Valhalla
from openrouteservice.client import Client
from haversine import haversine, Unit
from statistics import mean
from math import inf

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from common.credentials import POSTGRE_CONNECTION
from common.models import PassengerRouteEntity, DriverRouteEntity, RouteEntity


def openMapForDebug(path, map):
    html_page = f'{path}'
    map.save(html_page)
    new = 2
    webbrowser.open(html_page, new=new)

class PyRouter:
    def __init__(self, passenger_point, passenger_range, driver_point, end_point):
        self.passenger_point = passenger_point
        self.range = passenger_range
        self.driver_point = driver_point
        self.end_point = end_point
        self.closest_marker_distance = inf
        self.closest_marker_coords = [0, 0]
        self.closestROIs = []

    def getRoute(self):
        '''
        Returns list of route points in geocode
        '''
        # flip coords
        coords = [self.driver_point, self.end_point]
        flip_coords = [lst[::-1] for lst in coords]

        valhol = Valhalla()
        route = valhol.directions(locations=flip_coords, profile='auto')

        route_reversed = []
        for point in route.geometry:
            route_reversed.append(list(reversed(point)))

        return route_reversed

    def findClosestMarker(self, route):
        distances = []
        for marker in route:
            distances.append(haversine(marker, self.passenger_point, unit=Unit.METERS))

        idx = distances.index(min(distances))
        self.closest_marker_distance = min(distances)
        self.closest_marker_coords = route[idx]

        return self.closest_marker_coords

    def isInRange(self):
        if self.range > self.closest_marker_distance:
            return True
        else:
            return False

    def getNearestROIs(self):
        ors_client = Client(key='5b3ce3597851110001cf62482b47d9c527024ee38c455a63fc4f22ef')
        ROI_points = ors_client.pelias_reverse(list(reversed(self.closest_marker_coords))).get('features')
        for point in ROI_points:
            self.closestROIs.append(point.get('properties').get('label'))

        return self.closestROIs

    def prepareHTMLmap(self, route):
        map_center = [mean(x) for x in zip(self.driver_point, self.end_point)]
        m = folium.Map(location=list(map_center), zoom_start=13)

        # Label starting points
        folium.Marker(self.driver_point, icon=folium.Icon(color='red'),
                      tooltip="Driver starting point").add_to(m)
        folium.Marker(self.end_point, icon=folium.Icon(color='red'),
                      tooltip="Endpoint").add_to(m)

        # plot passenger
        folium.Marker(self.passenger_point, icon=folium.Icon(color='green'), tooltip='passenger starting point').add_to(m)
        folium.Circle(location=self.passenger_point, radius=self.range, fill_opacity=0.4, opacity=1,
                      fill_color='green', tooltip="passenger walking distance").add_to(m)

        # plot path
        folium.PolyLine(route, color='blue').add_to(m)
        folium.Marker(self.closest_marker_coords, icon=folium.Icon(color='black'),
                      tooltip=f"Suggested pickup point: {self.closestROIs[0]}", ).add_to(m)

        openMapForDebug('map.html', m)

@dataclass
class GeoDriverRoute:
    driver_id: str
    route_id: str
    latitude: float
    longitude: float
    office_latitude: float
    office_longitude: float


@dataclass
class GeoPassengerRoute:
    passenger_id: str
    route_id: str
    latitude: float
    longitude: float
    max_distance: float


if __name__ == "__main__":
    passenger_id = "b0e2eb8f-b2be-4266-947e-2757f21b62c3"
    engine = create_engine(POSTGRE_CONNECTION)
    session_maker = sessionmaker(engine)
    session = session_maker()
    passanger = [join_part for join_part in session.query(PassengerRouteEntity, RouteEntity).join(RouteEntity).filter(PassengerRouteEntity.id == passenger_id).first()]
    geo_passenger = GeoPassengerRoute(passenger_id=str(passanger[0].id),
                                      route_id=str(passanger[0].route_id),
                                      latitude=float(passanger[1].latitude),
                                      longitude=float(passanger[1].longitude),
                                      max_distance=passanger[0].max_distance)
    driver_routes = []
    for single_join in session.query(DriverRouteEntity, RouteEntity).join(RouteEntity).filter(RouteEntity.office_id == passanger[1].office.id).all():
        join = [join_part for join_part in single_join]
        geo_driver = GeoDriverRoute(driver_id=str(join[0].id),
                                       route_id=str(join[0].route_id),
                                       latitude=float(join[1].latitude),
                                       longitude=float(join[1].longitude),
                                       office_latitude=join[1].office.latitude,
                                       office_longitude=join[1].office.longitude)
        driver_routes.append(geo_driver)

    for driver_route in driver_routes:
        passenger_start = [float(geo_passenger.latitude),float(geo_passenger.longitude)]
        driver_start = [float(driver_route.latitude), float(driver_route.longitude)]
        range = geo_passenger.max_distance
        destination = [float(driver_route.office_latitude),float(driver_route.office_longitude)]
        router = PyRouter(passenger_start, range, driver_start, destination)
        car_path = router.getRoute()
        marker = router.findClosestMarker(car_path)

        if router.isInRange():
            router.getNearestROIs()
            router.prepareHTMLmap(car_path)

