import asyncio

from app.core.dependencies.tg_bots import UserDispatcher, UserTgBot
from app.core.dependencies import container

from app.bots.user_tg_bot.init_dispatcher import init_bot


async def main() -> None:
    await init_bot()

    bot = await container.get(UserTgBot)
    dp = await container.get(UserDispatcher)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
