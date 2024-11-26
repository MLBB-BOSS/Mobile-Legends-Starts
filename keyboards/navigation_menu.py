from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_navigation_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="🏠 Головне меню"),
            KeyboardButton(text="📚 Гайди"),
            KeyboardButton(text="⚔️ Контрпіки")
        ],
        [
            KeyboardButton(text="🔧 Білди"),
            KeyboardButton(text="📊 Голосування"),
            KeyboardButton(text="🆘 Допомога")
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard

def get_guides_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="🆕 Нові гайди"),
            KeyboardButton(text="⭐ Популярні гайди"),
            KeyboardButton(text="📘 Для початківців")
        ],
        [
            KeyboardButton(text="🧙 Просунуті техніки"),
            KeyboardButton(text="🛡️ Командні стратегії"),
            KeyboardButton(text="◀️ Назад до Навігації")
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard

def get_counterpicks_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="🔍 Пошук контр-піку"),
            KeyboardButton(text="📜 Список персонажів"),
            KeyboardButton(text="🏆 Топ контр-піки")
        ],
        [KeyboardButton(text="◀️ Назад до Навігації")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard

def get_builds_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="🔧 Створити білд"),
            KeyboardButton(text="📄 Мої білди"),
            KeyboardButton(text="⭐ Популярні білди")
        ],
        [
            KeyboardButton(text="🔍 Порівняння білдів"),
            KeyboardButton(text="◀️ Назад до Навігації")
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard
