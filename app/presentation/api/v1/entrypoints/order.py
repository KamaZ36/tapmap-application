from uuid import UUID
from fastapi import APIRouter, Depends

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from app.domain.entities.order import OrderStatus

from app.application.commands.order import UpdateOrderStatusCommand
from app.application.dtos.order import GetOrdersFilters
from app.application.interactions.order.cancel_order import CancelOrderInteraction
from app.application.interactions.order.get_order import GetOrderInteraction
from app.application.interactions.order.get_orders import GetOrdersInteraction
from app.application.interactions.order.update_status import UpdateStatusInteraction

from app.presentation.api.dependencies import CurrentUserDep
from app.presentation.api.v1.schemas.order import (
    CancelOrderSchema, 
    GetOrderSFiltersSchema, 
    ResponseExtendedOrderSchema, 
    ResponseOrderSchema
)


router = APIRouter(route_class=DishkaRoute)


@router.get(
    '',
    summary="Получить список заказов по фильтрам"
)
async def get_filtered_orders(
    current_user: CurrentUserDep,
    interactor: FromDishka[GetOrdersInteraction],
    data: GetOrderSFiltersSchema = Depends(),
) -> list[ResponseOrderSchema]:
    filters = GetOrdersFilters(**data.model_dump())
    orders = await interactor(filters=filters, current_user=current_user)
    return [ResponseOrderSchema.from_domain(order) for order in orders]
    
@router.get(
    '/{order_id}',
    summary='Получить конкретный заказ.'
)    
async def get_order(
    current_user: CurrentUserDep,
    order_id: UUID,
    interactor: FromDishka[GetOrderInteraction]
) -> ResponseExtendedOrderSchema:
    extended_order = await interactor(order_id=order_id, current_user=current_user)
    return ResponseExtendedOrderSchema.from_domain(extended_order)

@router.patch(
    '/{order_id}/status',
    summary="Обновить статус заказа (Водитель или администратор)"
)
async def update_order_status(
    order_id: UUID,
    current_user: CurrentUserDep,
    interactor: FromDishka[UpdateStatusInteraction]
) -> OrderStatus:
    status = await interactor(current_user=current_user, command=UpdateOrderStatusCommand(order_id=order_id))
    return status

@router.post(
    '/{order_id}/cancel',
    summary="Отменить заказ"
)
async def cancel_order(
    order_id: UUID,
    data: CancelOrderSchema,
    current_user: CurrentUserDep,
    interactor: FromDishka[CancelOrderInteraction]
) -> None:
    await interactor(current_user=current_user, order_id=order_id, reason=data.reason)
