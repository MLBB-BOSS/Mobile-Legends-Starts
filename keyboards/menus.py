# keyboards/menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from enum import Enum
import logging

# Логування
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MenuButton(Enum):
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Мій Профіль"
    HEROES = "🛡️ Персонажі"
    GUIDES = "📚 Гайди"
    SEARCH_HERO = "🔎 Пошук Персонажа"
    FIGHTER = "🥊 Боєць"
    TANK = "🛡️ Танк"
    MAGE = "🧙‍♂️ Маг"
    MARKSMAN = "🎯 Стрілець"
    ASSASSIN = "🗡️ Асасін"
    SUPPORT = "❤️ Підтримка"
    COMPARISON = "⚖️ Порівняння"
    BACK = "🔄 Назад"
    NEW_GUIDES = "🆕 Нові Гайди"
    POPULAR_GUIDES = "🌟 Популярні Гайди"
    BEGINNER_GUIDES = "📘 Для Початківців"
    ADVANCED_TECHNIQUES = "🧙 Просунуті Техніки"
    TEAMPLAY_GUIDES = "🛡️ Командна Гра"
    COUNTER_PICKS = "⚖️ Контр-піки"
    COUNTER_SEARCH = "🔎 Пошук Контр-піку"
    COUNTER_LIST = "📝 Список Персонажів"
    CREATE_BUILD = "🏗️ Створити Білд"
    MY_BUILDS = "📄 Мої Білди"
    POPULAR_BUILDS = "💎 Популярні Білди"
    BUILDS = "⚜️ Білди"
    CURRENT_VOTES = "📍 Поточні Опитування"
    MY_VOTES = "📋 Мої Голосування"
    SUGGEST_TOPIC = "➕ Запропонувати Тему"
    VOTING = "📊 Голосування"
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
    HELP_SUPPORT = "🆘 Підтримка"

heroes_by_class = {
    "Боєць": [
        "Balmond", "Alucard", "Bane", "Zilong", "Freya", "Alpha", "Ruby", "Roger",
        "Gatotkaca", "Jawhead", "Martis", "Aldous", "Minsitthar", "Terizla", "X.Borg",
        "Dyroth", "Masha", "Silvanna", "Yu Zhong", "Khaleed", "Barats", "Paquito",
        "Phoveus", "Aulus", "Fiddrin", "Arlott", "Cici", "Kaja", "Leomord", "Thamuz",
        "Badang", "Guinevere"
    ],
    "Танк": [
        "Alice", "Tigreal", "Akai", "Franco", "Minotaur", "Lolia", "Gatotkaca", "Grock",
        "Hylos", "Uranus", "Belerick", "Khufra", "Esmeralda", "Terizla", "Baxia", "Masha",
        "Atlas", "Barats", "Edith", "Fredrinn", "Johnson", "Hilda", "Carmilla", "Gloo", "Chip"
    ],
    "Асасін": [
        "Saber", "Alucard", "Zilong", "Fanny", "Natalia", "Yi Sun-shin", "Lancelot", "Helcurt",
        "Lesley", "Selena", "Mathilda", "Paquito", "Yin", "Arlott", "Harley", "Suyou"
    ],
    "Стрілець": [
        "Popol and Kupa", "Brody", "Beatrix", "Natan", "Melissa", "Ixia", "Hanabi", "Claude",
        "Kimmy", "Granger", "Wanwan", "Miya", "Bruno", "Clint", "Layla", "Yi Sun-shin", "Moskov",
        "Roger", "Karrie", "Irithel", "Lesley"
    ],
    "Маг": [
        "Vale", "Lunox", "Kadita", "Cecillion", "Luo Yi", "Xavier", "Novaria", "Zhuxin", "Harley",
        "Yve", "Aurora", "Faramis", "Esmeralda", "Kagura", "Cyclops", "Vexana", "Odette", "Zhask"
    ],
    "Підтримка": [
        "Rafaela", "Minotaur", "Lolita", "Estes", "Angela", "Faramis", "Mathilda", "Florin", "Johnson"
    ],
}

menu_button_to_class = {
    MenuButton.TANK.value: "Танк",
    MenuButton.MAGE.value: "Маг",
    MenuButton.MARKSMAN.value: "Стрілець",
    MenuButton.ASSASSIN.value: "Асасін",
    MenuButton.SUPPORT.value: "Підтримка",
    MenuButton.FIGHTER.value: "Боєць",
}

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
    keyboard = [
        [KeyboardButton(text=button.value if isinstance(button, MenuButton) else button) for button in buttons[i:i + row_width]]
        for i in range(0, len(buttons), row_width)
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
            MenuButton.FIGHTER,
            MenuButton.TANK,
            MenuButton.MAGE,
            MenuButton.MARKSMAN,
            MenuButton.ASSASSIN,
            MenuButton.SUPPORT,
            MenuButton.COMPARISON,
            MenuButton.BACK,
            MenuButton.SEARCH_HERO
        ],
        row_width=3
    )

def get_hero_class_menu(hero_class):
    heroes = heroes_by_class.get(hero_class, [])
    buttons = [KeyboardButton(text=hero) for hero in heroes]
    row_width = 3
    keyboard = [buttons[i:i+row_width] for i in range(0, len(buttons), row_width)]
    keyboard.append([KeyboardButton(text=MenuButton.BACK.value)])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

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
        row_width=3
    )

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

def get_profile_menu():
    return create_menu(
        [
            MenuButton.ACTIVITY,
            MenuButton.RANKING,
            MenuButton.GAME_STATS,
            MenuButton.BACK
        ],
        row_width=3
    )
