from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def main_menu_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    
    builder.row(
        KeyboardButton(text="🧭 Навігація"),
        KeyboardButton(text="🪪 Мій профіль")
    )

    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )
