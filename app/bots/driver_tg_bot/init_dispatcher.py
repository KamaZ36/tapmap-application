import logging

from app.bots.driver_tg_bot.handlers.driver import (
    command_start_router,
    driver_shift_router,
    driver_profile_router,
    driver_order_router,
)

from app.bots.driver_tg_bot.middlewares.auth_session import AuthSessionMiddleware
from app.core.dependencies import container
from app.core.dependencies.tg_bots import DriverDispatcher


def add_middlewares(dp: DriverDispatcher) -> None:
    driver_shift_router.message.middleware(AuthSessionMiddleware())
    driver_shift_router.callback_query.middleware(AuthSessionMiddleware())

    driver_profile_router.message.middleware(AuthSessionMiddleware())
    driver_profile_router.callback_query.middleware(AuthSessionMiddleware())

    driver_order_router.callback_query.middleware(AuthSessionMiddleware())


def add_routers(dp: DriverDispatcher) -> None:
    dp.include_router(command_start_router)
    dp.include_router(driver_shift_router)
    dp.include_router(driver_profile_router)
    dp.include_router(driver_order_router)


async def init_bot() -> None:
    logging.basicConfig(level=logging.INFO)

    dp = await container.get(DriverDispatcher)

    add_routers(dp)
    add_middlewares(dp)
