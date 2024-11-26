# keyboards/main_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def create_buttons(button_texts):
    return [KeyboardButton(text=text) for text in button_texts]

def create_keyboard(button_groups, resize_keyboard=True, placeholder=None):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=resize_keyboard, input_field_placeholder=placeholder)
    for group in button_groups:
        keyboard.add(*create_buttons(group))
    return keyboard

def get_main_keyboard() -> ReplyKeyboardMarkup:
    button_groups = [["🧭 Навігація", "🪪 Профіль"]]
    return create_keyboard(button_groups, placeholder="Виберіть опцію")

def get_profile_keyboard() -> ReplyKeyboardMarkup:
    button_groups = [
        ["📈 Статистика", "🏆 Досягнення", "💌 Зворотний Зв'язок"],
        ["⚙️ Налаштування", "❓ Допомога", "🔙 Назад до Головного"]
    ]
    return create_keyboard(button_groups, placeholder="Оберіть опцію профілю")

def get_guides_keyboard() -> ReplyKeyboardMarkup:
    button_groups = [
        ["🆕 Нові гайди", "⭐ Популярні гайди", "📘 Для початківців"],
        ["🧙 Просунуті техніки", "🛡️ Командні стратегії", "◀️ Назад до Навігації"]
    ]
    return create_keyboard(button_groups, placeholder="Оберіть розділ гайдів")

def get_counterpicks_keyboard() -> ReplyKeyboardMarkup:
    button_groups = [
        ["🔍 Пошук контр-піку", "📜 Список персонажів", "🏆 Топ контр-піки"],
        ["◀️ Назад до Навігації"]
    ]
    return create_keyboard(button_groups, placeholder="Оберіть опцію контр-піків")

def get_navigation_keyboard() -> ReplyKeyboardMarkup:
    button_groups = [
        ["🏠 Головне меню", "📚 Гайди", "⚔️ Контрпіки"],
        ["🔧 Білди", "📊 Голосування", "🆘 Допомога"]
    ]
    return create_keyboard(button_groups, placeholder="Оберіть опцію навігації")

def get_builds_keyboard() -> ReplyKeyboardMarkup:
    button_groups = [
        ["🔧 Створити білд", "📄 Мої білди", "⭐ Популярні білди"],
        ["🔍 Порівняння білдів", "◀️ Назад до Навігації"]
    ]
    return create_keyboard(button_groups, placeholder="Оберіть опцію білдів")

def get_voting_keyboard() -> ReplyKeyboardMarkup:
    button_groups = [
        ["📍 Поточні опитування", "🧾 Мої голосування", "➕ Запропонувати тему"],
        ["◀️ Назад до Навігації"]
    ]
    return create_keyboard(button_groups, placeholder="Оберіть опцію голосування")

def get_help_keyboard() -> ReplyKeyboardMarkup:
    button_groups = [
        ["📄 Інструкції", "❔ FAQ", "📞 Підтримка"],
        ["◀️ Назад до Навігації"]
    ]
    return create_keyboard(button_groups, placeholder="Оберіть розділ допомоги")
