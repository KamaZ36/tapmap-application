from uuid import UUID
from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.application.exceptions.order import OrderNotFound
from app.application.commands.order.cancel_order import (
    CancelOrderCommand,
    CancelOrderCommandHandler,
)
from app.core.dependencies import container
from app.infrastructure.repositories.tg_bot_session.base import (
    BaseTgBotSessionRepository,
)
from app.bots.user_tg_bot.messages.user.cancel_order import (
    GetCancelOrderReasonMessage,
    SuccessfulCancelCreateOrderMessage,
    SuccessfulCancelDraftOrderMessage,
)
from app.bots.user_tg_bot.states.user import UserCancelOrderStates


router = Router()


# ОТМЕНА СОЗДАНИЯ ЗАКАЗА
@router.callback_query(F.data.startswith("create_order:cancel:"))
async def cancel_create_order(callback: CallbackQuery, state: FSMContext) -> None:
    order_id = callback.data.replace("create_order:cancel:", "", 1)
    if not order_id:
        await callback.message.edit_reply_markup(reply_markup=None)  # type: ignore
        await callback.answer(SuccessfulCancelCreateOrderMessage().text)
        await state.clear()
        return

    async with container() as req_container:
        auth_session_repo = await req_container.get(BaseTgBotSessionRepository)
        auth_session = await auth_session_repo.get_by_tg_id(callback.from_user.id)

        command = CancelOrderCommand(
            current_user_id=auth_session.user_id, order_id=UUID(order_id)
        )
        cancel_order_interactor = await req_container.get(CancelOrderCommandHandler)
        try:
            await cancel_order_interactor(command=command)
        except OrderNotFound:
            pass

    await callback.message.edit_reply_markup(reply_markup=None)  # type: ignore
    await callback.answer(SuccessfulCancelCreateOrderMessage().text)
    await state.clear()


# ОТМЕНА ЗАКАЗА НА ЭТАПЕ РЕДАКТИРОВАНИЯ
@router.callback_query(F.data.startswith("draft_order:cancel:"))
async def cancel_draft_order(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.data is None:
        return

    order_id = callback.data.replace("draft_order:cancel:", "", 1)

    async with container() as req_container:
        auth_session_repository = await req_container.get(BaseTgBotSessionRepository)
        auth_session = await auth_session_repository.get_by_tg_id(callback.from_user.id)

        command = CancelOrderCommand(
            current_user_id=auth_session.user_id,  # type: ignore
            order_id=UUID(order_id),
        )

        cancel_order_interactor = await req_container.get(CancelOrderCommandHandler)

        await cancel_order_interactor(command=command)

    await state.clear()
    await callback.message.edit_text(**SuccessfulCancelDraftOrderMessage().pack())  # type: ignore


# ОТМЕНА АТИВНОГО ЗАКАЗА
@router.callback_query(F.data.startswith("order:cancel:"))
async def get_cancel_reason(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.data is None:
        return
    order_id = callback.data.replace("order:cancel:", "", 1)
    await state.set_state(UserCancelOrderStates.get_reason)
    msg = await callback.message.edit_text(**GetCancelOrderReasonMessage().pack())  # type: ignore
    await state.update_data(msg_id=msg.message_id, order_id=order_id)  # type: ignore


@router.message(UserCancelOrderStates.get_reason, F.text)
async def cancel_order(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.delete()

    order_id = await state.get_value("order_id")

    if order_id is None:
        return

    async with container() as req_container:
        auth_session_repository = await req_container.get(BaseTgBotSessionRepository)
        auth_session = await auth_session_repository.get_by_tg_id(message.from_user.id)  # type: ignore

        command = CancelOrderCommand(
            current_user_id=auth_session.user_id,
            order_id=UUID(order_id),
            reason=message.text,
        )

        cancel_order_interactor = await req_container.get(CancelOrderCommandHandler)

        await cancel_order_interactor(command=command)

    await state.clear()
