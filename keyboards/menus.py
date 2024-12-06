# keyboards/menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from enum import Enum, auto
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
    META = "🔥 Мета"            # Новий
    M6 = "🏆 M6"                # Новий
    GPT = "👾 GPT"              # Новий
    BACK_NAV = "🔙"

    # Розділ Персонажі
    TANK = "🛡️ Танк"
    MAGE = "🧙‍♂️ Маг"
    MARKSMAN = "🏹 Стрілець"
    ASSASSIN = "⚔️ Асасін"
    SUPPORT = "❤️ Підтримка"
    FIGHTER = "🗡️ Боєць"
    COMPARE = "⚖️ Порівняння"
    SEARCH_HERO = "🔎 Пошук"

    # Розділ Гайди
    NEW_GUIDES = "🆕 Нові"
    POPULAR_GUIDES = "🌟 Популярні"
    BEGINNER_GUIDES = "📘 Початківці"
    ADVANCED_TECHNIQUES = "🧙 Стратегії"
    TEAMPLAY_GUIDES = "🤝 Команда"
    BACK_GUIDES = "🔙"

    # Розділ Контр-піків
    COUNTER_SEARCH = "🔎 Пошук"
    COUNTER_LIST = "📝 Список"
    BACK_COUNTER = "🔙"

    # Розділ Білди
    CREATE_BUILD = "🏗️ Створити"
    MY_BUILDS = "📄 Мої"
    POPULAR_BUILDS = "🔥 Популярні"
    BACK_BUILDS = "🔙"

    # Розділ Голосування
    CURRENT_VOTES = "📍 Поточні"
    MY_VOTES = "📋 Мої"
    SUGGEST_TOPIC = "➕ Запропонувати"
    BACK_VOTING = "🔙"

    # Розділ Профіль
    STATISTICS = "📈 Статистика"
    ACHIEVEMENTS = "🏆 Досягнення"
    SETTINGS = "⚙️ Налаштування"
    FEEDBACK = "💌 Відгук"
    HELP = "❓ Допомога"
    BACK_PROFILE = "🔙"

    # Підрозділ Статистика
    ACTIVITY = "📊 Активність"
    RANKING = "🥇 Рейтинг"
    GAME_STATS = "🎮 Статистика"
    BACK_STATS = "🔙"

    # Підрозділ Досягнень
    BADGES = "🎖️ Бейджі"
    PROGRESS = "🚀 Прогрес"
    TOURNAMENT_STATS = "🏅 Турніри"
    AWARDS = "🎟️ Нагороди"
    BACK_ACHIEVEMENTS = "🔙"

    # Підрозділ Налаштування
    LANGUAGE = "🌐 Мова"
    CHANGE_USERNAME = "ℹ️ Username"
    UPDATE_ID = "🆔 Оновити ID"
    NOTIFICATIONS = "🔔 Сповіщення"
    BACK_SETTINGS = "🔙"

    # Підрозділ Зворотний Зв'язок
    SEND_FEEDBACK = "✏️ Відгук"
    REPORT_BUG = "🐛 Помилка"
    BACK_FEEDBACK = "🔙"

    # Підрозділ Допомога
    INSTRUCTIONS = "📄 Інструкції"
    FAQ = "❔ FAQ"
    HELP_SUPPORT = "📞 Підтримка"
    BACK_HELP = "🔙"

# Відповідність кнопок класам героїв
menu_button_to_class = {
    MenuButton.TANK.value: "Танк",
    MenuButton.MAGE.value: "Маг",
    MenuButton.MARKSMAN.value: "Стрілець",
    MenuButton.ASSASSIN.value: "Асасін",
    MenuButton.SUPPORT.value: "Підтримка",
    MenuButton.FIGHTER.value: "Боєць",
    MenuButton.META.value: "Мета",
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
        "Karrie", "Irithel", "Lesley"  # Переконайтеся, що "Lesley" належить тільки до Асасін
    ],
    "Маг": [
        "Vale", "Lunox", "Kadita", "Cecillion", "Luo Yi", "Xavier", "Novaria", "Zhuxin",
        "Yve", "Aurora", "Faramis", "Esmeralda", "Kagura", "Cyclops", "Vexana", "Odette", "Zhask"
    ],
    "Підтримка": [
        "Rafaela", "Lolita", "Estes", "Angela", "Florin", "Johnson"  # "Johnson" вже є в Танк
    ],
    "Мета": [
        "MetaHero1", "MetaHero2"  # Додайте тут Метових персонажів, якщо вони існують
    ],
}

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
            MenuButton.BACK_NAV
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
            MenuButton.COMPARE,
            MenuButton.SEARCH_HERO,
            MenuButton.BACK_NAV
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
            MenuButton.BACK_GUIDES
        ],
        "row_width": 3
    },
    "counter_picks": {
        "buttons": [
            MenuButton.COUNTER_SEARCH,
            MenuButton.COUNTER_LIST,
            MenuButton.BACK_COUNTER
        ],
        "row_width": 3
    },
    "builds": {
        "buttons": [
            MenuButton.CREATE_BUILD,
            MenuButton.MY_BUILDS,
            MenuButton.POPULAR_BUILDS,
            MenuButton.BACK_BUILDS
        ],
        "row_width": 3
    },
    "voting": {
        "buttons": [
            MenuButton.CURRENT_VOTES,
            MenuButton.MY_VOTES,
            MenuButton.SUGGEST_TOPIC,
            MenuButton.BACK_VOTING
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
            MenuButton.BACK_PROFILE
        ],
        "row_width": 3
    },
    "statistics": {
        "buttons": [
            MenuButton.ACTIVITY,
            MenuButton.RANKING,
            MenuButton.GAME_STATS,
            MenuButton.BACK_STATS
        ],
        "row_width": 3
    },
    "achievements": {
        "buttons": [
            MenuButton.BADGES,
            MenuButton.PROGRESS,
            MenuButton.TOURNAMENT_STATS,
            MenuButton.AWARDS,
            MenuButton.BACK_ACHIEVEMENTS
        ],
        "row_width": 3
    },
    "settings": {
        "buttons": [
            MenuButton.LANGUAGE,
            MenuButton.CHANGE_USERNAME,
            MenuButton.UPDATE_ID,
            MenuButton.NOTIFICATIONS,
            MenuButton.BACK_SETTINGS
        ],
        "row_width": 3
    },
    "feedback": {
        "buttons": [
            MenuButton.SEND_FEEDBACK,
            MenuButton.REPORT_BUG,
            MenuButton.BACK_FEEDBACK
        ],
        "row_width": 3
    },
    "help": {
        "buttons": [
            MenuButton.INSTRUCTIONS,
            MenuButton.FAQ,
            MenuButton.HELP_SUPPORT,
            MenuButton.BACK_HELP
        ],
        "row_width": 3
    }
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

def get_menu(menu_name):
    """
    Генерує клавіатуру для заданого меню.
    :param menu_name: Ідентифікатор меню.
    :return: ReplyKeyboardMarkup
    """
    menu = menus.get(menu_name)
    if not menu:
        logger.error(f"Меню '{menu_name}' не знайдено.")
        return ReplyKeyboardMarkup(resize_keyboard=True)
    return create_menu(menu["buttons"], menu["row_width"])

def get_main_menu():
    """
    Генерує клавіатуру для головного меню.
    :return: ReplyKeyboardMarkup
    """
    return get_menu("main")

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

    keyboard_buttons = [KeyboardButton(text=hero) for hero in heroes]
    # Додаємо кнопку "🔙" для повернення
    keyboard_buttons.append(KeyboardButton(text=MenuButton.BACK_NAV.value))

    row_width = 3
    keyboard = [
        keyboard_buttons[i:i + row_width]
        for i in range(0, len(keyboard_buttons), row_width)
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Додаткові функції для спеціальних меню, якщо необхідно
# Наприклад, можна додати функції для динамічного створення меню героїв

# Приклад використання
# main_menu = get_main_menu()
# navigation_menu = get_menu("navigation")
