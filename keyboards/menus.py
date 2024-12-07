from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
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

    # Інші кнопки
    BACK = "🔙 Назад"
    BACK_TO_MAIN_MENU = "🔙 Меню"

    # Розділ Навігація
    HEROES = "🥷 Персонажі"
    GUIDES = "📚 Гайди"
    COUNTER_PICKS = "⚖️ Контр-піки"
    BUILDS = "🛡️ Білди"
    VOTING = "📊 Голосування"

    # Розділ Гайди
    NEW_GUIDES = "🆕 Нові Гайди"
    POPULAR_GUIDES = "🌟 Топ Гайди"
    BEGINNER_GUIDES = "📘 Новачкам"
    ADVANCED_TECHNIQUES = "🧙 Стратегії гри"
    TEAMPLAY_GUIDES = "🤝 Командна Гра"

    # Розділ Персонажі
    TANK = "🛡️ Танки"
    MAGE = "🧙‍♂️ Маги"
    MARKSMAN = "🏹 Стрільці"
    ASSASSIN = "⚔️ Асасіни"
    SUPPORT = "❤️ Сапорти"
    FIGHTER = "🗡️ Бійці"
    COMPARISON = "⚖️ Порівняти"
    SEARCH_HERO = "🔎 Шукати"

# Відповідність кнопок класам героїв
menu_button_to_class = {
    MenuButton.TANK.value: "Танк",
    MenuButton.MAGE.value: "Маг",
    MenuButton.MARKSMAN.value: "Стрілець",
    MenuButton.ASSASSIN.value: "Асасін",
    MenuButton.SUPPORT.value: "Підтримка",
    MenuButton.FIGHTER.value: "Боєць",
}

def create_menu(buttons, row_width=3):
    """
    Створює клавіатуру з кнопками.
    :param buttons: Список кнопок (MenuButton або str).
    :param row_width: Кількість кнопок у рядку.
    :return: ReplyKeyboardMarkup
    """
    keyboard_buttons = [
        KeyboardButton(text=button.value if isinstance(button, MenuButton) else button) for button in buttons
    ]
    keyboard = [
        keyboard_buttons[i:i + row_width]
        for i in range(0, len(keyboard_buttons), row_width)
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Головне меню
def get_main_menu():
    return create_menu(
        [
            MenuButton.NAVIGATION,
            MenuButton.PROFILE,
            MenuButton.META,
            MenuButton.M6,
            MenuButton.GPT,
        ],
        row_width=3
    )

# Меню Навігації
def get_navigation_menu():
    return create_menu(
        [
            MenuButton.HEROES,
            MenuButton.GUIDES,
            MenuButton.COUNTER_PICKS,
            MenuButton.BUILDS,
            MenuButton.VOTING,
            MenuButton.BACK,
        ],
        row_width=3
    )

# Меню Персонажів
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
            MenuButton.BACK,
        ],
        row_width=3
    )

# Меню Гайдів
def get_guides_menu():
    return create_menu(
        [
            MenuButton.NEW_GUIDES,
            MenuButton.POPULAR_GUIDES,
            MenuButton.BEGINNER_GUIDES,
            MenuButton.ADVANCED_TECHNIQUES,
            MenuButton.TEAMPLAY_GUIDES,
            MenuButton.BACK,
        ],
        row_width=3
    )

# Інші меню
def get_meta_menu():
    return create_menu(
        [
            "📈 Аналітика",
            "📊 Статистика",
            MenuButton.BACK_TO_MAIN_MENU,
        ],
        row_width=3
    )

def get_m6_menu():
    return create_menu(
        [
            "🏆 Результати",
            "🔍 Деталі",
            MenuButton.BACK_TO_MAIN_MENU,
        ],
        row_width=3
    )

def get_gpt_menu():
    return create_menu(
        [
            "📝 Задати питання",
            "❓ Допомога",
            MenuButton.BACK_TO_MAIN_MENU,
        ],
        row_width=3
    )

# Inline клавіатури
def get_generic_inline_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("MLS Button", callback_data="mls_button"),
                InlineKeyboardButton("🔙 Назад", callback_data="menu_back"),
            ]
        ]
    )
