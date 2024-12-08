# keyboards/menus.py

from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    ReplyKeyboardRemove
)
from enum import Enum
import logging

# Налаштування логування
logger = logging.getLogger(__name__)

class MenuButton(Enum):
    # Головне Меню
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Профіль"
    META = "🔥 META"
    M6 = "🏆 M6"
    GPT = "👾 GPT"

    # Меню Навігації
    CHARACTERS = "🥷 Персонажі"
    GUIDES = "📚 Гайди"
    COUNTER_PICKS = "⚖️ Контр-піки"
    BUILDS = "🛡️ Білди"
    VOTING = "📊 Голосування"

    # Меню Гайди
    NEW_GUIDES = "🆕 Нові Гайди"
    TOP_GUIDES = "🌟 Топ Гайди"
    BEGINNER_GUIDES = "📘 Гайди для Новачків"
    ADVANCED_TECHNIQUES = "🧙‍♂️ Просунуті Техніки"
    TEAMPLAY_GUIDES = "🤝 Командна Гра"

    # Меню Контр-піки
    COUNTER_SEARCH = "🔎 Пошук Контр-піку"
    COUNTER_LIST = "📝 Список Контр-піків"

    # Меню Білди
    CREATE_BUILD = "🏗️ Створити Білд"
    MY_BUILDS = "📄 Збережені Білди"
    POPULAR_BUILDS = "🔥 Популярні Білди"

    # Меню Голосування
    CURRENT_VOTES = "📍 Поточні Опитування"
    MY_VOTES = "📋 Мої Голосування"
    SUGGEST_TOPIC = "➕ Запропонувати Тему"

    # Меню Профіль
    STATISTICS = "📈 Статистика"
    ACHIEVEMENTS = "🏆 Досягнення"
    SETTINGS = "⚙️ Налаштування"
    FEEDBACK = "💌 Зворотний Зв’язок"
    HELP = "❓ Допомога"

    # Меню Статистика
    ACTIVITY = "📊 Загальна Активність"
    RANKING = "🥇 Рейтинг"
    GAME_STATS = "🎮 Ігрова Статистика"

    # Меню Досягнення
    BADGES = "🎖️ Мої Бейджі"
    PROGRESS = "🚀 Прогрес"
    TOURNAMENT_STATS = "🏅 Турнірна Статистика"
    AWARDS = "🎟️ Отримані Нагороди"

    # Меню Налаштування
    LANGUAGE = "🌐 Мова Інтерфейсу"
    CHANGE_USERNAME = "ℹ️ Змінити Username"
    UPDATE_ID = "🆔 Оновити ID"
    NOTIFICATIONS = "🔔 Сповіщення"

    # Інші кнопки
    BACK = "🔙 Назад"
    BACK_TO_MAIN_MENU = "🔙 Меню"
    HEROES = "🦸‍♂️ Герої"
    SEARCH_HERO = "🔎 Шукати"
    COMPARISON = "⚖️ Порівняти"
    SUPPORT = "❤️ Сапорти"
    FIGHTERS = "🗡️ Бійці"

    # Інші кнопки для станів
    SEARCH_TOPIC = "🔍 Пошук Теми"

def create_menu(buttons, row_width=3):
    """
    Створює клавіатуру з кнопками.
    :param buttons: Список кнопок (MenuButton або str).
    :param row_width: Кількість кнопок у рядку.
    :return: ReplyKeyboardMarkup
    """
    if not all(isinstance(button, MenuButton) or isinstance(button, str) for button in buttons):
        raise ValueError("Усі елементи у списку кнопок повинні бути екземплярами MenuButton або str.")
    logger.info(f"Створення меню з кнопками: {[button.value if isinstance(button, MenuButton) else button for button in buttons]}")
    keyboard_buttons = [
        KeyboardButton(text=button.value if isinstance(button, MenuButton) else button) for button in buttons
    ]
    keyboard = [
        keyboard_buttons[i:i + row_width]
        for i in range(0, len(keyboard_buttons), row_width)
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Функції меню

def get_main_menu():
    return create_menu(
        [
            MenuButton.NAVIGATION,
            MenuButton.PROFILE
        ],
        row_width=2  # Дві кнопки на ряд
    )

def get_navigation_menu():
    return create_menu(
        [
            MenuButton.CHARACTERS,
            MenuButton.GUIDES,
            MenuButton.COUNTER_PICKS,
            MenuButton.BUILDS,
            MenuButton.VOTING,
            MenuButton.META,
            MenuButton.M6,
            MenuButton.GPT,
            MenuButton.BACK
        ],
        row_width=3
    )

def get_guides_menu():
    return create_menu(
        [
            MenuButton.NEW_GUIDES,
            MenuButton.TOP_GUIDES,
            MenuButton.BEGINNER_GUIDES,
            MenuButton.ADVANCED_TECHNIQUES,
            MenuButton.TEAMPLAY_GUIDES,
            MenuButton.BACK
        ],
        row_width=3
    )

def get_meta_menu():
    return create_menu(
        [
            MenuButton.ACTIVITY,
            MenuButton.RANKING,
            MenuButton.GAME_STATS,
            MenuButton.BACK_TO_MAIN_MENU
        ],
        row_width=3
    )

def get_m6_menu():
    return create_menu(
        [
            MenuButton.CREATE_BUILD,
            MenuButton.MY_BUILDS,
            MenuButton.POPULAR_BUILDS,
            MenuButton.BACK_TO_MAIN_MENU
        ],
        row_width=3
    )

def get_gpt_menu():
    return create_menu(
        [
            MenuButton.ASK_QUESTION,
            MenuButton.HELP,
            MenuButton.BACK_TO_MAIN_MENU
        ],
        row_width=3
    )

def get_profile_menu():
    return create_menu(
        [
            MenuButton.STATISTICS,
            MenuButton.ACHIEVEMENTS,
            MenuButton.SETTINGS,
            MenuButton.FEEDBACK,
            MenuButton.HELP,
            MenuButton.BACK_TO_MAIN_MENU
        ],
        row_width=3
    )

def get_heroes_menu():
    return create_menu(
        [
            MenuButton.TANKS,
            MenuButton.MAGES,
            MenuButton.MARKSMAN,
            MenuButton.ASSASSINS,
            MenuButton.SUPPORT,
            MenuButton.FIGHTERS,
            MenuButton.COMPARISON,
            MenuButton.SEARCH_HERO,
            MenuButton.BACK
        ],
        row_width=3
    )

def get_hero_class_menu(hero_class: str) -> ReplyKeyboardRemove:
    # Створюємо клавіатуру з героями певного класу
    # Це можна реалізувати за допомогою функції з `heroes_by_class`
    # Тут ми повертаємо видалення клавіатури для простоти
    return ReplyKeyboardRemove()

def get_counter_picks_menu():
    return create_menu(
        [
            MenuButton.COUNTER_SEARCH,
            MenuButton.COUNTER_LIST,
            MenuButton.BACK
        ],
        row_width=3
    )

def get_builds_menu():
    return create_menu(
        [
            MenuButton.CREATE_BUILD,
            MenuButton.MY_BUILDS,
            MenuButton.POPULAR_BUILDS,
            MenuButton.BACK
        ],
        row_width=3
    )

def get_voting_menu():
    return create_menu(
        [
            MenuButton.CURRENT_VOTES,
            MenuButton.MY_VOTES,
            MenuButton.SUGGEST_TOPIC,
            MenuButton.BACK
        ],
        row_width=3
    )

def get_statistics_menu():
    return create_menu(
        [
            MenuButton.ACTIVITY,
            MenuButton.RANKING,
            MenuButton.GAME_STATS,
            MenuButton.BACK_TO_PROFILE
        ],
        row_width=3
    )

def get_achievements_menu():
    return create_menu(
        [
            MenuButton.BADGES,
            MenuButton.PROGRESS,
            MenuButton.TOURNAMENT_STATS,
            MenuButton.AWARDS,
            MenuButton.BACK_TO_PROFILE
        ],
        row_width=3
    )

def get_settings_menu():
    return create_menu(
        [
            MenuButton.LANGUAGE,
            MenuButton.CHANGE_USERNAME,
            MenuButton.UPDATE_ID,
            MenuButton.NOTIFICATIONS,
            MenuButton.BACK_TO_PROFILE
        ],
        row_width=3
    )

def get_feedback_menu():
    return create_menu(
        [
            MenuButton.SEND_FEEDBACK,
            MenuButton.REPORT_BUG,
            MenuButton.BACK_TO_PROFILE
        ],
        row_width=3
    )

def get_help_menu():
    return create_menu(
        [
            MenuButton.INSTRUCTIONS,
            MenuButton.FAQ,
            MenuButton.HELP_SUPPORT,
            MenuButton.BACK_TO_PROFILE
        ],
        row_width=3
    )