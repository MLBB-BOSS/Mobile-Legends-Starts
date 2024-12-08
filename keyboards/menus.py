# keyboards/menus.py

from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardRemove
)
from enum import Enum
import logging

# Ініціалізація логера
logger = logging.getLogger(__name__)

class MenuButton(Enum):
    # Головне Меню
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Профіль"
    META = "🔥 META"
    M6 = "🏆 M6"
    GPT = "👾 GPT"

    # Інші кнопки...
    BACK = "🔙 Назад"
    BACK_TO_MAIN_MENU = "🔙 Меню"
    HEROES = "🦸‍♂️ Герої"

    # Класи героїв
    TANK = "🛡️ Танки"
    MAGE = "🧙‍♂️ Маги"
    MARKSMAN = "🏹 Стрільці"
    ASSASSIN = "⚔️ Асасіни"
    SUPPORT = "❤️ Сапорти"
    FIGHTER = "🗡️ Бійці"

    # Інші кнопки для меню Персонажі
    COUNTER_SEARCH = "🔎 Пошук Контр-піку"
    COUNTER_LIST = "📝 Список Персонажів"
    COMPARISON = "⚖️ Порівняти"
    SEARCH_HERO = "🔎 Шукати"

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

# Функції меню
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
            '📚 Гайди',
            '⚖️ Контр-піки',
            '🛡️ Білди',
            '📊 Голосування',
            MenuButton.META,
            MenuButton.M6,
            MenuButton.GPT,
            MenuButton.BACK
        ],
        row_width=3
    )

def get_profile_menu():
    return create_menu(
        [
            '📈 Статистика',
            '🏆 Досягнення',
            '⚙️ Налаштування',
            '💌 Зворотний Зв’язок',
            '❓ Допомога',
            MenuButton.BACK_TO_MAIN_MENU
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
            MenuButton.COUNTER_SEARCH,
            MenuButton.BACK
        ],
        row_width=3
    )

def get_hero_class_menu(hero_class: str) -> ReplyKeyboardMarkup:
    heroes_by_class = {
        "Танки": ["Герой1", "Герой2", "Герой3"],
        "Маги": ["Герой4", "Герой5", "Герой6"],
        "Стрільці": ["Герой7", "Герой8", "Герой9"],
        "Асасіни": ["Герой10", "Герой11", "Герой12"],
        "Сапорти": ["Герой13", "Герой14", "Герой15"],
        "Бійці": ["Герой16", "Герой17", "Герой18"],
    }
    heroes = heroes_by_class.get(hero_class, [])
    buttons = heroes.copy()
    buttons.append(MenuButton.BACK.value)
    return create_menu(buttons, row_width=3)

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
    button = InlineKeyboardButton("Розпочати 🚀", callback_data="intro_start")
    keyboard.add(button)
    return keyboard