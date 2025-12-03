from uuid import UUID
from fastapi import APIRouter

from app.core.mediator import get_mediator

from app.application.dtos.driver import DriverDTO
from app.application.dtos.order import OrderDTO
from app.application.dtos.user import UserDTO
from app.application.queries.driver.get_by_id import GetDriverByIdQuery
from app.application.queries.order.get_active_for_customer import (
    GetActiveOrderForCustomerQuery,
)
from app.application.queries.order.get_active_for_driver import (
    GetActiveOrderForDirverQuery,
)
from app.application.queries.user.get_by_id import GetUserByIdQuery

from app.api.dependencies import CurrentUserId

router = APIRouter()


@router.get("/users/{user_id}")
async def get_user_by_id(user_id: UUID, current_user_id: CurrentUserId) -> UserDTO:
    query = GetUserByIdQuery(user_id=user_id, current_user_id=current_user_id)
    mediator = get_mediator()
    user = await mediator.handle(query)

    return user


@router.get(
    "/users/{user_id}/orders/active",
    summary="Получить активный заказ пользователя по ID",
)
async def get_active_order_for_user(
    user_id: UUID, current_user_id: CurrentUserId
) -> OrderDTO:
    query = GetActiveOrderForCustomerQuery(
        current_user_id=current_user_id, customer_id=user_id
    )
    mediator = get_mediator()
    order = await mediator.handle(query)

    return order


@router.get("/drivers/{driver_id}", summary="Получить профиль водителя по ID")
async def get_driver_by_id(
    driver_id: UUID, current_user_id: CurrentUserId
) -> DriverDTO:
    query = GetDriverByIdQuery(current_user_id=current_user_id, driver_id=driver_id)
    mediator = get_mediator()
    driver = await mediator.handle(query)

    return driver


@router.get(
    "/drivers/{driver_id}/orders/active",
    summary="Получить активный заказ водителя по ID.",
)
async def get_active_order_for_current_driver(
    driver_id: UUID,
    current_user_id: CurrentUserId,
) -> OrderDTO:
    query = GetActiveOrderForDirverQuery(
        driver_id=driver_id, current_user_id=current_user_id
    )
    mediator = get_mediator()
    order = await mediator.handle(query)

    return order
