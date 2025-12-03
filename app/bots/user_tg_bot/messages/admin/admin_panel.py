from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bots.user_tg_bot.keyboards.common.buttons import inline_back_button
from app.bots.user_tg_bot.messages.base import BaseMessage


class AdminPanelMessage(BaseMessage):
    _text = "Админ-панель: "
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Управление пользователями", callback_data="admin:user"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Управление городами", callback_data="admin:city"
                )
            ],
            [
                InlineKeyboardButton(
                    text="Управление водителями", callback_data="admin:driver"
                )
            ],
        ]
    )


class AdminCityManagmentMessage(BaseMessage):
    _text = "Управление городами: "
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Добавить город", callback_data="admin:city:add"
                )
            ],
            [inline_back_button(callback_data="admin:admin_panel")],
        ]
    )


class AdminDriverManagementMessage(BaseMessage):
    _text = "Управление водителями: "
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Добавить водителя", callback_data="admin:driver:add"
                )
            ],
            [inline_back_button(callback_data="admin:admin_panel")],
        ]
    )


class AdminUserManagementMessage(BaseMessage):
    _text = "Управление пользователями: "
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Найти пользователя", callback_data="admin:user:search:methods"
                )
            ],
            [inline_back_button(callback_data="admin:admin_panel")],
        ]
    )
