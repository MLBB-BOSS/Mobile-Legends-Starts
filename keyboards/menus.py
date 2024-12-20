# keyboards/menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from enum import Enum, unique
import logging

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@unique
class MenuButton(Enum):
    # Головне Меню
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Мій Профіль"

    # Розділ Навігація
    TOURNAMENTS = "🏆 Турніри"
    HEROES = "🥷 Персонажі"
    CHALLENGES = "🧩 Челенджі"  # Додано Челенджі замість M6
    GUIDES = "📚 Гайди"
    BUILDS = "🛡️ Білди"
    BUST = "🚀 Буст"
    TEAMS = "🧑‍🤝‍🧑 Команди"
    TRADING = "💰 Торгівля"
    BACK = "🔙 Назад"

    # Розділ Гайди
    M1_6 = "🏆 M 1 - 6"  # Переміщено та перейменовано M6
    NEW_GUIDES = "🆕 Нові Гайди"
    POPULAR_GUIDES = "🌟 Популярні Гайди"
    BEGINNER_GUIDES = "📘 Для Початківців"
    ADVANCED_TECHNIQUES = "🧙 Стратегії Гри"
    TEAMPLAY_GUIDES = "🤝 Командна Гра"

    # Розділ Персонажі
    TANK = "🛡️ Танк"
    MAGE = "🧙‍♂️ Маг"
    MARKSMAN = "🏹 Стрілець"
    ASSASSIN = "⚔️ Асасін"
    SUPPORT = "❤️ Підтримка"
    FIGHTER = "🗡️ Боєць"
    COMPARISON = "⚖️ Порівняння"
    SEARCH_HERO = "🔎 Пошук персонажа"
    VOTING = "🗳️ Голосування"

    # Розділ Контр-піки
    COUNTER_SEARCH = "🔎 Пошук Контр-піка"
    COUNTER_LIST = "📝 Список Персонажів"
    COUNTER_PICKS = "♻️ Контр-пік"

    # Розділ META
    META_HERO_LIST = "🔍 Список Героїв META"
    META_RECOMMENDATIONS = "☑️ Рекомендації META"
    META_UPDATES = "📈 Оновлення META"
    META = "⭐ МЕТА"

    # Розділ Білди
    CREATE_BUILD = "🏗️ Створити Білд"
    MY_BUILDS = "📄 Мої Білди"
    POPULAR_BUILDS = "🔝 Популярні Білди"

    # Розділ Голосування
    CURRENT_VOTES = "📍 Поточні Опитування"
    MY_VOTES = "📋 Мої Голосування"
    SUGGEST_TOPIC = "➕ Запропонувати Тему"

    # Розділ Профіль
    MY_TEAM = "🧑‍🤝‍🧑 Моя команда"  # Додано Моя команда
    STATISTICS = "📈 Статистика"
    ACHIEVEMENTS = "🏆 Досягнення"
    SETTINGS = "⚙️ Налаштування"
    FEEDBACK = "💌 Зворотний Зв'язок"
    HELP = "❓ Допомога"
    GPT = "👾 GPT"

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

    # Підрозділ Зворотний зв'язок
    SEND_FEEDBACK = "✏️ Надіслати Відгук"
    REPORT_BUG = "🐛 Повідомити про Помилку"

    # Підрозділ Допомога
    INSTRUCTIONS = "📄 Інструкції"
    FAQ = "❔ FAQ"
    HELP_SUPPORT = "📞 Підтримка"

    # Новий розділ Команди
    CREATE_TEAM = "➕ Створити Команду"    # Додано
    VIEW_TEAMS = "👀 Переглянути Команди" # Додано

    # GPT Меню
    GPT_DATA_GENERATION = "📊 Генерація Даних"
    GPT_HINTS = "💡 Поради"
    GPT_HERO_STATS = "📈 Статистика Героїв"

    # Нові Кнопки
    SHOP = "📦 Магазин"
    SUPPORT_CENTER = "🆘 Підтримка"
    EVENTS_CALENDAR = "📅 Календар Подій"
    NOTIFICATIONS_SETTINGS = "🔔 Сповіщення"

# Відповідність кнопок класам героїв
menu_button_to_class = {
    MenuButton.TANK.value: "Танк",
    MenuButton.MAGE.value: "Маг",
    MenuButton.MARKSMAN.value: "Стрілець",
    MenuButton.ASSASSIN.value: "Асасін",
    MenuButton.SUPPORT.value: "Підтримка",
    MenuButton.FIGHTER.value: "Боєць",
}

# Списки героїв по класах (заповнити відповідно до потреб)
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

def create_menu(buttons, placeholder, row_width=2):
    """
    Створює меню з кнопками.

    :param buttons: Список кнопок (MenuButton або str)
    :param placeholder: Підказка для поля вводу
    :param row_width: Кількість кнопок у рядку
    :return: ReplyKeyboardMarkup об'єкт
    """
    if not all(isinstance(button, MenuButton) or isinstance(button, str) for button in buttons):
        raise ValueError("Усі елементи у списку кнопок повинні бути екземплярами MenuButton або str.")
    
    button_texts = [button.value if isinstance(button, MenuButton) else button for button in buttons]
    logger.info(f"Створення меню з кнопками: {button_texts} та підказкою: '{placeholder}'")
    
    keyboard_buttons = [
        KeyboardButton(text=button.value if isinstance(button, MenuButton) else button) for button in buttons
    ]
    
    keyboard = [
        keyboard_buttons[i:i + row_width]
        for i in range(0, len(keyboard_buttons), row_width)
    ]
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard, 
        resize_keyboard=True, 
        input_field_placeholder=placeholder
    )

def get_main_menu():
    """
    Створює головне меню.
    :return: ReplyKeyboardMarkup об'єкт
    """
    return create_menu(
        buttons=[
            MenuButton.NAVIGATION,
            MenuButton.PROFILE
        ],
        placeholder="Оберіть одну з основних опцій",
        row_width=2
    )

def get_navigation_menu():
    """
    Створює меню Навігації.
    :return: ReplyKeyboardMarkup об'єкт
    """
    return create_menu(
        buttons=[
            MenuButton.HEROES,
            MenuButton.BUILDS,
            MenuButton.GUIDES,
            MenuButton.TOURNAMENTS,
            MenuButton.TEAMS,
            MenuButton.CHALLENGES,  # Додано Челенджі
            MenuButton.TRADING,
            MenuButton.BUST,
            MenuButton.BACK
        ],
        placeholder="Виберіть розділ у навігації",
        row_width=3
    )

def get_guides_menu():
    """
    Створює меню Гайдів.
    :return: ReplyKeyboardMarkup об'єкт
    """
    return create_menu(
        buttons=[
            MenuButton.M1_6,  # Додано M 1 - 6
            MenuButton.NEW_GUIDES,
            MenuButton.POPULAR_GUIDES,
            MenuButton.BEGINNER_GUIDES,
            MenuButton.ADVANCED_TECHNIQUES,
            MenuButton.TEAMPLAY_GUIDES,
            MenuButton.BACK
        ],
        placeholder="Виберіть розділ гайдів",
        row_width=3
    )

def get_profile_menu():
    """
    Створює меню Профілю.
    :return: ReplyKeyboardMarkup об'єкт
    """
    return create_menu(
        buttons=[
            MenuButton.MY_TEAM,  # Додано Моя команда
            MenuButton.STATISTICS,
            MenuButton.ACHIEVEMENTS,
            MenuButton.SETTINGS,
            MenuButton.FEEDBACK,
            MenuButton.HELP,
            MenuButton.GPT,
            MenuButton.BACK
        ],
        placeholder="Оберіть дію з профілем",
        row_width=3
    )

def get_heroes_menu():
    """
    Створює меню Персонажів.
    :return: ReplyKeyboardMarkup об'єкт
    """
    return create_menu(
        buttons=[
            MenuButton.TANK,
            MenuButton.MAGE,
            MenuButton.MARKSMAN,
            MenuButton.ASSASSIN,
            MenuButton.FIGHTER,
            MenuButton.SUPPORT,
            MenuButton.COUNTER_PICKS,
            MenuButton.META,
            MenuButton.COMPARISON,
            MenuButton.VOTING,      # Перемістили VOTING сюди
            MenuButton.SEARCH_HERO,
            MenuButton.BACK
        ],
        placeholder="GPT-4: Персонажі",
        row_width=3
    )

def get_trading_menu():
    """
    Створює меню Торгівлі.
    :return: ReplyKeyboardMarkup об'єкт
    """
    return create_menu(
        buttons=[
            MenuButton.CREATE_TRADE,
            MenuButton.VIEW_TRADES,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію Торгівлі",
        row_width=2
    )

def get_my_team_menu():
    """
    Створює меню Моїї Команди.
    :return: ReplyKeyboardMarkup об'єкт
    """
    return create_menu(
        buttons=[
            MenuButton.CREATE_TEAM,
            MenuButton.VIEW_TEAMS,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію Моїї Команди",
        row_width=2
    )

def get_challenges_menu():
    """
    Створює меню Челенджів.
    :return: ReplyKeyboardMarkup об'єкт
    """
    return create_menu(
        buttons=[
            # Додайте відповідні кнопки для челенджів тут
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію Челенджів",
        row_width=2
    )

def get_shop_menu():
    """
    Створює меню Магазину.
    :return: ReplyKeyboardMarkup об'єкт
    """
    return create_menu(
        buttons=[
            MenuButton.CREATE_BUILD,  # Приклад: Створення продукту
            MenuButton.MY_BUILDS,     # Приклад: Мої покупки
            MenuButton.POPULAR_BUILDS, # Приклад: Популярні товари
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію Магазину",
        row_width=2
    )

def get_support_center_menu():
    """
    Створює меню Підтримки.
    :return: ReplyKeyboardMarkup об'єкт
    """
    return create_menu(
        buttons=[
            MenuButton.INSTRUCTIONS,
            MenuButton.FAQ,
            MenuButton.HELP_SUPPORT,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію Підтримки",
        row_width=2
    )

def get_events_calendar_menu():
    """
    Створює меню Календаря Подій.
    :return: ReplyKeyboardMarkup об'єкт
    """
    return create_menu(
        buttons=[
            MenuButton.CREATE_TOURNAMENT,
            MenuButton.VIEW_TOURNAMENTS,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію Календаря Подій",
        row_width=2
    )

def get_generic_inline_keyboard():
    """
    Створює інлайн-клавіатуру (заглушка).
    :return: None
    """
    # Цю функцію можна реалізувати для інлайн-кнопок, якщо потрібно.
    # Поки що залишимо заглушку.
    pass

# Реєстрація нових меню у функції створення меню
def get_all_menus():
    """
    Функція для отримання всіх меню. Може бути корисною для тестування або розширення.
    :return: dict з назвами меню та їх об'єктами
    """
    return {
        "main": get_main_menu(),
        "navigation": get_navigation_menu(),
        "guides": get_guides_menu(),
        "profile": get_profile_menu(),
        "heroes": get_heroes_menu(),
        "trading": get_trading_menu(),
        "my_team": get_my_team_menu(),
        "challenges": get_challenges_menu(),
        "shop": get_shop_menu(),
        "support_center": get_support_center_menu(),
        "events_calendar": get_events_calendar_menu(),
    }

# При необхідності додайте інші функції для інших меню
