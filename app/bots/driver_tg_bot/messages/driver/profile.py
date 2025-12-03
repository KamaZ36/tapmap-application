from app.domain.entities.driver import Driver
from app.domain.enums.driver_status import DriverStatus

from app.bots.driver_tg_bot.messages.base import BaseMessage


class DriverProfileMessage(BaseMessage):
    def __init__(self, driver: Driver) -> None:
        self.driver = driver

    @property
    def text(self) -> str:
        # Формируем ФИО
        full_name = f"{self.driver.last_name} {self.driver.first_name}"
        if self.driver.middle_name:
            full_name += f" {self.driver.middle_name}"

        # Статусы
        on_shift_status = "🟢 На смене" if self.driver.on_shift else "🔴 Не на смене"
        on_order_status = "🚗 На заказе" if self.driver.on_order else "✅ Свободен"
        status_text = {
            DriverStatus.active: "✅ Активен",
            DriverStatus.inactive: "⏸️ Неактивен",
            DriverStatus.banned: "🚫 Заблокирован",
        }.get(self.driver.status, self.driver.status.value)

        # Рейтинг отмен
        total_orders = (
            self.driver.completed_orders_count + self.driver.cancelled_orders_count
        )
        cancellation_rate = 0
        if total_orders > 0:
            cancellation_rate = round(
                (self.driver.cancelled_orders_count / total_orders) * 100, 1
            )

        return f"""
<b>👨‍💼 Профиль водителя</b>

<b>📝 Личные данные:</b>
• <b>ФИО:</b> <code>{full_name}</code>
• <b>Телефон:</b> <code>{self.driver.phone_number}</code>
• <b>Номер прав:</b> <code>{self.driver.license_number}</code>

<b>📊 Статистика:</b>
• <b>Выполнено поездок:</b> {self.driver.completed_orders_count}
• <b>Отменено заказов:</b> {self.driver.cancelled_orders_count}
• <b>Рейтинг отмен:</b> {cancellation_rate}%

<b>📍 Текущий статус:</b>
• <b>Активность:</b> {status_text}
• <b>Смена:</b> {on_shift_status}
• <b>На заказе:</b> {on_order_status}

<b>ID водителя:</b> <code>{self.driver.id}</code>

<i>Для изменения данных обратитесь к администратору</i>
""".strip()
