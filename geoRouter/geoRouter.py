import webbrowser
import folium
from routingpy import Valhalla
from openrouteservice.client import Client
from haversine import haversine, Unit
from statistics import mean
from math import inf

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


if __name__ == "__main__":

    # test :D
    destination = [52.23208696960101, 21.05542834618853]
    all_drivers_startpoints = [[52.21719277179523, 20.977368674875603]]
    passenger_start = [52.21015838034042, 21.02174343263609]
    range = 950

    for driver_start in all_drivers_startpoints:
        router = PyRouter(passenger_start, range, driver_start, destination)
        car_path = router.getRoute()
        marker = router.findClosestMarker(car_path)

        if router.isInRange():
            router.getNearestROIs()
            router.prepareHTMLmap(car_path)

