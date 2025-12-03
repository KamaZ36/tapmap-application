from uuid import UUID

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import or_f

from app.core.mediator import get_mediator

from app.application.commands.order.update_status import UpdateOrderStatusCommand

from app.bots.driver_tg_bot.dtos.auth_session import AuthSession


router = Router()


@router.callback_query(
    or_f(
        F.data == "driver:arrived",
        F.data == "driver:pickup_customer",
        F.data == "driver:complete_order",
    )
)
async def update_order_status(
    callback: CallbackQuery, state: FSMContext, auth_session: AuthSession
) -> None:
    order_id = UUID(await state.get_value("order_id"))
    if order_id is None:
        return

    mediator = get_mediator()
    command = UpdateOrderStatusCommand(
        current_user_id=auth_session.user_id, order_id=order_id
    )
    await mediator.handle(command)
