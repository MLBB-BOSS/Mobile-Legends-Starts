# keyboards/menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from enum import Enum
import logging

# Налаштування логування
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MenuButton(Enum):
    # Головне Меню
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Мій Профіль"

    # Розділ Навігація
    HEROES = "🥷 Персонажі"
    BUILDS = "🛡️ Білди"
    COUNTER_PICKS = "⚖️ Контр-піки"
    GUIDES = "📚 Гайди"
    VOTING = "📊 Голосування"
    M6 = "🏆 M6"
    GPT = "👾 GPT"
    META = "🔥 META"
    TOURNAMENTS = "🏆 Турніри"
    BACK_NAVIGATION = "🔙 Назад"

    # Розділ Персонажі
    TANK = "🛡️ Танк"
    MAGE = "🧙‍♂️ Маг"
    MARKSMAN = "🏹 Стрілець"
    ASSASSIN = "⚔️ Асасін"
    SUPPORT = "❤️ Підтримка"
    FIGHTER = "🗡️ Боєць"
    COMPARISON = "⚖️ Порівняння"
    SEARCH_HERO = "🔎 Пошук"
    BACK_HEROES = "🔙 Назад"

    # Розділ Гайди
    NEW_GUIDES = "🆕 Нові Гайди"
    POPULAR_GUIDES = "🌟 Топ Гайди"
    BEGINNER_GUIDES = "📘 Для Початківців"
    ADVANCED_TECHNIQUES = "🧙 Стратегії гри"
    TEAMPLAY_GUIDES = "🤝 Командна Гра"
    BACK_GUIDES = "🔙 Назад"

    # Розділ Контр-піки
    COUNTER_SEARCH = "🔎 Пошук"
    COUNTER_LIST = "📝 Список Персонажів"
    BACK_COUNTER_PICKS = "🔙 Назад"

    # Розділ Білди
    CREATE_BUILD = "🏗️ Створити"
    MY_BUILDS = "📄 Обрані"
    POPULAR_BUILDS = "🔥 Популярні"
    BACK_BUILDS = "🔙 Назад"

    # Розділ Голосування
    CURRENT_VOTES = "📍 Поточні Опитування"
    MY_VOTES = "📋 Мої Голосування"
    SUGGEST_TOPIC = "➕ Запропонувати Тему"
    BACK_VOTING = "🔙 Назад"

    # Розділ Профіль
    STATISTICS = "📈 Статистика"
    ACHIEVEMENTS = "🏆 Досягнення"
    SETTINGS = "⚙️ Налаштування"
    FEEDBACK = "💌 Зворотний Зв'язок"
    HELP = "❓ Допомога"
    BACK_TO_MAIN_MENU = "🔙 Назад до Головного Меню"

    # Підрозділ Статистика
    ACTIVITY = "📊 Загальна Активність"
    RANKING = "🥇 Рейтинг"
    GAME_STATS = "🎮 Ігрова Статистика"
    BACK_TO_PROFILE = "🔙 Назад"

    # Підрозділ Досягнення
    BADGES = "🎖️ Мої Бейджі"
    PROGRESS = "🚀 Прогрес"
    TOURNAMENT_STATS = "🏅 Турнірна Статистика"
    AWARDS = "🎟️ Отримані Нагороди"
    BACK_ACHIEVEMENTS = "🔙 Назад"

    # Підрозділ Налаштування
    LANGUAGE = "🌐 Мова Інтерфейсу"
    CHANGE_USERNAME = "ℹ️ Змінити Username"
    UPDATE_ID = "🆔 Оновити ID"
    NOTIFICATIONS = "🔔 Сповіщення"
    BACK_SETTINGS = "🔙 Назад"

    # Підрозділ Зворотний Зв'язок
    SEND_FEEDBACK = "✏️ Надіслати Відгук"
    REPORT_BUG = "🐛 Повідомити про Помилку"
    BACK_FEEDBACK = "🔙 Назад"

    # Підрозділ Допомога
    INSTRUCTIONS = "📄 Інструкції"
    FAQ = "❔ FAQ"
    HELP_SUPPORT = "📞 Підтримка"
    BACK_HELP = "🔙 Назад"

    # Підрозділи M6
    M6_TOURNAMENT_INFO = "🏆 Турнірна Інформація"
    M6_STATISTICS = "📈 Статистика M6"
    M6_NEWS = "📰 Новини M6"
    BACK_M6 = "🔙 Назад"

    # Підрозділи GPT
    GPT_DATA_GENERATION = "🤖 Генерація Даних"
    GPT_HINTS = "📝 Підказки"
    GPT_HERO_STATISTICS = "📊 Статистика Героїв"
    BACK_GPT = "🔙 Назад"

    # Підрозділи META
    META_HERO_LIST = "📋 Список Героїв у Мету"
    META_RECOMMENDATIONS = "🌟 Рекомендації"
    META_UPDATE = "🔄 Оновлення Мети"
    BACK_META = "🔙 Назад"

    # Підрозділи Турнірів
    CREATE_TOURNAMENT = "🆕 Створити Турнір"
    VIEW_TOURNAMENTS = "📋 Переглянути Турніри"
    BACK_TOURNAMENTS = "🔙 Назад"

    # Загальні кнопки
    BACK_TO_NAVIGATION = "🔙 Назад до Меню Навігації"
    BACK_TO_PROFILE_MENU = "🔙 Назад до Меню Профілю"

# Відповідність кнопок класам героїв
menu_button_to_class = {
    MenuButton.TANK.value: "Танк",
    MenuButton.MAGE.value: "Маг",
    MenuButton.MARKSMAN.value: "Стрілець",
    MenuButton.ASSASSIN.value: "Асасін",
    MenuButton.SUPPORT.value: "Підтримка",
    MenuButton.FIGHTER.value: "Боєць",
}

# Повний список героїв за класами
heroes_by_class = {
    "Танк": [
        "Alice", "Tigreal", "Akai", "Franco", "Minotaur", "Lolia", "Gatotkaca", "Grock",
        "Hylos", "Uranus", "Belerick", "Khufra", "Esmeralda", "Terizla", "Baxia", "Masha",
        "Atlas", "Barats", "Edith", "Fredrinn", "Johnson", "Hilda", "Carmilla", "Gloo", "Chip"
    ],
    "Маг": [
        "Vale", "Lunox", "Kadita", "Cecillion", "Luo Yi", "Xavier", "Novaria", "Zhuxin",
        "Harley", "Yve", "Aurora", "Faramis", "Esmeralda", "Kagura", "Cyclops", "Vexana",
        "Odette", "Zhask"
    ],
    "Стрілець": [
        "Popol and Kupa", "Brody", "Beatrix", "Natan", "Melissa", "Ixia", "Hanabi", "Claude",
        "Kimmy", "Granger", "Wanwan", "Miya", "Bruno", "Clint", "Layla", "Yi Sun-shin",
        "Moskov", "Roger", "Karrie", "Irithel", "Lesley"
    ],
    "Асасін": [
        "Saber", "Alucard", "Zilong", "Fanny", "Natalia", "Yi Sun-shin", "Lancelot",
        "Helcurt", "Lesley", "Selena", "Mathilda", "Paquito", "Yin", "Arlott", "Harley",
        "Suyou"
    ],
    "Підтримка": [
        "Rafaela", "Minotaur", "Lolita", "Estes", "Angela", "Faramis", "Mathilda",
        "Florin", "Johnson"
    ],
    "Боєць": [
        "Balmond", "Alucard", "Bane", "Zilong", "Freya", "Alpha", "Ruby", "Roger",
        "Gatotkaca", "Jawhead", "Martis", "Aldous", "Minsitthar", "Terizla", "X.Borg",
        "Dyroth", "Masha", "Silvanna", "Yu Zhong", "Khaleed", "Barats", "Paquito",
        "Phoveus", "Aulus", "Fiddrin", "Arlott", "Cici", "Kaja", "Leomord", "Thamuz",
        "Badang", "Guinevere"
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
            MenuButton.BUILDS,
            MenuButton.COUNTER_PICKS,
            MenuButton.GUIDES,
            MenuButton.VOTING,
            MenuButton.M6,
            MenuButton.GPT,
            MenuButton.META,
            MenuButton.TOURNAMENTS,
            MenuButton.BACK_NAVIGATION
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
            MenuButton.BACK_HEROES
        ],
        row_width=3
    )

def get_hero_class_menu(hero_class):
    heroes = heroes_by_class.get(hero_class, [])
    buttons = heroes.copy()
    # Розбиваємо кнопки на рядки по 3
    keyboard = [
        buttons[i:i+3] for i in range(0, len(buttons), 3)
    ]
    # Додаємо кнопку "🔙 Назад"
    keyboard.append([MenuButton.BACK_HEROES.value])
    logger.info(f"Створення меню класу героя '{hero_class}' з кнопками: {[button for row in keyboard for button in row]}")
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_guides_menu():
    return create_menu(
        [
            MenuButton.NEW_GUIDES,
            MenuButton.POPULAR_GUIDES,
            MenuButton.BEGINNER_GUIDES,
            MenuButton.ADVANCED_TECHNIQUES,
            MenuButton.TEAMPLAY_GUIDES,
            MenuButton.BACK_GUIDES
        ],
        row_width=3
    )

def get_counter_picks_menu():
    return create_menu(
        [
            MenuButton.COUNTER_SEARCH,
            MenuButton.COUNTER_LIST,
            MenuButton.BACK_COUNTER_PICKS
        ],
        row_width=3
    )

def get_builds_menu():
    return create_menu(
        [
            MenuButton.CREATE_BUILD,
            MenuButton.MY_BUILDS,
            MenuButton.POPULAR_BUILDS,
            MenuButton.BACK_BUILDS
        ],
        row_width=3
    )

def get_voting_menu():
    return create_menu(
        [
            MenuButton.CURRENT_VOTES,
            MenuButton.MY_VOTES,
            MenuButton.SUGGEST_TOPIC,
            MenuButton.BACK_VOTING
        ],
        row_width=3
    )

def get_profile_menu_buttons():
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
            MenuButton.BACK_ACHIEVEMENTS
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
            MenuButton.BACK_SETTINGS
        ],
        row_width=2
    )

def get_feedback_menu():
    return create_menu(
        [
            MenuButton.SEND_FEEDBACK,
            MenuButton.REPORT_BUG,
            MenuButton.BACK_FEEDBACK
        ],
        row_width=2
    )

def get_help_menu():
    return create_menu(
        [
            MenuButton.INSTRUCTIONS,
            MenuButton.FAQ,
            MenuButton.HELP_SUPPORT,
            MenuButton.BACK_HELP
        ],
        row_width=2
    )

def get_m6_menu():
    return create_menu(
        [
            MenuButton.M6_TOURNAMENT_INFO,
            MenuButton.M6_STATISTICS,
            MenuButton.M6_NEWS,
            MenuButton.BACK_M6
        ],
        row_width=2
    )

def get_gpt_menu():
    return create_menu(
        [
            MenuButton.GPT_DATA_GENERATION,
            MenuButton.GPT_HINTS,
            MenuButton.GPT_HERO_STATISTICS,
            MenuButton.BACK_GPT
        ],
        row_width=2
    )

def get_meta_menu():
    return create_menu(
        [
            MenuButton.META_HERO_LIST,
            MenuButton.META_RECOMMENDATIONS,
            MenuButton.META_UPDATE,
            MenuButton.BACK_META
        ],
        row_width=2
    )

def get_tournaments_menu():
    return create_menu(
        [
            MenuButton.CREATE_TOURNAMENT,
            MenuButton.VIEW_TOURNAMENTS,
            MenuButton.BACK_TOURNAMENTS
        ],
        row_width=2
    )