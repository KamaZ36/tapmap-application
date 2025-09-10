from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import ForeignKey

from app.domain.entities.vehicle import Vehicle
from app.domain.value_objects.vehicle_number import VehicleNumber

from app.infrastructure.database.models.base import BaseModel


class VehicleModel(BaseModel):
    __tablename__ = "vehicles"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, unique=True
    )

    driver_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), ForeignKey("drivers.id"), nullable=False
    )

    brand: Mapped[str] = mapped_column(nullable=False)
    model: Mapped[str] = mapped_column(nullable=False)
    color: Mapped[str] = mapped_column(nullable=False)
    number: Mapped[str] = mapped_column(nullable=False, unique=True)

    @classmethod
    def from_entity(cls, vehicle: Vehicle) -> "VehicleModel":
        return cls(
            id=vehicle.id,
            driver_id=vehicle.driver_id,
            brand=vehicle.brand,
            model=vehicle.model,
            color=vehicle.color,
            number=vehicle.number.value,
        )

    def to_entity(self) -> Vehicle:
        return Vehicle(
            id=self.id,
            driver_id=self.driver_id,
            brand=self.brand,
            model=self.model,
            color=self.color,
            number=VehicleNumber(self.number),
        )
