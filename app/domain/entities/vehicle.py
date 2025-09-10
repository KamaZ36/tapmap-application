from dataclasses import dataclass
from uuid import UUID

from app.domain.entities.base import Entity
from app.domain.value_objects.vehicle_number import VehicleNumber


@dataclass
class Vehicle(Entity):
    driver_id: UUID

    brand: str
    model: str
    color: str
    number: VehicleNumber

    def update_driver(self, driver_id: UUID) -> None:
        self.driver_id = driver_id

    def repaint(self, color: str) -> None:
        self.color = color

    def update_number(self, number: VehicleNumber) -> None:
        self.number = number

    def display_name(self) -> str:
        return f"{self.brand} {self.model} ({self.color} - {self.number.value})"
