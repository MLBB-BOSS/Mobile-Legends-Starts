
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardRemove
)
from enum import Enum

# Визначення кнопок для Reply Keyboards
class MenuButton(Enum):
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Профіль"
    META = "🔥 META"
    M6 = "🏆 M6"
    GPT = "👾 GPT"
    BACK = "🔙"
    BACK_TO_MAIN_MENU = "🔙 Меню"

# Функції для створення Reply Keyboards

def get_main_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(MenuButton.NAVIGATION.value), KeyboardButton(MenuButton.PROFILE.value)],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_profile_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("📈 Статистика"), KeyboardButton("🏆 Досягнення"), KeyboardButton("⚙️ Налаштування")],
            [KeyboardButton("💌 Зворотний Зв'язок"), KeyboardButton("❓ Допомога"), KeyboardButton(MenuButton.BACK.value)],
        ],
        resize_keyboard=True
    )
    return keyboard
