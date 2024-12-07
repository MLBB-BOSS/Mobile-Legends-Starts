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

    # Розділ Навігація
    HEROES = "🥷 Персонажі"
    GUIDES = "📚 Гайди"
    COUNTER_PICKS = "⚖️ Контр-піки"
    BUILDS = "🛡️ Білди"
    VOTING = "📊 Голосування"
    BACK = "🔙 Назад"

    # Розділ Персонажі
    TANK = "🛡️ Танки"
    MAGE = "🧙‍♂️ Маги"
    MARKSMAN = "🏹 Стрільці"
    ASSASSIN = "⚔️ Асасіни"
    SUPPORT = "❤️ Сапорти"
    FIGHTER = "🗡️ Бійці"
    COMPARISON = "⚖️ Порівняти"
    SEARCH_HERO = "🔎 Шукати"

    # Розділ Гайди
    NEW_GUIDES = "🆕 Нові Гайди"
    POPULAR_GUIDES = "🌟 Топ Гайди"
    BEGINNER_GUIDES = "📘 Новачкам"
    ADVANCED_TECHNIQUES = "🧙 Стратегії гри"
    TEAMPLAY_GUIDES = "🤝 Командна Гра"

    # Розділ Контр-піки
    COUNTER_SEARCH = "🔎 Пошук Контр-піку"
    COUNTER_LIST = "📝 Список Персонажів"

    # Розділ Білди
    CREATE_BUILD = "🏗️ Створити Білд"
    MY_BUILDS = "📄 Збережені Білди"
    POPULAR_BUILDS = "🔥 Популярні Білди"

    # Розділ Голосування
    CURRENT_VOTES = "📍 Поточні Опитування"
    MY_VOTES = "📋 Мої Голосування"
    SUGGEST_TOPIC = "➕ Запропонувати Тему"

    # Розділ Профіль
    STATISTICS = "📈 Статистика"
    ACHIEVEMENTS = "🏆 Досягнення"
    SETTINGS = "⚙️ Налаштування"
    FEEDBACK = "💌 Зворотний Зв’язок"
    HELP = "❓ Допомога"
    BACK_TO_MAIN_MENU = "🔙 Меню"

    # Підрозділ Статистика
    ACTIVITY = "📊 Загальна Активність"
    RANKING = "🥇 Рейтинг"
    GAME_STATS = "🎮 Ігрова Статистика"

    # Підрозділ Досягнення
    BADGES = "🎖️ Мої Бейджі"
    PROGRESS = "🚀 Прогрес"
    TOURNAMENT_STATS = "🏅 Турнірна Статистика"
    AWARDS = "🎟️ Отримані Нагороди"

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
    MenuButton.SUPPORT.value: "Сапорт",
    MenuButton.FIGHTER.value: "Бійці",
}

# Повний список героїв за класами
heroes_by_class = {
    "Танк": [
        "Alice", "Tigreal", "Akai", "Franco", "Minotaur", "Lolia", "Gatotkaca", "Grock",
        "Hylos", "Uranus", "Belerick", "Khufra", "Esmeralda", "Terizla", "Baxia", "Masha",
        "Atlas", "Barats", "Edith", "Fredrinn", "Johnson", "Hilda", "Carmilla", "Gloo", "Chip"
    ],
    "Маг": [
        "Vale", "Lunox", "Kadita", "Cecillion", "Luo Yi", "Xavier", "Novaria", "Zhuxin", "Harley",
        "Yve", "Aurora", "Faramis", "Esmeralda", "Kagura", "Cyclops", "Vexana", "Odette", "Zhask"
    ],
    "Стрілець": [
        "Popol and Kupa", "Brody", "Beatrix", "Natan", "Melissa", "Ixia", "Hanabi", "Claude",
        "Kimmy", "Granger", "Wanwan", "Miya", "Bruno", "Clint", "Layla", "Yi Sun-shin", "Moskov",
        "Roger", "Karrie", "Irithel", "Lesley"
    ],
    "Асасін": [
        "Saber", "Alucard", "Zilong", "Fanny", "Natalia", "Yi Sun-shin", "Lancelot", "Helcurt",
        "Lesley", "Selena", "Mathilda", "Paquito", "Yin", "Arlott", "Harley", "Suyou"
    ],
    "Підтримка": [
        "Rafaela", "Minotaur", "Lolita", "Estes", "Angela", "Faramis", "Mathilda", "Florin", "Johnson"
    ],
    "Боєць": [
        "Balmond", "Alucard", "Bane", "Zilong", "Freya", "Alpha", "Ruby", "Roger",
        "Gatotkaca", "Jawhead", "Martis", "Aldous", "Minsitthar", "Terizla", "X.Borg",
        "Dyroth", "Masha", "Silvanna", "Yu Zhong", "Khaleed", "Barats", "Paquito",
        "Phoveus", "Aulus", "Fiddrin", "Arlott", "Cici", "Kaja", "Leomord", "Thamuz",
        "Badang", "Guinevere"
    ],
}

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

# Відновлені функції меню

def get_main_menu():
    return create_menu(
        [
            MenuButton.NAVIGATION,
            MenuButton.PROFILE,
            MenuButton.META,
            MenuButton.M6,
            MenuButton.GPT
        ],
        row_width=3  # Розміщення у двох рядках по три кнопки
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
        row_width=3  # Розміщення у двох рядках по три кнопки
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
        row_width=3  # Розміщення у двох рядках по три кнопки
    )

def get_meta_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [MenuButton.ACTIVITY.value, MenuButton.RANKING.value, MenuButton.GAME_STATS.value],
            [MenuButton.BACK_TO_MAIN_MENU.value],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_m6_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            ['🏆 Результати', '🔍 Деталі', MenuButton.BACK_TO_MAIN_MENU.value],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_gpt_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [MenuButton.GPT.value, '📝 Задати питання', '❓ Допомога'],
            [MenuButton.BACK_TO_MAIN_MENU.value],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_profile_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [MenuButton.STATISTICS.value, MenuButton.ACHIEVEMENTS.value, MenuButton.SETTINGS.value],
            [MenuButton.FEEDBACK.value, MenuButton.HELP.value, MenuButton.BACK_TO_MAIN_MENU.value],
        ],
        resize_keyboard=True
    )
    return keyboard

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
        row_width=3  # Розміщення у трьох рядках по три кнопки
    )

def get_hero_class_menu(hero_class: str) -> ReplyKeyboardMarkup:
    # Створення клавіатури з героями певного класу
    heroes = heroes_by_class.get(hero_class, [])
    buttons = [KeyboardButton(text=hero) for hero in heroes]
    # Додатково додаємо кнопку '🔙 Назад'
    buttons.append(KeyboardButton(text=MenuButton.BACK.value))
    row_width = 3
    keyboard = [
        buttons[i:i + row_width]
        for i in range(0, len(buttons), row_width)
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

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
        row_width=3  # Розміщення у двох рядках
    )

def get_voting_menu() -> ReplyKeyboardMarkup:
    return create_menu(
        [
            MenuButton.CURRENT_VOTES,
            MenuButton.MY_VOTES,
            MenuButton.SUGGEST_TOPIC,
            MenuButton.BACK
        ],
        row_width=3  # Розміщення у двох рядках
    )

def get_statistics_menu() -> ReplyKeyboardMarkup:
    return create_menu(
        [
            MenuButton.ACTIVITY,
            MenuButton.RANKING,
            MenuButton.GAME_STATS,
            MenuButton.BACK_TO_MAIN_MENU
        ],
        row_width=3  # Розміщення у двох рядках
    )

def get_achievements_menu() -> ReplyKeyboardMarkup:
    return create_menu(
        [
            MenuButton.BADGES,
            MenuButton.PROGRESS,
            MenuButton.TOURNAMENT_STATS,
            MenuButton.AWARDS,
            MenuButton.BACK_TO_MAIN_MENU
        ],
        row_width=3  # Розміщення у двох рядках
    )

def get_settings_menu() -> ReplyKeyboardMarkup:
    return create_menu(
        [
            MenuButton.LANGUAGE,
            MenuButton.CHANGE_USERNAME,
            MenuButton.UPDATE_ID,
            MenuButton.NOTIFICATIONS,
            MenuButton.BACK_TO_MAIN_MENU
        ],
        row_width=3  # Розміщення у двох рядках
    )

def get_feedback_menu() -> ReplyKeyboardMarkup:
    return create_menu(
        [
            MenuButton.SEND_FEEDBACK,
            MenuButton.REPORT_BUG,
            MenuButton.BACK_TO_MAIN_MENU
        ],
        row_width=3  # Розміщення у одному рядку з трьома кнопками
    )

def get_help_menu() -> ReplyKeyboardMarkup:
    return create_menu(
        [
            MenuButton.INSTRUCTIONS,
            MenuButton.FAQ,
            MenuButton.HELP_SUPPORT,
            MenuButton.BACK_TO_MAIN_MENU
        ],
        row_width=3  # Розміщення у двох рядках
    )

# Функції для створення Inline Keyboards залишаються без змін

def get_generic_inline_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("MLS Button", callback_data="mls_button"),
        InlineKeyboardButton("🔙 Назад", callback_data="menu_back"),
    ]
    keyboard.add(*buttons)
    return keyboard

def get_intro_page_1_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Далі", callback_data="intro_next_1")
    keyboard.add(button)
    return keyboard

def get_intro_page_2_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Далі", callback_data="intro_next_2")
    keyboard.add(button)
    return keyboard

def get_intro_page_3_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Розпочати", callback_data="intro_start")
    keyboard.add(button)
    return keyboard
