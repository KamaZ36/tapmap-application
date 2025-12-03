from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey


from app.core.dependencies.tg_bots import (
    DriverDispatcher,
    DriverTgBot,
)


def get_user_fsm_context(
    dp: DriverDispatcher, bot: DriverTgBot, tg_id: int
) -> FSMContext:
    storage_key = StorageKey(bot_id=bot.id, chat_id=tg_id, user_id=tg_id)
    return FSMContext(storage=dp.storage, key=storage_key)
