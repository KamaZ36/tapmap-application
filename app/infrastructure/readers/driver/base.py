from typing import Protocol
from uuid import UUID

from app.application.dtos.driver import DriverDTO


class BaseDriverReader(Protocol):
    async def get_by_id(self, driver_id: UUID) -> DriverDTO | None: ...
