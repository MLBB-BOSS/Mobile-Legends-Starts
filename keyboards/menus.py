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

    # Перегляд Турнірів
    TOURNAMENT_RESULTS = "🏅 Результати Турнірів"
    TOURNAMENT_SCHEDULE = "📅 Розклад Матчів"
    TOURNAMENT_PARTICIPANTS = "👥 Список Учасників"

    # GPT Меню
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

def create_menu(buttons, placeholder, row_width=2):
    """
    Створює клавіатуру з кнопками та встановлює текст підказки.
    :param buttons: Список кнопок (MenuButton або str).
    :param placeholder: Текст підказки для input_field_placeholder.
    :param row_width: Кількість кнопок у рядку.
    :return: ReplyKeyboardMarkup
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
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, input_field_placeholder=placeholder)

def get_main_menu():
    return create_menu(
        buttons=[
            MenuButton.NAVIGATION,
            MenuButton.PROFILE
        ],
        placeholder="Оберіть одну з основних опцій",
        row_width=2
    )

def get_navigation_menu():
    return create_menu(
        buttons=[
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
        placeholder="Виберіть розділ у навігації",
        row_width=3
    )

def get_heroes_menu():
    return create_menu(
        buttons=[
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
        placeholder="GPT-4: Персонажі",  # Оновлено
        row_width=3
    )

def get_hero_class_menu(hero_class):
    heroes = heroes_by_class.get(hero_class, [])
    buttons = heroes + [MenuButton.BACK]
    return create_menu(
        buttons=buttons,
        placeholder=f"GPT-4: {hero_class}",  # Оновлено для конкретного класу
        row_width=3
    )

def get_guides_menu():
    return create_menu(
        buttons=[
            MenuButton.NEW_GUIDES,
            MenuButton.POPULAR_GUIDES,
            MenuButton.BEGINNER_GUIDES,
            MenuButton.ADVANCED_TECHNIQUES,
            MenuButton.TEAMPLAY_GUIDES,
            MenuButton.BACK
        ],
        placeholder="GPT-4: Гайди",  # Оновлено
        row_width=3
    )

def get_counter_picks_menu():
    return create_menu(
        buttons=[
            MenuButton.COUNTER_SEARCH,
            MenuButton.COUNTER_LIST,
            MenuButton.BACK
        ],
        placeholder="GPT-4: Контр-пік",  # Оновлено
        row_width=3
    )

def get_builds_menu():
    return create_menu(
        buttons=[
            MenuButton.CREATE_BUILD,
            MenuButton.MY_BUILDS,
            MenuButton.POPULAR_BUILDS,
            MenuButton.BACK
        ],
        placeholder="GPT-4: Білд",  # Оновлено
        row_width=3
    )

def get_voting_menu():
    return create_menu(
        buttons=[
            MenuButton.CURRENT_VOTES,
            MenuButton.MY_VOTES,
            MenuButton.SUGGEST_TOPIC,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію голосування",
        row_width=3
    )

def get_profile_menu():
    return create_menu(
        buttons=[
            MenuButton.STATISTICS,
            MenuButton.ACHIEVEMENTS,
            MenuButton.SETTINGS,
            MenuButton.FEEDBACK,
            MenuButton.HELP,
            MenuButton.BACK
        ],
        placeholder="Оберіть дію з профілем",
        row_width=3
    )

def get_statistics_menu():
    return create_menu(
        buttons=[
            MenuButton.ACTIVITY,
            MenuButton.RANKING,
            MenuButton.GAME_STATS,
            MenuButton.BACK
        ],
        placeholder="Оберіть тип статистики",
        row_width=3
    )

def get_achievements_menu():
    return create_menu(
        buttons=[
            MenuButton.BADGES,
            MenuButton.PROGRESS,
            MenuButton.TOURNAMENT_STATS,
            MenuButton.AWARDS,
            MenuButton.BACK
        ],
        placeholder="Оберіть категорію досягнень",
        row_width=3
    )

def get_settings_menu():
    return create_menu(
        buttons=[
            MenuButton.LANGUAGE,
            MenuButton.CHANGE_USERNAME,
            MenuButton.UPDATE_ID,
            MenuButton.NOTIFICATIONS,
            MenuButton.BACK
        ],
        placeholder="Налаштуйте свій профіль",
        row_width=3
    )

def get_feedback_menu():
    return create_menu(
        buttons=[
            MenuButton.SEND_FEEDBACK,
            MenuButton.REPORT_BUG,
            MenuButton.BACK
        ],
        placeholder="Виберіть тип зворотного зв'язку",
        row_width=3
    )

def get_help_menu():
    return create_menu(
        buttons=[
            MenuButton.INSTRUCTIONS,
            MenuButton.FAQ,
            MenuButton.HELP_SUPPORT,
            MenuButton.BACK
        ],
        placeholder="Оберіть розділ допомоги",
        row_width=3
    )

def get_tournaments_menu():
    return create_menu(
        buttons=[
            MenuButton.CREATE_TOURNAMENT,
            MenuButton.VIEW_TOURNAMENTS,
            MenuButton.BACK
        ],
        placeholder="Оберіть дію з турнірами",
        row_width=3
    )

def get_meta_menu():
    return create_menu(
        buttons=[
            MenuButton.META_HERO_LIST,
            MenuButton.META_RECOMMENDATIONS,
            MenuButton.META_UPDATES,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію META",
        row_width=3
    )

def get_m6_menu():
    return create_menu(
        buttons=[
            MenuButton.M6_INFO,
            MenuButton.M6_STATS,
            MenuButton.M6_NEWS,
            MenuButton.BACK
        ],
        placeholder="Оберіть інформацію про M6",
        row_width=3
    )

def get_hero_details_menu():
    return create_menu(
        buttons=[
            MenuButton.HERO_BIO,
            MenuButton.HERO_SKILLS,
            MenuButton.HERO_BUILDS,
            MenuButton.HERO_ROLES,
            MenuButton.HERO_STATS,
            MenuButton.BACK
        ],
        placeholder="Оберіть деталь про героя",
        row_width=2
    )

def get_meta_submenu():
    return create_menu(
        buttons=[
            MenuButton.META_SKILLS_STRENGTHS,
            MenuButton.META_GAME_TIPS,
            MenuButton.META_BUILDS,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію META",
        row_width=2
    )

def get_tournament_view_submenu():
    return create_menu(
        buttons=[
            MenuButton.TOURNAMENT_RESULTS,
            MenuButton.TOURNAMENT_SCHEDULE,
            MenuButton.TOURNAMENT_PARTICIPANTS
        ],
        placeholder="Оберіть перегляд турніру",
        row_width=2
    )

def get_gpt_menu():
    """
    Створює клавіатуру для GPT Меню.
    :return: ReplyKeyboardMarkup
    """
    return create_menu(
        buttons=[
            MenuButton.GPT_DATA_GENERATION,
            MenuButton.GPT_HINTS,
            MenuButton.GPT_HERO_STATS,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію GPT",
        row_width=2
    )

def get_generic_inline_keyboard():
    """
    Повертає загальну Inline клавіатуру (при необхідності).
    :return: InlineKeyboardMarkup
    """
    # Ви можете реалізувати цю функцію відповідно до ваших потреб
    pass