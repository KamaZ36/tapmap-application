from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dtos.driver import DriverDTO
from app.infrastructure.database.models.driver import DriverModel
from app.infrastructure.readers.driver.base import BaseDriverReader
from app.infrastructure.readers.driver.converter import convert_driver_model_to_dto


class DriverReader(BaseDriverReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, driver_id: UUID) -> DriverDTO | None:
        query = select(DriverModel).where(DriverModel.id == driver_id)
        result = await self._session.execute(query)
        driver_model = result.scalar_one_or_none()
        return convert_driver_model_to_dto(driver_model) if driver_model else None
