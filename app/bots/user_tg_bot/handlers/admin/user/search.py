from dataclasses import asdict
from uuid import UUID
from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from app.application.exceptions.user import UserNotFound
from app.application.queries.user.get_by_id import (
    GetUserByIdQueryHandler,
    GetUserByIdQuery,
)
from app.application.queries.user.get_by_phone_number import (
    GetUserByPhoneQueryHandler,
    GetUserByPhoneQuery,
)
from app.core.dependencies import container
from app.domain.exceptions.phone_number import InvalidPhoneNumber
from app.infrastructure.repositories.tg_bot_session.base import (
    BaseTgBotSessionRepository,
)
from app.bots.user_tg_bot.messages.admin.user.search import (
    GetPhoneNumberMessage,
    GetUserIdMessage,
    UserNotFoundMessage,
    UserSearchPanelMessage,
)
from app.bots.user_tg_bot.messages.admin.user.selected import (
    AdminSelectedUserPanelMessage,
)
from app.bots.user_tg_bot.states.admin import AdminSearchUserStates


router = Router()


# ВЫБОР МЕТОДА ДЛЯ ПОИСКА ПОЛЬЗОВАТЕЛЯ
@router.callback_query(F.data == "admin:user:search:methods")
async def get_user_search_method(callback: CallbackQuery) -> None:
    await callback.message.edit_text(**UserSearchPanelMessage().pack())  # type: ignore


# ПОИСК ПО НОМЕРУ ТЕЛЕФОНА
@router.callback_query(F.data == "admin:user:search:by_phone")
async def get_phone_number(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminSearchUserStates.get_phone_number)
    msg = await callback.message.edit_text(**GetPhoneNumberMessage().pack())  # type: ignore
    await state.update_data(msg_id=msg.message_id)  # type: ignore


@router.message(AdminSearchUserStates.get_phone_number, F.text)
async def get_user_by_phone_number(
    message: Message, state: FSMContext, bot: Bot
) -> None:
    await message.delete()

    msg_id = await state.get_value("msg_id")

    async with container() as req_container:
        auth_session_repository = await req_container.get(BaseTgBotSessionRepository)
        auth_session = await auth_session_repository.get_by_tg_id(message.from_user.id)  # type: ignore

        query = GetUserByPhoneQuery(
            phone_number=message.text, current_user_id=auth_session.user_id
        )

        get_user_interactor = await req_container.get(GetUserByPhoneQueryHandler)
        try:
            user = await get_user_interactor(query=query)
        except UserNotFound:
            await bot.edit_message_text(
                **UserNotFoundMessage().pack(),
                chat_id=message.from_user.id,
                message_id=msg_id,
            )
            return
        except InvalidPhoneNumber:
            return

    await state.update_data(selected_user_id=str(user.id))
    await state.set_state(None)
    await bot.edit_message_text(
        **AdminSelectedUserPanelMessage(asdict(user)).pack(),
        chat_id=message.from_user.id,
        message_id=msg_id,
    )


# ПОИСК ПО ИД
@router.callback_query(F.data == "admin:user:search:by_id")
async def get_user_id(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(AdminSearchUserStates.get_user_id)
    msg = await callback.message.edit_text(**GetUserIdMessage().pack())  # type: ignore
    await state.update_data(msg_id=msg.message_id)  # type: ignore


@router.message(AdminSearchUserStates.get_user_id, F.text)
async def get_user_by_user_id(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.delete()

    try:
        user_id = UUID(message.text)
    except Exception:
        return

    msg_id = await state.get_value("msg_id")

    async with container() as req_container:
        auth_session_repository = await req_container.get(BaseTgBotSessionRepository)
        auth_session = await auth_session_repository.get_by_tg_id(message.from_user.id)  # type: ignore

        query = GetUserByIdQuery(user_id=user_id, current_user_id=auth_session.user_id)

        get_user_interactor = await req_container.get(GetUserByIdQueryHandler)

        try:
            user = await get_user_interactor(query=query)
        except UserNotFound:
            await bot.edit_message_text(
                **UserNotFoundMessage().pack(),
                chat_id=message.from_user.id,
                message_id=msg_id,
            )
            return

    await state.update_data(selected_user_id=str(user.id))
    await state.set_state(None)
    await bot.edit_message_text(
        **AdminSelectedUserPanelMessage(asdict(user)).pack(),
        chat_id=message.from_user.id,
        message_id=msg_id,
    )
