from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import ForeignKey, String

from app.domain.entities.user import User, UserRole
from app.domain.value_objects.phone_number import PhoneNumber

from app.infrastructure.database.models.base import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, unique=True
    )

    name: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False, unique=True)

    completed_orders_count: Mapped[int] = mapped_column(nullable=False)
    cancelled_orders_count: Mapped[int] = mapped_column(nullable=False)

    roles: Mapped[list[UserRole]] = mapped_column(ARRAY(String), nullable=False)

    base_city_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("cities.id"),
        nullable=True,
    )

    @classmethod
    def from_entity(cls, user: User) -> "UserModel":
        return cls(
            id=user.id,
            name=user.name,
            phone_number=user.phone_number.value,
            completed_orders_count=user.completed_orders_count,
            cancelled_orders_count=user.cancelled_orders_count,
            roles=[role.value for role in user.roles],
            base_city_id=user.base_city_id,
        )

    def to_entity(self) -> User:
        return User(
            id=self.id,
            name=self.name,
            phone_number=PhoneNumber(self.phone_number),
            completed_orders_count=self.completed_orders_count,
            cancelled_orders_count=self.cancelled_orders_count,
            roles=[UserRole(role) for role in self.roles],
            base_city_id=self.base_city_id,
        )
