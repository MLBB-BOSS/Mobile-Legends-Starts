# UTC:21:03
# 2024-11-25
# keyboards/main_menu.py
# Author: MLBB-BOSS
# Description: Main menu keyboard layouts
# The era of artificial intelligence.

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def create_buttons(button_texts):
    return [KeyboardButton(text=text) for text in button_texts]

def create_keyboard(button_groups, placeholder="") -> ReplyKeyboardMarkup:
    buttons = [create_buttons(group) for group in button_groups]
    return ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder=placeholder
    )

def get_main_keyboard() -> ReplyKeyboardMarkup:
    buttons = create_buttons(["🧭 Навігація", "🪪 Профіль"])
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        input_field_placeholder="Виберіть опцію"
    )
    return keyboard

def get_profile_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        create_buttons(["📈 Статистика", "🏆 Досягнення", "💌 Зворотний Зв'язок"]),
        create_buttons(["⚙️ Налаштування", "❓ Допомога", "🔙 Назад до Головного"])
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Оберіть опцію профілю"
    )
    return keyboard

def get_guides_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        create_buttons(["🆕 Нові гайди", "🌟 Популярні гайди", "📘 Для початківців"]),
        create_buttons(["🧙 Просунуті техніки", "🛡️ Командні стратегії", "◀️ Назад до Навігації"])
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Оберіть розділ гайдів"
    )
    return keyboard

def get_counterpicks_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        create_buttons(["🔍 Пошук контр-піку", "📜 Список персонажів", "🏆 Топ контр-піки"]),
        create_buttons(["◀️ Назад до Навігації"])
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Оберіть опцію контр-піків"
    )
    return keyboard

def get_navigation_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        create_buttons(["🏠 Головне меню", "📖 Гайди", "⚔️ Контрпіки"]),
        create_buttons(["🔨 Білди", "🗳️ Голосування", "🆘 Допомога"])
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Оберіть опцію навігації"
    )
    return keyboard

def get_builds_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        create_buttons(["🔨 Створити білд", "📃 Мої білди", "🌟 Популярні білди"]),
        create_buttons(["🆚 Порівняння білдів", "◀️ Назад до Навігації"])
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Оберіть опцію білдів"
    )
    return keyboard

def get_voting_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        create_buttons(["📍 Поточні опитування", "🗳️ Мої голосування", "➕ Запропонувати тему"]),
        create_buttons(["◀️ Назад до Навігації"])
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Оберіть опцію голосування"
    )
    return keyboard  

def get_help_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        create_buttons(["📄 Інструкції", "❔ FAQ", "📞 Підтримка"]),
        create_buttons(["◀️ Назад до Навігації"])
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Оберіть розділ допомоги"
    )
    return keyboard
