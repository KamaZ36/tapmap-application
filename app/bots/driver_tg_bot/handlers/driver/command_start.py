from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart

from app.core.dependencies import container
from app.core.mediator import get_mediator

from app.domain.enums.driver_status import DriverStatus

from app.application.exceptions.order import OrderNotFound
from app.application.queries.driver.get_by_id import GetDriverByIdQuery
from app.application.queries.order.get_active_for_driver import (
    GetActiveOrderForDirverQuery,
)

from app.infrastructure.repositories.tg_bot_session.base import (
    BaseTgBotSessionRepository,
)

from app.bots.driver_tg_bot.messages.driver.command_start import WelcomeMessage
from app.bots.driver_tg_bot.messages.driver.order import OrderPanelMessage
from app.bots.driver_tg_bot.messages.errors import (
    DriverNotAuthInUserBotMessage,
    UserNotIsDriverMessage,
)


router = Router()


@router.message(CommandStart())
async def command_start(message: Message) -> None:
    async with container() as req_container:
        auth_session_repository = await req_container.get(BaseTgBotSessionRepository)
        auth_session = await auth_session_repository.get_by_tg_id(message.from_user.id)

    if auth_session is None:
        await message.answer(**DriverNotAuthInUserBotMessage().pack())
        return

    mediator = get_mediator()

    query = GetDriverByIdQuery(
        current_user_id=auth_session.user_id, driver_id=auth_session.user_id
    )
    driver = await mediator.handle(query)

    if driver.status != DriverStatus.active:
        await message.answer(**UserNotIsDriverMessage().pack())
        return

    try:
        query = GetActiveOrderForDirverQuery(
            current_user_id=auth_session.user_id, driver_id=auth_session.user_id
        )
        order = await mediator.handle(query)
        await message.answer(**OrderPanelMessage(order).pack())
    except OrderNotFound:
        await message.answer(**WelcomeMessage(driver).pack())
