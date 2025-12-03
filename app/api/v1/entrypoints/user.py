from fastapi import APIRouter

from app.core.mediator import get_mediator

from app.application.commands.user.create_user import CreateUserCommand
from app.application.dtos.order import OrderDTO
from app.application.dtos.user import UserDTO
from app.application.queries.order.get_active_for_customer import (
    GetActiveOrderForCustomerQuery,
)
from app.application.queries.user.get_by_id import GetUserByIdQuery

from app.api.v1.schemas.user import CreateUserSchema
from app.api.dependencies import CurrentUserId

router = APIRouter()


@router.post("", summary="Создание нового пользователя")
async def create_user(data: CreateUserSchema) -> UserDTO:
    command = CreateUserCommand(phone_number=data.phone_number, name=data.name)
    mediator = get_mediator()
    user = await mediator.handle(command)

    return user


@router.get("/@me", summary="Получить профиль текущего пользователя")
async def get_me_user(current_user_id: CurrentUserId) -> UserDTO:
    query = GetUserByIdQuery(user_id=current_user_id, current_user_id=current_user_id)
    mediator = get_mediator()
    user = await mediator.handle(query)

    return user


@router.get("/@me/orders/active")
async def get_active_order_for_current_user(current_user_id: CurrentUserId) -> OrderDTO:
    query = GetActiveOrderForCustomerQuery(
        customer_id=current_user_id, current_user_id=current_user_id
    )
    mediator = get_mediator()
    order = await mediator.handle(query)

    return order
