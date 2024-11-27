# menus.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from enum import Enum
import logging

# Логування
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MenuButton(Enum):
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Профіль"
    HEROES = "🛡️ Персонажі"
    GUIDES = "📚 Гайди"
    SEARCH_HERO = "🔎 Пошук Персонажа"
    FIGHTER = "💪 Боєць"  # Додано клас "Боєць"
    TANK = "🛡️ Танк"
    MAGE = "🔮 Маг"
    MARKSMAN = "🏹 Стрілець"
    ASSASSIN = "⚔️ Асасін"
    SUPPORT = "🧬 Підтримка"
    BACK = "🔄 Назад"
    NEW_GUIDES = "🆕 Нові Гайди"
    POPULAR_GUIDES = "🌟 Популярні Гайди"
    BEGINNER_GUIDES = "📘 Для Початківців"
    ADVANCED_TECHNIQUES = "🧙 Просунуті Техніки"
    TEAMPLAY_GUIDES = "🛡️ Командна Гра"
    COUNTER_PICKS = "⚖️ Контр-піки"
    COUNTER_SEARCH = "🔎 Пошук Контр-піку"
    COUNTER_LIST = "📝 Список Персонажів"
    CREATE_BUILD = "🏗️ Створити Білд"
    MY_BUILDS = "📄 Мої Білди"
    POPULAR_BUILDS = "💎 Популярні Білди"
    BUILDS = "⚜️ Білди"  # Додано для відповідності в обробниках
    CURRENT_VOTES = "📍 Поточні Опитування"
    MY_VOTES = "📋 Мої Голосування"
    SUGGEST_TOPIC = "➕ Запропонувати Тему"
    VOTING = "📊 Голосування"  # Додано цю кнопку
    ACTIVITY = "📊 Загальна Активність"
    RANKING = "🥇 Рейтинг"
    GAME_STATS = "🎮 Ігрова Статистика"
    BADGES = "🎖️ Мої Бейджі"
    PROGRESS = "🚀 Прогрес"
    TOURNAMENT_STATS = "🏅 Турнірна Статистика"
    AWARDS = "🎟️ Отримані Нагороди"
    LANGUAGE = "🌐 Мова Інтерфейсу"
    CHANGE_USERNAME = "🆔 Змінити Username"
    UPDATE_ID = "🛡️ Оновити ID Гравця"
    NOTIFICATIONS = "🔔 Сповіщення"
    INSTRUCTIONS = "📄 Інструкції"
    FAQ = "❔ FAQ"
    HELP_SUPPORT = "🆘 Підтримка"  # Додано для меню "Допомога"

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
