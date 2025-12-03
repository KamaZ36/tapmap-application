from datetime import datetime
from typing import Any
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.domain.enums.user import UserRole
from app.bots.user_tg_bot.keyboards.common.buttons import inline_back_button
from app.bots.user_tg_bot.messages.base import BaseMessage


class AdminSelectedUserPanelMessage(BaseMessage):
    def __init__(self, user_data: dict[str, Any]) -> None:
        self.user_data = user_data

    @property
    def text(self) -> str:
        total_orders = (
            self.user_data["completed_orders_count"]
            + self.user_data["cancelled_orders_count"]
        )
        success_rate = (
            (self.user_data["completed_orders_count"] / total_orders * 100)
            if total_orders > 0
            else 0
        )

        def make_progress_bar(percent):
            filled = "█" * int(percent / 10)
            empty = "░" * (10 - len(filled))
            return f"{filled}{empty} {percent:.0f}%"

        # Добавляем информацию о блокировке
        blocking_info = ""
        if self.user_data.get("blocking"):
            from datetime import datetime

            # Проверяем не истекла ли блокировка
            is_active = (
                self.user_data["blocking"]["expires_at"] > datetime.now()
                if self.user_data["blocking"]["expires_at"]
                else True
            )

            if is_active:
                expires_str = self.user_data["blocking"]["expires_at"].strftime(
                    "%d.%m.%Y %H:%M"
                )
                blocking_info = (
                    f"\n\n🚫 <b>Активная блокировка</b>\n"
                    f"│\n"
                    f"├📝 Причина: {self.user_data['blocking']['reason']}\n"
                    f"└⏰ Истекает: {expires_str}"
                )
            else:
                return ""

        text = f"""
📌 Профиль {self.user_data["id"]}
│
├👤 Имя: {self.user_data["name"] or "Не указано"}
└📞 Телефон: `{self.user_data["phone_number"]}`

📊 Статистика заказов:
│
├ ✅ Завершено: {self.user_data["completed_orders_count"]}
├ ❌ Отменено: {self.user_data["cancelled_orders_count"]}
└ {"🟢" if success_rate > 70 else "🟡" if success_rate > 30 else "🔴"} {make_progress_bar(success_rate)}

📅 *Дата регистрации:* {self.user_data["created_at"]}
{blocking_info}
        """
        return text.strip()

    @property
    def reply_markup(self) -> Any:
        buttons = []

        if UserRole.driver not in self.user_data["roles"]:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="🚗 Сделать водителем",
                        callback_data="admin:user:selected:make_driver",
                    ),
                ],
            )

        is_blocked = self.user_data.get("blocking")

        if is_blocked:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="✅ Разблокировать",
                        callback_data="admin:user:selected:unblock",
                    ),
                ],
            )
        else:
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="🚫 Заблокировать",
                        callback_data="admin:user:selected:block",
                    ),
                ],
            )

        buttons.append([inline_back_button(callback_data="admin:user:search:methods")])
        return InlineKeyboardMarkup(inline_keyboard=buttons)
