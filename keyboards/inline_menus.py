# keyboards/inline_menus.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from enum import Enum

class CallbackData(Enum):
    HEROES = "menu_heroes"
    GUIDES = "menu_guides"
    BUILDS = "menu_builds"
    STATISTICS = "menu_statistics"
    BACK = "menu_back"
    # Додайте інші callback data

def get_main_inline_keyboard():
    """Головне меню"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🛡️ Персонажі",
                callback_data=CallbackData.HEROES.value
            ),
            InlineKeyboardButton(
                text="📚 Гайди",
                callback_data=CallbackData.GUIDES.value
            ),
        ],
        [
            InlineKeyboardButton(
                text="⚔️ Білди",
                callback_data=CallbackData.BUILDS.value
            ),
            InlineKeyboardButton(
                text="📊 Статистика",
                callback_data=CallbackData.STATISTICS.value
            ),
        ],
    ])

def get_heroes_inline_keyboard():
    """Меню персонажів"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🛡️ Танки", callback_data="hero_class_tank"),
            InlineKeyboardButton(text="🗡️ Бійці", callback_data="hero_class_fighter"),
        ],
        [
            InlineKeyboardButton(text="🎯 Стрільці", callback_data="hero_class_marksman"),
            InlineKeyboardButton(text="🔮 Маги", callback_data="hero_class_mage"),
        ],
        [
            InlineKeyboardButton(text="🔄 Назад", callback_data=CallbackData.BACK.value),
        ],
    ])

# Додайте інші клавіатури для різних меню
