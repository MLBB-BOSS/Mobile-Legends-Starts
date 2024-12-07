
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
    BACK = "🔙 Назад"
    BACK_TO_MAIN_MENU = "🔙 Меню"

# Функції для створення Reply Keyboards

def get_main_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(MenuButton.NAVIGATION.value), KeyboardButton(MenuButton.PROFILE.value)],
            [KeyboardButton(MenuButton.META.value), KeyboardButton(MenuButton.M6.value), KeyboardButton(MenuButton.GPT.value)],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_meta_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton('📈 Аналітика'), KeyboardButton('📊 Статистика'), KeyboardButton(MenuButton.BACK_TO_MAIN_MENU.value)],
        ],
        resize_keyboard=True
    )
    return keyboard
