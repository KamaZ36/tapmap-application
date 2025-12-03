from datetime import datetime
import orjson

from dataclasses import asdict
from uuid import UUID
from redis.asyncio import Redis

from app.domain.entities.order import Order
from app.domain.enums.order_status import OrderStatus
from app.domain.value_objects.coordinates import Coordinates
from app.domain.value_objects.money import Money
from app.domain.value_objects.order_comment import OrderComment
from app.domain.value_objects.order_point import OrderPoint

from app.infrastructure.repositories.draft_order.base import BaseDraftOrderRepository


class RedisDraftOrderRepository(BaseDraftOrderRepository):
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    def _make_order_key(self, order_id: UUID) -> str:
        return f"draft_order:{str(order_id)}"

    def _make_user_index_key(self, user_id: UUID) -> str:
        return f"draft_order:user_id:{str(user_id)}"

    async def create(self, order: Order) -> None:
        order_key = self._make_order_key(order.id)
        user_index_key = self._make_user_index_key(order.customer_id)
        order_row = orjson.dumps(self._to_dict(order))
        async with self._redis.pipeline() as pipe:
            await pipe.setex(name=order_key, time=1800, value=order_row)
            await pipe.setex(name=user_index_key, time=1800, value=str(order.id))
            await pipe.execute()

    async def get_by_id(self, order_id: UUID) -> Order | None:
        order_key = self._make_order_key(order_id)
        order_row = await self._redis.get(order_key)
        return self._to_domain(order_row) if order_row else None

    async def get_by_customer_id(self, user_id: UUID) -> Order | None:
        user_index_key = self._make_user_index_key(user_id)
        order_id_row = await self._redis.get(user_index_key)
        if not order_id_row:
            return None
        try:
            # Декодируем bytes в строку и создаем UUID
            order_id = UUID(order_id_row.decode("utf-8"))
            return await self.get_by_id(order_id)
        except (ValueError, AttributeError, UnicodeDecodeError):
            return None

    async def update(self, order: Order) -> None:
        await self.create(order)

    async def delete(self, order_id: UUID) -> None:
        order = await self.get_by_id(order_id)
        if order:
            order_key = self._make_order_key(order.id)
            user_index_key = self._make_user_index_key(order.customer_id)
            async with self._redis.pipeline() as pipe:
                await pipe.delete(order_key)
                await pipe.delete(user_index_key)
                await pipe.execute()

    def _to_dict(self, order: Order) -> dict:
        return {
            "id": str(order.id),
            "customer_id": str(order.customer_id),
            "city_id": str(order.city_id),
            "points": [asdict(point) for point in order.points],
            "price": str(order.price.value) if order.price else None,
            "service_commission": str(order.service_commission.value)
            if order.service_commission
            else None,
            "status": order.status.value,
            "travel_time": order.travel_time if order.travel_time else None,
            "travel_distance": order.travel_distance if order.travel_distance else None,
            "comment": order.comment.text if order.comment else None,
            "created_at": order.created_at.isoformat(),
        }

    def _to_domain(self, data: bytes) -> Order:
        row = orjson.loads(data)

        # Безопасное создание Money объектов
        price = None
        if row.get("price") and row["price"] != "None":
            try:
                price = Money(row["price"])
            except (ValueError, TypeError):
                price = None

        service_commission = None
        if row.get("service_commission") and row["service_commission"] != "None":
            try:
                service_commission = Money(row["service_commission"])
            except (ValueError, TypeError):
                service_commission = None

        return Order(
            id=UUID(row["id"]),
            customer_id=UUID(row["customer_id"]),
            city_id=UUID(row["city_id"]),
            points=[
                OrderPoint(
                    address=p["address"],
                    coordinates=Coordinates(
                        latitude=float(p["coordinates"]["latitude"]),
                        longitude=float(p["coordinates"]["longitude"]),
                    ),
                )
                for p in row["points"]
            ],
            service_commission=service_commission,
            price=price,
            status=OrderStatus(row["status"]),
            travel_distance=row["travel_distance"],
            travel_time=row["travel_time"],
            comment=OrderComment(row["comment"]) if row.get("comment") else None,
            created_at=datetime.fromisoformat(row["created_at"]),
        )
