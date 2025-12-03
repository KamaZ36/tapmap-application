from decimal import Decimal

from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.application.commands.city.create import (
    CreateCityCommand,
    CreateCityInteraction,
)
from app.core.dependencies import container
from app.infrastructure.repositories.tg_bot_session.base import (
    BaseTgBotSessionRepository,
)
from app.bots.user_tg_bot.messages.admin.admin_panel import AdminCityManagmentMessage
from app.bots.user_tg_bot.messages.admin.city.create_city import (
    CreateCityPanelMessage,
    GetCityBasePriceMessage,
    GetCityNameMessage,
    GetCityPolygonMessage,
    GetCityPricePerKmMessage,
    GetCityServiceCommissionMessage,
    GetCityStateMessage,
)
from app.bots.user_tg_bot.states.admin import AdminCreateCityStates


router = Router()


@router.callback_query(F.data == "admin:city:add")
async def start_create_city(callback: CallbackQuery, state: FSMContext) -> None:
    city_data = await state.get_value("city")
    if city_data is None:
        city_data = {}

    current_message = await callback.message.edit_text(
        **CreateCityPanelMessage(city_data).pack()
    )
    await state.update_data(msg_id=current_message.message_id, city=city_data)


# УСТАНОВКА НАЗВАНИЯ ГОРОДА
@router.callback_query(F.data == "admin:city:add:set_name")
async def get_name_handler(callback: CallbackQuery, state: FSMContext) -> None:
    msg = await callback.message.edit_text(**GetCityNameMessage().pack())
    await state.set_state(AdminCreateCityStates.get_city_name)
    await state.update_data(msg_id=msg.message_id)


@router.message(AdminCreateCityStates.get_city_name, F.text)
async def set_name(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.delete()

    city_data = await state.get_value("city")
    if city_data is None:
        return

    city_data["name"] = message.text

    msg_id = await state.get_value("msg_id")
    await bot.edit_message_text(
        **CreateCityPanelMessage(city_data).pack(),
        chat_id=message.from_user.id,
        message_id=msg_id,
    )
    await state.update_data(city=city_data)
    await state.set_state(None)


# УСТАНОВКА ШТАТА/ОБЛАСТИ
@router.callback_query(F.data == "admin:city:add:set_state")
async def get_state_handler(callback: CallbackQuery, state: FSMContext) -> None:
    msg = await callback.message.edit_text(**GetCityStateMessage().pack())
    await state.set_state(AdminCreateCityStates.get_city_state)
    await state.update_data(msg_id=msg.message_id)


@router.message(AdminCreateCityStates.get_city_state, F.text)
async def set_state(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.delete()

    city_data = await state.get_value("city")
    if city_data is None:
        return

    city_data["state"] = message.text

    msg_id = await state.get_value("msg_id")
    await bot.edit_message_text(
        **CreateCityPanelMessage(city_data).pack(),
        chat_id=message.from_user.id,
        message_id=msg_id,
    )
    await state.update_data(city=city_data)
    await state.set_state(None)


# УСТАНОВКА БАЗОВОЙ ЦЕНЫ
@router.callback_query(F.data == "admin:city:add:set_base_price")
async def get_base_price_handler(callback: CallbackQuery, state: FSMContext) -> None:
    msg = await callback.message.edit_text(**GetCityBasePriceMessage().pack())
    await state.set_state(AdminCreateCityStates.get_city_base_price)
    await state.update_data(msg_id=msg.message_id)


@router.message(AdminCreateCityStates.get_city_base_price, F.text)
async def set_base_price(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.delete()

    city_data = await state.get_value("city")
    if city_data is None:
        return

    city_data["base_price"] = Decimal(message.text)

    msg_id = await state.get_value("msg_id")
    await bot.edit_message_text(
        **CreateCityPanelMessage(city_data).pack(),
        chat_id=message.from_user.id,
        message_id=msg_id,
    )
    await state.update_data(city=city_data)
    await state.set_state(None)


# УСТАНОВКА ЦЕНЫ ЗА КИЛОМЕТР
@router.callback_query(F.data == "admin:city:add:set_price_per_km")
async def get_price_per_km_handler(callback: CallbackQuery, state: FSMContext) -> None:
    msg = await callback.message.edit_text(**GetCityPricePerKmMessage().pack())
    await state.set_state(AdminCreateCityStates.get_city_price_per_km)
    await state.update_data(msg_id=msg.message_id)


@router.message(AdminCreateCityStates.get_city_price_per_km, F.text)
async def set_price_per_km(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.delete()

    city_data = await state.get_value("city")
    if city_data is None:
        return

    city_data["price_per_kilometer"] = Decimal(message.text)

    msg_id = await state.get_value("msg_id")
    await bot.edit_message_text(
        **CreateCityPanelMessage(city_data).pack(),
        chat_id=message.from_user.id,
        message_id=msg_id,
    )
    await state.update_data(city=city_data)
    await state.set_state(None)


# УСТАНОВКА КОМИССИИ СЕРВИСА
@router.callback_query(F.data == "admin:city:add:set_service_commission")
async def get_service_commission_handler(
    callback: CallbackQuery, state: FSMContext
) -> None:
    msg = await callback.message.edit_text(**GetCityServiceCommissionMessage().pack())
    await state.set_state(AdminCreateCityStates.get_city_service_commission)
    await state.update_data(msg_id=msg.message_id)


@router.message(AdminCreateCityStates.get_city_service_commission, F.text)
async def set_service_commission(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.delete()

    city_data = await state.get_value("city")
    if city_data is None:
        return

    city_data["service_commission_pct"] = Decimal(message.text)

    msg_id = await state.get_value("msg_id")
    await bot.edit_message_text(
        **CreateCityPanelMessage(city_data).pack(),
        chat_id=message.from_user.id,
        message_id=msg_id,
    )
    await state.update_data(city=city_data)
    await state.set_state(None)


# УСТАНОВКА КОМИССИИ СЕРВИСА
@router.callback_query(F.data == "admin:city:add:set_polygon_coords")
async def get_polygon_coords_handler(
    callback: CallbackQuery, state: FSMContext
) -> None:
    msg = await callback.message.edit_text(**GetCityPolygonMessage().pack())
    await state.set_state(AdminCreateCityStates.get_city_polygon_coords)
    await state.update_data(msg_id=msg.message_id)


@router.message(AdminCreateCityStates.get_city_polygon_coords, F.text)
async def set_polygon_coords(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.delete()

    city_data = await state.get_value("city")
    if city_data is None:
        return

    import json

    coords_text = message.text.strip()

    polygon_coords: list[tuple[float, float]] = []

    try:
        coords_list = json.loads(coords_text)
        for coord in coords_list:
            if len(coord) == 2:
                polygon_coords.append((float(coord[0]), float(coord[1])))
    except:
        await message.answer("❌ Неверный формат координат")
        return

    city_data["polygon_coords"] = polygon_coords

    msg_id = await state.get_value("msg_id")
    await bot.edit_message_text(
        **CreateCityPanelMessage(city_data).pack(),
        chat_id=message.from_user.id,
        message_id=msg_id,
    )
    await state.update_data(city=city_data)
    await state.set_state(None)


# ПОДТВЕРДИТЬ СОЗДАНИЕ ГОРОДА
@router.callback_query(F.data == "admin:city:add:confirm")
async def confirm_create_city(callback: CallbackQuery, state: FSMContext) -> None:
    city_data = await state.get_value("city")
    if city_data is None:
        return

    async with container() as req_container:
        auth_session_repository = await req_container.get(BaseTgBotSessionRepository)
        auth_session = await auth_session_repository.get_by_tg_id(callback.from_user.id)

        try:
            command = CreateCityCommand(
                current_user_id=auth_session.user_id,
                name=city_data["name"],
                state=city_data["state"],
                base_price=city_data["base_price"],
                price_per_kilometer=city_data["price_per_kilometer"],
                service_commission=city_data["service_commission_pct"],
                polygon_coords=city_data["polygon_coords"],
            )
        except (KeyError, TypeError) as e:
            await callback.answer("❌ Заполните все поля города")
            return

        create_city_interactor = await req_container.get(CreateCityInteraction)
        await create_city_interactor(command=command)

    await state.clear()
    await callback.message.edit_text(**AdminCityManagmentMessage().pack())
