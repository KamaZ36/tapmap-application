from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bots.user_tg_bot.keyboards.common.buttons import inline_back_button
from app.bots.user_tg_bot.messages.base import BaseMessage


class SuccessfulCancelCreateOrderMessage(BaseMessage):
    _text = "✔️ Создание заказа отменено"


class SuccessfulCancelDraftOrderMessage(BaseMessage):
    _text = "✔️ Заказ отменен"


class GetCancelOrderReasonMessage(BaseMessage):
    _text = "📦 Опишите причину, почему вы отменяете заказ?"
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[inline_back_button(callback_data="user:order")]]
    )


class SuccessfulCancelOrderMessage(BaseMessage):
    def __init__(self, reason: str) -> None:
        self.reason = reason

    @property
    def text(self) -> str:
        return f"❌ Ваш заказ отменен с причиной: {self.reason}"
