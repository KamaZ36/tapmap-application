from uuid import UUID
from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.application.commands.driver.create import (
    CreateDriverCommand,
    CreateDriverCommandHandler,
)
from app.core.dependencies import container
from app.infrastructure.repositories.tg_bot_session.base import (
    BaseTgBotSessionRepository,
)
from app.bots.user_tg_bot.messages.admin.admin_panel import AdminDriverManagementMessage
from app.bots.user_tg_bot.messages.admin.driver.create_driver import (
    CreateDriverPanelMessage,
    GetDriverFirstNameMessage,
    GetDriverLastNameMessage,
    GetDriverMiddleNameMessage,
    GetDriverLicenseMessage,
    GetDriverPhoneMessage,
    GetDriverUserIdMessage,
)
from app.bots.user_tg_bot.states.admin import AdminCreateDriverStates


router = Router()


@router.callback_query(F.data == "admin:driver:add")
async def start_create_driver(callback: CallbackQuery, state: FSMContext) -> None:
    driver_data = await state.get_value("driver_data")
    if driver_data is None:
        driver_data = {}

    await callback.message.edit_text(
        **CreateDriverPanelMessage(driver_data=driver_data).pack()
    )
    await state.update_data(driver_data=driver_data)


# УСТАНОВКА USER_ID
@router.callback_query(F.data == "admin:driver:add:set_user_id")
async def get_user_id_handler(callback: CallbackQuery, state: FSMContext) -> None:
    msg = await callback.message.edit_text(**GetDriverUserIdMessage().pack())
    await state.set_state(AdminCreateDriverStates.get_user_id)
    await state.update_data(msg_id=msg.message_id)


@router.message(AdminCreateDriverStates.get_user_id, F.text)
async def set_user_id(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.delete()

    driver_data = await state.get_value("driver")
    if driver_data is None:
        return

    try:
        driver_data["user_id"] = UUID(message.text)
    except ValueError:
        await message.answer("❌ Неверный формат UUID")
        return

    msg_id = await state.get_value("msg_id")
    await bot.edit_message_text(
        **CreateDriverPanelMessage(driver_data=driver_data).pack(),
        chat_id=message.from_user.id,
        message_id=msg_id,
    )
    await state.update_data(driver_data=driver_data)
    await state.set_state(None)


# УСТАНОВКА ИМЕНИ
@router.callback_query(F.data == "admin:driver:add:set_first_name")
async def get_first_name_handler(callback: CallbackQuery, state: FSMContext) -> None:
    msg = await callback.message.edit_text(**GetDriverFirstNameMessage().pack())
    await state.set_state(AdminCreateDriverStates.get_driver_first_name)
    await state.update_data(msg_id=msg.message_id)


@router.message(AdminCreateDriverStates.get_driver_first_name, F.text)
async def set_first_name(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.delete()

    driver_data = await state.get_value("driver_data")
    if driver_data is None:
        return

    driver_data["first_name"] = message.text

    msg_id = await state.get_value("msg_id")
    await bot.edit_message_text(
        **CreateDriverPanelMessage(driver_data=driver_data).pack(),
        chat_id=message.from_user.id,
        message_id=msg_id,
    )
    await state.update_data(driver_data=driver_data)
    await state.set_state(None)


# УСТАНОВКА ФАМИЛИИ
@router.callback_query(F.data == "admin:driver:add:set_last_name")
async def get_last_name_handler(callback: CallbackQuery, state: FSMContext) -> None:
    msg = await callback.message.edit_text(**GetDriverLastNameMessage().pack())
    await state.set_state(AdminCreateDriverStates.get_driver_last_name)
    await state.update_data(msg_id=msg.message_id)


@router.message(AdminCreateDriverStates.get_driver_last_name, F.text)
async def set_last_name(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.delete()

    driver_data = await state.get_value("driver_data")
    if driver_data is None:
        return

    driver_data["last_name"] = message.text

    msg_id = await state.get_value("msg_id")
    await bot.edit_message_text(
        **CreateDriverPanelMessage(driver_data=driver_data).pack(),
        chat_id=message.from_user.id,
        message_id=msg_id,
    )
    await state.update_data(driver_data=driver_data)
    await state.set_state(None)


# УСТАНОВКА ОТЧЕСТВА
@router.callback_query(F.data == "admin:driver:add:set_middle_name")
async def get_middle_name_handler(callback: CallbackQuery, state: FSMContext) -> None:
    msg = await callback.message.edit_text(**GetDriverMiddleNameMessage().pack())
    await state.set_state(AdminCreateDriverStates.get_driver_middle_name)
    await state.update_data(msg_id=msg.message_id)


@router.message(AdminCreateDriverStates.get_driver_middle_name, F.text)
async def set_middle_name(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.delete()

    driver_data = await state.get_value("driver_data")
    if driver_data is None:
        return

    driver_data["middle_name"] = message.text

    msg_id = await state.get_value("msg_id")
    await bot.edit_message_text(
        **CreateDriverPanelMessage(driver_data=driver_data).pack(),
        chat_id=message.from_user.id,
        message_id=msg_id,
    )
    await state.update_data(driver_data=driver_data)
    await state.set_state(None)


# УСТАНОВКА НОМЕРА ПРАВ
@router.callback_query(F.data == "admin:driver:add:set_license_number")
async def get_license_handler(callback: CallbackQuery, state: FSMContext) -> None:
    msg = await callback.message.edit_text(**GetDriverLicenseMessage().pack())
    await state.set_state(AdminCreateDriverStates.get_driver_license)
    await state.update_data(msg_id=msg.message_id)


@router.message(AdminCreateDriverStates.get_driver_license, F.text)
async def set_license(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.delete()

    driver_data = await state.get_value("driver_data")
    if driver_data is None:
        return

    driver_data["license_number"] = message.text

    msg_id = await state.get_value("msg_id")
    await bot.edit_message_text(
        **CreateDriverPanelMessage(driver_data=driver_data).pack(),
        chat_id=message.from_user.id,
        message_id=msg_id,
    )
    await state.update_data(driver_data=driver_data)
    await state.set_state(None)


# УСТАНОВКА ТЕЛЕФОНА
@router.callback_query(F.data == "admin:driver:add:set_phone_number")
async def get_phone_handler(callback: CallbackQuery, state: FSMContext) -> None:
    msg = await callback.message.edit_text(**GetDriverPhoneMessage().pack())
    await state.set_state(AdminCreateDriverStates.get_driver_phone_number)
    await state.update_data(msg_id=msg.message_id)


@router.message(AdminCreateDriverStates.get_driver_phone_number, F.text)
async def set_phone(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.delete()

    driver_data = await state.get_value("driver_data")
    if driver_data is None:
        return

    driver_data["phone_number"] = message.text

    msg_id = await state.get_value("msg_id")
    await bot.edit_message_text(
        **CreateDriverPanelMessage(driver_data=driver_data).pack(),
        chat_id=message.from_user.id,
        message_id=msg_id,
    )
    await state.update_data(driver_data=driver_data)
    await state.set_state(None)


# ПОДТВЕРДИТЬ СОЗДАНИЕ ВОДИТЕЛЯ
@router.callback_query(F.data == "admin:driver:add:confirm")
async def confirm_create_driver(callback: CallbackQuery, state: FSMContext) -> None:
    driver_data = await state.get_value("driver_data")
    if driver_data is None:
        return

    async with container() as req_container:
        auth_session_repository = await req_container.get(BaseTgBotSessionRepository)
        auth_session = await auth_session_repository.get_by_tg_id(callback.from_user.id)

        try:
            command = CreateDriverCommand(
                current_user_id=auth_session.user_id,
                user_id=driver_data["user_id"],
                first_name=driver_data["first_name"],
                last_name=driver_data["last_name"],
                middle_name=driver_data.get("middle_name"),
                license_number=driver_data["license_number"],
                phone_number=driver_data["phone_number"],
            )
        except (KeyError, TypeError) as e:
            await callback.answer("❌ Заполните все обязательные поля водителя")
            return

        create_driver_interactor = await req_container.get(CreateDriverCommandHandler)
        await create_driver_interactor(command=command)

    await state.clear()
    await callback.message.edit_text(**AdminDriverManagementMessage().pack())
