from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from app.application.dtos.driver import DriverDTO


def main_menu_keyboard(driver: DriverDTO) -> ReplyKeyboardMarkup:
    keyboard = [
        [
            KeyboardButton(
                text=f"{'🔴 Уйти с линии' if driver.on_shift else '🟢 Выйти на линию'}"
            )
        ],
        [KeyboardButton(text="👤 Профиль")],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
