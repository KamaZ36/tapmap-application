from dataclasses import dataclass
from math import radians, cos, sin, atan2, sqrt

from app.domain.entities.city import City
from app.domain.value_objects.coordinates import Coordinates
from app.domain.value_objects.order_point import OrderPoint

from app.application.exceptions.draft_order import InvalidLocation
from app.application.dtos.location import RouteInfoDTO

from app.infrastructure.exceptions.geocoder import IncorrectGeolocation, GeocodingFailed
from app.infrastructure.services.geocoder.base import BaseGeocoder
from app.infrastructure.services.router.base import BaseRouter


@dataclass
class GeolocationService:
    geocoder: BaseGeocoder
    router: BaseRouter

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
        self, location: str | tuple[float, float], city: City | None = None
    ) -> OrderPoint:
        try:
            if isinstance(location, str) and city:
                query = f"Россия, {city.state}, {city.name}, {location}"
                data = await self.geocoder.get_coordinates(address=query)
            elif isinstance(location, tuple):
                data = await self.geocoder.get_address(
                    latitude=location[1], longitude=location[0]
                )
            else:
                raise TypeError()
        except (IncorrectGeolocation, GeocodingFailed):
            raise InvalidLocation(location=location)
        return OrderPoint(
            address=data.get("address"),
            coordinates=Coordinates(
                latitude=data["coordinates"]["latitude"],
                longitude=data["coordinates"]["longitude"],
            ),
        )

    async def get_route_details(
        self, coordinates_list: list[Coordinates]
    ) -> RouteInfoDTO:
        travel_distance = await self.router.get_distance_route(coordinates_list)
        travel_time = self.calculating_time_route(distance=travel_distance)
        return RouteInfoDTO(travel_distance=travel_distance, travel_time=travel_time)
