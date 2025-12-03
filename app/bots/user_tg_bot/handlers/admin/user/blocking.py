from dataclasses import asdict
from datetime import timedelta

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.application.commands.user.block import (
    BlockUserCommand,
    BlockUserCommandHandler,
)
from app.application.queries.user.get_by_id import (
    GetUserByIdQuery,
    GetUserByIdQueryHandler,
)
from app.bots.user_tg_bot.messages.admin.user.block import (
    CreateUserBlockingMessage,
    GetBlockingDaysMessage,
    GetBlockingHoursMessage,
    GetBlockingMinutesMessage,
    GetBlockingReasonMessage,
)
from app.bots.user_tg_bot.messages.admin.user.selected import (
    AdminSelectedUserPanelMessage,
)
from app.bots.user_tg_bot.states.admin import AdminBlockUserStates
from app.core.dependencies import container
from app.infrastructure.repositories.tg_bot_session.base import (
    BaseTgBotSessionRepository,
)
from app.utils import get_datetime_utc_now


router = Router()


# ПРИЧИНА БЛОКИРОВКИ
@router.callback_query(F.data == "admin:user_blocking:set_reason")
async def get_blocking_reason(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminBlockUserStates.get_reason)
    msg = await callback.message.edit_text(**GetBlockingReasonMessage().pack())
    await state.update_data(msg_id=msg.message_id)


@router.message(AdminBlockUserStates.get_reason, F.text)
async def set_blocking_reason(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.delete()

    msg_id = await state.get_value("msg_id")
    blocking_user_data = await state.get_value("blocking_user_data")
    if blocking_user_data is None:
        return

    blocking_user_data["reason"] = message.text

    await bot.edit_message_text(
        **CreateUserBlockingMessage(blocking_user_data).pack(),
        chat_id=message.from_user.id,
        message_id=msg_id,
    )

    await state.update_data(blocking_user_data=blocking_user_data)
    await state.set_state(None)


# КОЛИЧЕСТВО ДНЕЙ
@router.callback_query(F.data == "admin:user_blocking:set_days")
async def get_blocking_days(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminBlockUserStates.get_days)
    msg = await callback.message.edit_text(**GetBlockingDaysMessage().pack())
    await state.update_data(msg_id=msg.message_id)


@router.message(AdminBlockUserStates.get_days, F.text)
async def set_blocking_days(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.delete()

    msg_id = await state.get_value("msg_id")
    blocking_user_data = await state.get_value("blocking_user_data")
    if blocking_user_data is None:
        return

    blocking_user_data["days"] = int(message.text)

    await bot.edit_message_text(
        **CreateUserBlockingMessage(blocking_user_data).pack(),
        chat_id=message.from_user.id,
        message_id=msg_id,
    )
    await state.set_state(None)
    await state.update_data(blocking_user_data=blocking_user_data)


# КОЛИЧЕСТВО ЧАСОВ
@router.callback_query(F.data == "admin:user_blocking:set_hours")
async def get_blocking_hours(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminBlockUserStates.get_hours)
    msg = await callback.message.edit_text(**GetBlockingHoursMessage().pack())
    await state.update_data(msg_id=msg.message_id)


@router.message(AdminBlockUserStates.get_hours, F.text)
async def set_blocking_hours(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.delete()

    msg_id = await state.get_value("msg_id")
    blocking_user_data = await state.get_value("blocking_user_data")
    if blocking_user_data is None:
        return

    blocking_user_data["hours"] = float(message.text)

    await bot.edit_message_text(
        **CreateUserBlockingMessage(blocking_user_data).pack(),
        chat_id=message.from_user.id,
        message_id=msg_id,
    )
    await state.set_state(None)
    await state.update_data(blocking_user_data=blocking_user_data)


# КОЛЧИЕСТВО МИНУТ
@router.callback_query(F.data == "admin:user_blocking:set_minutes")
async def get_blocking_minutes(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminBlockUserStates.get_minutes)
    msg = await callback.message.edit_text(**GetBlockingMinutesMessage().pack())
    await state.update_data(msg_id=msg.message_id)


@router.message(AdminBlockUserStates.get_minutes, F.text)
async def set_blocking_minutes(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.delete()

    msg_id = await state.get_value("msg_id")
    blocking_user_data = await state.get_value("blocking_user_data")
    if blocking_user_data is None:
        return

    blocking_user_data["minutes"] = float(message.text)

    await bot.edit_message_text(
        **CreateUserBlockingMessage(blocking_user_data).pack(),
        chat_id=message.from_user.id,
        message_id=msg_id,
    )
    await state.set_state(None)
    await state.update_data(blocking_user_data=blocking_user_data)


# ПОДТВЕРЖДЕНИЕ БЛОКИРОВКИ
@router.callback_query(F.data == "admin:user_blocking:confirm")
async def confirm_blocking(callback: CallbackQuery, state: FSMContext) -> None:
    blocking_user_data = await state.get_value("blocking_user_data")
    if blocking_user_data is None:
        await callback.message.delete()
        return

    async with container() as req_container:
        auth_session_repo = await req_container.get(BaseTgBotSessionRepository)
        auth_session = await auth_session_repo.get_by_tg_id(callback.from_user.id)

        addition_time = timedelta(
            hours=blocking_user_data["hours"],
            minutes=blocking_user_data["minutes"],
            days=blocking_user_data["days"],
        )
        expires_at = get_datetime_utc_now() + addition_time

        command = BlockUserCommand(
            current_user_id=auth_session.user_id,
            user_id=blocking_user_data["user_id"],
            reason=blocking_user_data["reason"],
            expires_at=expires_at,
        )
        block_user_interactor = await req_container.get(BlockUserCommandHandler)
        await block_user_interactor(command=command)

        query = GetUserByIdQuery(
            user_id=blocking_user_data["user_id"], current_user_id=auth_session.user_id
        )
        get_user_interactor = await req_container.get(GetUserByIdQueryHandler)
        user = await get_user_interactor(query=query)

    await callback.message.edit_text(
        **AdminSelectedUserPanelMessage(asdict(user)).pack()
    )
