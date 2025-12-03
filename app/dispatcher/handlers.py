from faststream.redis import RedisRouter

from app.dispatcher.schemas import OrderConfirmedEvent

from app.core.config import settings
from app.core.dependencies import container

from app.application.commands.order.process_order import ProcessOrderInteraction


router = RedisRouter()


@router.subscriber(channel=settings.order_confirmed_topic)
async def confirmed_order_handler(message: OrderConfirmedEvent) -> None:
    async with container() as req_container:
        order_processing_interactor = await req_container.get(ProcessOrderInteraction)
        await order_processing_interactor(message.order_id)
