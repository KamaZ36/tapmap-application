from dataclasses import asdict
from uuid import UUID

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.application.commands.user import SetBaseUserLocationCommand
from app.presentation.api.dependencies import CurrentUserDep

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from app.application.commands.driver import CreateDriverCommand

from app.application.interactions.driver.get_last_location import (
    GetLastLocationDriverInteraction,
)
from app.application.interactions.order.get_orders import GetOrdersInteraction
from app.application.interactions.vehicle.get_vehicles import GetVehiclesInteraction
from app.application.interactions.driver.create_driver import CreateDriverInteraction
from app.application.interactions.driver.get_active_order import (
    GetActiveOrderForDriverInteraction,
)
from app.application.interactions.driver.get_driver import GetDriverInteraction
from app.application.interactions.driver.switch_on_shift import (
    SwitchDriverOnShiftInteraction,
)
from app.application.interactions.driver.update_location import (
    UpdateLocationInteraction,
)

from app.presentation.api.v1.schemas.driver import (
    CreateDriverSchema,
    ResponseDriverSchema,
    UpdateDriverLocationSchema,
)
from app.presentation.api.v1.schemas.location import CoordinatesSchema
from app.presentation.api.v1.schemas.order import (
    GetOrderSFiltersSchema,
    ResponseExtendedOrderSchema,
    ResponseOrderSchema,
)
from app.presentation.api.v1.schemas.vehicle import ResponseVehicleSchema


router = APIRouter(route_class=DishkaRoute)


@router.post("", summary="Создать водителя (Только администраторам)")
async def register_driver(
    current_user: CurrentUserDep,
    data: CreateDriverSchema,
    interactor: FromDishka[CreateDriverInteraction],
) -> ResponseDriverSchema:
    command = CreateDriverCommand(**data.model_dump())
    driver = await interactor(command=command, current_user=current_user)
    return ResponseDriverSchema.from_domain(driver)


@router.get("/me", summary="Получить профиль текущего водителя")
async def get_driver_me(
    current_user: CurrentUserDep, interactor: FromDishka[GetDriverInteraction]
) -> ResponseDriverSchema:
    driver = await interactor(current_user=current_user, driver_id=current_user.user_id)
    return ResponseDriverSchema.from_domain(driver)


@router.get("/me/orders/active", summary="Получить активный заказ текущего водителя")
async def get_active_order_for_driver(
    current_user: CurrentUserDep,
    interactor: FromDishka[GetActiveOrderForDriverInteraction],
) -> ResponseExtendedOrderSchema:
    extended_order = await interactor(current_user=current_user)
    return ResponseExtendedOrderSchema.from_domain(extended_order)


@router.get("/me/vehicles")
async def get_driver_vehicles(
    current_user: CurrentUserDep, interactor: FromDishka[GetVehiclesInteraction]
) -> list[ResponseVehicleSchema]:
    vehicles = await interactor(
        driver_id=current_user.user_id, current_user=current_user
    )
    return [ResponseVehicleSchema.from_domain(vehicle) for vehicle in vehicles]


@router.get("/me/orders", summary="Получить список заказов текущего водителя")
async def get_driver_order_list(
    current_user: CurrentUserDep,
    interactor: FromDishka[GetOrdersInteraction],
    offset: int = 0,
    limit: int = 5,
) -> list[ResponseOrderSchema]:
    filters = GetOrderSFiltersSchema(
        driver_id=current_user.user_id, offset=offset, limit=limit
    )
    orders = await interactor(filters=filters, current_user=current_user)
    return [ResponseOrderSchema.from_domain(order) for order in orders]


@router.patch("/me/on_shift", summary="Переключить статус смены текущего водителя")
async def switch_on_shift_status(
    current_user: CurrentUserDep,
    status: bool,
    interactor: FromDishka[SwitchDriverOnShiftInteraction],
) -> JSONResponse:
    await interactor(
        current_user=current_user, driver_id=current_user.user_id, status=status
    )
    return JSONResponse(status_code=200, content={"message": "success"})


@router.patch("/me/location", summary="Обновить последнюю геолокацию текущего водителя")
async def update_location_driver(
    current_user: CurrentUserDep,
    data: UpdateDriverLocationSchema,
    interactor: FromDishka[UpdateLocationInteraction],
) -> JSONResponse:
    command = SetBaseUserLocationCommand(coordinates=data.coordinates)
    await interactor(command=command, current_user=current_user)
    return JSONResponse(status_code=200, content={"message": "success"})


@router.get(
    "/me/location",
    summary="Получить координаты последнего местонахождения текущего водителя",
)
async def get_location_driver(
    current_user: CurrentUserDep,
    interactor: FromDishka[GetLastLocationDriverInteraction],
) -> CoordinatesSchema | None:
    coordinates = await interactor(current_user.user_id)
    return (
        CoordinatesSchema.model_validate(asdict(coordinates)) if coordinates else None
    )
