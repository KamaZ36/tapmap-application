from typing import Any
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.bots.user_tg_bot.keyboards.common.buttons import inline_back_button
from app.bots.user_tg_bot.messages.base import BaseMessage


class CreateDriverPanelMessage(BaseMessage):
    def __init__(self, driver_data: dict[str, Any]) -> None:
        self.driver_data = driver_data

    @property
    def text(self) -> str:
        text_lines = ["👤 *Информация о водителе* 👤\n"]

        text_lines.append(f"👤 Имя: {self.driver_data.get('first_name', 'Не указано')}")
        text_lines.append(
            f"📝 Фамилия: {self.driver_data.get('last_name', 'Не указана')}"
        )
        text_lines.append(
            f"🔸 Отчество: {self.driver_data.get('middle_name', 'Не указано')}"
        )

        if "user_id" in self.driver_data:
            text_lines.append(f"🆔 ID пользователя: {self.driver_data['user_id']}")
        else:
            text_lines.append("🆔 ID пользователя: Не указан")

        if "license_number" in self.driver_data:
            text_lines.append(f"📄 Номер прав: {self.driver_data['license_number']}")
        else:
            text_lines.append("📄 Номер прав: Не указан")

        if "phone_number" in self.driver_data:
            text_lines.append(f"📱 Телефон: {self.driver_data['phone_number']}")
        else:
            text_lines.append("📱 Телефон: Не указан")

        return "\n".join(text_lines)

    @property
    def reply_markup(self) -> Any:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="ID пользователя",
                        callback_data="admin:driver:add:set_user_id",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="👤 Имя", callback_data="admin:driver:add:set_first_name"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📝 Фамилия",
                        callback_data="admin:driver:add:set_last_name",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="🔸 Отчество",
                        callback_data="admin:driver:add:set_middle_name",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📄 Номер вод. прав",
                        callback_data="admin:driver:add:set_license_number",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="📱 Номер телефона",
                        callback_data="admin:driver:add:set_phone_number",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="✅ Подтвердить", callback_data="admin:driver:add:confirm"
                    )
                ],
                [inline_back_button(callback_data="admin:user:selected")],
            ]
        )


class GetDriverUserIdMessage(BaseMessage):
    _text = "Введите ID пользователя (UUID):"
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[inline_back_button(callback_data="admin:driver:add")]]
    )


class GetDriverFirstNameMessage(BaseMessage):
    _text = "Введите имя водителя:"
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[inline_back_button(callback_data="admin:driver:add")]]
    )


class GetDriverLastNameMessage(BaseMessage):
    _text = "Введите фамилию водителя:"
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[inline_back_button(callback_data="admin:driver:add")]]
    )


class GetDriverMiddleNameMessage(BaseMessage):
    _text = "Введите отчество водителя:"
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[inline_back_button(callback_data="admin:driver:add")]]
    )


class GetDriverLicenseMessage(BaseMessage):
    _text = "Введите номер водительского удостоверения:"
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[inline_back_button(callback_data="admin:driver:add")]]
    )


class GetDriverPhoneMessage(BaseMessage):
    _text = "Введите номер телефона водителя:"
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[inline_back_button(callback_data="admin:driver:add")]]
    )
