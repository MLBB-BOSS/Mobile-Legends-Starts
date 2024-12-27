# keyboards/menus.py

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove
)
from enum import Enum, unique
from typing import List, Dict, Union, Optional
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
    CHALLENGES = "🧩 Челендж"
    GUIDES = "📚 Гайди"
    BUILDS = "🛡️ Білди"
    BUST = "🚀 Буст"
    TEAMS = "🧑‍🤝‍🧑 Команди"
    TRADING = "💰 Торгівля"
    BACK = "🔙 Назад"

    # Додані константи для Турнірів та M6
    CREATE_TOURNAMENT = "➕ Створити Турнір"
    VIEW_TOURNAMENTS = "🔍 Переглянути Турніри"

    M6_INFO = "ℹ️ Інфо M6"
    M6_STATS = "📊 Статистика M6"
    M6_NEWS = "📰 Новини M6"

    # Розділ Персонажі
    TANK = "🛡️ Танк"
    MAGE = "🧙‍♂️ Маг"
    MARKSMAN = "🏹 Стрілець"
    ASSASSIN = "⚔️ Асасін"
    SUPPORT = "❤️ Підтримка"
    FIGHTER = "🗡️ Боєць"
    COMPARISON = "⚖️ Порівняй"
    SEARCH_HERO = "🔎 Пошук"
    VOTING = "🗳️ Голосуй"

    # Розділ Контр-піки
    COUNTER_SEARCH = "🔎 Пошук Контр-піка"
    COUNTER_LIST = "📝 Список Персонажів"
    COUNTER_PICKS = "♻️ Контр-пік"

    # Розділ META
    META_HERO_LIST = "🔍 Список Героїв META"
    META_RECOMMENDATIONS = "☑️ Рекомендації META"
    META_UPDATES = "📈 Оновлення META"
    META = "🔥 МЕТА"

    # Розділ Гайди
    NEW_GUIDES = "🆕 Нові Гайди"
    M6 = "🏆 M6"
    POPULAR_GUIDES = "🌟 Популярні Гайди"
    BEGINNER_GUIDES = "📘 Для Початківців"
    ADVANCED_TECHNIQUES = "🧙 Стратегії Гри"
    TEAMPLAY_GUIDES = "🤝 Командна Гра"

    # Розділ Білди
    CREATE_BUILD = "🏗️ Створити Білд"
    MY_BUILDS = "📄 Мої Білди"
    POPULAR_BUILDS = "🔝 Популярні Білди"

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
    MY_TEAM = "🧍 Моя команда"
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
    CHANGE_USERNAME = "✏️ Змінити Username"
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
    CREATE_TEAM = "➕ Створити Команду"
    VIEW_TEAMS = "👀 Переглянути Команди"

    # Нові константи для Торгівлі
    CREATE_TRADE = "➕ Створити Торгівлю"
    VIEW_TRADES = "👀 Переглянути Торгівлі"
    MANAGE_TRADES = "🔧 Управління Торгівлями"

    # GPT Меню
    GPT_DATA_GENERATION = "📊 Генерація Даних"
    GPT_HINTS = "💡 Поради"
    GPT_HERO_STATS = "📈 Статистика Героїв"

@unique
class LanguageButton(Enum):
    UKRAINIAN = "🇺🇦 Українська"
    ENGLISH = "🇬🇧 English"
    BACK = "🔙 Назад"

# Мапінг кнопок до класів персонажів
MENU_BUTTON_TO_CLASS: Dict[str, str] = {
    MenuButton.TANK.value: "Танк",
    MenuButton.MAGE.value: "Маг",
    MenuButton.MARKSMAN.value: "Стрілець",
    MenuButton.ASSASSIN.value: "Асасін",
    MenuButton.SUPPORT.value: "Підтримка",
    MenuButton.FIGHTER.value: "Боєць"
}

# Списки героїв по класах
heroes_by_class: Dict[str, List[str]] = {
    "Боєць": [
        "Balmond", "Alucard", "Bane", "Zilong", "Freya", "Alpha", "Ruby", "Roger",
        "Gatotkaca", "Jawhead", "Martis", "Aldous", "Minsitthar", "Terizla", "X.Borg",
        "Dyroth", "Masha", "Silvanna", "Yu Zhong", "Khaleed", "Barats", "Paquito",
        "Phoveus", "Aulus", "Fiddrin", "Arlott", "Cici", "Kaja", "Leomord", "Thamuz",
        "Badang", "Guinevere"
    ],
    "Танк": [
        "Alice", "Tigreal", "Akai", "Franco", "Minotaur", "Lolita", "Grock",
        "Hylos", "Uranus", "Belerick", "Khufra", "Esmeralda", "Terizla", "Baxia",
        "Masha", "Atlas", "Barats", "Edith", "Fredrinn", "Johnson", "Hilda",
        "Carmilla", "Gloo", "Chip"
    ],
    "Асасін": [
        "Saber", "Alucard", "Zilong", "Fanny", "Natalia", "Yi Sun-shin",
        "Lancelot", "Helcurt", "Lesley", "Selena", "Mathilda", "Paquito",
        "Yin", "Arlott", "Harley", "Suyou"
    ],
    "Стрілець": [
        "Popol and Kupa", "Brody", "Beatrix", "Natan", "Melissa", "Ixia",
        "Hanabi", "Claude", "Kimmy", "Granger", "Wanwan", "Miya", "Bruno",
        "Clint", "Layla", "Yi Sun-shin", "Moskov", "Roger", "Karrie",
        "Irithel", "Lesley"
    ],
    "Маг": [
        "Vale", "Lunox", "Kadita", "Cecillion", "Luo Yi", "Xavier",
        "Novaria", "Zhuxin", "Harley", "Yve", "Aurora", "Faramis",
        "Esmeralda", "Kagura", "Cyclops", "Vexana", "Odette", "Zhask"
    ],
    "Підтримка": [
        "Rafaela", "Minotaur", "Lolita", "Estes", "Angela", "Faramis",
        "Mathilda", "Florin", "Johnson"
    ],
}

def create_menu(
    buttons: List[Union[MenuButton, LanguageButton]], 
    placeholder: str = "", 
    row_width: int = 2
) -> ReplyKeyboardMarkup:
    """
    Створює меню з кнопками.
    """
    keyboard_buttons = [KeyboardButton(text=button.value) for button in buttons]
    keyboard = [
        keyboard_buttons[i:i + row_width]
        for i in range(0, len(keyboard_buttons), row_width)
    ]
    logger.info(f"Створення меню з кнопками: {[button.value for button in buttons]} та підказкою: '{placeholder}'")
    return ReplyKeyboardMarkup(
        keyboard=keyboard, 
        resize_keyboard=True, 
        input_field_placeholder=placeholder
    )

def create_inline_menu(
    buttons: List[InlineKeyboardButton], 
    row_width: int = 3
) -> InlineKeyboardMarkup:
    """
    Створює інлайн меню з кнопками.
    """
    keyboard = [
        buttons[i:i + row_width]
        for i in range(0, len(buttons), row_width)
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_main_menu() -> ReplyKeyboardMarkup:
    """
    Створює головне меню.
    """
    return create_menu(
        buttons=[
            MenuButton.NAVIGATION,
            MenuButton.PROFILE
        ],
        placeholder="Оберіть одну з основних опцій",
        row_width=2
    )

def get_navigation_menu() -> ReplyKeyboardMarkup:
    """
    Створює меню Навігації.
    """
    return create_menu(
        buttons=[
            MenuButton.TOURNAMENTS,
            MenuButton.HEROES,
            MenuButton.BUILDS,
            MenuButton.GUIDES,
            MenuButton.TEAMS,
            MenuButton.CHALLENGES,
            MenuButton.BUST,
            MenuButton.TRADING,
            MenuButton.BACK
        ],
        placeholder="Виберіть розділ у навігації",
        row_width=3
    )

def get_challenges_menu() -> ReplyKeyboardMarkup:
    """
    Створює меню Challenges.
    """
    return create_menu(
        buttons=[
            MenuButton.ADD_CHALLENGE,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію для Challenges",
        row_width=2
    )

def get_guides_menu() -> ReplyKeyboardMarkup:
    """
    Створює меню Guides.
    """
    return create_menu(
        buttons=[
            MenuButton.NEW_GUIDES,
            MenuButton.POPULAR_GUIDES,
            MenuButton.BEGINNER_GUIDES,
            MenuButton.ADVANCED_TECHNIQUES,
            MenuButton.TEAMPLAY_GUIDES,
            MenuButton.M6,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію для Guides",
        row_width=2
    )

def get_bust_menu() -> ReplyKeyboardMarkup:
    """
    Створює меню Bust.
    """
    return create_menu(
        buttons=[
            MenuButton.BUST_BOOST,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію для Bust",
        row_width=2
    )

def get_teams_menu() -> ReplyKeyboardMarkup:
    """
    Створює меню Teams.
    """
    return create_menu(
        buttons=[
            MenuButton.CREATE_TEAM,
            MenuButton.VIEW_TEAMS,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію для Teams",
        row_width=2
    )

def get_trading_menu() -> ReplyKeyboardMarkup:
    """
    Створює меню Trading.
    """
    return create_menu(
        buttons=[
            MenuButton.CREATE_TRADE,
            MenuButton.VIEW_TRADES,
            MenuButton.MANAGE_TRADES,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію для Trading",
        row_width=2
    )

def get_settings_menu() -> ReplyKeyboardMarkup:
    """
    Створює меню Settings.
    """
    return create_menu(
        buttons=[
            MenuButton.LANGUAGE,
            MenuButton.CHANGE_USERNAME,
            MenuButton.UPDATE_ID,
            MenuButton.NOTIFICATIONS,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію для Налаштувань",
        row_width=2
    )

def get_help_menu() -> ReplyKeyboardMarkup:
    """
    Створює меню Help.
    """
    return create_menu(
        buttons=[
            MenuButton.INSTRUCTIONS,
            MenuButton.FAQ,
            MenuButton.HELP_SUPPORT,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію для Допомоги",
        row_width=2
    )

def get_my_team_menu() -> ReplyKeyboardMarkup:
    """
    Створює меню My Team.
    """
    return create_menu(
        buttons=[
            MenuButton.CREATE_TEAM,
            MenuButton.VIEW_TEAMS,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію для Моїй Команді",
        row_width=2
    )

def get_language_menu() -> ReplyKeyboardMarkup:
    """
    Створює меню вибору мови.
    """
    return create_menu(
        buttons=[
            LanguageButton.UKRAINIAN,
            LanguageButton.ENGLISH,
            LanguageButton.BACK
        ],
        placeholder="Оберіть мову інтерфейсу",
        row_width=2
    )

def get_profile_menu() -> ReplyKeyboardMarkup:
    """
    Створює меню Профілю.
    """
    return create_menu(
        buttons=[
            MenuButton.STATISTICS,
            MenuButton.ACHIEVEMENTS,
            MenuButton.SETTINGS,
            MenuButton.FEEDBACK,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію для Профілю",
        row_width=2
    )

def get_statistics_menu() -> ReplyKeyboardMarkup:
    """
    Створює меню Статистики.
    """
    return create_menu(
        buttons=[
            MenuButton.ACTIVITY,
            MenuButton.RANKING,
            MenuButton.GAME_STATS,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію для Статистики",
        row_width=2
    )

def get_achievements_menu() -> ReplyKeyboardMarkup:
    """
    Створює меню Досягнень.
    """
    return create_menu(
        buttons=[
            MenuButton.BADGES,
            MenuButton.PROGRESS,
            MenuButton.TOURNAMENT_STATS,
            MenuButton.AWARDS,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію для Досягнень",
        row_width=2
    )

def get_feedback_menu() -> ReplyKeyboardMarkup:
    """
    Створює меню Зворотного Зв'язку.
    """
    return create_menu(
        buttons=[
            MenuButton.SEND_FEEDBACK,
            MenuButton.REPORT_BUG,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію для Зворотного Зв'язку",
        row_width=2
    )

def get_gpt_menu() -> ReplyKeyboardMarkup:
    """
    Створює меню GPT.
    """
    return create_menu(
        buttons=[
            MenuButton.GPT_DATA_GENERATION,
            MenuButton.GPT_HINTS,
            MenuButton.GPT_HERO_STATS,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію для GPT",
        row_width=2
    )

def get_m6_menu() -> ReplyKeyboardMarkup:
    """
    Створює меню M6.
    """
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

# Додаткові меню для конкретних функцій
def get_bust_boost_menu() -> ReplyKeyboardMarkup:
    """
    Створює меню для функції Буст.
    """
    return create_menu(
        buttons=[
            MenuButton.BUST_BOOST,  # Переконайтеся, що ця кнопка визначена в MenuButton
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію для Буст",
        row_width=2
    )

# Додайте будь-які додаткові меню, які потрібні для інших розділів