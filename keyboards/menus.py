import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.menus import (
    MenuButton,
    get_main_menu,
    get_navigation_menu,
    get_heroes_menu,
    get_guides_menu,
    get_counter_picks_menu,
    get_builds_menu,
    get_voting_menu,
    get_profile_menu,
    get_hero_class_menu,
    menu_button_to_class,
    heroes_by_class,
)

# Список героїв за класами
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
        "Rafaela", "Minotaur", "Lolita", "Estes", "Angela", "Faramis", "Mathilda", "Florin", "Johnso"
    ],
}

# Відображення MenuButton на назви класів
menu_button_to_class = {
    MenuButton.TANK.value: "Танк",
    MenuButton.MAGE.value: "Маг",
    MenuButton.MARKSMAN.value: "Стрілець",
    MenuButton.ASSASSIN.value: "Асасін",
    MenuButton.SUPPORT.value: "Підтримка",
    MenuButton.FIGHTER.value: "Боєць",
}

# Функція для створення меню героїв
def get_heroes_menu():
    return create_menu(
        [
            MenuButton.SEARCH_HERO,
            MenuButton.FIGHTER,
            MenuButton.TANK,
            MenuButton.MAGE,
            MenuButton.MARKSMAN,
            MenuButton.ASSASSIN,
            MenuButton.SUPPORT,
            MenuButton.BACK
        ],
        row_width=2
    )

# Функція для створення клавіатури з героями обраного класу
def get_hero_class_menu(hero_class):
    heroes = heroes_by_class.get(hero_class, [])
    buttons = [KeyboardButton(text=hero) for hero in heroes]
    # Створення клавіатури з героями
    row_width = 2
    keyboard = [buttons[i:i+row_width] for i in range(0, len(buttons), row_width)]
    keyboard.append([KeyboardButton(text=MenuButton.BACK.value)])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Функція для створення клавіатур
def create_menu(buttons, row_width=2):
    """
    Створює клавіатуру з кнопками.
    :param buttons: Список кнопок (MenuButton або str).
    :param row_width: Кількість кнопок у рядку.
    :return: ReplyKeyboardMarkup
    """
    # Перевірка типу кнопок
    if not all(isinstance(button, MenuButton) or isinstance(button, str) for button in buttons):
        raise ValueError("Усі елементи у списку кнопок повинні бути екземплярами MenuButton або str.")
    logger.info(f"Створення меню з кнопками: {[button.value if isinstance(button, MenuButton) else button for button in buttons]}")
    keyboard = [
        [KeyboardButton(text=button.value if isinstance(button, MenuButton) else button) for button in buttons[i:i + row_width]]
        for i in range(0, len(buttons), row_width)
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Інші функції меню залишаються без змін
# ...
