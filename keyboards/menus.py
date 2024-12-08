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

    # Інші кнопки...
    BACK = "🔙 Назад"
    BACK_TO_MAIN_MENU = "🔙 Меню"
    HEROES = "🦸‍♂️ Герої"

# Відповідність кнопок класам героїв
menu_button_to_class = {
    MenuButton.NAVIGATION.value: "Навігація",
    MenuButton.PROFILE.value: "Профіль",
    # Додайте відповідність для інших кнопок за потребою
}

# Приклад структури для героїв за класом
heroes_by_class = {
    "Танки": ["Герой1", "Герой2", "Герой3"],
    "Маги": ["Герой4", "Герой5", "Герой6"],
    "Стрільці": ["Герой7", "Герой8", "Герой9"],
    "Асасіни": ["Герой10", "Герой11", "Герой12"],
    "Сапорти": ["Герой13", "Герой14", "Герой15"],
    "Бійці": ["Герой16", "Герой17", "Герой18"],
    # Додайте інших класів та героїв за потребою
}

# Функція для створення клавіатури з заданою кількістю кнопок у рядку
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
        row_width=2  # Adjusted for two buttons per row
    )

def get_navigation_menu():
    return create_menu(
        [
            '🥷 Персонажі',
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

def get_guides_menu():
    return create_menu(
        [
            '🆕 Нові Гайди',
            '🌟 Топ Гайди',
            '📘 Новачкам',
            '🧙 Стратегії гри',
            '🤝 Командна Гра',
            MenuButton.BACK
        ],
        row_width=3
    )

def get_meta_menu():
    return create_menu(
        [
            '📈 Аналітика',
            '📊 Статистика',
            MenuButton.BACK_TO_MAIN_MENU
        ],
        row_width=3
    )

def get_m6_menu():
    return create_menu(
        [
            '🏆 Результати',
            '🔍 Деталі',
            MenuButton.BACK_TO_MAIN_MENU
        ],
        row_width=3
    )

def get_gpt_menu():
    return create_menu(
        [
            '📝 Задати питання',
            '❓ Допомога',
            MenuButton.BACK_TO_MAIN_MENU
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
            '🛡️ Танки',
            '🧙‍♂️ Маги',
            '🏹 Стрільці',
            '⚔️ Асасіни',
            '❤️ Сапорти',
            '🗡️ Бійці',
            '⚖️ Порівняти',
            '🔎 Шукати',
            MenuButton.BACK
        ],
        row_width=3
    )

def get_hero_class_menu(hero_class: str) -> ReplyKeyboardMarkup:
    # Приклад: створення клавіатури з героями певного класу
    heroes = heroes_by_class.get(hero_class, [])
    buttons = heroes.copy()  # Assuming heroes are strings
    # Додатково додаємо кнопку '🔙 Назад'
    buttons.append(MenuButton.BACK.value)
    return create_menu(buttons, row_width=3)

def get_counter_picks_menu():
    return create_menu(
        [
            '🔎 Пошук Контр-піку',
            '📝 Список Персонажів',
            MenuButton.BACK
        ],
        row_width=3
    )

def get_builds_menu():
    return create_menu(
        [
            '🏗️ Створити Білд',
            '📄 Збережені Білди',
            '🔥 Популярні Білди',
            MenuButton.BACK
        ],
        row_width=3
    )

def get_voting_menu():
    return create_menu(
        [
            '📍 Поточні Опитування',
            '📋 Мої Голосування',
            '➕ Запропонувати Тему',
            MenuButton.BACK
        ],
        row_width=3
    )

def get_statistics_menu():
    return create_menu(
        [
            '📊 Загальна Активність',
            '🥇 Рейтинг',
            '🎮 Ігрова Статистика',
            '🔙 Повернутися до Профілю'
        ],
        row_width=3
    )

def get_achievements_menu():
    return create_menu(
        [
            '🎖️ Мої Бейджі',
            '🚀 Прогрес',
            '🏅 Турнірна Статистика',
            '🎟️ Отримані Нагороди',
            '🔙 Повернутися до Профілю'
        ],
        row_width=3
    )

def get_settings_menu():
    return create_menu(
        [
            '🌐 Мова Інтерфейсу',
            'ℹ️ Змінити Username',
            '🆔 Оновити ID',
            '🔔 Сповіщення',
            '🔙 Повернутися до Профілю'
        ],
        row_width=3
    )

def get_feedback_menu():
    return create_menu(
        [
            '✏️ Надіслати Відгук',
            '🐛 Повідомити про Помилку',
            '🔙 Повернутися до Профілю'
        ],
        row_width=3
    )

def get_help_menu():
    return create_menu(
        [
            '📄 Інструкції',
            '❔ FAQ',
            '📞 Підтримка',
            '🔙 Повернутися до Профілю'
        ],
        row_width=3
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