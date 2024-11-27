# keyboards/menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from enum import Enum
import logging

# Налаштування логування
logger = logging.getLogger(__name__)  # Використовується '__name__' для коректного логування
logging.basicConfig(level=logging.INFO)

class MenuButton(Enum):
    # Головне Меню
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Профіль"

    # Розділ Навігація
    HEROES = "🛡️ Герої"
    GUIDES = "📚 Гайди"
    COUNTER_PICKS = "⚖️ Контр-піки"
    BUILDS = "⚜️ Білди"
    VOTING = "📊 Голосування"
    BACK = "🔄 Назад"

    # Розділ Персонажі
    SEARCH_HERO = "🔍 Пошук Героя"
    TANK = "🛡️ Танки"
    MAGE = "🔮 Маги"
    MARKSMAN = "🏹 Стрільці"
    ASSASSIN = "⚔️ Асасіни"
    SUPPORT = "🧬 Підтримка"
    FIGHTER = "🥊 Боєць"
    COMPARISON = "⚖️ Порівняння"

    # Розділ Гайди
    NEW_GUIDES = "🆕 Нові Гайди"
    POPULAR_GUIDES = "🌟 Популярні"
    BEGINNER_GUIDES = "📘 Для Новачків"
    ADVANCED_TECHNIQUES = "🧙 Просунуті"
    TEAMPLAY_GUIDES = "🛡️ Командна Гра"

    # Розділ Контр-піки
    COUNTER_SEARCH = "🔎 Пошук Контр-піку"
    COUNTER_LIST = "📝 Список Героїв"

    # Розділ Білди
    CREATE_BUILD = "🏗️ Створити Білд"
    MY_BUILDS = "📄 Мої Білди"
    POPULAR_BUILDS = "💎 Топ Білди"

    # Розділ Голосування
    CURRENT_VOTES = "📍 Поточні Опитування"
    MY_VOTES = "📋 Мої Голоси"
    SUGGEST_TOPIC = "➕ Запропонувати Тему"

    # Розділ Профіль
    STATISTICS = "📈 Статистика"
    ACHIEVEMENTS = "🏆 Досягнення"
    SETTINGS = "⚙️ Налаштування"
    FEEDBACK = "💌 Зворотний Зв'язок"
    HELP = "❓ Допомога"
    BACK_TO_MAIN_MENU = "🔄 Повернутися до Головного Меню"

    # Підрозділ Статистика
    ACTIVITY = "📊 Загальна Активність"
    RANKING = "🥇 Рейтинг"
    GAME_STATS = "🎮 Ігрова Статистика"
    BACK_TO_PROFILE = "🔄 Назад до Профілю"

    # Підрозділ Досягнення
    BADGES = "🎖️ Мої Бейджі"
    PROGRESS = "🚀 Прогрес"
    TOURNAMENT_STATS = "🏅 Турнірна Статистика"
    AWARDS = "🎟️ Отримані Нагороди"

    # Підрозділ Налаштування
    LANGUAGE = "🌐 Мова Інтерфейсу"
    CHANGE_USERNAME = "🆔 Змінити Ім'я"
    UPDATE_ID = "🛡️ Оновити ID"
    NOTIFICATIONS = "🔔 Сповіщення"

    # Підрозділ Зворотний Зв'язок
    SEND_FEEDBACK = "✏️ Відгук"
    REPORT_BUG = "🐛 Повідомити про Баг"

    # Підрозділ Допомога
    INSTRUCTIONS = "📄 Інструкції"
    FAQ = "❔ FAQ"
    HELP_SUPPORT = "📞 Підтримка"

# Відповідність кнопок класам героїв
menu_button_to_class = {
    MenuButton.TANK.value: "Танк",
    MenuButton.MAGE.value: "Маг",
    MenuButton.MARKSMAN.value: "Стрільці",
    MenuButton.ASSASSIN.value: "Асасіни",
    MenuButton.SUPPORT.value: "Підтримка",
    MenuButton.FIGHTER.value: "Боєць",
}

# Повний список героїв за класами
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
    "Асасіни": [
        "Saber", "Alucard", "Zilong", "Fanny", "Natalia", "Yi Sun-shin", "Lancelot", "Helcurt",
        "Lesley", "Selena", "Mathilda", "Paquito", "Yin", "Arlott", "Harley", "Suyou"
    ],
    "Стрільці": [
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
            MenuButton.SEARCH_HERO,
            MenuButton.TANK,
            MenuButton.MAGE,
            MenuButton.MARKSMAN,
            MenuButton.ASSASSIN,
            MenuButton.SUPPORT,
            MenuButton.FIGHTER,
            MenuButton.COMPARISON,
            MenuButton.BACK
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
