from uuid import UUID
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def user_edit_order_keyboard(order_id: UUID) -> InlineKeyboardMarkup:
    order_id_str = str(order_id)

    button = [
        [
            InlineKeyboardButton(
                text="➕ Добавить точку",
                callback_data=f"draft_order:add_point:{order_id_str}",
            )
        ],
        [
            InlineKeyboardButton(
                text="✍️ Добавить комментарий водителю",
                callback_data=f"draft_order:add_comment:{order_id_str}",
            )
        ],
        [
            InlineKeyboardButton(
                text="✅ Подтвердить заказ",
                callback_data=f"draft_order:confirm:{order_id_str}",
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Отменить заказ",
                callback_data=f"draft_order:cancel:{order_id_str}",
            )
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=button, resize_keyboard=True)
