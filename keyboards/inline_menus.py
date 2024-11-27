# keyboards/inline_menus.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from enum import Enum

class CallbackData(Enum):
    HEROES = "menu_heroes"
    GUIDES = "menu_guides"
    BUILDS = "menu_builds"
    STATISTICS = "menu_statistics"
    BACK = "menu_back"

def get_generic_inline_keyboard():
    """
    Створює базову інлайн-клавіатуру
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🛡️ Персонажі", callback_data=CallbackData.HEROES.value),
            InlineKeyboardButton(text="📚 Гайди", callback_data=CallbackData.GUIDES.value)
        ],
        [
            InlineKeyboardButton(text="⚔️ Білди", callback_data=CallbackData.BUILDS.value),
            InlineKeyboardButton(text="📊 Статистика", callback_data=CallbackData.STATISTICS.value)
        ],
        [
            InlineKeyboardButton(text="🔄 Назад", callback_data=CallbackData.BACK.value)
        ]
    ])

def get_main_inline_keyboard():
    """Альтернативна назва для get_generic_inline_keyboard"""
    return get_generic_inline_keyboard()

def get_heroes_inline_keyboard():
    """Клавіатура для меню героїв"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🛡️ Танки", callback_data="hero_class_tank"),
            InlineKeyboardButton(text="⚔️ Бійці", callback_data="hero_class_fighter")
        ],
        [
            InlineKeyboardButton(text="🎯 Стрільці", callback_data="hero_class_marksman"),
            InlineKeyboardButton(text="🔮 Маги", callback_data="hero_class_mage")
        ],
        [
            InlineKeyboardButton(text="🗡️ Асасини", callback_data="hero_class_assassin"),
            InlineKeyboardButton(text="💖 Сапорти", callback_data="hero_class_support")
        ],
        [
            InlineKeyboardButton(text="🔄 Назад", callback_data=CallbackData.BACK.value)
        ]
    ])

def get_guides_inline_keyboard():
    """Клавіатура для меню гайдів"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🎓 Базові механіки", callback_data="guide_basics"),
            InlineKeyboardButton(text="🏆 Мета", callback_data="guide_meta")
        ],
        [
            InlineKeyboardButton(text="🎯 Ролі", callback_data="guide_roles"),
            InlineKeyboardButton(text="⚔️ Контр-піки", callback_data="guide_counter")
        ],
        [
            InlineKeyboardButton(text="🔄 Назад", callback_data=CallbackData.BACK.value)
        ]
    ])

def get_builds_inline_keyboard():
    """Клавіатура для меню білдів"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📝 Створити білд", callback_data="build_create"),
            InlineKeyboardButton(text="📚 Мої білди", callback_data="build_my")
        ],
        [
            InlineKeyboardButton(text="🏆 Топ білдів", callback_data="build_top"),
            InlineKeyboardButton(text="🔍 Пошук білдів", callback_data="build_search")
        ],
        [
            InlineKeyboardButton(text="🔄 Назад", callback_data=CallbackData.BACK.value)
        ]
    ])

def get_statistics_inline_keyboard():
    """Клавіатура для меню статистики"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📊 Моя статистика", callback_data="stats_my"),
            InlineKeyboardButton(text="🏆 Рейтинг", callback_data="stats_rating")
        ],
        [
            InlineKeyboardButton(text="📈 Прогрес", callback_data="stats_progress"),
            InlineKeyboardButton(text="🎯 Досягнення", callback_data="stats_achievements")
        ],
        [
            InlineKeyboardButton(text="🔄 Назад", callback_data=CallbackData.BACK.value)
        ]
    ])
