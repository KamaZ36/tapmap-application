from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import or_f, StateFilter

from app.application.commands.driver.exit_from_shift import DriverExitFromShiftCommand
from app.application.commands.driver.go_to_shift import DriverGoToShiftCommand

from app.application.commands.driver.update_location import UpdateDriverLocationCommand
from app.bots.driver_tg_bot.dtos.auth_session import AuthSession
from app.bots.driver_tg_bot.messages.driver.shift import (
    CancelDriverGoToShiftMessage,
    GetDriverLocationMessage,
    SucessfulDriverEndShiftMessage,
    SucessfulShiftDeparture,
)
from app.bots.driver_tg_bot.states.driver import DriverShiftStates
from app.core.mediator import get_mediator


router = Router()


# ВЫХОД НА СМЕНУ
@router.message(StateFilter(None), F.text == "🟢 Выйти на линию")
async def get_location_driver(message: Message, state: FSMContext) -> None:
    await state.set_state(DriverShiftStates.get_translate_location)
    await message.answer(**GetDriverLocationMessage().pack())


@router.message(DriverShiftStates.get_translate_location, or_f(F.location, F.text))
async def go_to_shift(
    message: Message, state: FSMContext, auth_session: AuthSession
) -> None:
    if message.text:
        await message.delete()
        return

    mediator = get_mediator()

    command = DriverGoToShiftCommand(
        current_user_id=auth_session.user_id,
        driver_id=auth_session.user_id,
        location=(message.location.latitude, message.location.longitude),
    )
    driver = await mediator.handle(command)

    await state.update_data(
        current_location=(
            message.location.longitude,  # type: ignore
            message.location.latitude,  # type: ignore
        ),
        last_location=(
            message.location.longitude,  # type: ignore
            message.location.latitude,  # type: ignore
        ),
    )
    await message.answer(**SucessfulShiftDeparture(driver).pack())
    await state.clear()


@router.callback_query(
    DriverShiftStates.get_translate_location, F.data == "driver:go_to_shift:cancel"
)
async def cancel_driver_go_to_shift(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.edit_text(**CancelDriverGoToShiftMessage().pack())


# ВЫХОД СО СМЕНЫ
@router.message(F.text == "🔴 Уйти с линии")
async def driver_exit_from_line(message: Message, auth_session: AuthSession) -> None:
    await message.delete()

    mediator = get_mediator()
    command = DriverExitFromShiftCommand(
        current_user_id=auth_session.user_id, driver_id=auth_session.user_id
    )
    driver = await mediator.handle(command)

    await message.answer(**SucessfulDriverEndShiftMessage(driver).pack())


# ОТСЛЕЖИВАНИЕ ЛОКАЦИИ
@router.edited_message(F.location)
async def update_live_location_driver(
    message: Message, state: FSMContext, auth_session: AuthSession
) -> None:
    # Получаем текущие данные из состояния
    data = await state.get_data()

    # Инициализация начальных значений, если их нет
    if "current_location" not in data:
        await state.update_data(
            current_location=(
                message.location.longitude,  # type: ignore
                message.location.latitude,  # type: ignore
            ),
            last_location=(
                message.location.longitude,  # type: ignore
                message.location.latitude,  # type: ignore
            ),
        )
    else:
        # Получаем предыдущую и новую локации
        current_location = (
            message.location.longitude,  # type: ignore
            message.location.latitude,  # type: ignore
        )
        last_location = data[
            "current_location"
        ]  # Берем предыдущую локацию из состояния

        # Вычисляем расстояние между текущей и предыдущей локацией
        # distance = calculate_distance(
        #     last_location[0], last_location[1], current_location[0], current_location[1]
        # )

        # # Если расстояние меньше 10 метров, ничего не делаем
        # if distance < 1:
        #     return

        mediator = get_mediator()

        command = UpdateDriverLocationCommand(
            current_user_id=auth_session.user_id,
            driver_id=auth_session.user_id,
            location=current_location,
        )
        await mediator.handle(command)

        await state.update_data(
            current_location=current_location,
            last_location=last_location,
        )
