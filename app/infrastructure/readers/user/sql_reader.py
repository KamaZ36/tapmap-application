from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select

from app.domain.value_objects.phone_number import PhoneNumber
from app.infrastructure.readers.user.converter import convert_user_to_dto
from app.utils import get_datetime_utc_now

from app.application.dtos.user import UserDTO

from app.infrastructure.database.models.user import BlockingUserModel, UserModel
from app.infrastructure.readers.user.base import BaseUserReader


class SQLUserReader(BaseUserReader):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, user_id: UUID) -> UserDTO | None:
        query = (
            select(UserModel, BlockingUserModel)
            .select_from(UserModel)
            .outerjoin(
                BlockingUserModel,
                and_(
                    UserModel.id == BlockingUserModel.user_id,
                    BlockingUserModel.is_active,
                    BlockingUserModel.expires_at > get_datetime_utc_now(),
                ),
            )
            .where(UserModel.id == user_id)
        )
        result = await self._session.execute(query)
        row = result.first()
        if row is None:
            return None
        user_model: UserModel = row[0]
        user_blocking_model: BlockingUserModel = row[1]

        return convert_user_to_dto(
            user_model=user_model, user_blocking_model=user_blocking_model
        )

    async def get_by_phone_number(self, phone_number: PhoneNumber) -> UserDTO | None:
        query = (
            select(UserModel, BlockingUserModel)
            .select_from(UserModel)
            .outerjoin(
                BlockingUserModel,
                and_(
                    UserModel.id == BlockingUserModel.user_id,
                    BlockingUserModel.is_active,
                    BlockingUserModel.expires_at > get_datetime_utc_now(),
                ),
            )
            .limit(1)
            .where(UserModel.phone_number == phone_number.value)
        )
        result = await self._session.execute(query)
        row = result.first()
        if row is None:
            return None
        user_model: UserModel = row[0]
        user_blocking_model: BlockingUserModel = row[1]

        return convert_user_to_dto(
            user_model=user_model, user_blocking_model=user_blocking_model
        )
