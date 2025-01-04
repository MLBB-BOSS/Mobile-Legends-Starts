# keyboards/menus.py

# -------------------------
# 📦 Імпорти
# -------------------------
import logging
from typing import List, Dict, Union
from enum import Enum, unique

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove
)

# -------------------------
# 🔢 Перерахування (Enums) для Кнопок Меню
# -------------------------
@unique
class MenuButton(Enum):
    """Перерахування для кнопок меню бота."""

    # 🏠 Головне Меню
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Мій Профіль"

    # 🧭 Розділ Навігація
    TOURNAMENTS = "🏆 Турніри"
    HEROES = "🥷 Персонажі"
    CHALLENGES = "🧩 Челендж"
    GUIDES = "📚 Гайди"
    BUILDS = "🛡️ Білди"
    BUST = "🚀 Буст"
    TEAMS = "🧑‍🤝‍🧑 Команди"
    TRADING = "💰 Торгівля"
    BACK = "🔙 Назад"

    # ➕ Додані Константи для Турнірів та M6
    CREATE_TOURNAMENT = "➕ Створити Турнір"
    VIEW_TOURNAMENTS = "🔍 Переглянути Турніри"
    M6_INFO = "ℹ️ Інфо M6"
    M6_STATS = "📊 Статистика M6"
    M6_NEWS = "📰 Новини M6"

    # 🥷 Розділ Персонажі
    TANK = "🛡️ Танк"
    MAGE = "🧙‍♂️ Маг"
    MARKSMAN = "🏹 Стрілець"
    ASSASSIN = "⚔️ Асасін"
    SUPPORT = "❤️ Підтримка"
    FIGHTER = "🗡️ Боєць"
    COMPARISON = "⚖️ Порівняй"
    SEARCH_HERO = "🔎 Пошук"
    VOTING = "🗳️ Голосуй"

    # 🧩 Розділ Контр-піки
    COUNTER_SEARCH = "🔎 Пошук Контр-піка"
    COUNTER_LIST = "📝 Список Персонажів"
    COUNTER_PICKS = "♻️ Контр-пік"

    # 🔥 Розділ META
    META_HERO_LIST = "🔍 Список Героїв META"
    META_RECOMMENDATIONS = "☑️ Рекомендації META"
    META_UPDATES = "📈 Оновлення META"
    META = "🔥 МЕТА"

    # 📚 Розділ Гайди
    NEW_GUIDES = "🆕 Нові Гайди"
    M6 = "🏆 M6"
    POPULAR_GUIDES = "🌟 Популярні Гайди"
    BEGINNER_GUIDES = "📘 Для Початківців"
    ADVANCED_TECHNIQUES = "🧙 Стратегії Гри"
    TEAMPLAY_GUIDES = "🤝 Командна Гра"

    # 🛡️ Розділ Білди
    CREATE_BUILD = "🏗️ Створити Білд"
    MY_BUILDS = "📄 Мої Білди"
    POPULAR_BUILDS = "🔝 Популярні Білди"

    # 🗳️ Розділ Голосування
    CURRENT_VOTES = "📍 Поточні Опитування"
    MY_VOTES = "📋 Мої Голосування"
    SUGGEST_TOPIC = "➕ Запропонувати Тему"

    # 🪪 Розділ Профіль
    STATISTICS = "📈 Статистика"
    ACHIEVEMENTS = "🏆 Досягнення"
    SETTINGS = "⚙️ Налаштування"
    FEEDBACK = "💌 Зворотний Зв'язок"
    HELP = "❓ Допомога"
    MY_TEAM = "🧍 Моя команда"
    GPT = "👾 GPT"

    # 📊 Підрозділ Статистика
    ACTIVITY = "📊 Загальна Активність"
    RANKING = "🥇 Рейтинг"
    GAME_STATS = "🎮 Ігрова Статистика"

    # 🏅 Підрозділ Досягнення
    BADGES = "🎖️ Мої Бейджі"
    PROGRESS = "🚀 Прогрес"
    TOURNAMENT_STATS = "🏅 Турнірна Статистика"
    AWARDS = "🎟️ Отримані Нагороди"

    # 🌐 Підрозділ Налаштування
    LANGUAGE = "🌐 Мова Інтерфейсу"
    CHANGE_USERNAME = "ℹ️ Змінити Username"
    UPDATE_ID = "🆔 Оновити ID"
    NOTIFICATIONS = "🔔 Сповіщення"

    # ✏️ Підрозділ Зворотний зв'язок
    SEND_FEEDBACK = "✏️ Надіслати Відгук"
    REPORT_BUG = "🐛 Повідомити про Помилку"

    # ❓ Підрозділ Допомога
    INSTRUCTIONS = "📄 Інструкції"
    FAQ = "❔ FAQ"
    HELP_SUPPORT = "📞 Підтримка"

    # ➕ Новий Розділ Команди
    CREATE_TEAM = "➕ Створити Команду"
    VIEW_TEAMS = "👀 Переглянути Команди"

    # ➕ Нові Константи для Торгівлі
    CREATE_TRADE = "➕ Створити Торгівлю"
    VIEW_TRADES = "👀 Переглянути Торгівлі"
    MANAGE_TRADES = "🔧 Управління Торгівлями"

    # 👾 GPT Меню
    GPT_DATA_GENERATION = "📊 Генерація Даних"
    GPT_HINTS = "💡 Поради"
    GPT_HERO_STATS = "📈 Статистика Героїв"

@unique
class LanguageButton(Enum):
    """Перерахування для кнопок вибору мови (Reply-меню)."""
    UKRAINIAN = "🇺🇦 Українська"
    ENGLISH = "🇬🇧 English"
    BACK = "🔙 Назад"

# -------------------------
# 🗂️ Мапінги Даних
# -------------------------
MENU_BUTTON_TO_CLASS: Dict[str, str] = {
    MenuButton.TANK.value: "Танк",
    MenuButton.MAGE.value: "Маг",
    MenuButton.MARKSMAN.value: "Стрілець",
    MenuButton.ASSASSIN.value: "Асасін",
    MenuButton.SUPPORT.value: "Підтримка",
    MenuButton.FIGHTER.value: "Боєць",
}

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

# -------------------------
# 📝 Конфігурація Логування
# -------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# -------------------------
# 🛠️ Функції Створення Reply-Меню
# -------------------------
def create_menu(
    buttons: List[Union[MenuButton, LanguageButton]],
    placeholder: str = "",
    row_width: int = 2
) -> ReplyKeyboardMarkup:
    """
    Створює звичайне (Reply) меню з кнопками (MenuButton або LanguageButton).
    """
    # Перевірка, що всі кнопки належать Enum'ам
    if not all(isinstance(button, (MenuButton, LanguageButton)) for button in buttons):
        logger.error("Список кнопок містить некоректні елементи.")
        raise ValueError("Усі елементи у списку кнопок повинні бути екземплярами MenuButton або LanguageButton Enum.")

    # Створюємо список кнопок
    keyboard_buttons = [KeyboardButton(text=b.value) for b in buttons]

    # Групуємо кнопки по row_width
    keyboard = [
        keyboard_buttons[i : i + row_width]
        for i in range(0, len(keyboard_buttons), row_width)
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder=placeholder
    )

def get_main_menu() -> ReplyKeyboardMarkup:
    """
    Головне меню (Reply).
    """
    return create_menu(
        buttons=[MenuButton.NAVIGATION, MenuButton.PROFILE],
        placeholder="Оберіть одну з основних опцій",
        row_width=2
    )

def get_navigation_menu() -> ReplyKeyboardMarkup:
    """
    Меню Навігації (Reply).
    """
    return create_menu(
        buttons=[
            MenuButton.HEROES,
            MenuButton.BUILDS,
            MenuButton.GUIDES,
            MenuButton.TOURNAMENTS,
            MenuButton.TEAMS,
            MenuButton.CHALLENGES,
            MenuButton.BUST,
            MenuButton.TRADING,
            MenuButton.BACK
        ],
        placeholder="Виберіть розділ у навігації",
        row_width=3
    )

def get_hero_class_menu() -> ReplyKeyboardMarkup:
    """
    Меню вибору класу героїв (Reply).
    """
    return create_menu(
        buttons=[
            MenuButton.TANK,
            MenuButton.MAGE,
            MenuButton.MARKSMAN,
            MenuButton.ASSASSIN,
            MenuButton.FIGHTER,
            MenuButton.SUPPORT,
            MenuButton.BACK
        ],
        placeholder="Виберіть клас персонажа",
        row_width=2
    )

def get_heroes_menu() -> ReplyKeyboardMarkup:
    """
    Меню Персонажів (Reply).
    """
    return create_menu(
        buttons=[
            MenuButton.TANK,
            MenuButton.MAGE,
            MenuButton.MARKSMAN,
            MenuButton.ASSASSIN,
            MenuButton.FIGHTER,
            MenuButton.SUPPORT,
            MenuButton.META,
            MenuButton.COUNTER_PICKS,
            MenuButton.COMPARISON,
            MenuButton.VOTING,
            MenuButton.SEARCH_HERO,
            MenuButton.BACK
        ],
        placeholder="Виберіть клас персонажа",
        row_width=3
    )

def get_profile_menu() -> ReplyKeyboardMarkup:
    """
    Меню Профілю (Reply).
    """
    return create_menu(
        buttons=[
            MenuButton.STATISTICS,
            MenuButton.MY_TEAM,
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

def get_language_menu() -> ReplyKeyboardMarkup:
    """
    Клавіатура для вибору мови (Reply).
    """
    return create_menu(
        buttons=[
            LanguageButton.UKRAINIAN,
            LanguageButton.ENGLISH,
            LanguageButton.BACK
        ],
        placeholder="Оберіть мову інтерфейсу",
        row_width=1
    )

def get_challenges_menu() -> ReplyKeyboardMarkup:
    """
    Клавіатура для розділу Челенджів (Reply).
    """
    return create_menu(
        buttons=[
            MenuButton.CREATE_CHALLENGE,
            MenuButton.VIEW_CHALLENGES,
            MenuButton.BACK
        ],
        placeholder="Виберіть опцію челенджів",
        row_width=2
    )

def get_bust_menu() -> ReplyKeyboardMarkup:
    """
    Клавіатура для розділу Буст (Reply).
    """
    return create_menu(
        buttons=[MenuButton.BUST, MenuButton.BACK],
        placeholder="Виберіть опцію бустів",
        row_width=2
    )

def get_my_team_menu() -> ReplyKeyboardMarkup:
    """
    Клавіатура для розділу Моєї Команди (Reply).
    """
    return create_menu(
        buttons=[MenuButton.MY_TEAM, MenuButton.BACK],
        placeholder="Виберіть опцію Моєї Команди",
        row_width=2
    )

def get_guides_menu() -> ReplyKeyboardMarkup:
    """
    Меню Гайдів (Reply).
    """
    return create_menu(
        buttons=[
            MenuButton.NEW_GUIDES,
            MenuButton.M6,
            MenuButton.POPULAR_GUIDES,
            MenuButton.BEGINNER_GUIDES,
            MenuButton.ADVANCED_TECHNIQUES,
            MenuButton.TEAMPLAY_GUIDES,
            MenuButton.BACK
        ],
        placeholder="Оберіть розділ гайдів",
        row_width=3
    )

def get_counter_picks_menu() -> ReplyKeyboardMarkup:
    """
    Меню Контр-піків (Reply).
    """
    return create_menu(
        buttons=[
            MenuButton.COUNTER_SEARCH,
            MenuButton.COUNTER_LIST,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію Контр-піків",
        row_width=3
    )

def get_builds_menu() -> ReplyKeyboardMarkup:
    """
    Меню Білдів (Reply).
    """
    return create_menu(
        buttons=[
            MenuButton.CREATE_BUILD,
            MenuButton.MY_BUILDS,
            MenuButton.POPULAR_BUILDS,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію Білдів",
        row_width=3
    )

def get_voting_menu() -> ReplyKeyboardMarkup:
    """
    Меню Голосування (Reply).
    """
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

def get_statistics_menu() -> ReplyKeyboardMarkup:
    """
    Меню Статистики (Reply).
    """
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

def get_achievements_menu() -> ReplyKeyboardMarkup:
    """
    Меню Досягнень (Reply).
    """
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

def get_settings_menu() -> ReplyKeyboardMarkup:
    """
    Меню Налаштувань (Reply).
    """
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

def get_feedback_menu() -> ReplyKeyboardMarkup:
    """
    Меню Зворотного Зв'язку (Reply).
    """
    return create_menu(
        buttons=[
            MenuButton.SEND_FEEDBACK,
            MenuButton.REPORT_BUG,
            MenuButton.BACK
        ],
        placeholder="Виберіть тип зворотного зв'язку",
        row_width=3
    )

def get_help_menu() -> ReplyKeyboardMarkup:
    """
    Меню Допомоги (Reply).
    """
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

def get_tournaments_menu() -> ReplyKeyboardMarkup:
    """
    Меню Турнірів (Reply).
    """
    return create_menu(
        buttons=[
            MenuButton.CREATE_TOURNAMENT,
            MenuButton.VIEW_TOURNAMENTS,
            MenuButton.BACK
        ],
        placeholder="Оберіть дію з турнірами",
        row_width=3
    )

def get_meta_menu() -> ReplyKeyboardMarkup:
    """
    Меню META (Reply).
    """
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

def get_m6_menu() -> ReplyKeyboardMarkup:
    """
    Меню M6 (Reply).
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

def get_gpt_menu() -> ReplyKeyboardMarkup:
    """
    Меню GPT (Reply).
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

def get_teams_menu() -> ReplyKeyboardMarkup:
    """
    Меню Команд (Reply).
    """
    return create_menu(
        buttons=[
            MenuButton.CREATE_TEAM,
            MenuButton.VIEW_TEAMS,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію Команди",
        row_width=2
    )

def get_trading_menu() -> ReplyKeyboardMarkup:
    """
    Меню Торгівлі (Reply).
    """
    return create_menu(
        buttons=[
            MenuButton.CREATE_TRADE,
            MenuButton.VIEW_TRADES,
            MenuButton.MANAGE_TRADES,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію Торгівлі",
        row_width=2
    )

# -------------------------
# 🛠️ Функції Створення Інлайн-Меню
# -------------------------
def create_inline_menu(
    buttons: List[InlineKeyboardButton],
    row_width: int = 3
) -> InlineKeyboardMarkup:
    """
    Створює інлайн-меню (InlineKeyboardMarkup).
    """
    if not buttons:
        logger.warning("Список інлайн-кнопок порожній.")
        return InlineKeyboardMarkup()

    keyboard = [
        buttons[i : i + row_width]
        for i in range(0, len(buttons), row_width)
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_generic_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру з однією кнопкою «Назад».
    """
    logger.info("Створення генералізованої інлайн клавіатури з кнопкою 'Назад'.")
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="░▒▓█ Ｍ Ｌ Ｓ █▓▒░ 🔙 Назад",
                    callback_data="menu_back"
                )
            ]
        ]
    )

# -------------------------
# Функції для конкретних Inline-меню (профіль, гайди тощо)
# -------------------------
def get_profile_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Інлайн-клавіатура для розділу Профіль.
    """
    return create_inline_menu([
        InlineKeyboardButton(text="📈 Статистика", callback_data="statistics"),
        InlineKeyboardButton(text="🧍 Моя команда", callback_data="my_team"),
        InlineKeyboardButton(text="🏆 Досягнення", callback_data="achievements"),
        InlineKeyboardButton(text="⚙️ Налаштування", callback_data="settings"),
        InlineKeyboardButton(text="💌 Зворотний Зв'язок", callback_data="feedback"),
        InlineKeyboardButton(text="❓ Допомога", callback_data="help"),
        InlineKeyboardButton(text="👾 GPT", callback_data="gpt"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="menu_back")
    ], row_width=2)

def get_guides_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Інлайн-клавіатура для розділу Гайди.
    """
    return create_inline_menu([
        InlineKeyboardButton(text="🆕 Нові Гайди", callback_data="new_guides"),
        InlineKeyboardButton(text="🏆 M6", callback_data="m6"),
        InlineKeyboardButton(text="🌟 Популярні Гайди", callback_data="popular_guides"),
        InlineKeyboardButton(text="📘 Для Початківців", callback_data="beginner_guides"),
        InlineKeyboardButton(text="🧙 Стратегії Гри", callback_data="advanced_techniques"),
        InlineKeyboardButton(text="🤝 Командна Гра", callback_data="teamplay_guides"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="menu_back")
    ], row_width=2)

def get_challenges_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Інлайн-клавіатура для розділу Челенджів.
    """
    return create_inline_menu([
        InlineKeyboardButton(text="➕ Створити Челендж", callback_data="create_challenge"),
        InlineKeyboardButton(text="🔍 Переглянути Челенджі", callback_data="view_challenges"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="menu_back")
    ], row_width=2)

def get_bust_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Інлайн-клавіатура для розділу Буст.
    """
    return create_inline_menu([
        InlineKeyboardButton(text="🚀 Буст", callback_data="bust"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="menu_back")
    ], row_width=2)

def get_my_team_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Інлайн-клавіатура для розділу Моя Команда.
    """
    return create_inline_menu([
        InlineKeyboardButton(text="🧍 Моя команда", callback_data="my_team"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="menu_back")
    ], row_width=2)

def get_counter_picks_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Інлайн-клавіатура для розділу Контр-піки.
    """
    return create_inline_menu([
        InlineKeyboardButton(text="🔎 Пошук Контр-піка", callback_data="counter_search"),
        InlineKeyboardButton(text="📝 Список Персонажів", callback_data="counter_list"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="menu_back")
    ], row_width=2)

def get_builds_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Інлайн-клавіатура для розділу Білди.
    """
    return create_inline_menu([
        InlineKeyboardButton(text="🏗️ Створити Білд", callback_data="create_build"),
        InlineKeyboardButton(text="📄 Мої Білди", callback_data="my_builds"),
        InlineKeyboardButton(text="🔝 Популярні Білди", callback_data="popular_builds"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="menu_back")
    ], row_width=2)

def get_voting_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Інлайн-клавіатура для розділу Голосування.
    """
    return create_inline_menu([
        InlineKeyboardButton(text="📍 Поточні Опитування", callback_data="current_votes"),
        InlineKeyboardButton(text="📋 Мої Голосування", callback_data="my_votes"),
        InlineKeyboardButton(text="➕ Запропонувати Тему", callback_data="suggest_topic"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="menu_back")
    ], row_width=2)

def get_statistics_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Інлайн-клавіатура для розділу Статистика.
    """
    return create_inline_menu([
        InlineKeyboardButton(text="📊 Загальна Активність", callback_data="activity"),
        InlineKeyboardButton(text="🥇 Рейтинг", callback_data="ranking"),
        InlineKeyboardButton(text="🎮 Ігрова Статистика", callback_data="game_stats"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="menu_back")
    ], row_width=2)

def get_achievements_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Інлайн-клавіатура для розділу Досягнення.
    """
    return create_inline_menu([
        InlineKeyboardButton(text="🎖️ Мої Бейджі", callback_data="badges"),
        InlineKeyboardButton(text="🚀 Прогрес", callback_data="progress"),
        InlineKeyboardButton(text="🏅 Турнірна Статистика", callback_data="tournament_stats"),
        InlineKeyboardButton(text="🎟️ Отримані Нагороди", callback_data="awards"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="menu_back")
    ], row_width=2)

def get_settings_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Інлайн-клавіатура для розділу Налаштувань.
    """
    return create_inline_menu([
        InlineKeyboardButton(text="🌐 Мова Інтерфейсу", callback_data="language"),
        InlineKeyboardButton(text="ℹ️ Змінити Username", callback_data="change_username"),
        InlineKeyboardButton(text="🆔 Оновити ID", callback_data="update_id"),
        InlineKeyboardButton(text="🔔 Сповіщення", callback_data="notifications"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="menu_back")
    ], row_width=2)

def get_feedback_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Інлайн-клавіатура для розділу Зворотного Зв'язку.
    """
    return create_inline_menu([
        InlineKeyboardButton(text="✏️ Надіслати Відгук", callback_data="send_feedback"),
        InlineKeyboardButton(text="🐛 Повідомити про Помилку", callback_data="report_bug"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="menu_back")
    ], row_width=2)

def get_help_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Інлайн-клавіатура для розділу Допомога.
    """
    return create_inline_menu([
        InlineKeyboardButton(text="📄 Інструкції", callback_data="instructions"),
        InlineKeyboardButton(text="❔ FAQ", callback_data="faq"),
        InlineKeyboardButton(text="📞 Підтримка", callback_data="help_support"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="menu_back")
    ], row_width=2)

def get_gpt_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Інлайн-клавіатура для GPT-розділу.
    """
    return create_inline_menu([
        InlineKeyboardButton(text="📊 Генерація Даних", callback_data="gpt_data_generation"),
        InlineKeyboardButton(text="💡 Поради", callback_data="gpt_hints"),
        InlineKeyboardButton(text="📈 Статистика Героїв", callback_data="gpt_hero_stats"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="menu_back")
    ], row_width=2)

# -------------------------
# Додаткові приклади функцій виклику Меню
# -------------------------
def get_main_menu_keyboard():
    """Демонструє виклик головного меню (Reply)."""
    return get_main_menu()

def get_main_menu_inline_keyboard():
    """Демонструє виклик типового інлайн-меню (просто одна кнопка Назад)."""
    return get_generic_inline_keyboard()

def get_navigation_inline_keyboard():
    """Демонструє інлайн-кнопки для «Навігації» (приклад, можна наповнити за потреби)."""
    return create_inline_menu([
        InlineKeyboardButton(text="Персонажі", callback_data="nav_heroes"),
        InlineKeyboardButton(text="Челенджі", callback_data="nav_challenges"),
        InlineKeyboardButton(text="🔙 Назад", callback_data="menu_back")
    ], row_width=2)