from faststream.redis import RedisRouter

from app.application.queries.order.get_order_by_id import (
    GetOrderByIdQuery,
    GetOrderByIdQueryHandler,
)
from app.bots.user_tg_bot.messages.user.cancel_order import SuccessfulCancelOrderMessage
from app.core.config import settings
from app.core.dependencies import container
from app.core.dependencies.tg_bots import UserDispatcher, UserTgBot

from app.domain.enums.order_status import OrderStatus
from app.infrastructure.repositories.tg_bot_session.base import (
    BaseTgBotSessionRepository,
)
from app.bots.user_tg_bot.consumer.schemas import (
    CancelOrderEventSchema,
    DriverAssignedToOrderEventSchema,
    UpdateOrderStatusEventSchema,
)
from app.bots.user_tg_bot.messages.user.order import (
    DriverArrivedToStartPointNotificationMessage,
    DriverAssignedToOrderNotificationMessage,
    OrderCompleteNotificationMessage,
    OrderPanelMessage,
    OrderProcessStartNotificationMessage,
)
from app.bots.user_tg_bot.utils.fsm_context import get_user_fsm_context


router = RedisRouter()


@router.subscriber(channel=settings.driver_assigned_order_topic)
async def driver_assigned_to_order_event_handler(
    message: DriverAssignedToOrderEventSchema,
) -> None:
    dispatcher = await container.get(UserDispatcher)
    bot = await container.get(UserTgBot)

    async with container() as req_conatiner:
        auth_session_repository = await req_conatiner.get(BaseTgBotSessionRepository)

        auth_session = await auth_session_repository.get_by_user_id(message.customer_id)
        if auth_session is None:
            return

        query = GetOrderByIdQuery(
            current_user_id=auth_session.user_id, order_id=message.order_id
        )
        get_order_interactor = await req_conatiner.get(GetOrderByIdQueryHandler)
        order = await get_order_interactor(query=query)

    user_context = get_user_fsm_context(
        dp=dispatcher, bot=bot, tg_id=auth_session.tg_id
    )

    order_msg_id = await user_context.get_value("order_msg_id")

    if order_msg_id:
        await bot.edit_message_text(
            **OrderPanelMessage(order).pack(),
            chat_id=auth_session.tg_id,
            message_id=order_msg_id,
        )
    else:
        await bot.send_message(
            **OrderPanelMessage(order).pack(), chat_id=auth_session.tg_id
        )

    await bot.send_message(
        **DriverAssignedToOrderNotificationMessage().pack(), chat_id=auth_session.tg_id
    )


@router.subscriber(channel=settings.order_status_update_topic)
async def update_order_status_handler(message: UpdateOrderStatusEventSchema) -> None:
    bot = await container.get(UserTgBot)
    dp = await container.get(UserDispatcher)

    async with container() as req_container:
        auth_session_repo = await req_container.get(BaseTgBotSessionRepository)
        auth_session = await auth_session_repo.get_by_user_id(message.customer_id)

    if message.status == OrderStatus.driver_waiting_customer:
        content = DriverArrivedToStartPointNotificationMessage().pack()
    elif message.status == OrderStatus.processing:
        content = OrderProcessStartNotificationMessage().pack()
    elif message.status == OrderStatus.completed:
        user_context = get_user_fsm_context(dp=dp, bot=bot, tg_id=auth_session.tg_id)
        order_msg_id = await user_context.get_value("order_msg_id")
        if order_msg_id:
            await bot.edit_message_reply_markup(
                chat_id=auth_session.tg_id, message_id=order_msg_id, reply_markup=None
            )
        content = OrderCompleteNotificationMessage().pack()
    else:
        return

    await bot.send_message(**content, chat_id=auth_session.tg_id)


@router.subscriber(channel=settings.order_cancel_topic)
async def cancel_order_handler(message: CancelOrderEventSchema) -> None:
    bot = await container.get(UserTgBot)
    dispatcher = await container.get(UserDispatcher)

    async with container() as req_container:
        auth_session_repo = await req_container.get(BaseTgBotSessionRepository)
        auth_session = await auth_session_repo.get_by_user_id(message.customer_id)

    user_context = get_user_fsm_context(
        dp=dispatcher, bot=bot, tg_id=auth_session.tg_id
    )

    order_msg_id = await user_context.get_value("order_msg_id", None)

    if order_msg_id:
        await bot.edit_message_reply_markup(
            reply_markup=None, message_id=order_msg_id, chat_id=auth_session.tg_id
        )
    await bot.send_message(
        **SuccessfulCancelOrderMessage(message.reason).pack(),
        chat_id=auth_session.tg_id,
    )
    await user_context.clear()
