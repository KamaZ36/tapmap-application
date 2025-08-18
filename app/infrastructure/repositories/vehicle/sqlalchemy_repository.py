from uuid import UUID
from sqlalchemy import ScalarResult, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.entities.vehicle import Vehicle
from app.infrastructure.database.models.vehicles import VehicleModel
from app.infrastructure.repositories.vehicle.base import BaseVehicleRepository


class SQLAlhcemyVehicleRepository(BaseVehicleRepository): 
    
    def __init__(self, session: AsyncSession) -> None: 
        self.session = session
    
    async def create(self, vehicle: Vehicle) -> None: 
        new_vehicle = VehicleModel.create(vehicle)
        self.session.add(new_vehicle)
    
    async def get_by_id(self, vehicle_id: UUID) -> Vehicle | None:
        query = select(VehicleModel).where(VehicleModel.id == vehicle_id)
        result = await self.session.execute(query)
        vehicle_model: VehicleModel | None = result.scalar_one_or_none()
        return vehicle_model.to_entity() if vehicle_model else None
    
    async def get_by_driver_id(self, driver_id: UUID) -> Vehicle | None:
        query = select(VehicleModel).where(VehicleModel.driver_id == driver_id)
        result = await self.session.execute(query)
        vehicle_model = result.scalar_one_or_none()
        # vehicle_models: ScalarResult[VehicleModel] | None = result.scalars()
        # vehicles = [vehicle_model.to_entity() for vehicle_model in vehicle_models]
        return vehicle_model.to_entity() if vehicle_model else None

    async def update(self, vehicle: Vehicle) -> None:
        stmt = (
            update(VehicleModel)
            .where(VehicleModel.id == vehicle.id)
            .values(
                driver_id=vehicle.driver_id,
                brand=vehicle.brand,
                model=vehicle.model,
                color=vehicle.color,
                number=vehicle.number.value
            )
        )
        await self.session.execute(stmt)
