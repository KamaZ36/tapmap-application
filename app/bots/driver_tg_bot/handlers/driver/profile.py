from aiogram import Router, F
from aiogram.types import Message

from app.core.mediator import get_mediator

from app.application.queries.driver.get_by_id import GetDriverByIdQuery

from app.bots.driver_tg_bot.dtos.auth_session import AuthSession
from app.bots.driver_tg_bot.messages.driver.profile import DriverProfileMessage


router = Router()


@router.message(F.text == "👤 Профиль")
async def driver_profile(message: Message, auth_session: AuthSession) -> None:
    await message.delete()

    mediator = get_mediator()
    query = GetDriverByIdQuery(
        current_user_id=auth_session.user_id, driver_id=auth_session.user_id
    )
    driver = await mediator.handle(query)

    await message.answer(**DriverProfileMessage(driver).pack())
