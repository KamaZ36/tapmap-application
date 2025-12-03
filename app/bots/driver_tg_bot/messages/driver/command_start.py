from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from app.application.dtos.driver import DriverDTO
from app.bots.driver_tg_bot.keyboards.driver.main_menu import main_menu_keyboard
from app.bots.driver_tg_bot.messages.base import BaseMessage


class WelcomeMessage(BaseMessage):
    _text = "👋 Привет, водитель!\n\nРад видеть вас в нашем такси-сервисе!"

    def __init__(self, driver: DriverDTO) -> None:
        self.driver = driver

    @property
    def reply_markup(self) -> ReplyKeyboardMarkup:
        return main_menu_keyboard(self.driver)
