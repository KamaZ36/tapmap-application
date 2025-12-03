from dataclasses import asdict
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ENUM, JSON
from sqlalchemy import ForeignKey, DECIMAL

from app.domain.entities.order import Order, OrderStatus
from app.domain.value_objects.coordinates import Coordinates
from app.domain.value_objects.money import Money
from app.domain.value_objects.order_comment import OrderComment
from app.domain.value_objects.order_point import OrderPoint

from app.infrastructure.database.models.base import (
    BaseModel,
    CreatedAtMixin,
    UpdatedAtMixin,
)
from app.infrastructure.database.models.driver import DriverModel
from app.infrastructure.database.models.user import UserModel


class OrderModel(BaseModel, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "orders"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, unique=True
    )

    customer_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
    )
    driver_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("drivers.id"),
        nullable=True,
        default=None,
        server_default=None,
    )
    city_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("cities.id"), nullable=False
    )

    points: Mapped[list[dict]] = mapped_column(JSON, nullable=False)
    status: Mapped[OrderStatus] = mapped_column(
        ENUM(OrderStatus, name="order_status"),
        nullable=False,
        server_default=OrderStatus.draft.value,
        default=OrderStatus.draft,
    )

    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=True)
    service_commission: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    travel_distance: Mapped[int] = mapped_column(nullable=False)
    travel_time: Mapped[int] = mapped_column(nullable=False)

    feeding_distance: Mapped[int] = mapped_column(nullable=True)
    feeding_time: Mapped[int] = mapped_column(nullable=True)

    comment: Mapped[str] = mapped_column(nullable=True)

    driver: Mapped[DriverModel] = relationship(
        DriverModel,
        foreign_keys=[driver_id],
    )
    customer: Mapped[UserModel] = relationship(UserModel, foreign_keys=[customer_id])

    @classmethod
    def from_entity(cls, order: Order) -> "OrderModel":
        return cls(
            id=order.id,
            customer_id=order.customer_id,
            driver_id=order.driver_id,
            city_id=order.city_id,
            points=[asdict(point) for point in order.points],
            status=order.status,
            price=order.price.value,
            service_commission=order.service_commission.value,
            travel_distance=order.travel_distance,
            travel_time=order.travel_time,
            feeding_distance=order.feeding_distance,
            feeding_time=order.feeding_time,
            comment=order.comment.text if order.comment else None,
            created_at=order.created_at,
        )

    def to_entity(self) -> Order:
        return Order(
            id=self.id,
            created_at=self.created_at,
            customer_id=self.customer_id,
            driver_id=self.driver_id,
            city_id=self.city_id,
            points=[
                OrderPoint(
                    address=point["address"],
                    coordinates=Coordinates(
                        latitude=point["coordinates"]["latitude"],
                        longitude=point["coordinates"]["longitude"],
                    ),
                )
                for point in self.points
            ],
            status=OrderStatus(self.status),
            price=Money(Decimal(self.price)),
            service_commission=Money(Decimal(self.service_commission)),
            travel_distance=self.travel_distance,
            travel_time=self.travel_time,
            feeding_distance=self.feeding_distance,
            feeding_time=self.feeding_time,
            comment=OrderComment(self.comment) if self.comment else None,
        )
