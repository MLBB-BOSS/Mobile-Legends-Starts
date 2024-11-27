# keyboards/inline_menus.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from enum import Enum

class CallbackData(Enum):
    HEROES = "menu_heroes"
    GUIDES = "menu_guides"
    BUILDS = "menu_builds"
    STATISTICS = "menu_statistics"
    BACK = "menu_back"

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

def get_hero_class_inline_keyboard(hero_class: str) -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру для вибору героя з певного класу.
    
    :param hero_class: Клас героя (наприклад, "Танк", "Маг" і т.д.)
    :return: InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"🔍 {hero_class} 1", callback_data=f"hero_class_{hero_class.lower()}_1"),
            InlineKeyboardButton(text=f"🔍 {hero_class} 2", callback_data=f"hero_class_{hero_class.lower()}_2")
        ],
        [
            InlineKeyboardButton(text="🔄 Назад", callback_data=CallbackData.BACK.value)
        ]
    ])
