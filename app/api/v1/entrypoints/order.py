from uuid import UUID
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.mediator import get_mediator

from app.application.commands.order.add_comment import AddCommentToOrderCommand
from app.application.commands.order.add_point import AddPointToOrderCommand
from app.application.commands.order.cancel_order import CancelOrderCommand
from app.application.commands.order.confirm import ConfirmOrderCommand
from app.application.commands.order.create import CreateOrderCommand
from app.application.dtos.order import OrderDTO
from app.application.queries.order.get_order_by_id import GetOrderByIdQuery

from app.api.dependencies import CurrentUserId
from app.api.v1.schemas.order import (
    AddCommentToOrderSchema,
    AddPointToOrderSchema,
    CancelOrderSchema,
    CreateOrderSchema,
)


router = APIRouter()


@router.get("/{order_id}", summary="Получить заказ по ID")
async def get_order_by_id(order_id: UUID, current_user_id: UUID) -> OrderDTO:
    query = GetOrderByIdQuery(current_user_id=current_user_id, order_id=order_id)
    mediator = get_mediator()
    order = await mediator.handle(query)

    return order


@router.post("/draft", summary="Создать черновик заказа")
async def create_order(
    data: CreateOrderSchema, current_user_id: CurrentUserId
) -> OrderDTO:
    command = CreateOrderCommand(
        current_user_id=current_user_id,
        user_id=current_user_id,
        start_point=data.start_point,
    )
    mediator = get_mediator()
    order = await mediator.handle(command)

    return order


@router.post("/draft/{order_id}/point", summary="Добавить точку к заказу")
async def add_point_to_order(
    data: AddPointToOrderSchema, order_id: UUID, current_user_id: CurrentUserId
) -> OrderDTO:
    command = AddPointToOrderCommand(
        order_id=order_id, point=data.point, current_user_id=current_user_id
    )
    mediator = get_mediator()
    order = await mediator.handle(command)

    return order


@router.post("/draft/{order_id}/comment", summary="Добавить комментарий к заказу")
async def add_comment_to_order(
    data: AddCommentToOrderSchema, order_id: UUID, current_user_id: CurrentUserId
) -> OrderDTO:
    command = AddCommentToOrderCommand(
        current_user_id=current_user_id, order_id=order_id, comment=data.comment
    )
    mediator = get_mediator()
    order = await mediator.handle(command)

    return order


@router.post("/draft/{order_id}/confirm", summary="Подтвердить заказ")
async def confirm_order(order_id: UUID, current_user_id: CurrentUserId) -> OrderDTO:
    command = ConfirmOrderCommand(order_id=order_id, current_user_id=current_user_id)
    mediator = get_mediator()
    order = await mediator.handle(command)

    return order


@router.post("/draft/{order_id}/cancel", summary="Отменить черновик заказа")
async def cancel_draft_order(
    order_id: UUID, current_user_id: CurrentUserId
) -> JSONResponse:
    command = CancelOrderCommand(current_user_id=current_user_id, order_id=order_id)
    mediator = get_mediator()
    result = await mediator.handle(command)

    if result:
        return JSONResponse(status_code=200, content={"message": "Заказ отменен."})
    return JSONResponse(status_code=500, content={"message": "Что-то пошло не так..."})


@router.post("/{order_id}/cancel", summary="Отменить активный заказ")
async def cancel_order(
    data: CancelOrderSchema, order_id: UUID, current_user_id: CurrentUserId
) -> JSONResponse:
    command = CancelOrderCommand(
        current_user_id=current_user_id, order_id=order_id, reason=data.reason
    )
    mediator = get_mediator()
    result = await mediator.handle(command)

    if result:
        return JSONResponse(status_code=200, content={"Заказ отменен."})
    return JSONResponse(status_code=500, content={"message": "Что-то пошло не так..."})
