# keyboards/menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from enum import Enum

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
    # Додайте інші кнопки за потребою

def create_menu(buttons, row_width=2):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    button_objs = [KeyboardButton(text=button.value) for button in buttons]
    keyboard.add(*button_objs)
    keyboard.row_width = row_width
    return keyboard

# Головне меню
def get_main_menu():
    return create_menu([MenuButton.NAVIGATION, MenuButton.PROFILE], row_width=2)

# Навігаційне меню
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

# Меню героїв
def get_heroes_menu():
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

# Додайте інші меню за потребою
