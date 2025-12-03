from uuid import UUID
from aiogram import Bot, Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter, or_f
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from app.application.exceptions.city import CityNotSupported
from app.application.exceptions.geolocation import (
    InaccurateAddress,
    InaccurateGeolocation,
)
from app.application.exceptions.order import OrderNotFound
from app.application.exceptions.user import NotSetBaseCityForUser
from app.application.commands.order.add_comment import (
    AddCommentToOrderCommand,
    AddCommentToOrderCommandHandler,
)
from app.application.commands.order.add_point import (
    AddPointToOrderCommand,
    AddPointToOrderCommandHandler,
)
from app.application.commands.order.confirm import (
    ConfirmOrderCommand,
    ConfirmOrderCommandHandler,
)
from app.application.commands.order.create import CreateOrderCommand
from app.core.mediator import get_mediator
from app.application.queries.order.get_active_for_customer import (
    GetActiveOrderForCustomerQuery,
)
from app.application.queries.order.get_order_by_id import (
    GetOrderByIdQuery,
    GetOrderByIdQueryHandler,
)
from app.bots.user_tg_bot.dtos.auth_session import AuthSession
from app.bots.user_tg_bot.messages.errors import CityNotSupportedMessage
from app.bots.user_tg_bot.messages.user.order import OrderPanelMessage
from app.core.dependencies import container

from app.domain.enums.order_status import OrderStatus
from app.infrastructure.repositories.tg_bot_session.base import (
    BaseTgBotSessionRepository,
)
from app.bots.user_tg_bot.messages.user.create_order import (
    AskEndPointForOrderMessage,
    AskStartPointForOrderMessage,
    CityNotSpecifiedWarningMessage,
    GetCommentToOrderMessage,
    GetPointMessage,
    InaccurateAddressErrorMessage,
    InaccurateGeolocationErrorMessage,
    ThereIsAnActiveDraftOrderMessage,
)
from app.bots.user_tg_bot.states.user import UserCreateOrderStates


router = Router()


@router.message(StateFilter(None), F.text == "Вызвать такси 🚕")
async def start_create_order(
    message: Message, state: FSMContext, auth_session: AuthSession
) -> None:
    await message.delete()
    mediator = get_mediator()

    try:
        query = GetActiveOrderForCustomerQuery(
            customer_id=auth_session.user_id, current_user_id=auth_session.user_id
        )
        order = await mediator.handle(query)

        if order.status == OrderStatus.draft:
            await message.answer(**ThereIsAnActiveDraftOrderMessage().pack())
        order_msg = await message.answer(**OrderPanelMessage(order).pack())
        await state.update_data(
            order_msg_id=order_msg.message_id, order_id=str(order.id)
        )
    except OrderNotFound:
        msg = await message.answer(**AskStartPointForOrderMessage().pack())
        await state.set_state(UserCreateOrderStates.get_start_point)
        await state.update_data(msg_id=msg.message_id)


@router.message(UserCreateOrderStates.get_start_point, or_f(F.text, F.location))
async def get_start_point(
    message: Message, state: FSMContext, bot: Bot, auth_session: AuthSession
) -> None:
    prev_message_id = await state.get_value("msg_id")
    warning_msg_id = await state.get_value("warning_msg_id", None)
    try:
        if warning_msg_id:
            await bot.delete_message(
                chat_id=message.from_user.id, message_id=warning_msg_id
            )
    except TelegramBadRequest:
        pass

    if message.location:
        start_point = (message.location.latitude, message.location.longitude)
    elif message.text:
        start_point = message.text
    else:
        return

    mediator = get_mediator()

    command = CreateOrderCommand(
        current_user_id=auth_session.user_id,
        user_id=auth_session.user_id,
        start_point=start_point,
    )

    try:
        order = await mediator.handle(command)
    except NotSetBaseCityForUser:
        await message.delete()
        warning_msg = await message.answer(
            **CityNotSpecifiedWarningMessage(street=message.text).pack()
        )
        await state.update_data(warning_msg_id=warning_msg.message_id)
        return
    except CityNotSupported:
        await message.answer(**CityNotSupportedMessage().pack())
        await state.clear()
        return
    except InaccurateAddress as e:
        warning_msg = await message.answer(
            **InaccurateAddressErrorMessage(e.address).pack()
        )
        await state.update_data(warning_msg_id=warning_msg.message_id)
        return
    except InaccurateGeolocation as e:
        warning_msg = await message.answer(**InaccurateGeolocationErrorMessage().pack())
        await state.update_data(warning_msg_id=warning_msg.message_id)
        return

    current_message = await message.answer(
        **AskEndPointForOrderMessage(order.id).pack(),
    )
    if prev_message_id:
        await bot.edit_message_reply_markup(
            chat_id=message.from_user.id, message_id=prev_message_id, reply_markup=None
        )
    await state.set_state(UserCreateOrderStates.get_end_point)
    await state.update_data(msg_id=current_message.message_id, order_id=str(order.id))  # type: ignore


@router.message(UserCreateOrderStates.get_end_point, or_f(F.text, F.location))
async def get_end_point(message: Message, state: FSMContext, bot: Bot) -> None:
    warning_msg_id = await state.get_value("warning_msg_id", None)
    try:
        if warning_msg_id:
            await bot.delete_message(
                chat_id=message.from_user.id, message_id=warning_msg_id
            )
    except TelegramBadRequest:
        pass

    if message.location:
        end_point = (message.location.latitude, message.location.longitude)
    elif message.text:
        end_point = message.text
    else:
        return

    prev_message_id = await state.get_value("msg_id")
    order_id = await state.get_value("order_id")

    async with container() as req_container:
        auth_session_repository = await req_container.get(BaseTgBotSessionRepository)
        auth_session = await auth_session_repository.get_by_tg_id(message.from_user.id)  # type: ignore

        command = AddPointToOrderCommand(
            order_id=order_id, point=end_point, current_user_id=auth_session.user_id
        )
        add_point_to_order_interactor = await req_container.get(
            AddPointToOrderCommandHandler
        )
        try:
            order = await add_point_to_order_interactor(command=command)
        except InaccurateAddress as e:
            warning_msg = await message.answer(
                **InaccurateAddressErrorMessage(e.address).pack()
            )
            await state.update_data(warning_msg_id=warning_msg.message_id)
            return
        except InaccurateGeolocation as e:
            warning_msg = await message.answer(
                **InaccurateGeolocationErrorMessage().pack()
            )
            await state.update_data(warning_msg_id=warning_msg.message_id)
            return

    if prev_message_id:
        await bot.edit_message_reply_markup(
            chat_id=message.from_user.id, message_id=prev_message_id, reply_markup=None
        )
    order_msg = await message.answer(**OrderPanelMessage(order).pack())
    await state.set_state(None)
    await state.update_data(order_msg_id=order_msg.message_id)  # type: ignore


# ДОБАВЛЕНИЕ КОММЕНТАРИЯ К ЗАКАЗУ
@router.callback_query(F.data.startswith("draft_order:add_comment:"))
async def get_comment_to_order(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.data is None:
        return
    order_id = callback.data.replace("draft_order:add_comment:", "", 1)
    await state.set_state(UserCreateOrderStates.get_comment)
    msg = await callback.message.edit_text(  # type: ignore
        **GetCommentToOrderMessage(order_id).pack()
    )
    await state.update_data(msg_id=msg.message_id, order_id=order_id)  # type: ignore


@router.message(UserCreateOrderStates.get_comment, F.text)
async def set_comment_to_order(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.delete()

    order_msg_id = await state.get_value("order_msg_id")
    order_id = await state.get_value("order_id")
    if order_id is None or order_msg_id is None:
        return

    async with container() as req_container:
        auth_session_repository = await req_container.get(BaseTgBotSessionRepository)
        auth_session = await auth_session_repository.get_by_tg_id(message.from_user.id)

        command = AddCommentToOrderCommand(
            current_user_id=auth_session.user_id,
            order_id=order_id,
            comment=message.text,  # type: ignore
        )

        add_comment_to_order_interactor = await req_container.get(
            AddCommentToOrderCommandHandler
        )
        order = await add_comment_to_order_interactor(command=command)

    await state.set_state(None)
    order_msg = await bot.edit_message_text(
        **OrderPanelMessage(order).pack(),
        chat_id=message.from_user.id,  # type: ignore
        message_id=order_msg_id,
    )
    await state.update_data(order_msg_id=order_msg.message_id)


# ДОБАВЛЕНИЕ ТОЧКИ К ЗАКАЗУ
@router.callback_query(F.data.startswith("draft_order:add_point:"))
async def get_point(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.data is None:
        return
    order_id = callback.data.replace("draft_order:add_point:", "", 1)
    await state.set_state(UserCreateOrderStates.get_point)
    msg = await callback.message.edit_text(**GetPointMessage(order_id).pack())
    await state.update_data(msg_id=msg.message_id, order_id=order_id)  # type: ignore


@router.message(UserCreateOrderStates.get_point, or_f(F.text, F.location))
async def add_point_to_order(message: Message, state: FSMContext, bot: Bot) -> None:
    await message.delete()

    if message.location:
        point = (message.location.latitude, message.location.longitude)
    elif message.text:
        point = message.text
    else:
        return

    prev_message_id = await state.get_value("msg_id")
    order_id = await state.get_value("order_id")

    async with container() as req_container:
        auth_session_repository = await req_container.get(BaseTgBotSessionRepository)
        auth_session = await auth_session_repository.get_by_tg_id(message.from_user.id)  # type: ignore

        command = AddPointToOrderCommand(
            order_id=UUID(order_id), point=point, current_user_id=auth_session.user_id
        )
        create_order_interactor = await req_container.get(AddPointToOrderCommandHandler)
        order = await create_order_interactor(command=command)

    order_msg = await bot.edit_message_text(
        **OrderPanelMessage(order).pack(),
        chat_id=message.from_user.id,  # type: ignore
        message_id=prev_message_id,
    )
    await state.set_state(None)
    await state.update_data(order_msg_id=order_msg.message_id)  # type: ignore


# ПОДТВЕРЖДЕНИЕ ЗАКАЗА
@router.callback_query(F.data.startswith("draft_order:confirm:"))
async def confrim_draft_order(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.data is None:
        return
    order_id = callback.data.replace("draft_order:confirm:", "", 1)

    async with container() as req_container:
        auth_session_repo = await req_container.get(BaseTgBotSessionRepository)
        auth_session = await auth_session_repo.get_by_tg_id(callback.from_user.id)

        command = ConfirmOrderCommand(
            current_user_id=auth_session.user_id, order_id=UUID(order_id)
        )

        confirm_order_interactor = await req_container.get(ConfirmOrderCommandHandler)
        order = await confirm_order_interactor(command=command)

        order_msg = await callback.message.edit_text(**OrderPanelMessage(order).pack())
        await state.update_data(order_msg_id=order_msg.message_id)


# ВОЗВРАТ НАЗАД К ПАНЕЛИ ЗАКАЗА ИЗ ПУНКТОВ РЕДАКТИРОВАНИЯ ЗАКАЗОВ
@router.callback_query(F.data.startswith("draft_order:"))
async def draft_order_panel(callback: CallbackQuery, state: FSMContext) -> None:
    if callback.data is None:
        return
    order_id = callback.data.replace("draft_order:", "", 1)

    async with container() as req_container:
        auth_session_repository = await req_container.get(BaseTgBotSessionRepository)
        auth_session = await auth_session_repository.get_by_tg_id(callback.from_user.id)

        query = GetOrderByIdQuery(
            current_user_id=auth_session.user_id, order_id=UUID(order_id)
        )
        get_order_interactor = await req_container.get(GetOrderByIdQueryHandler)
        order = await get_order_interactor(query=query)

    await callback.message.edit_text(**OrderPanelMessage(order).pack())  # type: ignore
    await state.set_state(None)
