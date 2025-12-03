from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware, Bot
from aiogram.types import TelegramObject, Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.bots.driver_tg_bot.messages.errors import AtuhSessionNotFoundErrorMessage
from app.core.dependencies import container
from app.infrastructure.repositories.tg_bot_session.base import (
    BaseTgBotSessionRepository,
)


class AuthSessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with container() as req_container:
            auth_session_repo = await req_container.get(BaseTgBotSessionRepository)
            auth_session = await auth_session_repo.get_by_tg_id(event.from_user.id)

        if auth_session is None:
            await self._handle_auth_error(event=event, data=data)
            return

        data["auth_session"] = auth_session
        result = await handler(event, data)
        return result

    async def _handle_auth_error(self, event: TelegramObject, data: dict[str, Any]):
        context: FSMContext | None = data.get("state")
        bot: Bot | None = data.get("bot")
        if context is None or bot is None:
            return

        if isinstance(event, Message):
            chat_id = event.chat.id
        elif isinstance(event, CallbackQuery) and event.message:
            chat_id = event.message.chat.id
        else:
            return

        await bot.send_message(
            **AtuhSessionNotFoundErrorMessage().pack(), chat_id=chat_id
        )
        return
