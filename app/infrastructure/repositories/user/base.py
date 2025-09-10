from typing import Protocol
from uuid import UUID

from app.application.dtos.user import GetUsersFilters
from app.domain.entities.user import User
from app.domain.value_objects.phone_number import PhoneNumber


class BaseUserRepository(Protocol):
    async def create(self, user: User) -> None: ...

    async def get_by_id(self, user_id: UUID) -> User | None: ...

    async def try_get_by_id(self, user_id: UUID) -> User | None: ...

    async def get_by_phone(self, phone_number: str) -> User | None: ...

    async def get_filtered_users(self, filters: GetUsersFilters) -> list[User]: ...

    async def update(self, user: User) -> None: ...
