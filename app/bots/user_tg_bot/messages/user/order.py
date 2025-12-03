from aiogram.types import InlineKeyboardMarkup

from app.bots.driver_tg_bot.keyboards.common.buttons import (
    inline_back_button,
    inline_cancel_button,
)
from app.domain.enums.order_status import OrderStatus

from app.application.dtos.order import OrderDTO

from app.bots.driver_tg_bot.messages.base import BaseMessage
from app.bots.user_tg_bot.keyboards.user.edit_order import user_edit_order_keyboard


class OrderPanelMessage(BaseMessage):
    def __init__(self, order_dto: OrderDTO) -> None:
        self.order_dto = order_dto

    @property
    def text(self) -> str:
        # Базовые секции которые есть всегда
        sections = [
            self._get_header_section(),
            self._get_status_section(),
            self._get_route_section(),
            self._get_order_details_section(),
        ]

        # Динамически добавляем секции в зависимости от статуса
        if self.order_dto.driver:
            sections.insert(2, self._get_driver_section())

        if self.order_dto.vehicle and self.order_dto.driver:
            sections.insert(3, self._get_vehicle_section())

        if self.order_dto.comment:
            sections.append(self._get_comment_section())

        # Фильтруем пустые секции и объединяем
        return "\n\n".join([section for section in sections if section])

    @property
    def reply_markup(self) -> InlineKeyboardMarkup:
        """Клавиатура зависит от статуса заказа"""
        if self.order_dto.status == OrderStatus.draft:
            return user_edit_order_keyboard(order_id=self.order_dto.id)
        elif self.order_dto.status in [
            OrderStatus.driver_search,
            OrderStatus.waiting_driver,
        ]:
            return InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        inline_cancel_button(
                            callback_data=f"order:cancel:{str(self.order_dto.id)}"
                        )
                    ]
                ]
            )
        else:
            # Для остальных статусов - пустая клавиатура
            return InlineKeyboardMarkup(inline_keyboard=[])

    def _get_header_section(self) -> str:
        return f"📦 <b>Заказ</b> #<code>{str(self.order_dto.id)}</code>"

    def _get_status_section(self) -> str:
        status_config = {
            OrderStatus.draft: {
                "icon": "✏️",
                "text": "Черновик",
                "description": "Вы можете редактировать детали заказа",
            },
            OrderStatus.driver_search: {
                "icon": "🔍",
                "text": "Ищем водителя",
                "description": "Подбираем ближайшего свободного водителя",
            },
            OrderStatus.waiting_driver: {
                "icon": "✅",
                "text": "Водитель найден",
                "description": f"Машина подъезжает, время подачи: ~{self.order_dto.feeding_time} мин",
            },
            OrderStatus.driver_waiting_customer: {
                "icon": "⏳",
                "text": "Водитель ожидает вас",
                "description": "Водитель прибыл к точке подачи",
            },
            OrderStatus.processing: {
                "icon": "🚗",
                "text": "В пути",
                "description": f"Примерное время до прибытия: {self.order_dto.travel_time} мин",
            },
            OrderStatus.completed: {
                "icon": "🏁",
                "text": "Завершен",
                "description": "Поездка успешно завершена",
            },
            OrderStatus.cancelled: {
                "icon": "❌",
                "text": "Отменен",
                "description": "Заказ отменен",
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

    def _get_driver_section(self) -> str:
        driver = self.order_dto.driver
        full_name = f"{driver.first_name}"
        if driver.middle_name:
            full_name += f" {driver.middle_name}"

        return (
            "👨‍💼 <b>Водитель:</b>\n"
            f"   ├─ <b>ФИО:</b> {full_name}\n"
            f"   └─ <b>Телефон:</b> {driver.phone_number}"
        )

    def _get_vehicle_section(self) -> str:
        vehicle = self.order_dto.vehicle
        return (
            "🚗 <b>Автомобиль:</b>\n"
            f"   ├─ <b>Марка:</b> {vehicle.brand} {vehicle.model}\n"
            f"   ├─ <b>Цвет:</b> {vehicle.color}\n"
            f"   └─ <b>Номер:</b> {vehicle.number}"
        )

    def _get_route_section(self) -> str:
        route_points = []
        for i, point in enumerate(self.order_dto.points):
            if i == 0:
                icon = "🚩"
                label = "Откуда"
            elif i == len(self.order_dto.points) - 1:
                icon = "🏁"
                label = "Куда"
            else:
                icon = "📍"
                label = f"Остановка {i}"

            route_points.append(f"{icon} <b>{label}:</b>\n   └─ {point.address}")

        return "🛣️ <b>Маршрут:</b>\n" + "\n".join(route_points)

    def _get_order_details_section(self) -> str:
        details = [
            "📊 <b>Детали поездки:</b>",
            f"   🛣️ <b>Дистанция:</b> {self.order_dto.travel_distance / 1000:.1f} км",
            f"   ⏱️ <b>Время:</b> {self.order_dto.travel_time} мин",
            f"   💰 <b>Стоимость:</b> {self.order_dto.price} ₽",
        ]

        if self.order_dto.feeding_distance and self.order_dto.status in [
            OrderStatus.waiting_driver,
            OrderStatus.driver_waiting_customer,
        ]:
            details.insert(
                3,
                f"   📍 <b>Расстояние подачи:</b> {self.order_dto.feeding_distance / 1000:.1f} км",
            )
            details.insert(
                4, f"   ⏰ <b>Время подачи:</b> {self.order_dto.feeding_time} мин"
            )

        return "\n".join(details)

    def _get_comment_section(self) -> str:
        return f"💭 <b>Комментарий к поездке:</b>\n   └─ {self.order_dto.comment}"


class GetCommentToOrderMessage(BaseMessage):
    _text = (
        "✍️ Добавьте комментарий для водителя\n\n"
        "Напишите дополнительную информацию, которая поможет водителю:\n"
        "— Особенности посадки 🚪 (например, «Заберите у второго подъезда»)\n"
        "— Детали маршрута 🛣 (например, «Заедем в магазин по пути»)\n"
        "— Дополнительные пожелания ✅ (например, «У меня будет багаж»)\n\n"
        "Отправьте ваш комментарий одним сообщением."
    )
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[inline_back_button(callback_data="draft_order")]]
    )


class DriverAssignedToOrderNotificationMessage(BaseMessage):
    _text = (
        "🎯 <b>Водитель назначен!</b>\n"
        "🚗 Машина уже в пути к вам\n\n"
        "📄 <b>Подробности в карточке заказа выше</b> 👆"
    )


class DriverArrivedToStartPointNotificationMessage(BaseMessage):
    _text = (
        "🚗 Водитель прибыл к точке подачи\n\nВаш водитель уже на месте и ожидает вас!"
    )


class OrderProcessStartNotificationMessage(BaseMessage):
    _text = "✨ Поездка началась\n\n🦺 Пристегните ремни безопасности"


class OrderCompleteNotificationMessage(BaseMessage):
    _text = "🎊 Поездка завершена!\n\nБлагодарим вас за выбор нашего сервиса!"
