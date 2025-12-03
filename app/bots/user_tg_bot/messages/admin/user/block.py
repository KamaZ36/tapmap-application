from typing import Any

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bots.user_tg_bot.keyboards.common.buttons import inline_back_button
from app.bots.user_tg_bot.messages.base import BaseMessage


class CreateUserBlockingMessage(BaseMessage):
    def __init__(self, blocking_data: dict[str, Any]) -> None:
        self.blocking_data = blocking_data

    @property
    def text(self) -> str:
        text_lines = ["🚫 *Информация о блокировке* 🚫\n"]

        text_lines.append(
            f"📝 Причина: {self.blocking_data.get('reason', 'Не указана')}"
        )
        text_lines.append(f"📅 Дней: {self.blocking_data.get('days', 0)}")
        text_lines.append(f"⏰ Часов: {self.blocking_data.get('hours', 0)}")
        text_lines.append(f"⏱️ Минут: {self.blocking_data.get('minutes', 0)}")

        return "\n".join(text_lines)

    @property
    def reply_markup(self) -> Any:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📝 Причина блокировки",
                        callback_data="admin:user_blocking:set_reason",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📅 Дни",
                        callback_data="admin:user_blocking:set_days",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⏰ Часы",
                        callback_data="admin:user_blocking:set_hours",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="⏱️ Минуты",
                        callback_data="admin:user_blocking:set_minutes",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="✅ Подтвердить блокировку",
                        callback_data="admin:user_blocking:confirm",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="❌ Отмена",
                        callback_data="admin:user:selected",
                    )
                ],
            ]
        )


class GetBlockingReasonMessage(BaseMessage):
    _text = "Введите причину блокировки: "
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[inline_back_button(callback_data="admin:user:selected")]]
    )


class GetBlockingDaysMessage(BaseMessage):
    _text = "Введите количество дней блокировки: "
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[inline_back_button(callback_data="admin:user:selected")]]
    )


class GetBlockingMinutesMessage(BaseMessage):
    _text = "Введите количество минут блокировки: "
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[inline_back_button(callback_data="admin:user:selected")]]
    )


class GetBlockingHoursMessage(BaseMessage):
    _text = "Введите количество часов блокировки: "
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[inline_back_button(callback_data="admin:user:selected")]]
    )
