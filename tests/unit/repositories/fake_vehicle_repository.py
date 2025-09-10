from uuid import UUID

from app.domain.entities.vehicle import Vehicle
from app.infrastructure.repositories.vehicle.base import BaseVehicleRepository


class FakeVehicleRepository(BaseVehicleRepository):
    def __init__(self) -> None:
        self._vehicles: dict[UUID, Vehicle] = {}
        self._vehicle_by_driver: dict[UUID, UUID] = {}

    async def create(self, vehicle: Vehicle) -> None:
        self._vehicles[vehicle.id] = vehicle
        self._vehicle_by_driver[vehicle.driver_id] = vehicle.id

    async def get_by_id(self, vehicle_id: UUID) -> Vehicle | None:
        vehicle = self._vehicles.get(vehicle_id, None)
        return vehicle

    async def get_by_driver_id(self, driver_id: UUID) -> Vehicle | None:
        vehicle_id = self._vehicle_by_driver.get(driver_id)
        return self._vehicles.get(vehicle_id, None)

    async def update(self, vehicle: Vehicle) -> None:
        self._vehicles[vehicle.id] = vehicle
        self._vehicle_by_driver[vehicle.driver_id] = vehicle.id
