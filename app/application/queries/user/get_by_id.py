from dataclasses import dataclass
from uuid import UUID

from app.application.dtos.user import UserDTO
from app.application.exceptions.user import UserNotFound

from app.application.queries.base import Query, QueryHandler
from app.infrastructure.readers.user.base import BaseUserReader


@dataclass(frozen=True, eq=False)
class GetUserByIdQuery(Query):
    user_id: UUID
    current_user_id: UUID


@dataclass
class GetUserByIdQueryHandler(QueryHandler[GetUserByIdQuery, UserDTO]):
    user_reader: BaseUserReader

    async def __call__(self, query: GetUserByIdQuery) -> UserDTO:
        user = await self.user_reader.get_by_id(query.user_id)
        if user is None:
            raise UserNotFound()
        return user
