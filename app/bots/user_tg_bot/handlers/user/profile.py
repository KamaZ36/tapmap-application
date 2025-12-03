from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from app.core.mediator import get_mediator

from app.application.queries.user.get_by_id import GetUserByIdQuery

from app.bots.driver_tg_bot.dtos.auth_session import AuthSession
from app.bots.user_tg_bot.messages.user.profile import (
    ProfilePanelMessage,
)

router = Router()


@router.message(F.text == "Профиль 👤")
async def user_profile(message: Message, auth_session: AuthSession) -> None:
    mediator = get_mediator()
    query = GetUserByIdQuery(
        user_id=auth_session.user_id, current_user_id=auth_session.user_id
    )
    user = await mediator.handle(query)

    await message.answer(**ProfilePanelMessage(user).pack())


@router.callback_query(F.data == "user:profile")
async def user_profile_callback(
    callback: CallbackQuery, auth_session: AuthSession
) -> None:
    mediator = get_mediator()
    query = GetUserByIdQuery(
        user_id=auth_session.user_id, current_user_id=auth_session.user_id
    )
    user = await mediator.handle(query)

    await callback.message.edit_text(**ProfilePanelMessage(user).pack())
