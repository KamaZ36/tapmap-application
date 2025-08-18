from math import radians, cos, sin, atan2, sqrt

from app.domain.entities.city import City
from app.domain.value_objects.coordinates import Coordinates
from app.domain.value_objects.point import Point
from app.presentation.api.v1.schemas.location import RouteInfoSchema
from app.services.geocoder.base import BaseGeocoder
from app.services.router.base import BaseRouter


class GeolocationService:

    def __init__(self, geocoder: BaseGeocoder, router: BaseRouter):
        self.geocoder = geocoder
        self.router = router

    @staticmethod
    def calculating_time_route(distance: int) -> int:
        """Рассчитать время поездки по расстоянию (50 км/ч в среднем)"""
        return int(round((float(distance) / 1000) / 50 * 60 + 2))

    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Рассчитать геодезическое расстояние между точками (метры)"""
        earth_radius = 6371000  # Радиус Земли в метрах
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return earth_radius * c

    async def resolve_location(
            self,
            location: str | tuple[float, float],
            city: City
    ) -> Point:
        if isinstance(location, str):
            query = f"Россия, {city.state}, {city.name}, {location}"
            data = await self.geocoder.get_coordinates(address=query)
        elif isinstance(location, tuple):
            data = await self.geocoder.get_address(latitude=location[0], longitude=location[1])
        else:
            raise ValueError("Нужно передать или адрес, или координаты.")
        return Point(
            address=data.get("address"),
            coordinates=Coordinates(**data.get('coordinates')),
        )

    async def get_route_details(self, coordinates_list: list[Coordinates]) -> RouteInfoSchema:
        travel_distance = await self.router.get_distance_route(coordinates_list)
        travel_time = self.calculating_time_route(distance=travel_distance)
        return RouteInfoSchema(
            travel_distance=travel_distance,
            travel_time=travel_time
        )
        