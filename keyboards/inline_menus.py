# keyboards/inline_menus.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from enum import Enum

class CallbackData(Enum):
    HEROES = "menu_heroes"
    GUIDES = "menu_guides"
    BUILDS = "menu_builds"
    STATISTICS = "menu_statistics"
    BACK = "menu_back"
    # Додайте інші необхідні CallbackData

def get_generic_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Створює базову інлайн-клавіатуру для головного меню.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🛡️ Персонажі", callback_data=CallbackData.HEROES.value),
            InlineKeyboardButton(text="📚 Гайди", callback_data=CallbackData.GUIDES.value)
        ],
        [
            InlineKeyboardButton(text="⚜️ Білди", callback_data=CallbackData.BUILDS.value),
            InlineKeyboardButton(text="📈 Статистика", callback_data=CallbackData.STATISTICS.value)
        ],
        [
            InlineKeyboardButton(text="🔄 Назад", callback_data=CallbackData.BACK.value)
        ]
    ])
