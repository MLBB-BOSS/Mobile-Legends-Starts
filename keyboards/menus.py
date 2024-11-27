# keyboards/menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from enum import Enum
import logging

# Логування
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MenuButton(Enum):
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Мій Профіль"
    HEROES = "🛡️ Персонажі"
    GUIDES = "📚 Гайди"
    SEARCH_HERO = "🔎 Пошук Персонажа"
    FIGHTER = "💪 Боєць"
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
    BUILDS = "⚜️ Білди"
    CURRENT_VOTES = "📍 Поточні Опитування"
    MY_VOTES = "📋 Мої Голосування"
    SUGGEST_TOPIC = "➕ Запропонувати Тему"
    VOTING = "📊 Голосування"
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
    HELP_SUPPORT = "🆘 Підтримка"

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

# Функція для створення Reply клавіатур
def create_reply_menu(buttons, row_width=2):
    """
    Створює ReplyKeyboardMarkup з кнопками.
    :param buttons: Список кнопок (MenuButton).
    :param row_width: Кількість кнопок у рядку.
    :return: ReplyKeyboardMarkup
    """
    keyboard = [
        [KeyboardButton(text=button.value) for button in buttons[i:i + row_width]]
        for i in range(0, len(buttons), row_width)
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Функція для створення Inline клавіатур з Callback Queries
def create_inline_menu(buttons, row_width=3):
    """
    Створює InlineKeyboardMarkup з кнопками.
    :param buttons: Список кнопок (tuple(text, callback_data)).
    :param row_width: Кількість кнопок у рядку.
    :return: InlineKeyboardMarkup
    """
    inline_buttons = [
        InlineKeyboardButton(text=text, callback_data=callback_data) for text, callback_data in buttons
    ]
    keyboard = [
        inline_buttons[i:i + row_width]
        for i in range(0, len(inline_buttons), row_width)
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Меню "Головне меню" з двома кнопками (Reply Keyboard)
def get_main_menu():
    return create_reply_menu(
        [
            MenuButton.NAVIGATION,
            MenuButton.PROFILE
        ],
        row_width=2
    )

# Меню "Навігація" (Inline Keyboard з трьома колонками)
def get_navigation_menu():
    return create_inline_menu(
        [
            (MenuButton.HEROES.value, "navigate_heroes"),
            (MenuButton.GUIDES.value, "navigate_guides"),
            (MenuButton.COUNTER_PICKS.value, "navigate_counter"),
            (MenuButton.BUILDS.value, "navigate_builds"),
            (MenuButton.VOTING.value, "navigate_voting"),
            (MenuButton.BACK.value, "navigate_back")
        ],
        row_width=3
    )

# Меню "Персонажі" (Inline Keyboard з трьома колонками)
def get_heroes_menu():
    return create_inline_menu(
        [
            (MenuButton.SEARCH_HERO.value, "heroes_search"),
            (MenuButton.FIGHTER.value, "heroes_fighter"),
            (MenuButton.TANK.value, "heroes_tank"),
            (MenuButton.MAGE.value, "heroes_mage"),
            (MenuButton.MARKSMAN.value, "heroes_marksman"),
            (MenuButton.ASSASSIN.value, "heroes_assassin"),
            (MenuButton.SUPPORT.value, "heroes_support"),
            (MenuButton.BACK.value, "heroes_back")
        ],
        row_width=3
    )

# Функція для створення меню героїв конкретного класу (Inline Keyboard з трьома колонками)
def get_hero_class_menu(hero_class):
    heroes = heroes_by_class.get(hero_class, [])
    buttons = [(hero, f"hero_{hero}") for hero in heroes]
    # Додати кнопку "Назад"
    buttons.append((MenuButton.BACK.value, "heroes_back"))
    return create_inline_menu(
        buttons,
        row_width=3
    )

# Меню "Гайди" (Inline Keyboard з трьома колонками)
def get_guides_menu():
    return create_inline_menu(
        [
            (MenuButton.NEW_GUIDES.value, "guides_new"),
            (MenuButton.POPULAR_GUIDES.value, "guides_popular"),
            (MenuButton.BEGINNER_GUIDES.value, "guides_beginner"),
            (MenuButton.ADVANCED_TECHNIQUES.value, "guides_advanced"),
            (MenuButton.TEAMPLAY_GUIDES.value, "guides_teamplay"),
            (MenuButton.BACK.value, "guides_back")
        ],
        row_width=3
    )

# Меню "Контр-піки" (Inline Keyboard з трьома колонками)
def get_counter_picks_menu():
    return create_inline_menu(
        [
            (MenuButton.COUNTER_SEARCH.value, "counter_search"),
            (MenuButton.COUNTER_LIST.value, "counter_list"),
            (MenuButton.BACK.value, "counter_back")
        ],
        row_width=3
    )

# Меню "Білди" (Inline Keyboard з трьома колонками)
def get_builds_menu():
    return create_inline_menu(
        [
            (MenuButton.CREATE_BUILD.value, "builds_create"),
            (MenuButton.MY_BUILDS.value, "builds_my"),
            (MenuButton.POPULAR_BUILDS.value, "builds_popular"),
            (MenuButton.BACK.value, "builds_back")
        ],
        row_width=3
    )

# Меню "Голосування" (Inline Keyboard з трьома колонками)
def get_voting_menu():
    return create_inline_menu(
        [
            (MenuButton.CURRENT_VOTES.value, "voting_current"),
            (MenuButton.MY_VOTES.value, "voting_my"),
            (MenuButton.SUGGEST_TOPIC.value, "voting_suggest"),
            (MenuButton.BACK.value, "voting_back")
        ],
        row_width=3
    )

# Меню "Профіль" (Inline Keyboard з трьома колонками)
def get_profile_menu():
    return create_inline_menu(
        [
            (MenuButton.ACTIVITY.value, "profile_activity"),
            (MenuButton.RANKING.value, "profile_ranking"),
            (MenuButton.GAME_STATS.value, "profile_game_stats"),
            (MenuButton.BACK.value, "profile_back")
        ],
        row_width=3
    )
# keyboards/menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from enum import Enum
import logging

# Логування
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MenuButton(Enum):
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Мій Профіль"
    HEROES = "🛡️ Персонажі"
    GUIDES = "📚 Гайди"
    SEARCH_HERO = "🔎 Пошук Персонажа"
    FIGHTER = "💪 Боєць"
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
    BUILDS = "⚜️ Білди"
    CURRENT_VOTES = "📍 Поточні Опитування"
    MY_VOTES = "📋 Мої Голосування"
    SUGGEST_TOPIC = "➕ Запропонувати Тему"
    VOTING = "📊 Голосування"
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
    HELP_SUPPORT = "🆘 Підтримка"

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

# Функція для створення Reply клавіатур
def create_reply_menu(buttons, row_width=2):
    """
    Створює ReplyKeyboardMarkup з кнопками.
    :param buttons: Список кнопок (MenuButton).
    :param row_width: Кількість кнопок у рядку.
    :return: ReplyKeyboardMarkup
    """
    keyboard = [
        [KeyboardButton(text=button.value) for button in buttons[i:i + row_width]]
        for i in range(0, len(buttons), row_width)
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Функція для створення Inline клавіатур з Callback Queries
def create_inline_menu(buttons, row_width=3):
    """
    Створює InlineKeyboardMarkup з кнопками.
    :param buttons: Список кнопок (tuple(text, callback_data)).
    :param row_width: Кількість кнопок у рядку.
    :return: InlineKeyboardMarkup
    """
    inline_buttons = [
        InlineKeyboardButton(text=text, callback_data=callback_data) for text, callback_data in buttons
    ]
    keyboard = [
        inline_buttons[i:i + row_width]
        for i in range(0, len(inline_buttons), row_width)
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# Меню "Головне меню" з двома кнопками (Reply Keyboard)
def get_main_menu():
    return create_reply_menu(
        [
            MenuButton.NAVIGATION,
            MenuButton.PROFILE
        ],
        row_width=2
    )

# Меню "Навігація" (Inline Keyboard з трьома колонками)
def get_navigation_menu():
    return create_inline_menu(
        [
            (MenuButton.HEROES.value, "navigate_heroes"),
            (MenuButton.GUIDES.value, "navigate_guides"),
            (MenuButton.COUNTER_PICKS.value, "navigate_counter"),
            (MenuButton.BUILDS.value, "navigate_builds"),
            (MenuButton.VOTING.value, "navigate_voting"),
            (MenuButton.BACK.value, "navigate_back")
        ],
        row_width=3
    )

# Меню "Персонажі" (Inline Keyboard з трьома колонками)
def get_heroes_menu():
    return create_inline_menu(
        [
            (MenuButton.SEARCH_HERO.value, "heroes_search"),
            (MenuButton.FIGHTER.value, "heroes_fighter"),
            (MenuButton.TANK.value, "heroes_tank"),
            (MenuButton.MAGE.value, "heroes_mage"),
            (MenuButton.MARKSMAN.value, "heroes_marksman"),
            (MenuButton.ASSASSIN.value, "heroes_assassin"),
            (MenuButton.SUPPORT.value, "heroes_support"),
            (MenuButton.BACK.value, "heroes_back")
        ],
        row_width=3
    )

# Функція для створення меню героїв конкретного класу (Inline Keyboard з трьома колонками)
def get_hero_class_menu(hero_class):
    heroes = heroes_by_class.get(hero_class, [])
    buttons = [(hero, f"hero_{hero}") for hero in heroes]
    # Додати кнопку "Назад"
    buttons.append((MenuButton.BACK.value, "heroes_back"))
    return create_inline_menu(
        buttons,
        row_width=3
    )

# Меню "Гайди" (Inline Keyboard з трьома колонками)
def get_guides_menu():
    return create_inline_menu(
        [
            (MenuButton.NEW_GUIDES.value, "guides_new"),
            (MenuButton.POPULAR_GUIDES.value, "guides_popular"),
            (MenuButton.BEGINNER_GUIDES.value, "guides_beginner"),
            (MenuButton.ADVANCED_TECHNIQUES.value, "guides_advanced"),
            (MenuButton.TEAMPLAY_GUIDES.value, "guides_teamplay"),
            (MenuButton.BACK.value, "guides_back")
        ],
        row_width=3
    )

# Меню "Контр-піки" (Inline Keyboard з трьома колонками)
def get_counter_picks_menu():
    return create_inline_menu(
        [
            (MenuButton.COUNTER_SEARCH.value, "counter_search"),
            (MenuButton.COUNTER_LIST.value, "counter_list"),
            (MenuButton.BACK.value, "counter_back")
        ],
        row_width=3
    )

# Меню "Білди" (Inline Keyboard з трьома колонками)
def get_builds_menu():
    return create_inline_menu(
        [
            (MenuButton.CREATE_BUILD.value, "builds_create"),
            (MenuButton.MY_BUILDS.value, "builds_my"),
            (MenuButton.POPULAR_BUILDS.value, "builds_popular"),
            (MenuButton.BACK.value, "builds_back")
        ],
        row_width=3
    )

# Меню "Голосування" (Inline Keyboard з трьома колонками)
def get_voting_menu():
    return create_inline_menu(
        [
            (MenuButton.CURRENT_VOTES.value, "voting_current"),
            (MenuButton.MY_VOTES.value, "voting_my"),
            (MenuButton.SUGGEST_TOPIC.value, "voting_suggest"),
            (MenuButton.BACK.value, "voting_back")
        ],
        row_width=3
    )

# Меню "Профіль" (Inline Keyboard з трьома колонками)
def get_profile_menu():
    return create_inline_menu(
        [
            (MenuButton.ACTIVITY.value, "profile_activity"),
            (MenuButton.RANKING.value, "profile_ranking"),
            (MenuButton.GAME_STATS.value, "profile_game_stats"),
            (MenuButton.BACK.value, "profile_back")
        ],
        row_width=3
    )
