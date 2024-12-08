# keyboards/menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from enum import Enum

def create_reply_keyboard(buttons, row_width=2):
    """
    Допоміжна функція для створення Reply Keyboard Markup.
    :param buttons: Список екземплярів MenuButton.
    :param row_width: Кількість кнопок у рядку.
    :return: Об'єкт ReplyKeyboardMarkup.
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons[i:i + row_width] for i in range(0, len(buttons), row_width)],
        resize_keyboard=True
    )
    return keyboard

def create_inline_keyboard(buttons, row_width=2):
    """
    Допоміжна функція для створення Inline Keyboard Markup.
    :param buttons: Список об'єктів InlineKeyboardButton.
    :param row_width: Кількість кнопок у рядку.
    :return: Об'єкт InlineKeyboardMarkup.
    """
    keyboard = InlineKeyboardMarkup(row_width=row_width)
    keyboard.add(*buttons)
    return keyboard

class MenuButton(Enum):
    # Головне Меню
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Профіль"
    META = "🔥 META"
    M6 = "🏆 M6"
    GPT = "👾 GPT"

    # Навігаційне меню
    HEROES = "🥷 Персонажі"
    GUIDES = "📚 Гайди"
    COUNTER_PICKS = "⚖️ Контр-піки"
    BUILDS = "🛡️ Білди"
    VOTING = "📊 Голосування"
    BACK = "🔙 Назад"

    # Профіль меню
    STATISTICS = "📈 Статистика"
    ACHIEVEMENTS = "🏆 Досягнення"
    SETTINGS = "⚙️ Налаштування"
    FEEDBACK = "💌 Зворотний Зв’язок"
    HELP = "❓ Допомога"
    BACK_TO_MAIN_MENU = "🔙 Меню"

    # Гайди меню
    NEW_GUIDES = "🆕 Нові Гайди"
    POPULAR_GUIDES = "🌟 Топ Гайди"
    BEGINNER_GUIDES = "📘 Новачкам"
    ADVANCED_TECHNIQUES = "🧙 Стратегії гри"
    TEAMPLAY_GUIDES = "🤝 Командна Гра"

    # Контр-піки меню
    COUNTER_SEARCH = "🔎 Пошук Контр-піку"
    COUNTER_LIST = "📝 Список Персонажів"

    # Білди меню
    CREATE_BUILD = "🏗️ Створити Білд"
    MY_BUILDS = "📄 Збережені Білди"
    POPULAR_BUILDS = "🔥 Популярні Білди"

    # Голосування меню
    CURRENT_VOTES = "📍 Поточні Опитування"
    MY_VOTES = "📋 Мої Голосування"
    SUGGEST_TOPIC = "➕ Запропонувати Тему"

    # Статистика меню
    ACTIVITY = "📊 Загальна Активність"
    RANKING = "🥇 Рейтинг"
    GAME_STATS = "🎮 Ігрова Статистика"

    # Досягнення меню
    BADGES = "🎖️ Мої Бейджі"
    PROGRESS = "🚀 Прогрес"
    TOURNAMENT_STATS = "🏅 Турнірна Статистика"
    AWARDS = "🎟️ Отримані Нагороди"

    # Налаштування меню
    LANGUAGE = "🌐 Мова Інтерфейсу"
    CHANGE_USERNAME = "ℹ️ Змінити Username"
    UPDATE_ID = "🆔 Оновити ID"
    NOTIFICATIONS = "🔔 Сповіщення"

# Відповідність кнопок класам героїв (можна розширити за потребою)
menu_button_to_class = {
    MenuButton.HEROES.value: "Навігація",
    MenuButton.PROFILE.value: "Профіль",
    # Додайте відповідність для інших кнопок за потребою
}

# Визначення кнопок меню
MAIN_MENU_BUTTONS = [
    MenuButton.NAVIGATION,
    MenuButton.PROFILE,
    MenuButton.META,
    MenuButton.M6,
    MenuButton.GPT
]

NAVIGATION_MENU_BUTTONS = [
    MenuButton.HEROES,
    MenuButton.GUIDES,
    MenuButton.COUNTER_PICKS,
    MenuButton.BUILDS,
    MenuButton.VOTING,
    MenuButton.BACK
]

PROFILE_MENU_BUTTONS = [
    MenuButton.STATISTICS,
    MenuButton.ACHIEVEMENTS,
    MenuButton.SETTINGS,
    MenuButton.FEEDBACK,
    MenuButton.HELP,
    MenuButton.BACK_TO_MAIN_MENU
]

META_MENU_BUTTONS = [
    MenuButton("📈 Аналітика", "📈 Аналітика"),
    MenuButton("📊 Статистика", "📊 Статистика"),
    MenuButton.BACK_TO_MAIN_MENU
]

M6_MENU_BUTTONS = [
    MenuButton("🏆 Результати", "🏆 Результати"),
    MenuButton("🔍 Деталі", "🔍 Деталі"),
    MenuButton.BACK_TO_MAIN_MENU
]

GPT_MENU_BUTTONS = [
    MenuButton("📝 Задати питання", "📝 Задати питання"),
    MenuButton("❓ Допомога", "❓ Допомога"),
    MenuButton.BACK_TO_MAIN_MENU
]

# Визначення Inline-кнопок
GENERIC_INLINE_BUTTONS = [
    InlineKeyboardButton("MLS Button", callback_data="mls_button"),
    InlineKeyboardButton("🔙 Назад", callback_data="menu_back")
]

INTRO_PAGE_1_BUTTONS = [
    InlineKeyboardButton("Далі", callback_data="intro_next_1")
]

INTRO_PAGE_2_BUTTONS = [
    InlineKeyboardButton("Далі", callback_data="intro_next_2")
]

INTRO_PAGE_3_BUTTONS = [
    InlineKeyboardButton("Розпочати", callback_data="intro_start")
]

# Функції для отримання клавіатур
def get_main_menu():
    return create_reply_keyboard(MAIN_MENU_BUTTONS, row_width=3)

def get_navigation_menu():
    return create_reply_keyboard(NAVIGATION_MENU_BUTTONS, row_width=3)

def get_profile_menu():
    return create_reply_keyboard(PROFILE_MENU_BUTTONS, row_width=3)

def get_meta_menu():
    meta_buttons = [
        MenuButton("📈 Аналітика", "📈 Аналітика"),
        MenuButton("📊 Статистика", "📊 Статистика"),
        MenuButton.BACK_TO_MAIN_MENU
    ]
    return create_reply_keyboard(meta_buttons, row_width=2)

def get_m6_menu():
    m6_buttons = [
        MenuButton("🏆 Результати", "🏆 Результати"),
        MenuButton("🔍 Деталі", "🔍 Деталі"),
        MenuButton.BACK_TO_MAIN_MENU
    ]
    return create_reply_keyboard(m6_buttons, row_width=2)

def get_gpt_menu():
    gpt_buttons = [
        MenuButton("📝 Задати питання", "📝 Задати питання"),
        MenuButton("❓ Допомога", "❓ Допомога"),
        MenuButton.BACK_TO_MAIN_MENU
    ]
    return create_reply_keyboard(gpt_buttons, row_width=2)

def get_generic_inline_keyboard():
    return create_inline_keyboard(GENERIC_INLINE_BUTTONS, row_width=2)

def get_intro_page_1_keyboard():
    return create_inline_keyboard(INTRO_PAGE_1_BUTTONS)

def get_intro_page_2_keyboard():
    return create_inline_keyboard(INTRO_PAGE_2_BUTTONS)

def get_intro_page_3_keyboard():
    return create_inline_keyboard(INTRO_PAGE_3_BUTTONS)

# Функції для спеціальних меню

def get_feedback_menu():
    feedback_buttons = [
        KeyboardButton("✏️ Надіслати Відгук"),
        KeyboardButton("🐛 Повідомити про Помилку"),
        KeyboardButton("🔙 Повернутися до Профілю")
    ]
    return create_reply_keyboard(feedback_buttons, row_width=1)

def get_builds_menu():
    builds_buttons = [
        KeyboardButton("🏗️ Створити Білд"),
        KeyboardButton("📄 Збережені Білди"),
        KeyboardButton("🔥 Популярні Білди"),
        KeyboardButton("🔙 Назад")
    ]
    return create_reply_keyboard(builds_buttons, row_width=2)

def get_voting_menu():
    voting_buttons = [
        KeyboardButton("📍 Поточні Опитування"),
        KeyboardButton("📋 Мої Голосування"),
        KeyboardButton("➕ Запропонувати Тему"),
        KeyboardButton("🔙 Назад")
    ]
    return create_reply_keyboard(voting_buttons, row_width=2)

def get_statistics_menu():
    statistics_buttons = [
        KeyboardButton("📊 Загальна Активність"),
        KeyboardButton("🥇 Рейтинг"),
        KeyboardButton("🎮 Ігрова Статистика"),
        KeyboardButton("🔙 Повернутися до Профілю")
    ]
    return create_reply_keyboard(statistics_buttons, row_width=2)

def get_achievements_menu():
    achievements_buttons = [
        KeyboardButton("🎖️ Мої Бейджі"),
        KeyboardButton("🚀 Прогрес"),
        KeyboardButton("🏅 Турнірна Статистика"),
        KeyboardButton("🎟️ Отримані Нагороди"),
        KeyboardButton("🔙 Повернутися до Профілю")
    ]
    return create_reply_keyboard(achievements_buttons, row_width=2)

def get_settings_menu():
    settings_buttons = [
        KeyboardButton("🌐 Мова Інтерфейсу"),
        KeyboardButton("ℹ️ Змінити Username"),
        KeyboardButton("🆔 Оновити ID"),
        KeyboardButton("🔔 Сповіщення"),
        KeyboardButton("🔙 Повернутися до Профілю")
    ]
    return create_reply_keyboard(settings_buttons, row_width=2)

def get_help_menu():
    help_buttons = [
        KeyboardButton("📄 Інструкції"),
        KeyboardButton("❔ FAQ"),
        KeyboardButton("📞 Підтримка"),
        KeyboardButton("🔙 Повернутися до Профілю")
    ]
    return create_reply_keyboard(help_buttons, row_width=2)

def get_language_keyboard():
    language_buttons = [
        KeyboardButton("🇺🇦 Українська"),
        KeyboardButton("🇬🇧 English"),
        KeyboardButton("🔙 Назад")
    ]
    return create_reply_keyboard(language_buttons, row_width=2)

def get_notifications_keyboard():
    notifications_buttons = [
        KeyboardButton("🔔 Включити Сповіщення"),
        KeyboardButton("🔕 Вимкнути Сповіщення"),
        KeyboardButton("🔙 Назад")
    ]
    return create_reply_keyboard(notifications_buttons, row_width=2)
