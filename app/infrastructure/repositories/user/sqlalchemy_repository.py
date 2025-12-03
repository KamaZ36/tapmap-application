from uuid import UUID

from sqlalchemy import ScalarResult, and_, between, exists, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.value_objects.phone_number import PhoneNumber
from app.domain.entities.user import User

from app.application.exceptions.user import UserNotFound
from app.application.dtos.user import GetUsersFilters, UserBlockingDTO

from app.infrastructure.database.models.user import BlockingUserModel, UserModel
from app.infrastructure.repositories.user.base import BaseUserRepository


class SQLAlchemyUserRepository(BaseUserRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, user: User) -> None:
        user_model = UserModel.from_entity(user)
        self._session.add(user_model)

    async def get_by_id(self, user_id: UUID) -> User | None:
        query = select(UserModel).where(UserModel.id == user_id)
        result = await self._session.execute(query)
        user_model = result.scalar_one_or_none()
        return user_model.to_entity() if user_model else None

    async def try_get_by_id(self, user_id: UUID) -> User | None:
        user = await self.get_by_id(user_id)
        if user is None:
            raise UserNotFound()
        return user

    async def get_by_phone(self, phone_number: PhoneNumber) -> User | None:
        query = select(UserModel).where(UserModel.phone_number == phone_number.value)
        result = await self._session.execute(query)
        user_model = result.scalar_one_or_none()
        return user_model.to_entity() if user_model else None

    async def get_filtered_users(self, filters: GetUsersFilters) -> list[User]:
        query = select(User)

        conditions = []

        for field in ["phone_number"]:
            if value := getattr(filters, field):
                conditions.append(getattr(UserModel, field) == value)

        range_filters = {
            "completed_orders": ("completed_orders_min", "completed_orders_max"),
            "cancelled_orders": ("cancelled_orders_min", "cancelled_orders_max"),
        }

        for field, (min_attr, max_attr) in range_filters.items():
            min_val = getattr(filters, min_attr)
            max_val = getattr(filters, max_attr)

            if min_val is not None and max_val is not None:
                conditions.append(between(getattr(UserModel, field), min_val, max_val))
            elif min_val is not None:
                conditions.append(getattr(UserModel, field) >= min_val)
            elif max_val is not None:
                conditions.append(getattr(UserModel, field) <= max_val)

        if conditions:
            query = query.where(and_(*conditions))

        if filters.limit:
            query = query.limit(filters.limit)
        if filters.offset:
            query = query.offset(filters.offset)

        result = await self._session.execute(query)
        user_models: ScalarResult[UserModel] | None = result.scalars()
        users = [user for user in user_models]
        return users

    async def create_blocking_for_user(self, user_blocking: UserBlockingDTO) -> None:
        user_blocking_model = BlockingUserModel.from_dto(user_blocking)
        self._session.add(user_blocking_model)

    async def get_active_blocking_for_user(
        self, user_id: UUID
    ) -> UserBlockingDTO | None:
        query = (
            select(BlockingUserModel)
            .where(
                BlockingUserModel.user_id == user_id,
                BlockingUserModel.expires_at > func.now(),
            )
            .limit(1)
        )
        result = await self._session.execute(query)
        user_blocking_model = result.scalar_one_or_none()
        return user_blocking_model.to_dto() if user_blocking_model else None

    async def check_exist_active_blocking_user(self, user_id: UUID) -> bool:
        stmt = select(
            exists().where(
                BlockingUserModel.user_id == user_id,
                BlockingUserModel.expires_at > func.now(),
            )
        )
        result = await self._session.scalar(stmt)
        return result or False

    async def update(self, user: User) -> None:
        stmt = (
            update(UserModel)
            .where(UserModel.id == user.id)
            .values(
                name=user.name,
                phone_number=user.phone_number.value,
                completed_orders_count=user.completed_orders_count,
                cancelled_orders_count=user.cancelled_orders_count,
                roles=[role.value for role in user.roles],
                base_city_id=user.base_city_id,
            )
            .execution_options(synchronize_session="fetch")
        )
        await self._session.execute(stmt)
