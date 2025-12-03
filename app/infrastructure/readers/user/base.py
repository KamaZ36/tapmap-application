from uuid import UUID
from typing import Protocol

from app.application.dtos.user import UserDTO

from app.domain.value_objects.phone_number import PhoneNumber


class BaseUserReader(Protocol):
    async def get_by_id(self, user_id: UUID) -> UserDTO | None: ...

    async def get_by_phone_number(
        self, phone_number: PhoneNumber
    ) -> UserDTO | None: ...
