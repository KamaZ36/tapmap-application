from typing import Protocol
from uuid import UUID

from app.domain.entities.user import User
from app.domain.value_objects.phone_number import PhoneNumber


class BaseUserRepository(Protocol): 

    async def create(self, user: User) -> None: ...

    async def get_by_id(self, user_id: UUID) -> User | None: ...
    
    async def get_by_phone(self, phone_number: str) -> User: ...
    
    async def update(self, user: User) -> None: ...
    