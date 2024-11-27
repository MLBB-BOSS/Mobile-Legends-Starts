from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from enum import Enum
import logging

# Логування
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Enum для текстів кнопок
class MenuButton(Enum):
    SEARCH_HERO = "🔎 Пошук Персонажа"
    TANK = "🛡️ Танк"
    MAGE = "🔮 Маг"
    MARKSMAN = "🏹 Стрілець"
    ASSASSIN = "⚔️ Асасін"
    SUPPORT = "📞 Підтримка"  # Changed this one to avoid conflict
    BACK = "🔄 Назад"
    NEW_GUIDES = "🆕 Нові Гайди"
    POPULAR_GUIDES = "🌟 Популярні Гайди"
    BEGINNER_GUIDES = "📘 Для Початківців"
    ADVANCED_TECHNIQUES = "🧙 Просунуті Техніки"
    TEAMPLAY_GUIDES = "🛡️ Командна Гра"
    COUNTER_SEARCH = "🔎 Пошук Контр-піку"
    COUNTER_LIST = "📝 Список Персонажів"
    CREATE_BUILD = "🏗️ Створити Білд"
    MY_BUILDS = "📄 Мої Білди"
    POPULAR_BUILDS = "💎 Популярні Білди"
    CURRENT_VOTES = "📍 Поточні Опитування"
    MY_VOTES = "📋 Мої Голосування"
    SUGGEST_TOPIC = "➕ Запропонувати Тему"
    ACTIVITY = "📊 Загальна Активність"
    RANKING = "🥇 Рейтинг"
    GAME_STATS = "🎮 Ігрова Статистика"
    BADGES = "🎖️ Мої Бейджі"
    PROGRESS = "🚀 Прогрес"
    TOURNAMENT_STATS = "🏅 Турнірна Статистика"
    AWARDS = "🎟️ Отримані Нагороди"
    LANGUAGE = "🌐 Мова Інтерфейсу"
    CHANGE_USERNAME = "🆔 Змінити Username"
    UPDATE_ID = "🛡️ Оновити ID Гравця"
    NOTIFICATIONS = "🔔 Сповіщення"
    INSTRUCTIONS = "📄 Інструкції"
    FAQ = "❔ FAQ"
    # Removed duplicate SUPPORT definition

# Функція для створення клавіатур
def create_menu(buttons, row_width=2):
    """
    Створює клавіатуру з кнопками.
    :param buttons: Список кнопок (MenuButton).
    :param row_width: Кількість кнопок у рядку.
    :return: ReplyKeyboardMarkup
    """
    logger.info(f"Створення меню з кнопками: {[button.value for button in buttons]}")
    keyboard = [
        [KeyboardButton(text=button.value) for button in buttons[i:i + row_width]]
        for i in range(0, len(buttons), row_width)
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Меню "Персонажі"
def get_heroes_menu():
    return create_menu(
        [
            MenuButton.SEARCH_HERO,
            MenuButton.TANK,
            MenuButton.MAGE,
            MenuButton.MARKSMAN,
            MenuButton.ASSASSIN,
            MenuButton.SUPPORT,  # Make sure this matches the correct SUPPORT value
            MenuButton.BACK
        ],
        row_width=2
    )

# Меню "Гайди"
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

# Меню "Контр-піки"
def get_counter_picks_menu():
    return create_menu(
        [
            MenuButton.COUNTER_SEARCH,
            MenuButton.COUNTER_LIST,
            MenuButton.BACK
        ],
        row_width=1
    )

# Меню "Білди"
def get_builds_menu():
    return create_menu(
        [
            MenuButton.CREATE_BUILD,
            MenuButton.MY_BUILDS,
            MenuButton.POPULAR_BUILDS,
            MenuButton.BACK
        ],
        row_width=1
    )

# Меню "Голосування"
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

# Меню "Профіль"
def get_profile_menu():
    return create_menu(
        [
            MenuButton.ACTIVITY,
            MenuButton.RANKING,
            MenuButton.GAME_STATS,
            MenuButton.BACK
        ],
        row_width=2
    )

# Меню "Досягнення"
def get_achievements_menu():
    return create_menu(
        [
            MenuButton.BADGES,
            MenuButton.PROGRESS,
            MenuButton.TOURNAMENT_STATS,
            MenuButton.AWARDS,
            MenuButton.BACK
        ],
        row_width=2
    )

# Меню "Налаштування"
def get_settings_menu():
    return create_menu(
        [
            MenuButton.LANGUAGE,
            MenuButton.CHANGE_USERNAME,
            MenuButton.UPDATE_ID,
            MenuButton.NOTIFICATIONS,
            MenuButton.BACK
        ],
        row_width=2
    )

# Меню "Допомога"
def get_help_menu():
    return create_menu(
        [
            MenuButton.INSTRUCTIONS,
            MenuButton.FAQ,
            MenuButton.SUPPORT,  # Make sure this matches the correct SUPPORT value
            MenuButton.BACK
        ],
        row_width=1
    )

# Меню "Головне меню"
def get_main_menu():
    return create_menu(
        [
            MenuButton.SEARCH_HERO,
            MenuButton.NEW_GUIDES,
            MenuButton.POPULAR_GUIDES,
            MenuButton.COUNTER_SEARCH,
            MenuButton.CREATE_BUILD,
            MenuButton.CURRENT_VOTES,
            MenuButton.ACTIVITY,
            MenuButton.LANGUAGE,
            MenuButton.INSTRUCTIONS,
            MenuButton.FAQ
        ],
        row_width=2
    )
