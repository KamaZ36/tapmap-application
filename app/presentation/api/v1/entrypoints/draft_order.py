from fastapi import APIRouter, BackgroundTasks, status

from dishka.integrations.fastapi import DishkaRoute, FromDishka

from app.application.commands.order import (
    AddPointToDraftOrderCommand,
    CreateDraftOrderCommand,
    AddCommentToDraftOrderCommand,
)

from app.application.interactions.draft_order.add_comment import (
    AddCommentToDraftOrderInteraction,
)
from app.application.interactions.draft_order.add_point import (
    AddPointToDraftOrderInteraction,
)
from app.application.interactions.draft_order.confirm_draft_order import (
    ConfirmDraftOrderInteraction,
)
from app.application.interactions.draft_order.create_order import (
    CreateDraftOrderInteraction,
)
from app.application.interactions.draft_order.delete import DeleteDraftOrderInteraction
from app.application.interactions.draft_order.get_draft_order import (
    GetDraftOrderInteraction,
)
from app.application.interactions.order.process_order import ProcessOrderInteraction

from app.presentation.api.v1.schemas.draft_order import (
    AddCommentSchema,
    AddPointToDraftOrderSchema,
    CreateDraftOrderSchema,
    ResponseDraftOrderSchema,
)

from app.presentation.api.dependencies import CurrentUserDep
from app.presentation.api.v1.schemas.order import ResponseOrderSchema


router = APIRouter(route_class=DishkaRoute)


@router.post(
    "",
    summary="Создать черновик заказа",
    description="Эндпоинт создает черновик заказа на основе двух точек маршрута.",
    status_code=status.HTTP_201_CREATED,
    responses={status.HTTP_201_CREATED: {"model": ResponseDraftOrderSchema}},
)
async def create_draft_order(
    current_user: CurrentUserDep,
    data: CreateDraftOrderSchema,
    interactor: FromDishka[CreateDraftOrderInteraction],
) -> ResponseDraftOrderSchema:
    command = CreateDraftOrderCommand(
        start_point=data.start_point, end_point=data.end_point
    )
    draft_order = await interactor(command=command, user_id=current_user.user_id)
    return ResponseDraftOrderSchema.from_domain(draft_order)


@router.get("", summary="Получить черновик заказа текущего пользователя")
async def get_draft_order(
    current_user: CurrentUserDep, interactor: FromDishka[GetDraftOrderInteraction]
) -> ResponseDraftOrderSchema:
    draft_order = await interactor(user_id=current_user.user_id)
    return ResponseDraftOrderSchema.from_domain(draft_order)


@router.post(
    "/point",
    summary="Добавить точку к черновику заказа",
    description="Эндпоинт добавляет точку в конец маршрута черновика заказа.",
)
async def add_point_to_draft_order(
    current_user: CurrentUserDep,
    data: AddPointToDraftOrderSchema,
    interactor: FromDishka[AddPointToDraftOrderInteraction],
) -> ResponseDraftOrderSchema:
    command = AddPointToDraftOrderCommand(point=data.point)
    draft_order = await interactor(command=command, user_id=current_user.user_id)
    return ResponseDraftOrderSchema.from_domain(draft_order)


@router.patch("/comment", summary="Добавить комментарий к заказу")
async def add_comment_to_draft_order(
    current_user: CurrentUserDep,
    data: AddCommentSchema,
    interactor: FromDishka[AddCommentToDraftOrderInteraction],
) -> ResponseDraftOrderSchema:
    command = AddCommentToDraftOrderCommand(comment=data.comment)
    draft_order = await interactor(user_id=current_user.user_id, command=command)
    return ResponseDraftOrderSchema.from_domain(draft_order)


@router.post(
    "/confirm",
    summary="Подтвердить черновик заказа текущего пользователя и отправить его в работу",
)
async def confirm_draft_order(
    current_user: CurrentUserDep,
    interactor: FromDishka[ConfirmDraftOrderInteraction],
    order_processor: FromDishka[ProcessOrderInteraction],
    background_task: BackgroundTasks,
) -> ResponseOrderSchema:
    order = await interactor(user_id=current_user.user_id)
    background_task.add_task(order_processor, order.id)
    return ResponseOrderSchema.from_domain(order)


@router.delete("", summary="Удалить черновик заказа текущего пользователя")
async def delete_draft_order(
    current_user: CurrentUserDep, interactor: FromDishka[DeleteDraftOrderInteraction]
) -> None:
    await interactor(current_user.user_id)
