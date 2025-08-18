from uuid import UUID
from fastapi import APIRouter

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from app.application.commands.vehicle import CreateVehcielCommand
from app.application.interactions.vehicle.create_vehicle import CreateVehicleInteraction
from app.application.interactions.vehicle.get_vehicle import GetVehicleInteraction

from app.presentation.api.dependencies import CurrentUserDep
from app.presentation.api.v1.schemas.vehicle import CreateVehicleSchema, ResponseVehicleSchema


router = APIRouter(route_class=DishkaRoute)


@router.post(
    '',
    summary="Добавить автомобиль для водителя (Только администраторам)"
)
async def create_vehicle(
    current_user: CurrentUserDep,
    data: CreateVehicleSchema,
    interactor: FromDishka[CreateVehicleInteraction]
) -> ResponseVehicleSchema:
    command = CreateVehcielCommand(**data.model_dump())
    vehicle = await interactor(command=command, current_user=current_user)
    return ResponseVehicleSchema.from_domain(vehicle)

@router.get(
    '/{vehicle_id}',
    summary="Получить автомобиль по ID"
)
async def get_vehicle(
    vehicle_id: UUID,
    current_user: CurrentUserDep,
    interactor: FromDishka[GetVehicleInteraction]
) -> ResponseVehicleSchema:
    vehicle = await interactor(vehicle_id=vehicle_id, current_user=current_user)
    return ResponseVehicleSchema.from_domain(vehicle)
