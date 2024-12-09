# keyboards/menus.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
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
    BUILDS = "🛡️ Білди"
    COUNTER_PICKS = "⚖️ Контр-піки"
    GUIDES = "📚 Гайди"
    VOTING = "📊 Голосування"
    M6 = "🏆 M6"
    GPT = "👾 GPT"
    META = "🔥 META"
    TOURNAMENTS = "🏆 Турніри"
    BACK = "🔙 Назад"

    # Розділ Персонажі
    TANK = "🛡️ Танк"
    MAGE = "🧙‍♂️ Маг"
    MARKSMAN = "🏹 Стрілець"
    ASSASSIN = "⚔️ Асасін"
    SUPPORT = "❤️ Підтримка"
    FIGHTER = "🗡️ Боєць"
    COMPARISON = "⚖️ Порівняння"
    SEARCH_HERO = "🔎 Пошук"

    # Розділ Гайди
    NEW_GUIDES = "🆕 Нові Гайди"
    POPULAR_GUIDES = "🌟 Топ Гайди"
    BEGINNER_GUIDES = "📘 Для Початківців"
    ADVANCED_TECHNIQUES = "🧙 Стратегії гри"
    TEAMPLAY_GUIDES = "🤝 Командна Гра"

    # Розділ Контр-піки
    COUNTER_SEARCH = "🔎 Пошук"
    COUNTER_LIST = "📝 Список Персонажів"

    # Розділ Білди
    CREATE_BUILD = "🏗️ Створити"
    MY_BUILDS = "📄 Обрані"
    POPULAR_BUILDS = "🔥 Популярні"

    # Розділ Голосування
    CURRENT_VOTES = "📍 Поточні Опитування"
    MY_VOTES = "📋 Мої Голосування"
    SUGGEST_TOPIC = "➕ Запропонувати Тему"

    # Розділ Профіль
    STATISTICS = "📈 Статистика"
    ACHIEVEMENTS = "🏆 Досягнення"
    SETTINGS = "⚙️ Налаштування"
    FEEDBACK = "💌 Зворотний Зв'язок"
    HELP = "❓ Допомога"
    BACK_TO_MAIN_MENU = "🔙 Назад до Головного Меню"

    # Підрозділ Статистика
    ACTIVITY = "📊 Загальна Активність"
    RANKING = "🥇 Рейтинг"
    GAME_STATS = "🎮 Ігрова Статистика"
    BACK_TO_PROFILE = "🔙 Назад до Профілю"

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

    # Підрозділ Зворотного Зв'язку
    SEND_FEEDBACK = "✏️ Надіслати Відгук"
    REPORT_BUG = "🐛 Повідомити про Помилку"

    # Підрозділ Допомоги
    INSTRUCTIONS = "📄 Інструкції"
    FAQ = "❔ FAQ"
    HELP_SUPPORT = "📞 Підтримка"

    # Підрозділ Турніри
    CREATE_TOURNAMENT = "🆕 Створити Турнір"
    VIEW_TOURNAMENTS = "📋 Переглянути Турніри"

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

def create_inline_menu(buttons, row_width=2):
    """
    Створює InlineKeyboardMarkup з кнопками.
    :param buttons: Список кнопок (MenuButton або str).
    :param row_width: Кількість кнопок у рядку.
    :return: InlineKeyboardMarkup
    """
    if not all(isinstance(button, MenuButton) or isinstance(button, str) for button in buttons):
        raise ValueError("Усі елементи у списку кнопок повинні бути екземплярами MenuButton або str.")
    button_objects = []
    for button in buttons:
        if isinstance(button, MenuButton):
            callback = button.name
            button_text = button.value
        else:
            callback = button
            button_text = button
        button_objects.append(InlineKeyboardButton(text=button_text, callback_data=callback))
    keyboard = []
    for i in range(0, len(button_objects), row_width):
        keyboard.append(button_objects[i:i + row_width])
    logger.info(f"Створення меню з кнопками: {[button.text for button in button_objects]}")
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_main_menu():
    return create_inline_menu(
        [
            MenuButton.NAVIGATION,
            MenuButton.PROFILE
        ],
        row_width=2
    )

def get_navigation_menu():
    return create_inline_menu(
        [
            MenuButton.HEROES,
            MenuButton.BUILDS,
            MenuButton.COUNTER_PICKS,
            MenuButton.GUIDES,
            MenuButton.VOTING,
            MenuButton.M6,
            MenuButton.GPT,
            MenuButton.META,
            MenuButton.TOURNAMENTS,
            MenuButton.BACK
        ],
        row_width=3
    )

def get_heroes_menu():
    return create_inline_menu(
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

def get_hero_class_menu(hero_class):
    heroes = heroes_by_class.get(hero_class, [])
    buttons = [InlineKeyboardButton(text=hero, callback_data=f"hero:{hero}") for hero in heroes]
    row_width = 3
    keyboard = [buttons[i:i+row_width] for i in range(0, len(buttons), row_width)]
    keyboard.append([InlineKeyboardButton(text=MenuButton.BACK.value, callback_data="navigation")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_guides_menu():
    return create_inline_menu(
        [
            MenuButton.NEW_GUIDES,
            MenuButton.POPULAR_GUIDES,
            MenuButton.BEGINNER_GUIDES,
            MenuButton.ADVANCED_TECHNIQUES,
            MenuButton.TEAMPLAY_GUIDES,
            MenuButton.BACK
        ],
        row_width=3
    )

def get_counter_picks_menu():
    return create_inline_menu(
        [
            MenuButton.COUNTER_SEARCH,
            MenuButton.COUNTER_LIST,
            MenuButton.BACK
        ],
        row_width=2
    )

def get_builds_menu():
    return create_inline_menu(
        [
            MenuButton.CREATE_BUILD,
            MenuButton.MY_BUILDS,
            MenuButton.POPULAR_BUILDS,
            MenuButton.BACK
        ],
        row_width=2
    )

def get_voting_menu():
    return create_inline_menu(
        [
            MenuButton.CURRENT_VOTES,
            MenuButton.MY_VOTES,
            MenuButton.SUGGEST_TOPIC,
            MenuButton.BACK
        ],
        row_width=2
    )

def get_profile_menu():
    return create_inline_menu(
        [
            MenuButton.STATISTICS,
            MenuButton.ACHIEVEMENTS,
            MenuButton.SETTINGS,
            MenuButton.FEEDBACK,
            MenuButton.HELP,
            MenuButton.BACK_TO_MAIN_MENU
        ],
        row_width=2
    )

def get_statistics_menu():
    return create_inline_menu(
        [
            MenuButton.ACTIVITY,
            MenuButton.RANKING,
            MenuButton.GAME_STATS,
            MenuButton.BACK_TO_PROFILE
        ],
        row_width=2
    )

def get_achievements_menu():
    return create_inline_menu(
        [
            MenuButton.BADGES,
            MenuButton.PROGRESS,
            MenuButton.TOURNAMENT_STATS,
            MenuButton.AWARDS,
            MenuButton.BACK_TO_PROFILE
        ],
        row_width=2
    )

def get_settings_menu():
    return create_inline_menu(
        [
            MenuButton.LANGUAGE,
            MenuButton.CHANGE_USERNAME,
            MenuButton.UPDATE_ID,
            MenuButton.NOTIFICATIONS,
            MenuButton.BACK_TO_PROFILE
        ],
        row_width=2
    )

def get_feedback_menu():
    return create_inline_menu(
        [
            MenuButton.SEND_FEEDBACK,
            MenuButton.REPORT_BUG,
            MenuButton.BACK_TO_PROFILE
        ],
        row_width=2
    )

def get_help_menu():
    return create_inline_menu(
        [
            MenuButton.INSTRUCTIONS,
            MenuButton.FAQ,
            MenuButton.HELP_SUPPORT,
            MenuButton.BACK_TO_PROFILE
        ],
        row_width=2
    )

def get_tournaments_menu():
    return create_inline_menu(
        [
            MenuButton.CREATE_TOURNAMENT,
            MenuButton.VIEW_TOURNAMENTS,
            MenuButton.BACK
        ],
        row_width=2
    )

def get_create_tournament_menu():
    return create_inline_menu(
        [
            InlineKeyboardButton(text="5х5", callback_data="tournament:create:5x5"),
            InlineKeyboardButton(text="2х2", callback_data="tournament:create:2x2"),
            InlineKeyboardButton(text="1 на 1", callback_data="tournament:create:1x1"),
            InlineKeyboardButton(text=MenuButton.BACK.value, callback_data="tournaments")
        ],
        row_width=2
    )

def get_active_tournaments_menu():
    # Приклад списку активних турнірів
    tournaments = [
        {"name": "Турнір А", "type": "5х5", "status": "Активний"},
        {"name": "Турнір Б", "type": "2х2", "status": "Завершений"},
        # Додайте більше турнірів за потребою
    ]

    keyboard = []
    for tournament in tournaments:
        button_text = f"{tournament['name']} ({tournament['type']}) - {tournament['status']}"
        callback = f"tournament:view:{tournament['name']}"
        keyboard.append([InlineKeyboardButton(text=button_text, callback_data=callback)])
    
    keyboard.append([InlineKeyboardButton(text=MenuButton.BACK.value, callback_data="tournaments")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Головне меню
MAIN_MENU_TEXT = (
    """👋 <b>Вітаємо, {user_first_name}, у Mobile Legends: Starts!</b>
    
Оберіть потрібну опцію нижче, щоб досліджувати можливості та вдосконалювати свій ігровий досвід.
"""
)

# Функція для отримання тексту меню (цей текст ви використовуєте в handler-ах)
def get_main_menu_text(user_first_name):
    return MAIN_MENU_TEXT.format(user_first_name=user_first_name)

# Додаткові функції для інших меню можна додати аналогічно
