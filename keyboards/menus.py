# keyboards/menus.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class MenuButton(Enum):
    # Ваші визначені кнопки
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Мій Профіль"
    HEROES = "🛡️ Персонажі"
    GUIDES = "📚 Гайди"
    COUNTER_PICKS = "⚖️ Контр-піки"
    BUILDS = "⚜️ Білди"
    VOTING = "📊 Голосування"
    BACK = "🔄 Назад"
    TANK = "🛡️ Танк"
    MAGE = "🧙‍♂️ Маг"
    MARKSMAN = "🎯 Стрілець"
    ASSASSIN = "🗡️ Асасін"
    SUPPORT = "❤️ Підтримка"
    FIGHTER = "🥊 Боєць"
    COMPARISON = "⚖️ Порівняння"
    SEARCH_HERO = "🔎 Пошук Персонажа"
    # Додайте інші кнопки за потреби

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

def get_hero_class_menu(hero_class: str) -> ReplyKeyboardMarkup:
    """
    Створює клавіатуру для конкретного класу героїв
    
    :param hero_class: Клас героя (наприклад, "Танк", "Маг" і т.д.)
    :return: ReplyKeyboardMarkup
    """
    heroes_by_class = {
        "Боєць": [
            "Balmond", "Alucard", "Bane", "Zilong", "Freya",
            # ... ваш список героїв
        ],
        "Танк": [
            "Tigreal", "Akai", "Franco", "Minotaur",
            # ... ваш список героїв
        ],
        "Маг": [
            "Vale", "Lunox", "Kadita", "Cecillion", "Luo Yi", "Xavier",
            # ... ваш список героїв
        ],
        "Стрілець": [
            "Miya", "Granger", "Hanabi", "Layla",
            # ... ваш список героїв
        ],
        "Асасін": [
            "Natalia", "Gusion", "Hayabusa",
            # ... ваш список героїв
        ],
        "Підтримка": [
            "Estes", "Angela", "Rafaela",
            # ... ваш список героїв
        ],
        "Боєць": [
            "Ruby", "Roger",
            # ... ваш список героїв
        ],
        # Додайте інші класи за потреби
    }
    
    heroes = heroes_by_class.get(hero_class, [])
    buttons = [KeyboardButton(text=hero) for hero in heroes]
    keyboard = []
    
    # Розміщуємо кнопки по 3 в ряд
    for i in range(0, len(buttons), 3):
        keyboard.append(buttons[i:i + 3])
    
    # Додаємо кнопку "Назад"
    keyboard.append([KeyboardButton(text=MenuButton.BACK.value)])
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

# Інші функції для створення меню
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

def get_guides_menu():
    return create_menu(
        [
            "Нові гайди - Свіжі статті",
            "Популярні гайди - Найкращі гайди",
            "Для початківців - Основи гри",
            "Просунуті техніки - Для досвідчених",
            "Командна гра - Взаємодія в команді",
            MenuButton.BACK
        ],
        row_width=2
    )

def get_counter_picks_menu():
    return create_menu(
        [
            "Пошук Контр-піку - 🔍",
            "Список Персонажів - 📃",
            MenuButton.BACK
        ],
        row_width=2
    )

def get_builds_menu():
    return create_menu(
        [
            "Створити Білд - ➕",
            "Мої Білди - 📁",
            "Популярні Білди - 🌟",
            MenuButton.BACK
        ],
        row_width=2
    )

def get_voting_menu():
    return create_menu(
        [
            "Поточні Опитування - 🗳️",
            "Мої Голосування - 🗳️",
            "Запропонувати Тему - 💡",
            MenuButton.BACK
        ],
        row_width=2
    )

def get_profile_menu():
    return create_menu(
        [
            "📈 Статистика",
            "🏅 Досягнення",
            "⚙️ Налаштування",
            "📤 Зворотний Зв'язок",
            "❓ Допомога",
            MenuButton.BACK_TO_MAIN_MENU.value
        ],
        row_width=3
    )

# Додайте інші get_*_menu функції за потреби
