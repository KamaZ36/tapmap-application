from faststream.redis import RedisRouter

from app.bots.driver_tg_bot.messages.driver.cancel_order import (
    SuccessfulCancelOrderMessage,
)
from app.core.config import settings
from app.core.dependencies import container
from app.core.dependencies.tg_bots import DriverDispatcher, DriverTgBot
from app.infrastructure.repositories.tg_bot_session.base import (
    BaseTgBotSessionRepository,
)

from app.application.queries.order.get_order_by_id import (
    GetOrderByIdQuery,
    GetOrderByIdQueryHandler,
)

from app.bots.driver_tg_bot.consumer.schemas import (
    CancelOrderEventSchema,
    DriverAssignedToOrderEventSchema,
    UpdateOrderStatusEventSchema,
)
from app.bots.driver_tg_bot.utils.fsm_context import get_user_fsm_context
from app.bots.driver_tg_bot.messages.driver.order import OrderPanelMessage


router = RedisRouter()


@router.subscriber(channel=settings.driver_assigned_order_topic)
async def driver_assigned_to_order_handler(
    message: DriverAssignedToOrderEventSchema,
) -> None:
    bot = await container.get(DriverTgBot)
    dispatcher = await container.get(DriverDispatcher)

    async with container() as req_container:
        auth_session_repo = await req_container.get(BaseTgBotSessionRepository)
        auth_session = await auth_session_repo.get_by_user_id(message.driver_id)

        query = GetOrderByIdQuery(
            current_user_id=message.driver_id, order_id=message.order_id
        )
        get_order_interactor = await req_container.get(GetOrderByIdQueryHandler)
        order = await get_order_interactor(query=query)

    driver_context = get_user_fsm_context(
        dp=dispatcher, bot=bot, tg_id=auth_session.tg_id
    )

    order_msg = await bot.send_message(
        **OrderPanelMessage(order).pack(), chat_id=auth_session.tg_id
    )
    await driver_context.update_data(
        order_id=str(order.id), order_msg_id=order_msg.message_id
    )


@router.subscriber(channel=settings.order_status_update_topic)
async def update_order_status_handler(message: UpdateOrderStatusEventSchema) -> None:
    bot = await container.get(DriverTgBot)
    dispatcher = await container.get(DriverDispatcher)

    async with container() as req_container:
        auth_session_repo = await req_container.get(BaseTgBotSessionRepository)
        auth_session = await auth_session_repo.get_by_user_id(message.driver_id)

        query = GetOrderByIdQuery(
            current_user_id=message.driver_id, order_id=message.order_id
        )
        get_order_interactor = await req_container.get(GetOrderByIdQueryHandler)
        order = await get_order_interactor(query=query)

    driver_context = get_user_fsm_context(
        dp=dispatcher, bot=bot, tg_id=auth_session.tg_id
    )

    order_msg_id = await driver_context.get_value("order_msg_id")
    if order_msg_id:
        order_msg = await bot.edit_message_text(
            **OrderPanelMessage(order).pack(),
            chat_id=auth_session.tg_id,
            message_id=order_msg_id,
        )
    else:
        order_msg = await bot.send_message(
            **OrderPanelMessage(order).pack(),
            chat_id=auth_session.tg_id,
        )
    await driver_context.update_data(
        order_id=str(order.id), order_msg_id=order_msg.message_id
    )


@router.subscriber(channel=settings.order_cancel_topic)
async def cancel_order_handler(message: CancelOrderEventSchema) -> None:
    if message.driver_id is None:
        return None

    bot = await container.get(DriverTgBot)
    dispatcher = await container.get(DriverDispatcher)

    async with container() as req_container:
        auth_session_repo = await req_container.get(BaseTgBotSessionRepository)
        auth_session = await auth_session_repo.get_by_user_id(message.driver_id)

    driver_context = get_user_fsm_context(
        dp=dispatcher, bot=bot, tg_id=auth_session.tg_id
    )

    order_msg_id = await driver_context.get_value("order_msg_id", None)

    if order_msg_id:
        await bot.edit_message_reply_markup(
            reply_markup=None, message_id=order_msg_id, chat_id=auth_session.tg_id
        )
    await bot.send_message(
        **SuccessfulCancelOrderMessage(message.reason).pack(),
        chat_id=auth_session.tg_id,
    )
    await driver_context.clear()
