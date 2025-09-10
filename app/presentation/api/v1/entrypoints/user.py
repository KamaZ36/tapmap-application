from uuid import UUID
from fastapi import APIRouter, Depends, status
from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi.responses import JSONResponse


from app.application.commands.user import CreateUserCommand, SetBaseUserLocationCommand
from app.application.dtos.order import GetOrdersFilters
from app.application.dtos.user import GetUsersFilters
from app.application.interactions.order.get_orders import GetOrdersInteraction
from app.application.interactions.user.create_user import CreateUserInteraction
from app.application.interactions.user.get_active_order import (
    GetActiveOrderForUserInteraction,
)
from app.application.interactions.user.get_user import GetUserInteractor
from app.application.interactions.user.get_users import GetUsersInteraction
from app.application.interactions.user.set_base_location import (
    SetBaseLocationUserInteraction,
)

from app.presentation.api.dependencies import CurrentUserDep
from app.presentation.api.v1.schemas.order import (
    ResponseExtendedOrderSchema,
    ResponseOrderSchema,
)
from app.presentation.api.v1.schemas.user import (
    GetUsersFiltersSchema,
    ResponseUserSchema,
    CreateUserSchema,
    UpdateUserBaseLocationSchema,
)


router = APIRouter(route_class=DishkaRoute)


@router.post("", summary="Регистрирует нового пользователя")
async def register_user(
    data: CreateUserSchema, interactor: FromDishka[CreateUserInteraction]
) -> ResponseUserSchema:
    command = CreateUserCommand(phone_number=data.phone_number, name=data.name)
    user = await interactor(command=command)
    return ResponseUserSchema.from_domain(user)


@router.get("", summary="Получить список пользователей по фильтрам")
async def get_filtered_users(
    current_user: CurrentUserDep,
    interactor: FromDishka[GetUsersInteraction],
    data: GetUsersFiltersSchema = Depends(),
) -> list[ResponseUserSchema]:
    filters = GetUsersFilters(**data.model_dump())
    users = await interactor(current_user=current_user, filters=filters)
    return [ResponseUserSchema.from_domain(user) for user in users]


@router.get("/me", summary="Получить текущего пользователя")
async def get_current_user(
    interactor: FromDishka[GetUserInteractor],
    current_user: CurrentUserDep,
) -> ResponseUserSchema:
    user = await interactor(current_user=current_user, get_user_id=current_user.user_id)
    return ResponseUserSchema.from_domain(user)


@router.get(
    "/{user_id}", summary="Получить пользователя по ID (Только администраторам)"
)
async def get_user_by_id(
    user_id: UUID,
    current_user: CurrentUserDep,
    interactor: FromDishka[GetUserInteractor],
) -> ResponseUserSchema:
    user = await interactor(current_user=current_user, get_user_id=user_id)
    return ResponseUserSchema.from_domain(user)


@router.get(
    "/me/orders/active", summary="Получить активный заказ текущего пользователя"
)
async def get_active_order_for_user(
    current_user: CurrentUserDep,
    interactor: FromDishka[GetActiveOrderForUserInteraction],
) -> ResponseExtendedOrderSchema:
    extended_order = await interactor(current_user=current_user)
    return ResponseExtendedOrderSchema.from_domain(extended_order)


@router.get("/me/orders", summary="Получить список заказов пользователя")
async def get_order_list_for_user(
    current_user: CurrentUserDep,
    interactor: FromDishka[GetOrdersInteraction],
    offset: int = 5,
    limit: int = 0,
) -> list[ResponseOrderSchema]:
    filters = GetOrdersFilters(
        customer_id=current_user.user_id, offset=offset, limit=limit
    )
    orders = await interactor(filters=filters, current_user=current_user)
    return [ResponseOrderSchema.from_domain(order) for order in orders]


@router.patch("/me/location", summary="Обновить базовый город пользователя")
async def set_base_city_for_user(
    data: UpdateUserBaseLocationSchema,
    current_user: CurrentUserDep,
    interactor: FromDishka[SetBaseLocationUserInteraction],
) -> JSONResponse:
    command = SetBaseUserLocationCommand(data.coordinates)
    await interactor(command=command, user_id=current_user.user_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "success"})
