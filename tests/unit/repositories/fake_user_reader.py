from uuid import UUID
from app.application.dtos.user import UserDTO
from app.domain.entities.user import User
from app.domain.value_objects.phone_number import PhoneNumber
from app.infrastructure.readers.user.base import BaseUserReader


class FakeUserReader(BaseUserReader):
    def __init__(self, user_repository):
        self._user_repository = user_repository

    async def get_by_id(self, user_id: UUID) -> UserDTO | None:
        user = await self._user_repository.get_by_id(user_id)
        if user is None:
            return None
        return UserDTO.from_entity(user)

    async def get_by_phone_number(self, phone_number: PhoneNumber) -> UserDTO | None:
        user = await self._user_repository.get_by_phone(phone_number.value)
        if user is None:
            return None
        return UserDTO.from_entity(user)
