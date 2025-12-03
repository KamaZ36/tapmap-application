from aiogram.types import InlineKeyboardButton


def inline_back_button(callback_data: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text="◀️ Назад", callback_data=callback_data)


def inline_cancel_button(callback_data: str) -> InlineKeyboardButton:
    return InlineKeyboardButton(text="Отмена", callback_data=callback_data)
