from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bots.user_tg_bot.keyboards.common.buttons import inline_back_button
from app.bots.user_tg_bot.messages.base import BaseMessage


class UserSearchPanelMessage(BaseMessage):
    _text = "🔍 *Поиск пользователей*\n\nВыберите способ поиска:"
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📱 По номеру телефона",
                    callback_data="admin:user:search:by_phone",
                )
            ],
            [
                InlineKeyboardButton(
                    text="#️⃣ По ID", callback_data="admin:user:search:by_id"
                )
            ],
            [inline_back_button(callback_data="admin:user")],
        ]
    )


class GetPhoneNumberMessage(BaseMessage):
    _text = "Введите номер телефона: "
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [inline_back_button(callback_data="admin:user:search:methods")]
        ]
    )


class GetUserIdMessage(BaseMessage):
    _text = "Введите ид пользователя: "
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [inline_back_button(callback_data="admin:user:search:methods")]
        ]
    )


class UserNotFoundMessage(BaseMessage):
    _text = "Пользователь не найден"
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [inline_back_button(callback_data="admin:user:search:methods")]
        ]
    )
