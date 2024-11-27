# keyboards/menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class MenuButton(Enum):
    # Головне Меню
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Мій Профіль"

    # Розділ Навігація
    HEROES = "🛡️ Персонажі"
    GUIDES = "📚 Гайди"
    COUNTER_PICKS = "⚖️ Контр-піки"
    BUILDS = "⚜️ Білди"
    VOTING = "📊 Голосування"
    BACK = "🔄 Назад"

    # Розділ Персонажі
    TANK = "🛡️ Танк"
    MAGE = "🧙‍♂️ Маг"
    MARKSMAN = "🎯 Стрілець"
    ASSASSIN = "🗡️ Асасін"
    SUPPORT = "❤️ Підтримка"
    FIGHTER = "🥊 Боєць"
    COMPARISON = "⚖️ Порівняння"
    SEARCH_HERO = "🔎 Пошук Персонажа"

    # Розділ Гайди
    NEW_GUIDES = "🆕 Нові Гайди"
    POPULAR_GUIDES = "⭐ Популярні Гайди"
    BEGINNER_GUIDES = "👶 Гайди для Початківців"
    ADVANCED_TECHNIQUES = "🚀 Просунуті Техніки"
    TEAMPLAY_GUIDES = "🤝 Командна Гра"

    # Розділ Контр-піки
    COUNTER_SEARCH = "🔍 Пошук Контр-піку"
    COUNTER_LIST = "📃 Список Персонажів"

    # Розділ Білди
    CREATE_BUILD = "➕ Створити Білд"
    MY_BUILDS = "📁 Мої Білди"
    POPULAR_BUILDS = "🌟 Популярні Білди"

    # Розділ Голосування
    CURRENT_VOTES = "🗳️ Поточні Опитування"
    MY_VOTES = "🗳️ Мої Голосування"
    SUGGEST_TOPIC = "💡 Запропонувати Тему"

    # Розділ Статистика
    ACTIVITY = "📈 Загальна Активність"
    RANKING = "🏅 Рейтинг"
    GAME_STATS = "🎮 Ігрова Статистика"

    # Розділ Досягнення
    BADGES = "🏅 Мої Бейджі"
    PROGRESS = "📊 Прогрес"
    TOURNAMENT_STATS = "🏆 Турнірна Статистика"
    AWARDS = "🏆 Отримані Нагороди"

    # Розділ Налаштування
    LANGUAGE = "🌐 Мова Інтерфейсу"
    CHANGE_USERNAME = "✏️ Змінити Username"
    UPDATE_ID = "🔄 Оновити ID Гравця"
    NOTIFICATIONS = "🔔 Сповіщення"

    # Розділ Зворотний Зв'язок
    SEND_FEEDBACK = "📤 Надіслати Відгук"
    REPORT_BUG = "🐞 Повідомити про Помилку"

    # Розділ Допомога
    INSTRUCTIONS = "📖 Інструкції"
    FAQ = "❓ FAQ"
    HELP_SUPPORT = "🆘 Підтримка"

    # Назад до головного меню або профілю
    BACK_TO_MAIN_MENU = "🔙 Назад до Головного Меню"
    BACK_TO_PROFILE = "🔙 Назад до Профілю"

def create_menu(buttons, row_width=2):
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

def get_main_menu():
    return create_menu(
        [
            MenuButton.NAVIGATION,
            MenuButton.PROFILE
        ],
        row_width=2
    )

def get_navigation_menu():
    return create_menu(
        [
            MenuButton.HEROES,
            MenuButton.GUIDES,
            MenuButton.COUNTER_PICKS,
            MenuButton.BUILDS,
            MenuButton.VOTING,
            MenuButton.BACK
        ],
        row_width=3
    )

def get_heroes_menu():
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
        row_width=3
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
        row_width=2
    )

def get_counter_picks_menu():
    return create_menu(
        [
            MenuButton.COUNTER_SEARCH,
            MenuButton.COUNTER_LIST,
            MenuButton.BACK
        ],
        row_width=2
    )

def get_builds_menu():
    return create_menu(
        [
            MenuButton.CREATE_BUILD,
            MenuButton.MY_BUILDS,
            MenuButton.POPULAR_BUILDS,
            MenuButton.BACK
        ],
        row_width=2
    )

def get_voting_menu():
    return create_menu(
        [
            MenuButton.CURRENT_VOTES,
            MenuButton.MY_VOTES,
            MenuButton.SUGGEST_TOPIC,
            MenuButton.BACK
        ],
        row_width=2
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

def get_statistics_menu():
    return create_menu(
        [
            MenuButton.ACTIVITY,
            MenuButton.RANKING,
            MenuButton.GAME_STATS,
            MenuButton.BACK_TO_PROFILE
        ],
        row_width=2
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
        row_width=2
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
        row_width=2
    )

def get_feedback_menu():
    return create_menu(
        [
            MenuButton.SEND_FEEDBACK,
            MenuButton.REPORT_BUG,
            MenuButton.BACK_TO_PROFILE
        ],
        row_width=2
    )

def get_help_menu():
    return create_menu(
        [
            MenuButton.INSTRUCTIONS,
            MenuButton.FAQ,
            MenuButton.HELP_SUPPORT,
            MenuButton.BACK_TO_PROFILE
        ],
        row_width=2
    )

def get_hero_class_menu(hero_class: str) -> ReplyKeyboardMarkup:
    """
    Створює клавіатуру для конкретного класу героїв.

    :param hero_class: Клас героя (наприклад, "Танк", "Маг" і т.д.)
    :return: ReplyKeyboardMarkup
    """
    heroes_by_class = {
        "Боєць": [
            "Balmond", "Alucard", "Bane", "Zilong", "Freya",
            # ... (ваш список героїв)
        ],
        "Танк": [
            "Tigreal", "Akai", "Franco", "Minotaur",
            # ... (ваш список героїв)
        ],
        "Маг": [
            "Vale", "Lunox", "Kadita", "Cecillion", "Luo Yi", "Xavier",
            # ... (ваш список героїв)
        ],
        "Стрілець": [
            "Yi Sun-shin", "Granger", "Brody",
            # ... (ваш список героїв)
        ],
        "Асасін": [
            "Hayabusa", "Helcurt",
            # ... (ваш список героїв)
        ],
        "Підтримка": [
            "Angela", "Estes",
            # ... (ваш список героїв)
        ],
        # ... (інші класи, якщо є)
    }

    heroes = heroes_by_class.get(hero_class, [])
    buttons = [KeyboardButton(text=hero) for hero in heroes]
    keyboard = []

    # Розміщуємо кнопки по 3 в ряд
    for i in range(0, len(buttons), 3):
        keyboard.append(buttons[i:i + 3])

    # Додаємо кнопку "Назад"
    keyboard.append([KeyboardButton(text=MenuButton.BACK.value)])

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )
