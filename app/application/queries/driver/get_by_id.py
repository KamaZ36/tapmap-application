from dataclasses import dataclass
from uuid import UUID

from app.application.dtos.driver import DriverDTO
from app.application.exceptions.driver import DriverNotFound

from app.application.queries.base import Query, QueryHandler
from app.infrastructure.readers.driver.base import BaseDriverReader


@dataclass(frozen=True, eq=False)
class GetDriverByIdQuery(Query):
    current_user_id: UUID
    driver_id: UUID


@dataclass
class GetDriverByIdQueryHandler(QueryHandler[GetDriverByIdQuery, DriverDTO]):
    driver_reader: BaseDriverReader

    async def __call__(self, query: GetDriverByIdQuery) -> DriverDTO:
        driver = await self.driver_reader.get_by_id(query.driver_id)
        if driver is None:
            raise DriverNotFound()

        return driver
