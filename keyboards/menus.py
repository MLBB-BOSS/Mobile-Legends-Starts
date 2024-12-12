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

    # Підменю Зворотного зв'язку
    SEND_FEEDBACK = "📝 Надіслати відгук"
    REPORT_BUG = "🐛 Повідомити про помилку"

    # Підменю Допомоги
    INSTRUCTIONS = "📄 Інструкції"
    FAQ = "❔ FAQ"
    HELP_SUPPORT = "📞 Підтримка"

    # Підменю Турнірів
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

def get_hero_class_menu(hero_class):
    heroes = heroes_by_class.get(hero_class, [])
    if not heroes:
        logger.warning(f"Клас героїв '{hero_class}' не знайдено.")

    # Додаємо кнопку "🔙 Повернутися" для повернення
    buttons = heroes + [MenuButton.BACK.value]

    logger.info(f"Створення меню для класу '{hero_class}' з героями: {buttons}")

    # Використовуємо create_menu для створення клавіатури
    return create_menu(buttons, row_width=3)

# Інші функції меню залишаються без змін

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