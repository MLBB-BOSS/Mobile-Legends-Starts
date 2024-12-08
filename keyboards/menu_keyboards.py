# keyboards/menus.py

from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardRemove
)
from enum import Enum
import logging

# Налаштування логування
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MenuButton(Enum):
    # Головне Меню
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Профіль"
    META = "🔥 META"
    M6 = "🏆 M6"
    GPT = "👾 GPT"

    # Персонажі
    HEROES = "🥷 Персонажі"
    GUIDES = "📚 Гайди"
    COUNTER_PICKS = "⚖️ Контр-піки"
    BUILDS = "🛡️ Білди"
    VOTING = "📊 Голосування"

    # Класи героїв
    TANK = "🛡️ Танки"
    MAGE = "🧙‍♂️ Маги"
    MARKSMAN = "🏹 Стрільці"
    ASSASSIN = "⚔️ Асасіни"
    SUPPORT = "❤️ Сапорти"
    FIGHTER = "🗡️ Бійці"

    # Гайди
    NEW_GUIDES = "🆕 Нові Гайди"
    POPULAR_GUIDES = "🌟 Топ Гайди"
    BEGINNER_GUIDES = "📘 Новачкам"
    ADVANCED_TECHNIQUES = "🧙 Стратегії гри"
    TEAMPLAY_GUIDES = "🤝 Командна Гра"

    # Контр-піки
    COUNTER_SEARCH = "🔎 Пошук Контр-піку"
    COUNTER_LIST = "📝 Список Персонажів"

    # Білди
    CREATE_BUILD = "🏗️ Створити Білд"
    MY_BUILDS = "📄 Збережені Білди"
    POPULAR_BUILDS = "🔥 Популярні Білди"

    # Голосування
    CURRENT_VOTES = "📍 Поточні Опитування"
    MY_VOTES = "📋 Мої Голосування"
    SUGGEST_TOPIC = "➕ Запропонувати Тему"

    # Статистика
    ACTIVITY = "📊 Загальна Активність"
    RANKING = "🥇 Рейтинг"
    GAME_STATS = "🎮 Ігрова Статистика"

    # Досягнення
    BADGES = "🎖️ Мої Бейджі"
    PROGRESS = "🚀 Прогрес"
    TOURNAMENT_STATS = "🏅 Турнірна Статистика"
    AWARDS = "🎟️ Отримані Нагороди"

    # Налаштування
    LANGUAGE = "🌐 Мова Інтерфейсу"
    CHANGE_USERNAME = "ℹ️ Змінити Username"
    UPDATE_ID = "🆔 Оновити ID"
    NOTIFICATIONS = "🔔 Сповіщення"

    # Зворотний зв'язок
    SEND_FEEDBACK = "✏️ Надіслати Відгук"
    REPORT_BUG = "🐛 Повідомити про Помилку"

    # Допомога
    INSTRUCTIONS = "📄 Інструкції"
    FAQ = "❔ FAQ"
    HELP_SUPPORT = "📞 Підтримка"

    # Навігація
    BACK = "🔙 Назад"
    BACK_TO_MAIN_MENU = "🔙 Меню"
    BACK_TO_PROFILE_MENU = "🔙 Повернутися до Профілю"
# keyboards/menus.py

def get_navigation_menu():
    return create_menu(
        [
            MenuButton.HEROES,
            MenuButton.GUIDES,
            MenuButton.COUNTER_PICKS,
            MenuButton.BUILDS,
            MenuButton.VOTING,
            MenuButton.META,
            MenuButton.M6,
            MenuButton.GPT,
            MenuButton.BACK
        ],
        row_width=3  # Розміщення у три рядки по три кнопки
    )

def get_guides_menu():
    return create_menu(
        [
            MenuButton.NEW_GUIDES,
            MenuButton.POPULAR_GUIDES,
            MenuButton.BEGINNER_GUIDES,
            MenuButton.ADVANCED_TECHNIQUES,
            MenuButton.TEAMPLAY_GUIDES,
            MenuButton.BACK
        ],
        row_width=3  # Розміщення у два рядки по три кнопки
    )

def get_counter_picks_menu() -> ReplyKeyboardMarkup:
    return create_menu(
        [
            MenuButton.COUNTER_SEARCH,
            MenuButton.COUNTER_LIST,
            MenuButton.BACK
        ],
        row_width=3  # Розміщення у одному рядку з трьома кнопками
    )

def get_builds_menu() -> ReplyKeyboardMarkup:
    return create_menu(
        [
            MenuButton.CREATE_BUILD,
            MenuButton.MY_BUILDS,
            MenuButton.POPULAR_BUILDS,
            MenuButton.BACK
        ],
        row_width=3  # Розміщення у два рядки по три кнопки
    )

def get_voting_menu() -> ReplyKeyboardMarkup:
    return create_menu(
        [
            MenuButton.CURRENT_VOTES,
            MenuButton.MY_VOTES,
            MenuButton.SUGGEST_TOPIC,
            MenuButton.BACK
        ],
        row_width=3  # Розміщення у два рядки по три кнопки
    )

def get_heroes_menu() -> ReplyKeyboardMarkup:
    return create_menu(
        [
            MenuButton.TANK,
            MenuButton.MAGE,
            MenuButton.MARKSMAN,
            MenuButton.ASSASSIN,
            MenuButton.SUPPORT,
            MenuButton.FIGHTER,
            MenuButton.COMPARISON,
            MenuButton.SEARCH_HERO,
            MenuButton.BACK
        ],
        row_width=3  # Розміщення у три рядки по три кнопки
    )

def get_profile_menu() -> ReplyKeyboardMarkup:
    return create_menu(
        [
            MenuButton.STATISTICS,
            MenuButton.ACHIEVEMENTS,
            MenuButton.SETTINGS,
            MenuButton.SEND_FEEDBACK,
            MenuButton.REPORT_BUG,
            MenuButton.HELP_SUPPORT,
            MenuButton.BACK_TO_MAIN_MENU
        ],
        row_width=3  # Розміщення у три рядки по три кнопки
    )

def get_statistics_menu() -> ReplyKeyboardMarkup:
    return create_menu(
        [
            MenuButton.ACTIVITY,
            MenuButton.RANKING,
            MenuButton.GAME_STATS,
            MenuButton.BACK_TO_PROFILE_MENU
        ],
        row_width=3  # Розміщення у два рядки по три кнопки
    )

def get_achievements_menu() -> ReplyKeyboardMarkup:
    return create_menu(
        [
            MenuButton.BADGES,
            MenuButton.PROGRESS,
            MenuButton.TOURNAMENT_STATS,
            MenuButton.AWARDS,
            MenuButton.BACK_TO_PROFILE_MENU
        ],
        row_width=3  # Розміщення у два рядки по три кнопки
    )

def get_settings_menu() -> ReplyKeyboardMarkup:
    return create_menu(
        [
            MenuButton.LANGUAGE,
            MenuButton.CHANGE_USERNAME,
            MenuButton.UPDATE_ID,
            MenuButton.NOTIFICATIONS,
            MenuButton.BACK_TO_PROFILE_MENU
        ],
        row_width=3  # Розміщення у два рядки по три кнопки
    )

def get_feedback_menu() -> ReplyKeyboardMarkup:
    return create_menu(
        [
            MenuButton.SEND_FEEDBACK,
            MenuButton.REPORT_BUG,
            MenuButton.BACK_TO_PROFILE_MENU
        ],
        row_width=3  # Розміщення у одному рядку з трьома кнопками
    )

def get_help_menu() -> ReplyKeyboardMarkup:
    return create_menu(
        [
            MenuButton.INSTRUCTIONS,
            MenuButton.FAQ,
            MenuButton.HELP_SUPPORT,
            MenuButton.BACK_TO_PROFILE_MENU
        ],
        row_width=3  # Розміщення у два рядки по три кнопки
    )

def get_meta_menu() -> ReplyKeyboardMarkup:
    return create_menu(
        [
            MenuButton.ACTIVITY,
            MenuButton.RANKING,
            '📈 Аналітика',  # Якщо ці кнопки не входять до MenuButton, додайте їх
            '📊 Статистика',
            MenuButton.BACK_TO_MAIN_MENU
        ],
        row_width=2
    )

def get_m6_menu() -> ReplyKeyboardMarkup:
    return create_menu(
        [
            '🏆 Результати',
            '🔍 Деталі',
            MenuButton.BACK_TO_MAIN_MENU
        ],
        row_width=2
    )

def get_gpt_menu() -> ReplyKeyboardMarkup:
    return create_menu(
        [
            '📝 Задати питання',
            '❓ Допомога',
            MenuButton.BACK_TO_MAIN_MENU
        ],
        row_width=2
    )
