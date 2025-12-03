from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from app.application.queries.user.get_by_id import (
    GetUserByIdQueryHandler,
    GetUserByIdQuery,
)
from app.core.dependencies import container
from app.domain.enums.user import UserRole
from app.infrastructure.repositories.tg_bot_session.base import (
    BaseTgBotSessionRepository,
)
from app.bots.user_tg_bot.messages.admin.admin_panel import (
    AdminCityManagmentMessage,
    AdminDriverManagementMessage,
    AdminPanelMessage,
    AdminUserManagementMessage,
)

router = Router()


@router.message(Command("admin"))
async def admin_panel(message: Message) -> None:
    async with container() as req_container:
        auth_session_repository = await req_container.get(BaseTgBotSessionRepository)
        auth_session = await auth_session_repository.get_by_tg_id(message.from_user.id)  # type: ignore

        get_user_interactor = await req_container.get(GetUserByIdQueryHandler)
        query = GetUserByIdQuery(
            user_id=auth_session.user_id,
            current_user_id=auth_session.user_id,  # type: ignore
        )
        user = await get_user_interactor(query=query)

    if UserRole.admin not in user.roles:
        return

    await message.answer(**AdminPanelMessage().pack())


@router.callback_query(F.data == "admin:admin_panel")
async def admin_panel_callback(callback: CallbackQuery) -> None:
    await callback.message.edit_text(**AdminPanelMessage().pack())  # type: ignore


@router.callback_query(F.data == "admin:city")
async def city_managment(callback: CallbackQuery) -> None:
    await callback.message.edit_text(**AdminCityManagmentMessage().pack())  # type: ignore


@router.callback_query(F.data == "admin:driver")
async def driver_managment(callback: CallbackQuery) -> None:
    await callback.message.edit_text(**AdminDriverManagementMessage().pack())  # type: ignore


@router.callback_query(F.data == "admin:user")
async def user_management(callback: CallbackQuery) -> None:
    await callback.message.edit_text(**AdminUserManagementMessage().pack())  # type: ignore
