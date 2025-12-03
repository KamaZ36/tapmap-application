from typing import Any
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.bots.user_tg_bot.keyboards.common.buttons import (
    inline_back_button,
)
from app.bots.user_tg_bot.messages.base import BaseMessage


class CreateCityPanelMessage(BaseMessage):
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📍 Название города", callback_data="admin:city:add:set_name"
                )
            ],
            [
                InlineKeyboardButton(
                    text="🏛️ Область города", callback_data="admin:city:add:set_state"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💰 Базовая цена",
                    callback_data="admin:city:add:set_base_price",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🚗 Цена за километр",
                    callback_data="admin:city:add:set_price_per_km",
                )
            ],
            [
                InlineKeyboardButton(
                    text="💼 Коммиссия сервиса",
                    callback_data="admin:city:add:set_service_commission",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🗺️ Координаты полигона",
                    callback_data="admin:city:add:set_polygon_coords",
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Подтвердить", callback_data="admin:city:add:confirm"
                )
            ],
            [inline_back_button(callback_data="admin:city")],
        ]
    )

    def __init__(self, city_data: dict[str, Any]) -> None:
        self.city_data = city_data

    @property
    def text(self) -> str:
        text_lines = ["🏙️ *Информация о городе* 🏙️\n"]

        text_lines.append(f"📍 Город: {self.city_data.get('name', 'Не указан')}")
        text_lines.append(
            f"🏛️ Регион/Область: {self.city_data.get('state', 'Не указан')}"
        )

        if "base_price" in self.city_data:
            text_lines.append(f"💰 Базовая цена: {self.city_data['base_price']} ₽")
        else:
            text_lines.append("💰 Базовая цена: Не указана")

        if "price_per_kilometer" in self.city_data:
            text_lines.append(
                f"🚗 Цена за км: {self.city_data['price_per_kilometer']} ₽/км"
            )
        else:
            text_lines.append("🚗 Цена за км: Не указана")

        if "service_commission_pct" in self.city_data:
            text_lines.append(
                f"💼 Комиссия сервиса: {self.city_data['service_commission_pct']}%"
            )
        else:
            text_lines.append("💼 Комиссия сервиса: Не указана")

        if "polygon_coords" in self.city_data and self.city_data["polygon_coords"]:
            coords_count = len(self.city_data["polygon_coords"])
            text_lines.append(f"🗺️ Точки полигона: {coords_count} точек")
        else:
            text_lines.append("🗺️ Точки полигона: Не указаны")

        return "\n".join(text_lines)


class GetCityNameMessage(BaseMessage):
    _text = "Введите название города: "
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[inline_back_button(callback_data="admin:city:add")]]
    )


class GetCityStateMessage(BaseMessage):
    _text = "Введите название области города: "
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[inline_back_button(callback_data="admin:city:add")]]
    )


class GetCityBasePriceMessage(BaseMessage):
    _text = "Введите начальную цену тарифа для города: "
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[inline_back_button(callback_data="admin:city:add")]]
    )


class GetCityPricePerKmMessage(BaseMessage):
    _text = "Введите цену за километр: "
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[inline_back_button(callback_data="admin:city:add")]]
    )


class GetCityServiceCommissionMessage(BaseMessage):
    _text = "Введите коммиссию сервиса: "
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[inline_back_button(callback_data="admin:city:add")]]
    )


class GetCityPolygonMessage(BaseMessage):
    _text = (
        "Введите координаты полигона в формате Python списка:\n"
        "Пример: [[55.7558, 37.6176], [55.7558, 37.6177], [55.7559, 37.6177]]"
    )
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[inline_back_button(callback_data="admin:city:add")]]
    )
