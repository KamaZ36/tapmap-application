import asyncio

from app.core.dependencies.tg_bots import DriverDispatcher, DriverTgBot
from app.core.dependencies import container

from app.bots.driver_tg_bot.init_dispatcher import init_bot


async def start_polling() -> None:
    await init_bot()

    bot = await container.get(DriverTgBot)
    dp = await container.get(DriverDispatcher)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(start_polling())
