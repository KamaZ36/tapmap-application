from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ARRAY, ENUM
from sqlalchemy import ForeignKey, String

from app.domain.entities.blocking_user import BlockingUser
from app.domain.entities.user import User, UserRole
from app.domain.enums.user import UserStatus
from app.domain.value_objects.phone_number import PhoneNumber

from app.infrastructure.database.models.base import (
    BaseModel,
    CreatedAtMixin,
    UpdatedAtMixin,
)


class UserModel(BaseModel, CreatedAtMixin, UpdatedAtMixin):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, unique=True
    )

    name: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(nullable=False, unique=True)

    completed_orders_count: Mapped[int] = mapped_column(nullable=False)
    cancelled_orders_count: Mapped[int] = mapped_column(nullable=False)

    status: Mapped[UserStatus] = mapped_column(
        ENUM(UserStatus, name="user_status"),
        nullable=False,
        server_default=UserStatus.active.value,
        default=UserStatus.active,
    )

    roles: Mapped[list[UserRole]] = mapped_column(ARRAY(String), nullable=False)

    base_city_id: Mapped[UUID] = mapped_column(ForeignKey("cities.id"), nullable=True)

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


class BlockingUserModel(BaseModel, CreatedAtMixin):
    __tablename__ = "users_blockings"

    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    reason: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(
        nullable=False, default=True, server_default="True"
    )
    expires_at: Mapped[datetime] = mapped_column(nullable=False)

    @classmethod
    def from_entity(cls, blocking_user: BlockingUser) -> "BlockingUserModel":
        return cls(
            id=blocking_user.id,
            user_id=blocking_user.user_id,
            reason=blocking_user.reason,
            is_active=blocking_user.is_active,
            expires_at=blocking_user.expires_at,
        )

    def to_entity(self) -> BlockingUser:
        return BlockingUser(
            id=self.id,
            user_id=self.user_id,
            reason=self.reason,
            is_active=self.is_active,
            expires_at=self.expires_at,
            created_at=self.created_at,
        )
