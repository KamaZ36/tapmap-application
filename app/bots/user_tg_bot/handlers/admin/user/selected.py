from dataclasses import asdict
from uuid import UUID
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.application.commands.user.unblock import (
    UnblockUserCommand,
    UnblockUserCommandHandler,
)
from app.application.queries.user.get_by_id import (
    GetUserByIdQueryHandler,
    GetUserByIdQuery,
)
from app.bots.user_tg_bot.messages.admin.driver.create_driver import (
    CreateDriverPanelMessage,
)
from app.bots.user_tg_bot.messages.admin.user.block import CreateUserBlockingMessage
from app.bots.user_tg_bot.messages.admin.user.selected import (
    AdminSelectedUserPanelMessage,
)
from app.core.dependencies import container
from app.infrastructure.repositories.tg_bot_session.base import (
    BaseTgBotSessionRepository,
)


router = Router()


@router.callback_query(F.data == "admin:user:selected")
async def selected_user_panel(callback: CallbackQuery, state: FSMContext) -> None:
    selected_user_id = await state.get_value("selected_user_id")
    if selected_user_id is None:
        return

    async with container() as req_container:
        auth_session_repo = await req_container.get(BaseTgBotSessionRepository)
        auth_session = await auth_session_repo.get_by_tg_id(callback.from_user.id)

        query = GetUserByIdQuery(
            current_user_id=auth_session.user_id, user_id=selected_user_id
        )
        get_user_interactor = await req_container.get(GetUserByIdQueryHandler)
        user = await get_user_interactor(query=query)

    await callback.message.edit_text(  # type: ignore
        **AdminSelectedUserPanelMessage(asdict(user)).pack(),
    )


# НАЗНАЧИТЬ ПОЛЬЗОВАТЕЛЯ ВОДИТЕЛЕМ
@router.callback_query(F.data == "admin:user:selected:make_driver")
async def make_driver_selected_user(callback: CallbackQuery, state: FSMContext) -> None:
    selected_user_id = await state.get_value("selected_user_id")
    if selected_user_id is None:
        return

    driver_data = {"user_id": selected_user_id}
    await state.update_data(driver_data=driver_data)

    await callback.message.edit_text(
        **CreateDriverPanelMessage(driver_data=driver_data).pack()
    )


# ЗАБЛОКИРОВАТЬ ПОЛЬЗОВАТЕЛЯ
@router.callback_query(F.data == "admin:user:selected:block")
async def block_selected_user(callback: CallbackQuery, state: FSMContext) -> None:
    selected_user_id = await state.get_value("selected_user_id")
    if selected_user_id is None:
        return

    blocking_data = {"user_id": selected_user_id, "minutes": 0, "days": 0, "hours": 0}
    await callback.message.edit_text(**CreateUserBlockingMessage(blocking_data).pack())
    await state.update_data(blocking_user_data=blocking_data)


# РАЗБЛОКИРОВАТЬ ПОЛЬЗОВАТЕЛЯ
@router.callback_query(F.data == "admin:user:selected:unblock")
async def unblock_selected_user(callback: CallbackQuery, state: FSMContext) -> None:
    selected_user_id = await state.get_value("selected_user_id")
    if selected_user_id is None:
        await callback.message.delete()

    async with container() as req_container:
        auth_session_repo = await req_container.get(BaseTgBotSessionRepository)
        auth_session = await auth_session_repo.get_by_tg_id(callback.from_user.id)

        command = UnblockUserCommand(
            current_user_id=auth_session.user_id, user_id=UUID(selected_user_id)
        )
        unblock_user_interactor = await req_container.get(UnblockUserCommandHandler)
        await unblock_user_interactor(command=command)

        query = GetUserByIdQuery(
            user_id=UUID(selected_user_id), current_user_id=auth_session.user_id
        )
        get_user_interactor = await req_container.get(GetUserByIdQueryHandler)
        user = await get_user_interactor(query=query)

    await callback.message.edit_text(
        **AdminSelectedUserPanelMessage(asdict(user)).pack()
    )
