from uuid import UUID

from shapely import Polygon
from shapely import Point as SH_Point

from app.domain.entities.city import City
from app.domain.value_objects.coordinates import Coordinates
from app.infrastructure.repositories.city.base import BaseCityRepository


class FakeCityRepository(BaseCityRepository):
    
    def __init__(self) -> None:
        self._cities: dict[UUID, City]
        self._polygons: dict[UUID, Polygon]
    
    async def create(self, city: City) -> None:
        self._cities[city.id] = city
        self._polygons[city.id] = city.polygon
        
    async def get_by_id(self, city_id: UUID) -> City | None:
        city = self._cities.get(city_id, None)
        return city
    
    async def get_by_into_point(self, coordinates: Coordinates) -> City | None:
        sh_point = SH_Point(coordinates.longitude, coordinates.latitude)
        
        for city_id, polygon in self._polygons.items():
            if polygon.contains(sh_point):
                return self._cities[city_id]
        return None
        
    async def update(self, city: City) -> None:
        self._cities[city.id] = city
        self._polygons[city.id] = city.polygon
        