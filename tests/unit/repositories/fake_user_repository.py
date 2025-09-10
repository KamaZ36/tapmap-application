from optparse import OptionParser
from typing import Optional
from uuid import UUID
from app.domain.entities.user import User
from app.domain.value_objects.phone_number import PhoneNumber
from app.infrastructure.repositories.user.base import BaseUserRepository


class FakeUserRepository(BaseUserRepository):
    def __init__(self):
        self._users: dict[UUID, User] = {}
        self._users_by_phone: dict[str, UUID] = {}

    async def create(self, user: User) -> None:
        self._users[user.id] = user
        self._users_by_phone[user.phone_number.value] = user.id

    async def get_by_id(self, user_id: UUID) -> User | None:
        return self._users.get(user_id)

    async def get_by_phone(self, phone_number: str) -> User | None:
        user_id = self._users_by_phone.get(phone_number)
        return self._users.get(user_id) if user_id else None

    async def update(self, user: User) -> None:
        self._users[user.id] = user
        self._users_by_phone[user.phone_number.value] = user.id
