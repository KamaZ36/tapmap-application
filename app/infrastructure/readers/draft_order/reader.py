from uuid import UUID
import orjson
from redis.asyncio import Redis

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.application.dtos.order import OrderDTO

from app.infrastructure.database.models.user import UserModel
from app.infrastructure.readers.draft_order.base import BaseDraftOrderReader
from app.infrastructure.readers.draft_order.converter import convert_order_to_dto


class DraftOrderReader(BaseDraftOrderReader):
    def __init__(self, redis: Redis, session: AsyncSession) -> None:
        self._redis = redis
        self._session = session

    def _make_order_key(self, order_id: UUID) -> str:
        return f"draft_order:{str(order_id)}"

    def _make_user_index_key(self, customer_id: UUID) -> str:
        return f"draft_order:user_id:{str(customer_id)}"

    async def get_by_id(self, order_id: UUID) -> OrderDTO | None:
        order_key = self._make_order_key(order_id)
        order_row = await self._redis.get(order_key)
        if order_row is None:
            return None
        order_data = orjson.loads(order_row)

        customer_model = await self._get_customer(order_data["customer_id"])
        if customer_model is None:
            return None

        return (
            convert_order_to_dto(order_row=order_data, user_model=customer_model)
            if order_row
            else None
        )

    async def get_by_customer_id(self, customer_id: UUID) -> OrderDTO | None:
        user_index_key = self._make_user_index_key(customer_id)
        order_id_raw = await self._redis.get(user_index_key)
        if not order_id_raw:
            return None
        try:
            # Декодируем bytes в строку и создаем UUID
            order_id = UUID(order_id_raw.decode("utf-8"))
            return await self.get_by_id(order_id)
        except (ValueError, AttributeError, UnicodeDecodeError):
            return None

    async def _get_customer(self, user_id: UUID) -> UserModel | None:
        query = select(UserModel).where(UserModel.id == user_id)
        result = await self._session.execute(query)
        user_model = result.scalar_one_or_none()
        return user_model
