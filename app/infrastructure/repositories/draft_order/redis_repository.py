from dataclasses import asdict
import json
from uuid import UUID
from redis.asyncio import Redis

from app.application.exceptions.draft_order import DraftOrderNotFound
from app.domain.entities.draft_order import DraftOrder
from app.domain.value_objects.coordinates import Coordinates
from app.domain.value_objects.money import Money
from app.domain.value_objects.order_comment import OrderComment
from app.domain.value_objects.point import Point
from app.infrastructure.repositories.draft_order.base import BaseDraftOrderRepository


class RedisDraftOrderRepository(BaseDraftOrderRepository):
    
    def __init__(self, redis: Redis) -> None:
        self.redis = redis
         
    def _make_key(self, customer_id: UUID) -> str:
        return f"draft_order_user_id:{str(customer_id)}"
         
    async def create(self, draft_order: DraftOrder) -> None:
        key = self._make_key(draft_order.customer_id)
        data = json.dumps(self.to_dict(draft_order))
        await self.redis.set(name=key, value=data, ex=3600)
    
    async def get_by_customer_id(self, customer_id: UUID) -> DraftOrder | None:
        key = self._make_key(customer_id)
        draft_order_data = await self.redis.get(key)
        return self.to_domain(draft_order_data) if draft_order_data else None
        
    async def update(self, draft_order: DraftOrder) -> None: 
        await self.create(draft_order=draft_order)
        
    async def delete(self, customer_id: UUID) -> None:
        await self.redis.delete(self._make_key(customer_id))
        
    def to_dict(self, draft_order: DraftOrder) -> dict:
        return {
            'id': str(draft_order.id),
            'customer_id': str(draft_order.customer_id),
            'city_id': str(draft_order.city_id),
            'points': [asdict(point) for point in draft_order.points],
            'price': str(draft_order.price.value),
            'travel_distance': draft_order.travel_distance,
            'travel_time': draft_order.travel_time,
            'comment': draft_order.comment.text if draft_order.comment else None
        }
        
    
    def to_domain(self, data: str) -> DraftOrder:
        raw = json.loads(data)
        return DraftOrder(
            id=UUID(raw["id"]),
            customer_id=UUID(raw["customer_id"]),
            city_id=UUID(raw["city_id"]),
            points=[Point(
                        address=p['address'],
                        coordinates=Coordinates(
                            latitude=float(p['coordinates']['latitude']),
                            longitude=float(p['coordinates']['longitude'])
                        )
                    ) for p in raw["points"]],
            price=Money(raw["price"]),
            travel_distance=raw["travel_distance"],
            travel_time=raw["travel_time"],
            comment=OrderComment(raw["comment"]) if raw.get("comment") else None
        )
    
    def _serialize(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
