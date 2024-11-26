from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from .main_menu import create_buttons, create_keyboard

def get_navigation_keyboard() -> ReplyKeyboardMarkup:
    button_groups = [
        ["🥷 Персонажі", "⚙️ Білди", "📈 Мета"],
        ["📚 Гайди", "🏆 Турніри", "💡 Стратегії"],
        ["🎮 Механіки гри", "📢 Новини", "🔙 Назад"]
    ]
    return create_keyboard(button_groups)

def get_second_level_keyboard() -> ReplyKeyboardMarkup:
    button_groups = [
        ["🥷 Персонажі", "⚙️ Білди", "📈 Мета"],
        ["📚 Гайди", "🏆 Турніри", "💡 Стратегії"],
        ["🎮 Механіки гри", "📢 Новини", "🔙 Назад"]
    ]
    return create_keyboard(button_groups)

def get_guides_keyboard() -> ReplyKeyboardMarkup:
    button_groups = [
        ["🆕 Нові гайди", "⭐ Популярні гайди", "📘 Для початківців"],
        ["🧙 Просунуті техніки", "🛡️ Командні стратегії", "◀️ Назад до Навігації"]
    ]
    return create_keyboard(button_groups)

def get_counterpicks_keyboard() -> ReplyKeyboardMarkup:
    button_groups = [
        ["🔍 Пошук контр-піку", "📜 Список персонажів", "🏆 Топ контр-піки"],
        ["◀️ Назад до Навігації"]
    ]
    return create_keyboard(button_groups)

def get_builds_keyboard() -> ReplyKeyboardMarkup:
    button_groups = [
        ["🔧 Створити білд", "📄 Мої білди", "⭐ Популярні білди"],
        ["🔍 Порівняння білдів", "◀️ Назад до Навігації"]
    ]
    return create_keyboard(button_groups)

def get_characters_keyboard() -> ReplyKeyboardMarkup:
    button_groups = [
        ["🗡️ Бійці", "🏹 Стрільці", "🔮 Маги"],
        ["🛡️ Танки", "🏥 Саппорти", "⚔️ Гібриди"],
        ["🔥 Метові", "◀️ Назад до Навігації"]
    ]
    return create_keyboard(button_groups)

def get_voting_keyboard() -> ReplyKeyboardMarkup:
    button_groups = [
        ["🗳️ Нове голосування", "📊 Мої голосування", "⭐ Популярні голосування"],
        ["🔍 Пошук голосування", "◀️ Назад до Навігації"]
    ]
    return create_keyboard(button_groups)

def get_help_keyboard() -> ReplyKeyboardMarkup:
    button_groups = [
        ["❓ FAQ", "📞 Підтримка", "📝 Надіслати відгук"],
        ["◀️ Назад до Навігації"]
    ]
    return create_keyboard(button_groups)
