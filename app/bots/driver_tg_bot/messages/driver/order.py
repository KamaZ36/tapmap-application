from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.application.dtos.order import OrderDTO
from app.bots.driver_tg_bot.messages.base import BaseMessage
from app.domain.enums.order_status import OrderStatus


class OrderPanelMessage(BaseMessage):
    def __init__(self, order_dto: OrderDTO) -> None:
        self.order_dto = order_dto

    @property
    def text(self) -> str:
        sections = [
            self._get_header_section(),
            self._get_status_section(),
            self._get_customer_section(),
            self._get_route_section(),
            self._get_order_details_section(),
        ]

        if self.order_dto.comment:
            sections.append(self._get_comment_section())

        return "\n\n".join([section for section in sections if section])

    @property
    def reply_markup(self) -> InlineKeyboardMarkup:
        """Клавиатура для водителя в зависимости от статуса"""
        if self.order_dto.status == OrderStatus.waiting_driver:
            return InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="📍 Я на месте",
                            callback_data="driver:arrived",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="📞 Позвонить клиенту",
                            callback_data=f"driver:call_customer:{self.order_dto.customer.id}",
                        )
                    ],
                ]
            )
        elif self.order_dto.status == OrderStatus.driver_waiting_customer:
            return InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="👤 Клиент в машине",
                            callback_data="driver:pickup_customer",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="📞 Позвонить",
                            callback_data=f"driver:call_customer:{self.order_dto.customer.id}",
                        ),
                        InlineKeyboardButton(
                            text="💬 Написать",
                            callback_data=f"driver:message_customer:{self.order_dto.customer.id}",
                        ),
                    ],
                ]
            )
        elif self.order_dto.status == OrderStatus.processing:
            return InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="🏁 Завершить поездку",
                            callback_data="driver:complete_order",
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            text="🚨 Проблема с заказом",
                            callback_data=f"driver:report_issue:{self.order_dto.id}",
                        )
                    ],
                ]
            )
        else:
            return InlineKeyboardMarkup(inline_keyboard=[])

    def _get_header_section(self) -> str:
        return f"📦 <b>Заказ</b> #<code>{str(self.order_dto.id)}</code>"

    def _get_status_section(self) -> str:
        status_config = {
            OrderStatus.waiting_driver: {
                "icon": "🚗",
                "text": "Назначен вам",
                "description": f"Время подачи: ~{self.order_dto.feeding_time} мин",
            },
            OrderStatus.driver_waiting_customer: {
                "icon": "⏳",
                "text": "Ожидание клиента",
                "description": "Клиент выходит к вам",
            },
            OrderStatus.processing: {
                "icon": "🚗",
                "text": "В пути",
                "description": f"Время до прибытия: {self.order_dto.travel_time} мин",
            },
        }

        config = status_config.get(
            self.order_dto.status,
            {"icon": "📋", "text": self.order_dto.status.value, "description": ""},
        )

        return (
            f"{config['icon']} <b>Статус:</b> {config['text']}\n"
            f"   📝 {config['description']}"
        )

    def _get_customer_section(self) -> str:
        customer = self.order_dto.customer
        return (
            "👤 <b>Клиент:</b>\n"
            f"   ├─ <b>Имя:</b> {customer.name}\n"
            f"   └─ <b>Телефон:</b> {customer.phone_number}\n"
        )

    def _get_route_section(self) -> str:
        route_points = []
        for i, point in enumerate(self.order_dto.points):
            if i == 0:
                icon = "🚩"
                label = "Точка подачи"
            elif i == len(self.order_dto.points) - 1:
                icon = "🏁"
                label = "Пункт назначения"
            else:
                icon = "📍"
                label = f"Остановка {i}"

            route_points.append(f"{icon} <b>{label}:</b>\n   └─ {point.address}")

        return "🛣️ <b>Маршрут:</b>\n" + "\n".join(route_points)

    def _get_order_details_section(self) -> str:
        details = [
            "💰 <b>Финансы:</b>",
            f"   💵 <b>Стоимость поездки:</b> {self.order_dto.price} ₽",
            f"   📊 <b>Комиссия сервиса:</b> {self.order_dto.service_commission} ₽",
            f"   🤑 <b>Ваш заработок:</b> {self._calculate_driver_earnings()} ₽",
            "",
            "📊 <b>Детали поездки:</b>",
            f"   🛣️ <b>Дистанция:</b> {self.order_dto.travel_distance / 1000:.1f} км",
            f"   ⏱️ <b>Время:</b> {self.order_dto.travel_time} мин",
        ]

        if self.order_dto.feeding_distance:
            details.extend(
                [
                    f"   📍 <b>Расстояние до клиента:</b> {self.order_dto.feeding_distance / 1000:.1f} км",
                    f"   ⏰ <b>Время подачи:</b> {self.order_dto.feeding_time} мин",
                ]
            )

        return "\n".join(details)

    def _get_comment_section(self) -> str:
        return f"💭 <b>Комментарий клиента:</b>\n   └─ {self.order_dto.comment}"

    def _calculate_driver_earnings(self) -> str:
        # Расчет заработка водителя
        try:
            price = float(self.order_dto.price.replace(" ₽", "").replace(" ", ""))
            commission = float(
                self.order_dto.service_commission.replace(" ₽", "").replace(" ", "")
            )
            earnings = price - commission
            return f"{earnings:.0f}"
        except:
            return "расчет"
