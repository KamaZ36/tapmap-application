import logging

from app.bots.user_tg_bot.middlewares.auth_session_error import (
    AuthSessionMiddleware,
)
from app.core.dependencies import container

from app.bots.user_tg_bot.handlers.base import router as base_router

from app.bots.user_tg_bot.handlers.user import (
    command_start_router,
    create_order_router,
    cancel_order_router,
    user_profile_router,
    user_order_router,
)

from app.bots.user_tg_bot.handlers.admin import (
    admin_panel_router,
    create_city_router,
    create_driver_router,
    search_user_router,
    selected_user_router,
    block_user_router,
)

from app.core.dependencies.tg_bots import UserDispatcher


def add_middlewares() -> None:
    create_order_router.message.middleware(AuthSessionMiddleware())
    create_order_router.callback_query.middleware(AuthSessionMiddleware())

    cancel_order_router.message.middleware(AuthSessionMiddleware())
    cancel_order_router.callback_query.middleware(AuthSessionMiddleware())

    user_profile_router.message.middleware(AuthSessionMiddleware())
    user_profile_router.callback_query.middleware(AuthSessionMiddleware())


def add_routers(dp: UserDispatcher) -> None:
    dp.include_router(command_start_router)
    dp.include_router(cancel_order_router)
    dp.include_router(create_order_router)
    dp.include_router(user_profile_router)
    dp.include_router(user_order_router)

    dp.include_router(admin_panel_router)
    dp.include_router(create_city_router)
    dp.include_router(create_driver_router)
    dp.include_router(search_user_router)
    dp.include_router(selected_user_router)
    dp.include_router(block_user_router)

    dp.include_router(base_router)


async def init_bot() -> None:
    logging.basicConfig(level=logging.INFO)

    dp = await container.get(UserDispatcher)

    add_middlewares()
    add_routers(dp)
