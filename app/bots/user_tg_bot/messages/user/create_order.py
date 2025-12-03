from uuid import UUID
from aiogram.types import InlineKeyboardMarkup

from app.application.dtos.order import OrderDTO
from app.domain.entities.order import Order
from app.bots.user_tg_bot.keyboards.common.buttons import (
    inline_back_button,
    inline_cancel_button,
)
from app.bots.user_tg_bot.keyboards.user.edit_order import user_edit_order_keyboard
from app.bots.user_tg_bot.messages.base import BaseMessage
from app.domain.enums.order_status import OrderStatus


class AskStartPointForOrderMessage(BaseMessage):
    _text = (
        "<b>🚕 Откуда вас забрать?</b>\n\n"
        "1. <b>📎 Ручная геопозиция</b>\n"
        "→ Прикрепите точку на карте через скрепку\n\n"
        "2. <b>✏️ Текстовый адрес</b>\n"
        "→ Пример: '<code>Линейная 6</code>'"
    )
    _reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[[inline_cancel_button(callback_data="create_order:cancel:")]]
    )


class AskEndPointForOrderMessage(BaseMessage):
    _text = (
        "<b>🏁 Куда едем?</b>\n\n"
        "1. <b>📎 Ручная геопозиция</b>\n"
        "→ Прикрепите точку на карте через скрепку\n\n"
        "2. <b>✏️ Текстовый адрес</b>\n"
        "→ Пример: '<code>Линейная 6</code>'"
    )

    def __init__(self, order_id: UUID) -> None:
        self.order_id = str(order_id)

    @property
    def reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    inline_cancel_button(
                        callback_data=f"create_order:cancel:{self.order_id}"
                    )
                ]
            ]
        )


class EditDraftOrderPanelMessage(BaseMessage):
    def __init__(self, order: Order) -> None:
        self.order = order

    @property
    def text(self) -> str:
        route_points = []
        for i, point in enumerate(self.order.points):
            if i == 0:
                icon = "🚩"
                label = "Откуда"
            elif i == len(self.order.points) - 1:
                icon = "🏁"
                label = "Куда"
            else:
                icon = "📍"
                label = f"Остановка {i}"

            route_points.append(f"{icon} <b>{label}:</b>\n   └─ {point.address}")

        main_info = [
            f"📦 <b>Заказ</b> #<code>{str(self.order.id)}</code>",
            f"📋 <b>Статус:</b> {self._get_status_text()}",
            "",
            "📊 <b>Детали поездки:</b>",
            f"   🛣️ <b>Дистанция:</b> {self.order.travel_distance / 1000:.1f} км",
            f"   ⏱️ <b>Время:</b> {self.order.travel_time} мин",
            f"   💰 <b>Стоимость:</b> {self.order.price.value} ₽",
        ]

        if self.order.driver_id and self.order.status != OrderStatus.driver_search:
            driver_info = self._get_driver_info()
            if driver_info:
                main_info.insert(2, driver_info)

        comment_section = ""
        if self.order.comment:
            comment_section = (
                f"\n💭 <b>Комментарий к поездке:</b>\n   └─ {self.order.comment.text}"
            )

        return (
            "\n".join(main_info)
            + "\n\n"
            + "🛣️ <b>Маршрут:</b>\n"
            + "\n".join(route_points)
            + comment_section
        )

    @property
    def reply_markup(self) -> InlineKeyboardMarkup:
        if self.order.status == OrderStatus.draft:
            return user_edit_order_keyboard()
        else:
            return InlineKeyboardMarkup(
                inline_keyboard=[[inline_cancel_button(callback_data="order:cancel")]]
            )

    def _get_status_text(self) -> str:
        status_map = {
            OrderStatus.draft: "✏️ Черновик",
            OrderStatus.driver_search: "🔍 Ищем водителя",
            OrderStatus.waiting_driver: "✅ Водитель найден",
            OrderStatus.driver_waiting_customer: "⏳ Водитель ожидает вас",
            OrderStatus.processing: "🚗 В пути",
            OrderStatus.completed: "🏁 Завершен",
            OrderStatus.cancelled: "❌ Отменен",
        }
        return status_map.get(self.order.status, self.order.status.value)

    def _get_driver_info(self) -> str:
        """Информация о водителе в зависимости от статуса"""
        driver_status_map = {
            OrderStatus.waiting_driver: "подъезжает к вам",
            OrderStatus.driver_waiting_customer: "ожидает на точке подачи",
            OrderStatus.processing: "выполняет поездку",
        }
        status_text = driver_status_map.get(self.order.status)
        if status_text:
            return f"👤 <b>Водитель:</b> {status_text}"
        return ""


class GetCommentToOrderMessage(BaseMessage):
    _text = (
        "✍️ Добавьте комментарий для водителя\n\n"
        "Напишите дополнительную информацию, которая поможет водителю:\n"
        "— Особенности посадки 🚪 (например, «Заберите у второго подъезда»)\n"
        "— Детали маршрута 🛣 (например, «Заедем в магазин по пути»)\n"
        "— Дополнительные пожелания ✅ (например, «У меня будет багаж»)\n\n"
        "Отправьте ваш комментарий одним сообщением."
    )

    def __init__(self, order_id: str) -> None:
        self.order_id = order_id

    @property
    def reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [inline_back_button(callback_data=f"draft_order:{self.order_id}")]
            ]
        )


class GetPointMessage(BaseMessage):
    _text = (
        "<b>📍 Отправьте точку</b>\n\n"
        "1. <b>📎 Ручная геопозиция</b>\n"
        "→ Прикрепите точку на карте через скрепку\n\n"
        "2. <b>✏️ Текстовый адрес</b>\n"
        "Пример: '<code>Советская ул., 202А</code>'"
    )

    def __init__(self, order_id: str) -> None:
        self.order_id = order_id

    @property
    def reply_markup(self) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [inline_back_button(callback_data=f"draft_order:{self.order_id}")]
            ]
        )


class ThereIsAnActiveDraftOrderMessage(BaseMessage):
    _text = (
        "🚗 Нашли ваш незавершенный заказ!\n\n"
        "Можете продолжить его оформление или отменить и начать новый."
    )


class CityNotSpecifiedWarningMessage(BaseMessage):
    def __init__(self, street: str) -> None:
        self.street = street

    @property
    def text(self) -> str:
        return (
            "🏙️ Нужен город для первого заказа\n\n"
            f"Найдена улица: {self.street}\n"
            "Укажите город, например:\n"
            f"**Москва, {self.street}**\n\n"
            "Дальше будет проще — город запомним ✅\n\n"
            "---\n\n"
            "🔧 *Город указан, но не распознан? Сообщите нам!*"
        )


class InaccurateAddressErrorMessage(BaseMessage):
    def __init__(self, address: str) -> None:
        self._address = address

    @property
    def text(self) -> str:
        return (
            "🗺️ Адрес не распознан\n\n"
            f"Мы не смогли определить адрес: <code>{self._address}</code>.\n"
            "Пожалуйста, проверьте правильность его написания или прикрепите геолокацию.\n\n"
            "В случае, если адрес указан верно, свяжитесь с администратором."
        )


class InaccurateGeolocationErrorMessage(BaseMessage):
    _text = (
        "🗺️ Не удалось определить адрес по геолокации\n\n"
        "Мы не смогли определить адрес по отправленной геолокации.\n"
        "Пожалуйста, попробуйте отправить геолокацию еще раз или введите адрес вручную 📍\n\n"
        "В случае повторения проблемы, свяжитесь с администратором."
    )
