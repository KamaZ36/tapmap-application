from uuid import UUID

from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from geoalchemy2.functions import ST_Distance
from geoalchemy2.shape import from_shape

from shapely import Point as SH_Point

from app.domain.entities.driver import Driver
from app.domain.value_objects.coordinates import Coordinates
from app.domain.value_objects.phone_number import PhoneNumber

from app.application.exceptions.driver import DriverNotFound

from app.infrastructure.database.models.driver import DriverModel
from app.infrastructure.repositories.driver.base import BaseDriverRepository


class SQLAlchemyDriverRepository(BaseDriverRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, driver: Driver) -> None:
        driver_model = DriverModel.from_entity(driver)
        self.session.add(driver_model)

    async def get_by_id(self, driver_id: UUID) -> Driver | None:
        query = select(DriverModel).where(DriverModel.id == driver_id)
        result = await self.session.execute(query)
        driver_model = result.scalar_one_or_none()
        return driver_model.to_entity() if driver_model else None

    async def try_get_by_id(self, driver_id: UUID) -> Driver | None:
        driver = await self.get_by_id(driver_id)
        if driver is None:
            raise DriverNotFound()
        return driver

    async def get_by_phone(self, phone_number: PhoneNumber) -> Driver:
        query = select(DriverModel).where(
            DriverModel.phone_number == phone_number.value
        )
        result = await self.session.execute(query)
        driver_model: DriverModel | None = result.scalar_one_or_none()
        if driver_model is None:
            raise DriverNotFound()
        return driver_model.to_entity()

    async def get_nearest_free(self, coordinates: Coordinates) -> Driver | None:
        """Получение ближайшего водителя к заданной точке"""

        order_start_point = func.ST_SetSRID(
            func.ST_MakePoint(coordinates.longitude, coordinates.latitude), 4326
        )
        query = (
            select(DriverModel)
            .filter(
                DriverModel.on_order == False,
                DriverModel.on_shift == True,
                DriverModel.last_location.is_not(None),
            )
            .order_by(ST_Distance(DriverModel.last_location, order_start_point))
            .limit(1)
            .with_for_update(skip_locked=True, of=DriverModel)
        )

        response = await self.session.execute(query)
        driver_model: DriverModel | None = response.scalar_one_or_none()
        return driver_model.to_entity() if driver_model else None

    async def update(self, driver: Driver) -> None:
        location = None
        if driver.last_location:
            sh_point = SH_Point(
                driver.last_location.latitude, driver.last_location.longitude
            )
            location = from_shape(sh_point, srid=4326)

        stmt = (
            update(DriverModel)
            .where(DriverModel.id == driver.id)
            .values(
                phone_number=driver.phone_number.value,
                completed_orders_count=driver.completed_orders_count,
                cancelled_orders_count=driver.cancelled_orders_count,
                last_location=location,
                on_order=driver.on_order,
                on_shift=driver.on_shift,
            )
        )
        await self.session.execute(stmt)
