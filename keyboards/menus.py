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
    GPT = "👾 GPT"

    # Розділ Навігація
    TOURNAMENTS = "🏆 Турніри"
    HEROES = "🥷 Персонажі"
    META = "📊 META"
    M6 = "🔥 M6"
    GUIDES = "📚 Гайди"
    COUNTER_PICKS = "⚖️ Контр-піки"
    BUILDS = "🛡️ Білди"
    VOTING = "📋 Голосування"

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
    POPULAR_GUIDES = "🌟 Популярні Гайди"
    BEGINNER_GUIDES = "📘 Для Початківців"
    ADVANCED_TECHNIQUES = "🧙 Стратегії Гри"
    TEAMPLAY_GUIDES = "🤝 Командна Гра"

    # Розділ Контр-піки
    COUNTER_SEARCH = "🔎 Пошук Контр-піка"
    COUNTER_LIST = "📝 Список Персонажів"

    # Розділ Білди
    CREATE_BUILD = "🏗️ Створити Білд"
    MY_BUILDS = "📄 Мої Білди"
    POPULAR_BUILDS = "🔥 Популярні Білди"

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
    BACK = "🔙 Назад"

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

    # Підрозділ META
    META_HERO_LIST = "🔍 Список Героїв META"
    META_RECOMMENDATIONS = "🌟 Рекомендації META"
    META_UPDATES = "📈 Оновлення META"

    # Підрозділ M6
    M6_INFO = "ℹ️ Інформація про M6"
    M6_STATS = "📊 Статистика M6"
    M6_NEWS = "📰 Новини M6"

    # Розділ Турніри
    CREATE_TOURNAMENT = "🏗️ Створити Турнір"
    VIEW_TOURNAMENTS = "📄 Переглянути Турніри"

    # Додатковий функціонал у підменю "Персонажі"
    HERO_BIO = "📜 Біографія Героя"
    HERO_SKILLS = "⚔️ Навички"
    HERO_BUILDS = "🛠️ Оптимальні Білди"
    HERO_ROLES = "🎮 Ролі в Команді"
    HERO_STATS = "📊 Статистика Героя"

    # META (4-й рівень)
    META_SKILLS_STRENGTHS = "⚔️ Навички та Сильні Сторони"
    META_GAME_TIPS = "📜 Поради щодо Гри"
    META_BUILDS = "🛠️ Білди для Мети"

    # Перегляд Турнірів (4-й рівень)
    TOURNAMENT_RESULTS = "🏅 Результати Турнірів"
    TOURNAMENT_SCHEDULE = "📅 Розклад Матчів"
    TOURNAMENT_PARTICIPANTS = "👥 Список Учасників"

    # GPT Меню (новий розділ)
    GPT_DATA_GENERATION = "📊 Генерація Даних"
    GPT_HINTS = "💡 Поради"
    GPT_HERO_STATS = "📈 Статистика Героїв"

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

def create_menu(buttons, row_width=2, max_rows=None):
    """
    Створює клавіатуру з кнопками з обмеженням по кількості рядків.
    :param buttons: Список кнопок (MenuButton або str).
    :param row_width: Кількість кнопок у рядку.
    :param max_rows: Максимальна кількість рядків для основних кнопок. Якщо None, обмеження не застосовується.
    :return: ReplyKeyboardMarkup
    """
    if not all(isinstance(button, MenuButton) or isinstance(button, str) for button in buttons):
        raise ValueError("Усі елементи у списку кнопок повинні бути екземплярами MenuButton або str.")
    
    # Отримання тексту кнопок для логування
    button_texts = [button.value if isinstance(button, MenuButton) else button for button in buttons]
    logger.info(f"Створення меню з кнопками: {button_texts}")
    
    # Створення об'єктів KeyboardButton
    keyboard_buttons = [
        KeyboardButton(text=button.value if isinstance(button, MenuButton) else button) for button in buttons
    ]
    
    # Розбиття кнопок на рядки з урахуванням row_width
    keyboard = [
        keyboard_buttons[i:i + row_width]
        for i in range(0, len(keyboard_buttons), row_width)
    ]
    
    # Обмеження кількості рядків, якщо задано
    if max_rows is not None:
        keyboard = keyboard[:max_rows]
    
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_main_menu():
    return create_menu(
        [
            MenuButton.NAVIGATION,
            MenuButton.PROFILE
        ],
        row_width=2,
        max_rows=2  # Наприклад, максимум 2 рядки
    )

def get_navigation_menu():
    return create_menu(
        [
            MenuButton.HEROES,
            MenuButton.BUILDS,
            MenuButton.COUNTER_PICKS,
            MenuButton.GUIDES,
            MenuButton.TOURNAMENTS,
            MenuButton.M6,
            MenuButton.META,
            MenuButton.VOTING,
            MenuButton.GPT,  # Додано GPT до навігації
            MenuButton.BACK
        ],
        row_width=3,
        max_rows=3  # Максимум 3 рядки основних кнопок
    )

def get_heroes_menu():
    return create_menu(
        [
            MenuButton.TANK,
            MenuButton.MAGE,
            MenuButton.MARKSMAN,
            MenuButton.ASSASSIN,
            MenuButton.FIGHTER,
            MenuButton.SUPPORT,
            MenuButton.COMPARISON,
            MenuButton.SEARCH_HERO,
            MenuButton.BACK
        ],
        row_width=3,
        max_rows=3  # Максимум 3 рядки основних кнопок
    )

def get_hero_class_menu(hero_class, row_width=3, max_rows=3):
    heroes = heroes_by_class.get(hero_class, [])
    buttons = heroes + [MenuButton.BACK]
    return create_menu(buttons, row_width=row_width, max_rows=max_rows)

def get_guides_menu():
    return create_menu(
        [
            MenuButton.NEW_GUIDES,
            MenuButton.POPULAR_GUIDES,
            MenuButton.BEGINNER_GUIDES,
            MenuButton.ADVANCED_TECHNIQUES,
            MenuButton.TEAMPLAY_GUIDES,
            MenuButton.BACK
        ],
        row_width=3,
        max_rows=3  # Максимум 3 рядки основних кнопок
    )

def get_counter_picks_menu():
    return create_menu(
        [
            MenuButton.COUNTER_SEARCH,
            MenuButton.COUNTER_LIST,
            MenuButton.BACK
        ],
        row_width=3,
        max_rows=2  # Наприклад, максимум 2 рядки
    )

def get_builds_menu():
    return create_menu(
        [
            MenuButton.CREATE_BUILD,
            MenuButton.MY_BUILDS,
            MenuButton.POPULAR_BUILDS,
            MenuButton.BACK
        ],
        row_width=3,
        max_rows=3  # Максимум 3 рядки основних кнопок
    )

def get_voting_menu():
    return create_menu(
        [
            MenuButton.CURRENT_VOTES,
            MenuButton.MY_VOTES,
            MenuButton.SUGGEST_TOPIC,
            MenuButton.BACK
        ],
        row_width=3,
        max_rows=2  # Наприклад, максимум 2 рядки
    )

def get_profile_menu():
    return create_menu(
        [
            MenuButton.STATISTICS,
            MenuButton.ACHIEVEMENTS,
            MenuButton.SETTINGS,
            MenuButton.FEEDBACK,
            MenuButton.HELP,
            MenuButton.BACK
        ],
        row_width=3,
        max_rows=3  # Максимум 3 рядки основних кнопок
    )

def get_statistics_menu():
    return create_menu(
        [
            MenuButton.ACTIVITY,
            MenuButton.RANKING,
            MenuButton.GAME_STATS,
            MenuButton.BACK
        ],
        row_width=3,
        max_rows=2  # Наприклад, максимум 2 рядки
    )

def get_achievements_menu():
    return create_menu(
        [
            MenuButton.BADGES,
            MenuButton.PROGRESS,
            MenuButton.TOURNAMENT_STATS,
            MenuButton.AWARDS,
            MenuButton.BACK
        ],
        row_width=3,
        max_rows=3  # Максимум 3 рядки основних кнопок
    )

def get_settings_menu():
    return create_menu(
        [
            MenuButton.LANGUAGE,
            MenuButton.CHANGE_USERNAME,
            MenuButton.UPDATE_ID,
            MenuButton.NOTIFICATIONS,
            MenuButton.BACK
        ],
        row_width=3,
        max_rows=2  # Наприклад, максимум 2 рядки
    )

def get_feedback_menu():
    return create_menu(
        [
            MenuButton.SEND_FEEDBACK,
            MenuButton.REPORT_BUG,
            MenuButton.BACK
        ],
        row_width=3,
        max_rows=2  # Наприклад, максимум 2 рядки
    )

def get_help_menu():
    return create_menu(
        [
            MenuButton.INSTRUCTIONS,
            MenuButton.FAQ,
            MenuButton.HELP_SUPPORT,
            MenuButton.BACK
        ],
        row_width=3,
        max_rows=2  # Наприклад, максимум 2 рядки
    )

def get_tournaments_menu():
    return create_menu(
        [
            MenuButton.CREATE_TOURNAMENT,
            MenuButton.VIEW_TOURNAMENTS,
            MenuButton.BACK
        ],
        row_width=3,
        max_rows=2  # Наприклад, максимум 2 рядки
    )

def get_meta_menu():
    return create_menu(
        [
            MenuButton.META_HERO_LIST,
            MenuButton.META_RECOMMENDATIONS,
            MenuButton.META_UPDATES,
            MenuButton.BACK
        ],
        row_width=3,
        max_rows=3  # Максимум 3 рядки основних кнопок
    )

def get_m6_menu():
    return create_menu(
        [
            MenuButton.M6_INFO,
            MenuButton.M6_STATS,
            MenuButton.M6_NEWS,
            MenuButton.BACK
        ],
        row_width=3,
        max_rows=3  # Максимум 3 рядки основних кнопок
    )

def get_hero_details_menu():
    return create_menu(
        [
            MenuButton.HERO_BIO,
            MenuButton.HERO_SKILLS,
            MenuButton.HERO_BUILDS,
            MenuButton.HERO_ROLES,
            MenuButton.HERO_STATS,
            MenuButton.BACK
        ],
        row_width=2,
        max_rows=3  # Максимум 3 рядки основних кнопок
    )

def get_meta_submenu():
    return create_menu(
        [
            MenuButton.META_SKILLS_STRENGTHS,
            MenuButton.META_GAME_TIPS,
            MenuButton.META_BUILDS,
            MenuButton.BACK
        ],
        row_width=2,
        max_rows=2  # Наприклад, максимум 2 рядки
    )

def get_tournament_view_submenu():
    return create_menu(
        [
            MenuButton.TOURNAMENT_RESULTS,
            MenuButton.TOURNAMENT_SCHEDULE,
            MenuButton.TOURNAMENT_PARTICIPANTS
        ],
        row_width=2,
        max_rows=2  # Наприклад, максимум 2 рядки
    )

def get_gpt_menu():
    """
    Створює клавіатуру для GPT Меню з обмеженням по кількості рядків.
    :return: ReplyKeyboardMarkup
    """
    return create_menu(
        [
            MenuButton.GPT_DATA_GENERATION,
            MenuButton.GPT_HINTS,
            MenuButton.GPT_HERO_STATS,
            MenuButton.BACK
        ],
        row_width=2,
        max_rows=2  # Наприклад, максимум 2 рядки основних кнопок
    )

def get_generic_inline_keyboard():
    """
    Повертає загальну Inline клавіатуру (при необхідності).
    :return: InlineKeyboardMarkup
    """
    # Ви можете реалізувати цю функцію відповідно до ваших потреб
    pass
