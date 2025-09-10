from dataclasses import asdict
from datetime import datetime
from decimal import Decimal
from typing import Any
from uuid import UUID
from pydantic import BaseModel

from app.domain.entities.draft_order import DraftOrder


class CreateDraftOrderSchema(BaseModel):
    start_point: str | tuple[float, float]
    end_point: str | tuple[float, float]


class AddPointToDraftOrderSchema(BaseModel):
    point: str | tuple[float, float]


class AddCommentSchema(BaseModel):
    comment: str


class ResponseDraftOrderSchema(BaseModel):
    id: UUID
    customer_id: UUID
    city_id: UUID
    points: list[dict[str, Any]]
    price: Decimal
    travel_distance: int
    travel_time: int
    comment: str | None = None
    created_at: datetime

    @classmethod
    def from_domain(cls, draft_order: DraftOrder) -> "ResponseDraftOrderSchema":
        return cls(
            id=draft_order.id,
            customer_id=draft_order.customer_id,
            city_id=draft_order.city_id,
            points=[asdict(point) for point in draft_order.points],
            price=draft_order.price.value,
            travel_distance=draft_order.travel_distance,
            travel_time=draft_order.travel_time,
            comment=draft_order.comment.text if draft_order.comment else None,
            created_at=draft_order.created_at,
        )
