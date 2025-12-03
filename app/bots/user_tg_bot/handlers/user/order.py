from uuid import UUID
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.application.queries.order.get_order_by_id import (
    GetOrderByIdQuery,
    GetOrderByIdQueryHandler,
)
from app.bots.user_tg_bot.messages.user.order import OrderPanelMessage
from app.core.dependencies import container
from app.infrastructure.repositories.tg_bot_session.base import (
    BaseTgBotSessionRepository,
)


router = Router()


@router.callback_query(F.data == "user:order")
async def order_panel(callback: CallbackQuery, state: FSMContext) -> None:
    order_id = UUID(await state.get_value("order_id"))

    async with container() as req_container:
        auth_session_repo = await req_container.get(BaseTgBotSessionRepository)
        auth_session = await auth_session_repo.get_by_tg_id(callback.from_user.id)

        query = GetOrderByIdQuery(
            current_user_id=auth_session.user_id, order_id=order_id
        )
        get_order_interactor = await req_container.get(GetOrderByIdQueryHandler)
        order = await get_order_interactor(query=query)

    order_msg = await callback.message.edit_text(**OrderPanelMessage(order).pack())
    await state.set_state(None)
    await state.update_data(order_msg_id=order_msg.message_id)  # type: ignore
