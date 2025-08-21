from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from geoalchemy2.shape import from_shape
from geoalchemy2.functions import ST_Contains

from shapely import Point as ShapelyPoint

from app.application.exceptions.city import CityNotFound
from app.domain.entities.city import City
from app.domain.value_objects.coordinates import Coordinates
from app.domain.value_objects.point import Point
from app.infrastructure.database.models.city import CityModel
from app.infrastructure.repositories.city.base import BaseCityRepository


class SQLAlchemyCityRepository(BaseCityRepository): 
    
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        
    async def create(self, city: City) -> None: 
        city_model = CityModel.to_model(city)
        self.session.add(city_model)

    async def get_by_id(self, city_id: UUID) -> City: 
        query = select(CityModel).where(CityModel.id == city_id)
        result = await self.session.execute(query)
        city_model: CityModel | None = result.scalar_one_or_none()
        if city_model is None:
            raise CityNotFound()
        return city_model.to_entity()
    
    async def get_by_into_point(self, coordinates: Coordinates) -> City | None: 
        shapely_point = ShapelyPoint(coordinates.longitude, coordinates.latitude)
        geo_point = from_shape(shapely_point, srid=4326)
        
        query = select(CityModel).where(
            ST_Contains(CityModel.polygon, geo_point)
        )
        result = await self.session.execute(query)
        city_model: CityModel | None = result.scalar_one_or_none()
        return city_model.to_entity() if city_model else None

    async def update(self, city: City) -> None: 
        stmt = (
            update(CityModel)
            .where(CityModel.id == city.id)
            .values(
                name=city.name, 
                state=city.state,
                base_price=city.base_price,
                price_per_kilometer=city.price_per_kilometer,
                service_commission_pct=city.service_commission_pct,
                polygon=city.polygon_coords
            )
        )
        await self.session.execute(stmt)
