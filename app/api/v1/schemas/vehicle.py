from uuid import UUID
from pydantic import BaseModel

from app.domain.entities.vehicle import Vehicle


class CreateVehicleSchema(BaseModel):
    driver_id: UUID
    brand: str
    model: str
    color: str
    number: str


class ResponseVehicleSchema(BaseModel):
    id: UUID
    driver_id: UUID
    brand: str
    model: str
    color: str
    number: str

    @classmethod
    def from_domain(cls, vehicle: Vehicle) -> "ResponseVehicleSchema":
        return cls(
            id=vehicle.id,
            driver_id=vehicle.driver_id,
            brand=vehicle.brand,
            model=vehicle.model,
            color=vehicle.color,
            number=vehicle.number.value,
        )


class ResponseVehicleForOrder(BaseModel):
    id: UUID
    brand: str
    model: str
    color: str
    number: str

    @classmethod
    def from_domain(cls, vehicle: Vehicle) -> "ResponseVehicleForOrder":
        return cls(
            id=vehicle.id,
            brand=vehicle.brand,
            model=vehicle.model,
            color=vehicle.color,
            number=vehicle.number.value,
        )
