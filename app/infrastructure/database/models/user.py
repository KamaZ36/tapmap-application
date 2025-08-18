from uuid import UUID

from app.domain.entities.user import User, UserRole
from app.domain.value_objects.phone_number import PhoneNumber
from app.infrastructure.database.models.base import BaseModel

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import ForeignKey, String


class UserModel(BaseModel): 
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, unique=True)

    name: Mapped[str] = mapped_column(unique=False)
    phone_number: Mapped[str] = mapped_column(unique=False)
    
    completed_orders_count: Mapped[int] = mapped_column(unique=False)
    cancelled_orders_count: Mapped[int] = mapped_column(unique=False)
    
    roles: Mapped[list[UserRole]] = mapped_column(ARRAY(String), nullable=False)
    
    base_city_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), 
        ForeignKey('cities.id'), 
        unique=False,
        nullable=True,
        server_default=None,
        default=None
    )
    
    city: Mapped["CityModel"] = relationship('CityModel')
    
    
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
