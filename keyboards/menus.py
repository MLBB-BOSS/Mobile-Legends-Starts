from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from enum import Enum
import logging

# Налаштування логування
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Enum для кнопок
class MenuButton(Enum):
    # Головне меню
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Профіль"
    # Навігаційне меню
    HEROES = "🛡️ Персонажі"
    GUIDES = "📚 Гайди"
    COUNTER_PICKS = "⚖️ Контр-піки"
    BUILDS = "⚜️ Білди"
    VOTING = "📊 Голосування"
    BACK = "🔄 Назад"
    # Меню героїв
    SEARCH_HERO = "🔎 Пошук Персонажа"
    TANK = "🛡️ Танк"
    MAGE = "🔮 Маг"
    MARKSMAN = "🏹 Стрілець"
    ASSASSIN = "⚔️ Асасін"
    SUPPORT = "🧬 Підтримка"

# Функція для створення клавіатури
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

# Головне меню
def get_main_menu():
    """
    Створює головне меню.
    :return: ReplyKeyboardMarkup
    """
    return create_menu(
        [MenuButton.NAVIGATION, MenuButton.PROFILE],
        row_width=2
    )

# Навігаційне меню
def get_navigation_menu():
    """
    Створює навігаційне меню.
    :return: ReplyKeyboardMarkup
    """

# Меню героїв
def get_heroes_menu():
    """
    Створює меню вибору героїв.
    :return: ReplyKeyboardMarkup
    """
    return create_menu(
        [
            MenuButton.SEARCH_HERO,
            MenuButton.TANK,
            MenuButton.MAGE,
            MenuButton.MARKSMAN,
            MenuButton.ASSASSIN,
            MenuButton.SUPPORT,
            MenuButton.BACK
        ],
        row_width=3
    )

# Меню гайдів
def get_guides_menu():
    """
    Створює меню гайдів.
    :return: ReplyKeyboardMarkup
    """
    return create_menu(
        [
            MenuButton.SEARCH_HERO,
            MenuButton.TANK,
            MenuButton.MAGE,
            MenuButton.MARKSMAN,
            MenuButton.ASSASSIN,
            MenuButton.SUPPORT,
            MenuButton.BACK
        ],
        row_width=3
    )

# Меню контр-піків
def get_counter_picks_menu():
    """
    Створює меню контр-піків.
    :return: ReplyKeyboardMarkup
    """
    return create_menu(
        [
            MenuButton.SEARCH_HERO,
            MenuButton.TANK,
            MenuButton.MAGE,
            MenuButton.MARKSMAN,
            MenuButton.ASSASSIN,
            MenuButton.SUPPORT,
            MenuButton.BACK
        ],
        row_width=3
    )

# Меню білдів
def get_builds_menu():
    """
    Створює меню білдів.
    :return: ReplyKeyboardMarkup
    """
    return create_menu(
        [
            MenuButton.SEARCH_HERO,
            MenuButton.TANK,
            MenuButton.MAGE,
            MenuButton.MARKSMAN,
            MenuButton.ASSASSIN,
            MenuButton.SUPPORT,
            MenuButton.BACK
        ],
        row_width=3
    )

# Меню голосування
def get_voting_menu():
    """
    Створює меню голосування.
    :return: ReplyKeyboardMarkup
    """
    return create_menu(
        [
            MenuButton.SEARCH_HERO,
            MenuButton.TANK,
            MenuButton.MAGE,
            MenuButton.MARKSMAN,
            MenuButton.ASSASSIN,
            MenuButton.SUPPORT,
            MenuButton.BACK
        ],
        row_width=3
    )

# Меню профілю
def get_profile_menu():
    """
    Створює меню профілю.
    :return: ReplyKeyboardMarkup
    """
    return create_menu(
        [
            MenuButton.SEARCH_HERO,
            MenuButton.TANK,
            MenuButton.MAGE,
            MenuButton.MARKSMAN,
            MenuButton.ASSASSIN,
            MenuButton.SUPPORT,
            MenuButton.BACK
        ],
        row_width=3
    )
