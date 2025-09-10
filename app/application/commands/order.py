from dataclasses import dataclass
from uuid import UUID

from app.application.commands.base import BaseCommand


@dataclass(frozen=True)
class AddCommentToDraftOrderCommand(BaseCommand):
    comment: str


@dataclass(frozen=True)
class CreateDraftOrderCommand(BaseCommand):
    start_point: str | tuple[float, float]
    end_point: str | tuple[float, float]


@dataclass(frozen=True)
class AddPointToDraftOrderCommand(BaseCommand):
    point: str | tuple[float, float]


@dataclass(frozen=True)
class UpdateOrderStatusCommand(BaseCommand):
    order_id: UUID
