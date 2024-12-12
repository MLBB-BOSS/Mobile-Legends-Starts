# keyboards/menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
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
    GUIDES = "📚 Гайди"
    COUNTER_PICKS = "⚖️ Контр-піки"
    BUILDS = "🛡️ Білди"
    VOTING = "📊 Голосування"
    M6 = "🏆 M6"
    GPT = "🤖 GPT"
    META = "🔥 META"
    TOURNAMENTS = "🏆 Турніри"
    BACK = "🔙 Повернутися"

    # Підменю Персонажів
    TANK = "🛡️ Танк"
    MAGE = "🧙‍♂️ Маг"
    MARKSMAN = "🏹 Стрілець"
    ASSASSIN = "⚔️ Асасін"
    SUPPORT = "❤️ Підтримка"
    FIGHTER = "🗡️ Боєць"
    COMPARISON = "⚖️ Порівняння"
    SEARCH_HERO = "🔎 Пошук"

    # Підменю Білд
    CREATE_BUILD = "🏗️ Створити"
    MY_BUILDS = "📄 Мої білди"
    POPULAR_BUILDS = "🔥 Популярні білди"

    # Підменю Контр-піки
    COUNTER_SEARCH = "🔎 Пошук контр-піка"
    COUNTER_LIST = "📝 Список контр-піків"

    # Підменю Гайди
    NEW_GUIDES = "🆕 Нові гайди"
    POPULAR_GUIDES = "🌟 Топ гайди"
    BEGINNER_GUIDES = "📘 Для початківців"
    ADVANCED_TECHNIQUES = "🧙 Стратегії гри"
    TEAMPLAY_GUIDES = "🤝 Командна гра"

    # Підменю Голосування
    CURRENT_VOTES = "📍 Поточні опитування"
    MY_VOTES = "📋 Мої голосування"
    SUGGEST_TOPIC = "➕ Запропонувати тему"

    # Підменю Профілю
    STATISTICS = "📈 Статистика"
    ACHIEVEMENTS = "🏆 Досягнення"
    SETTINGS = "⚙️ Налаштування"
    FEEDBACK = "💌 Зворотний зв'язок"
    HELP = "❓ Допомога"
    BACK_TO_MAIN_MENU = "🔙 Повернутися до головного меню"

    # Підменю Статистика
    ACTIVITY = "📊 Загальна активність"
    RANKING = "🥇 Рейтинг"
    GAME_STATS = "🎮 Ігрова статистика"
    BACK_TO_PROFILE = "🔙 Повернутися до профілю"

    # Підменю Досягнення
    BADGES = "🎖️ Мої бейджі"
    PROGRESS = "🚀 Прогрес"
    TOURNAMENT_STATS = "🏅 Турнірна статистика"
    AWARDS = "🎟️ Отримані нагороди"

    # Підменю Налаштування
    LANGUAGE = "🌐 Мова інтерфейсу"
    CHANGE_USERNAME = "ℹ️ Змінити Username"
    UPDATE_ID = "🆔 Оновити ID"
    NOTIFICATIONS = "🔔 Сповіщення"

    # Підменю Зворотний зв'язок
    SEND_FEEDBACK = "📝 Надіслати відгук"
    REPORT_BUG = "🐛 Повідомити про помилку"

    # Підменю Допомога
    INSTRUCTIONS = "📄 Інструкції"
    FAQ = "❔ FAQ"
    HELP_SUPPORT = "📞 Підтримка"

    # Підменю Турніри
    CREATE_TOURNAMENT = "🆕 Створити турнір"
    VIEW_TOURNAMENTS = "📋 Переглянути турніри"

    # Підменю META
    META_HERO_LIST = "📋 Список героїв у меті"
    META_RECOMMENDATIONS = "🌟 Рекомендації"
    META_UPDATES = "🔄 Оновлення мети"

    # Підменю M6
    M6_INFO = "🏆 Інформація M6"
    M6_STATS = "📈 Статистика M6"
    M6_NEWS = "📰 Новини M6"

    # Підменю GPT
    GPT_FEATURES = "📚 Функції GPT"

def create_menu(buttons, row_width=2):
    """
    Створює клавіатуру з кнопками.
    :param buttons: Список кнопок (MenuButton або str).
    :param row_width: Кількість кнопок у рядку.
    :return: ReplyKeyboardMarkup
    """
    if not all(isinstance(button, MenuButton) or isinstance(button, str) for button in buttons):
        raise ValueError("Усі елементи у списку кнопок повинні бути екземплярами MenuButton або str.")

    button_texts = [button.value if isinstance(button, MenuButton) else button for button in buttons]
    logger.info(f"Створення меню з кнопками: {button_texts}")

    keyboard_buttons = [
        KeyboardButton(text=button.value if isinstance(button, MenuButton) else button) for button in buttons
    ]

    keyboard = [
        keyboard_buttons[i:i + row_width]
        for i in range(0, len(keyboard_buttons), row_width)
    ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def create_inline_menu(buttons):
    """
    Створює інлайн клавіатуру з кнопками.
    :param buttons: Список інлайн кнопок (InlineKeyboardButton).
    :return: InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[buttons]
    )

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
            MenuButton.M6,
            MenuButton.GPT,
            MenuButton.META,
            MenuButton.TOURNAMENTS,
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

def get_hero_class_menu(hero_class):
    heroes = heroes_by_class.get(hero_class, [])
    if not heroes:
        logger.warning(f"Клас героїв '{hero_class}' не знайдено.")

    # Додаємо кнопку "🔙 Повернутися" для повернення
    buttons = heroes + [MenuButton.BACK]

    logger.info(f"Створення меню для класу '{hero_class}' з героями: {buttons}")

    return create_menu(buttons, row_width=3)

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

# Додавання функцій для Турнірів
def get_tournaments_menu():
    return create_menu(
        [
            MenuButton.CREATE_TOURNAMENT,  # Створити турнір
            MenuButton.VIEW_TOURNAMENTS,   # Переглянути турніри
            MenuButton.BACK
        ],
        row_width=2
    )

def get_active_tournaments_menu():
    # Заглушка для перегляду активних турнірів
    tournaments = [
        {"name": "Турнір А", "type": "5х5", "status": "Активний"},
        {"name": "Турнір Б", "type": "2х2", "status": "Завершений"},
        # Додайте більше турнірів за потребою
    ]

    keyboard = []
    for tournament in tournaments:
        button_text = f"{tournament['name']} ({tournament['type']}) - {tournament['status']}"
        keyboard.append([KeyboardButton(text=button_text)])

    keyboard.append([MenuButton.BACK.value])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Додавання функцій для META
def get_meta_menu():
    return create_menu(
        [
            MenuButton.META_HERO_LIST,
            MenuButton.META_RECOMMENDATIONS,
            MenuButton.META_UPDATES,
            MenuButton.BACK
        ],
        row_width=2
    )

# Додавання функцій для M6
def get_m6_menu():
    return create_menu(
        [
            MenuButton.M6_INFO,
            MenuButton.M6_STATS,
            MenuButton.M6_NEWS,
            MenuButton.BACK
        ],
        row_width=2
    )

# Додавання функцій для GPT
def get_gpt_menu():
    return create_menu(
        [
            MenuButton.GPT_FEATURES,
            MenuButton.BACK
        ],
        row_width=2
    )

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