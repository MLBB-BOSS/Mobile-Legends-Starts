# UTC:21:38
# 2024-11-25
# keyboards/navigation_menu.py
# Author: MLBB-BOSS
# Description: Navigation menu keyboard layouts
# The era of artificial intelligence.

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_navigation_keyboard() -> ReplyKeyboardMarkup:
    """Головне навігаційне меню"""
    buttons = [
        [
            KeyboardButton(text="🛡️ Персонажі"),
            KeyboardButton(text="📖 Гайди")
        ],
        [
            KeyboardButton(text="⚔️ Контр-піки"),
            KeyboardButton(text="🛠️ Білди")
        ],
        [
            KeyboardButton(text="📊 Голосування"),
            KeyboardButton(text="❓ Допомога")
        ],
        [KeyboardButton(text="🔙 Назад")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_characters_keyboard() -> ReplyKeyboardMarkup:
    """Меню персонажів"""
    buttons = [
        [
            KeyboardButton(text="🗡️ Бійці"),
            KeyboardButton(text="🏹 Стрільці")
        ],
        [
            KeyboardButton(text="🔮 Маги"),
            KeyboardButton(text="🛡️ Танки")
        ],
        [
            KeyboardButton(text="🏥 Саппорти"),
            KeyboardButton(text="⚔️ Гібриди")
        ],
        [KeyboardButton(text="🔥 Метові")],
        [KeyboardButton(text="◀️ Назад до Навігації")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_guides_keyboard() -> ReplyKeyboardMarkup:
    """Меню гайдів"""
    buttons = [
        [
            KeyboardButton(text="🆕 Нові гайди"),
            KeyboardButton(text="🌟 Популярні гайди")
        ],
        [
            KeyboardButton(text="📘 Для початківців"),
            KeyboardButton(text="🧙 Просунуті техніки")
        ],
        [KeyboardButton(text="🛡️ Командні стратегії")],
        [KeyboardButton(text="◀️ Назад до Навігації")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_counterpicks_keyboard() -> ReplyKeyboardMarkup:
    """Меню контр-піків"""
    buttons = [
        [
            KeyboardButton(text="🔍 Пошук контр-піку"),
            KeyboardButton(text="📜 Список персонажів")
        ],
        [KeyboardButton(text="🏆 Топ контр-піки")],
        [KeyboardButton(text="◀️ Назад до Навігації")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_builds_keyboard() -> ReplyKeyboardMarkup:
    """Меню білдів"""
    buttons = [
        [
            KeyboardButton(text="🔨 Створити білд"),
            KeyboardButton(text="📃 Мої білди")
        ],
        [
            KeyboardButton(text="🌟 Популярні білди"),
            KeyboardButton(text="🆚 Порівняння білдів")
        ],
        [KeyboardButton(text="◀️ Назад до Навігації")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_voting_keyboard() -> ReplyKeyboardMarkup:
    """Меню голосування"""
    buttons = [
        [
            KeyboardButton(text="📍 Поточні опитування"),
            KeyboardButton(text="🗳️ Мої голосування")
        ],
        [KeyboardButton(text="➕ Запропонувати тему")],
        [KeyboardButton(text="◀️ Назад до Навігації")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

def get_help_keyboard() -> ReplyKeyboardMarkup:
    """Меню допомоги"""
    buttons = [
        [
            KeyboardButton(text="📄 Інструкції"),
            KeyboardButton(text="❔ FAQ")
        ],
        [KeyboardButton(text="📞 Підтримка")],
        [KeyboardButton(text="◀️ Назад до Навігації")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
