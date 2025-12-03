from dataclasses import dataclass
from uuid import UUID

from app.application.queries.base import Query, QueryHandler
from app.domain.value_objects.phone_number import PhoneNumber

from app.application.dtos.user import UserDTO
from app.application.exceptions.user import UserNotFound

from app.infrastructure.readers.user.base import BaseUserReader


@dataclass(frozen=True, eq=False)
class GetUserByPhoneQuery(Query):
    current_user_id: UUID
    phone_number: str


@dataclass(frozen=True, eq=False)
class GetUserByPhoneQueryHandler(QueryHandler[GetUserByPhoneQuery, UserDTO]):
    user_reader: BaseUserReader

    async def __call__(self, query: GetUserByPhoneQuery) -> UserDTO:
        phone_number = PhoneNumber(query.phone_number)

        user = await self.user_reader.get_by_phone_number(phone_number)
        if user is None:
            raise UserNotFound()
        return user
