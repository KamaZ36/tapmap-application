from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.enums import ParseMode

from app.application.dtos.user import UserDTO
from app.domain.entities.user import User

from app.bots.user_tg_bot.keyboards.common.buttons import inline_back_button
from app.bots.user_tg_bot.messages.base import BaseMessage


class ProfilePanelMessage(BaseMessage):
    def __init__(self, user: UserDTO) -> None:
        self.user = user

    @property
    def text(self) -> str:
        total_orders = (
            self.user.completed_orders_count + self.user.cancelled_orders_count
        )
        success_rate = (
            (self.user.completed_orders_count / total_orders * 100)
            if total_orders > 0
            else 0
        )

        def make_progress_bar(percent):
            filled = "█" * int(percent / 10)
            empty = "░" * (10 - len(filled))
            return f"{filled}{empty} {percent:.0f}%"

        # Формируем информацию о блокировке
        blocking_section = self._get_blocking_section()

        text = (
            "📌 Ваш профиль\n"
            "│\n"
            f"├👤 Имя: {self.user.name or 'Не указано'}\n"
            f"└📞 Телефон: <code>{self.user.phone_number}</code>\n\n"
            "📊 Статистика заказов:\n"
            "│\n"
            f"├ ✅ Завершено: {self.user.completed_orders_count}\n"
            f"├ ❌ Отменено: {self.user.cancelled_orders_count}\n"
            f"└ {'🟢' if success_rate > 70 else '🟡' if success_rate > 30 else '🔴'} {make_progress_bar(success_rate)}\n\n"
            f"📅 Дата регистрации: {self.user.created_at.strftime('%Y-%m-%d')}"
            f"{blocking_section}"
        )

        return text

    def _get_blocking_section(self) -> str:
        """Формирует секцию с информацией о блокировке"""
        if not self.user.blocking:
            return ""

        from datetime import datetime

        # Проверяем активна ли блокировка
        is_active = (
            self.user.blocking.expires_at > datetime.now()
            if self.user.blocking.expires_at
            else True
        )

        if is_active:
            expires_str = self.user.blocking.expires_at.strftime("%d.%m.%Y в %H:%M")
            days_left = (self.user.blocking.expires_at - datetime.now()).days

            days_text = f"({days_left} дн.)" if days_left > 0 else "(менее дня)"

            return (
                f"\n\n🚫 <b>Активная блокировка</b>\n"
                f"│\n"
                f"├📝 Причина: {self.user.blocking.reason}\n"
                f"├⏰ Истекает: {expires_str}\n"
                f"└📆 Осталось: {days_text}"
            )
        else:
            return ""


# СМЕНА ЛОКАЦИИ ПО УМОЛЧАНИЮ
class GetBaseLocationMessage(BaseMessage):
    _text = (
        "📍 *Отправьте вашу геолокацию*\n\n"
        "Нажмите на скрепочку 📎 рядом с полем ввода →\n "
        "Выберите «Геолокация» → \n"
        "«Отправить свою текущую геолокацию»\n\n"
        "Это нужно чтобы система узнала ваш город и автоматически добавляла его к адресам при заказе такси!"
    )
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[inline_back_button(callback_data="user:profile")]]
    )


class SuccessSetBaseLocationUserMessage(BaseMessage):
    _text = (
        "✅ Локация по умолчанию успешно установлена!\n\n"
        "Теперь вы можете заказывать такси, просто написав адрес текстом."
    )
