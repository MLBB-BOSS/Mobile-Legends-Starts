# keyboards/menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from enum import Enum
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MenuButton(Enum):
    # Головне Меню
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Профіль"

    # Розділ Навігація
    HEROES = "🥷 Персонажі"
    GUIDES = "📚 Гайди"
    COUNTER_PICKS = "⚖️ Контр-піки"
    BUILDS = "🛡️ Білди"
    VOTING = "📊 Голосування"
    META = "🔥 META"            # Новий
    M6 = "🏆 M6"                # Новий
    GPT = "👾 GPT"              # Новий
    BACK = "🔙"                 # Універсальна кнопка "Back"

    # Розділ Персонажі
    TANK = "🛡️ Танк"
    MAGE = "🧙‍♂️ Маг"
    MARKSMAN = "🏹 Стрілець"
    ASSASSIN = "⚔️ Асасін"
    SUPPORT = "❤️ Підтримка"
    FIGHTER = "🗡️ Боєць"
    COMPARISON = "⚖️ Порівняння"
    SEARCH_HERO = "🔎 Пошук"

    # Розділ Гайди
    NEW_GUIDES = "🆕 Нові Гайди"
    POPULAR_GUIDES = "🌟 Популярні Гайди"
    BEGINNER_GUIDES = "📘 Початківці"
    ADVANCED_TECHNIQUES = "🧙 Стратегії"
    TEAMPLAY_GUIDES = "🤝 Командна Гра"

    # Розділ Контр-піків
    COUNTER_SEARCH = "🔎 Пошук"
    COUNTER_LIST = "📝 Список Персонажів"

    # Розділ Білди
    CREATE_BUILD = "🏗️ Створити"
    MY_BUILDS = "📄 Обрані"
    POPULAR_BUILDS = "🔥 Популярні"

    # Розділ Голосування
    CURRENT_VOTES = "📍 Поточні Опитування"
    MY_VOTES = "📋 Мої Голосування"
    SUGGEST_TOPIC = "➕ Запропонувати Тему"

    # Розділ Профіль
    STATISTICS = "📈 Статистика"
    ACHIEVEMENTS = "🏆 Досягнення"
    SETTINGS = "⚙️ Налаштування"
    FEEDBACK = "💌 Відгук"
    HELP = "❓ Допомога"

    # Підрозділ Статистика
    ACTIVITY = "📊 Активність"
    RANKING = "🥇 Рейтинг"
    GAME_STATS = "🎮 Ігрова Статистика"

    # Підрозділ Досягнень
    BADGES = "🎖️ Бейджі"
    PROGRESS = "🚀 Прогрес"
    TOURNAMENT_STATS = "🏅 Турнірна Статистика"
    AWARDS = "🎟️ Нагороди"

    # Підрозділ Налаштування
    LANGUAGE = "🌐 Мова Інтерфейсу"
    CHANGE_USERNAME = "ℹ️ Змінити Username"
    UPDATE_ID = "🆔 Оновити ID"
    NOTIFICATIONS = "🔔 Сповіщення"

    # Підрозділ Зворотний Зв'язок
    SEND_FEEDBACK = "✏️ Надіслати Відгук"
    REPORT_BUG = "🐛 Повідомити про Помилку"

    # Підрозділ Допомога
    INSTRUCTIONS = "📄 Інструкції"
    FAQ = "❔ FAQ"
    HELP_SUPPORT = "📞 Підтримка"

# Відповідність кнопок класам героїв
menu_button_to_class = {
    MenuButton.TANK.value: "Танк",
    MenuButton.MAGE.value: "Маг",
    MenuButton.MARKSMAN.value: "Стрілець",
    MenuButton.ASSASSIN.value: "Асасін",
    MenuButton.SUPPORT.value: "Підтримка",
    MenuButton.FIGHTER.value: "Боєць",
    MenuButton.META.value: "META",
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
        "Alice", "Tigreal", "Akai", "Franco", "Minotaur", "Lolia", "Grock",
        "Hylos", "Uranus", "Belerick", "Khufra", "Esmeralda", "Baxia",
        "Atlas", "Edith", "Fredrinn", "Johnson", "Hilda", "Carmilla", "Gloo", "Chip"
    ],
    "Асасін": [
        "Saber", "Alucard", "Zilong", "Fanny", "Natalia", "Yi Sun-shin", "Lancelot", "Helcurt",
        "Lesley", "Selena", "Mathilda", "Paquito", "Yin", "Arlott", "Harley", "Suyou"
    ],
    "Стрілець": [
        "Popol and Kupa", "Brody", "Beatrix", "Natan", "Melissa", "Ixia", "Hanabi", "Claude",
        "Kimmy", "Granger", "Wanwan", "Miya", "Bruno", "Clint", "Layla", "Moskov",
        "Karrie", "Irithel", "Lesley"
    ],
    "Маг": [
        "Vale", "Lunox", "Kadita", "Cecillion", "Luo Yi", "Xavier", "Novaria", "Zhuxin",
        "Yve", "Aurora", "Faramis", "Esmeralda", "Kagura", "Cyclops", "Vexana", "Odette", "Zhask"
    ],
    "Підтримка": [
        "Rafaela", "Lolita", "Estes", "Angela", "Florin", "Johnson"  # "Johnson" вже є в Танк
    ],
    "META": [
        "MetaHero1", "MetaHero2"  # Додайте тут Метових персонажів, якщо вони існують
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

# Структура меню
menus = {
    "main": {
        "buttons": [
            MenuButton.NAVIGATION,
            MenuButton.PROFILE
        ],
        "row_width": 2
    },
    "navigation": {
        "buttons": [
            MenuButton.HEROES,
            MenuButton.GUIDES,
            MenuButton.COUNTER_PICKS,
            MenuButton.BUILDS,
            MenuButton.VOTING,
            MenuButton.META,        # Додано
            MenuButton.M6,           # Додано
            MenuButton.GPT,          # Додано
            MenuButton.BACK
        ],
        "row_width": 3
    },
    "heroes": {
        "buttons": [
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
        "row_width": 3
    },
    "guides": {
        "buttons": [
            MenuButton.NEW_GUIDES,
            MenuButton.POPULAR_GUIDES,
            MenuButton.BEGINNER_GUIDES,
            MenuButton.ADVANCED_TECHNIQUES,
            MenuButton.TEAMPLAY_GUIDES,
            MenuButton.BACK
        ],
        "row_width": 3
    },
    "counter_picks": {
        "buttons": [
            MenuButton.COUNTER_SEARCH,
            MenuButton.COUNTER_LIST,
            MenuButton.BACK
        ],
        "row_width": 3
    },
    "builds": {
        "buttons": [
            MenuButton.CREATE_BUILD,
            MenuButton.MY_BUILDS,
            MenuButton.POPULAR_BUILDS,
            MenuButton.BACK
        ],
        "row_width": 3
    },
    "voting": {
        "buttons": [
            MenuButton.CURRENT_VOTES,
            MenuButton.MY_VOTES,
            MenuButton.SUGGEST_TOPIC,
            MenuButton.BACK
        ],
        "row_width": 3
    },
    "profile": {
        "buttons": [
            MenuButton.STATISTICS,
            MenuButton.ACHIEVEMENTS,
            MenuButton.SETTINGS,
            MenuButton.FEEDBACK,
            MenuButton.HELP,
            MenuButton.BACK
        ],
        "row_width": 3
    },
    "statistics": {
        "buttons": [
            MenuButton.ACTIVITY,
            MenuButton.RANKING,
            MenuButton.GAME_STATS,
            MenuButton.BACK
        ],
        "row_width": 3
    },
    "achievements": {
        "buttons": [
            MenuButton.BADGES,
            MenuButton.PROGRESS,
            MenuButton.TOURNAMENT_STATS,
            MenuButton.AWARDS,
            MenuButton.BACK
        ],
        "row_width": 3
    },
    "settings": {
        "buttons": [
            MenuButton.LANGUAGE,
            MenuButton.CHANGE_USERNAME,
            MenuButton.UPDATE_ID,
            MenuButton.NOTIFICATIONS,
            MenuButton.BACK
        ],
        "row_width": 3
    },
    "feedback": {
        "buttons": [
            MenuButton.SEND_FEEDBACK,
            MenuButton.REPORT_BUG,
            MenuButton.BACK
        ],
        "row_width": 3
    },
    "help": {
        "buttons": [
            MenuButton.INSTRUCTIONS,
            MenuButton.FAQ,
            MenuButton.HELP_SUPPORT,
            MenuButton.BACK
        ],
        "row_width": 3
    }
}

def get_menu(menu_name):
    """
    Генерує клавіатуру для заданого меню.
    :param menu_name: Ідентифікатор меню.
    :return: ReplyKeyboardMarkup
    """
    menu = menus.get(menu_name)
    if not menu:
        logger.error(f"Меню '{menu_name}' не знайдено. Повертається головне меню.")
        return get_main_menu()
    return create_menu(menu["buttons"], menu["row_width"])

def get_main_menu():
    """
    Генерує клавіатуру для головного меню.
    :return: ReplyKeyboardMarkup
    """
    return get_menu("main")

def get_navigation_menu():
    """
    Генерує клавіатуру для меню Навігація.
    :return: ReplyKeyboardMarkup
    """
    return get_menu("navigation")

def get_heroes_menu():
    """
    Генерує клавіатуру для меню Персонажі.
    :return: ReplyKeyboardMarkup
    """
    return get_menu("heroes")

def get_guides_menu():
    """
    Генерує клавіатуру для меню Гайди.
    :return: ReplyKeyboardMarkup
    """
    return get_menu("guides")

def get_counter_picks_menu():
    """
    Генерує клавіатуру для меню Контр-піки.
    :return: ReplyKeyboardMarkup
    """
    return get_menu("counter_picks")

def get_builds_menu():
    """
    Генерує клавіатуру для меню Білди.
    :return: ReplyKeyboardMarkup
    """
    return get_menu("builds")

def get_voting_menu():
    """
    Генерує клавіатуру для меню Голосування.
    :return: ReplyKeyboardMarkup
    """
    return get_menu("voting")

def get_profile_menu():
    """
    Генерує клавіатуру для меню Профіль.
    :return: ReplyKeyboardMarkup
    """
    return get_menu("profile")

def get_statistics_menu():
    """
    Генерує клавіатуру для меню Статистика.
    :return: ReplyKeyboardMarkup
    """
    return get_menu("statistics")

def get_achievements_menu():
    """
    Генерує клавіатуру для меню Досягнення.
    :return: ReplyKeyboardMarkup
    """
    return get_menu("achievements")

def get_settings_menu():
    """
    Генерує клавіатуру для меню Налаштування.
    :return: ReplyKeyboardMarkup
    """
    return get_menu("settings")

def get_feedback_menu():
    """
    Генерує клавіатуру для меню Зворотний Зв'язок.
    :return: ReplyKeyboardMarkup
    """
    return get_menu("feedback")

def get_help_menu():
    """
    Генерує клавіатуру для меню Допомога.
    :return: ReplyKeyboardMarkup
    """
    return get_menu("help")

def get_hero_class_menu(hero_class):
    """
    Створює клавіатуру для обраного класу героя.
    :param hero_class: Назва класу героя.
    :return: ReplyKeyboardMarkup
    """
    heroes = heroes_by_class.get(hero_class, [])
    if not heroes:
        logger.warning(f"Не знайдено героїв для класу: {hero_class}")
        return get_menu("heroes")  # Повертаємо до меню персонажів

    # Додаємо кнопку "🔙" для повернення
    buttons = heroes + [MenuButton.BACK.value]
    return create_menu(
        buttons,
        row_width=3
)
