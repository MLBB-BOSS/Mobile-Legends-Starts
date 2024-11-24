from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def main_menu_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    
    builder.row(
        KeyboardButton(text="🦸‍♂️ Герої"),
        KeyboardButton(text="📊 Статистика")
    )
    
    builder.row(
        KeyboardButton(text="ℹ️ Інформація"),
        KeyboardButton(text="⚙️ Налаштування")
    )

    return builder.as_markup(
        resize_keyboard=True,
        one_time_keyboard=False
    )
