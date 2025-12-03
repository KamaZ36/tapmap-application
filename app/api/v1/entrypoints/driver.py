from fastapi import APIRouter

from app.core.mediator import get_mediator

from app.application.dtos.driver import DriverDTO
from app.application.dtos.order import OrderDTO
from app.application.queries.driver.get_by_id import GetDriverByIdQuery
from app.application.queries.order.get_active_for_driver import (
    GetActiveOrderForDirverQuery,
)

from app.api.dependencies import CurrentUserId


router = APIRouter()


@router.get("/@me", summary="Получить профиль текущего водителя")
async def get_driver_for_current_user(current_user_id: CurrentUserId) -> DriverDTO:
    query = GetDriverByIdQuery(
        current_user_id=current_user_id, driver_id=current_user_id
    )
    mediator = get_mediator()
    driver = await mediator.handle(query)

    return driver


@router.get(
    "@me/orders/active", summary="Получить активный заказ для текущего водителя."
)
async def get_active_order_for_current_driver(
    current_user_id: CurrentUserId,
) -> OrderDTO:
    query = GetActiveOrderForDirverQuery(
        driver_id=current_user_id, current_user_id=current_user_id
    )
    mediator = get_mediator()
    order = await mediator.handle(query)

    return order
