# keyboard/menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def create_reply_keyboard(buttons, row_width=2):
    """
    Допоміжна функція для створення Reply Keyboard Markup.
    :param buttons: Список текстів кнопок.
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

# Визначення кнопок меню
MAIN_MENU_BUTTONS = [
    KeyboardButton("🧭 Навігація"),
    KeyboardButton("🪪 Профіль")
]

NAVIGATION_MENU_BUTTONS = [
    KeyboardButton("🥷 Персонажі"),
    KeyboardButton("📚 Гайди"),
    KeyboardButton("⚖️ Контр-піки"),
    KeyboardButton("🛡️ Білди"),
    KeyboardButton("📊 Голосування"),
    KeyboardButton("🔥 META"),
    KeyboardButton("🏆 M6"),
    KeyboardButton("👾 GPT"),
    KeyboardButton("🔙 Назад")
]

PROFILE_MENU_BUTTONS = [
    KeyboardButton("📈 Статистика"),
    KeyboardButton("🏆 Досягнення"),
    KeyboardButton("⚙️ Налаштування"),
    KeyboardButton("💌 Зворотний Зв’язок"),
    KeyboardButton("❓ Допомога"),
    KeyboardButton("🔙 Меню")
]

META_MENU_BUTTONS = [
    KeyboardButton("📈 Аналітика"),
    KeyboardButton("📊 Статистика"),
    KeyboardButton("🔙 Меню")
]

M6_MENU_BUTTONS = [
    KeyboardButton("🏆 Результати"),
    KeyboardButton("🔍 Деталі"),
    KeyboardButton("🔙 Меню")
]

GPT_MENU_BUTTONS = [
    KeyboardButton("📝 Задати питання"),
    KeyboardButton("❓ Допомога"),
    KeyboardButton("🔙 Меню")
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
    return create_reply_keyboard(MAIN_MENU_BUTTONS)

def get_navigation_menu():
    return create_reply_keyboard(NAVIGATION_MENU_BUTTONS)

def get_profile_menu():
    return create_reply_keyboard(PROFILE_MENU_BUTTONS)

def get_meta_menu():
    return create_reply_keyboard(META_MENU_BUTTONS)

def get_m6_menu():
    return create_reply_keyboard(M6_MENU_BUTTONS)

def get_gpt_menu():
    return create_reply_keyboard(GPT_MENU_BUTTONS)

# Функції для отримання Inline-клавіатур
def get_generic_inline_keyboard():
    return create_inline_keyboard(GENERIC_INLINE_BUTTONS)

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
