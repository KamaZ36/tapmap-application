from typing import Protocol
from uuid import UUID

from app.application.dtos.user import GetUsersFilters, UserBlockingDTO
from app.domain.entities.user import User
from app.domain.value_objects.phone_number import PhoneNumber


class BaseUserRepository(Protocol):
    async def create(self, user: User) -> None: ...

    async def get_by_id(self, user_id: UUID) -> User | None: ...

    async def try_get_by_id(self, user_id: UUID) -> User | None: ...

    async def get_by_phone(self, phone_number: PhoneNumber) -> User | None: ...

    async def get_filtered_users(self, filters: GetUsersFilters) -> list[User]: ...

    async def create_blocking_for_user(
        self, user_blocking: UserBlockingDTO
    ) -> None: ...

    async def get_active_blocking_for_user(
        self, user_id: UUID
    ) -> UserBlockingDTO | None: ...

    async def check_exist_active_blocking_user(self, user_id: UUID) -> bool: ...

    async def update(self, user: User) -> None: ...
