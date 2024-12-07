# keyboards/menus.py

from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardRemove
)

# Визначення кнопок для Reply Keyboards
MenuButton = {
    # Головне меню
    'NAVIGATION': KeyboardButton(text='🧭 Навігація'),
    'PROFILE': KeyboardButton(text='🪪 Профіль'),
    'META': KeyboardButton(text='🔥 META'),
    'M6': KeyboardButton(text='🏆 M6'),
    'GPT': KeyboardButton(text='👾 GPT'),

    # Інші кнопки...
    'BACK': KeyboardButton(text='🔙 Назад'),
    'BACK_TO_MAIN_MENU': KeyboardButton(text='🔙 Меню'),
}

# Функції для створення Reply Keyboards

def get_main_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [MenuButton['NAVIGATION'], MenuButton['PROFILE']],
            [MenuButton['META'], MenuButton['M6'], MenuButton['GPT']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_meta_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='📈 Аналітика'), KeyboardButton(text='📊 Статистика')],
            [MenuButton['BACK_TO_MAIN_MENU']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_navigation_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='🥷 Персонажі'), KeyboardButton(text='📚 Гайди')],
            [KeyboardButton(text='⚖️ Контр-піки'), KeyboardButton(text='🛡️ Білди')],
            [KeyboardButton(text='📊 Голосування'), MenuButton['BACK']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_profile_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='📈 Дані'), KeyboardButton(text='🏆 Успіхи')],
            [KeyboardButton(text='⚙️ Опції'), KeyboardButton(text='💌 Відгук')],
            [KeyboardButton(text='❓ Питання'), MenuButton['BACK_TO_MAIN_MENU']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_m6_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='🏆 Результати'), KeyboardButton(text='🔍 Деталі')],
            [MenuButton['BACK_TO_MAIN_MENU']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_gpt_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='📝 Задати питання'), KeyboardButton(text='❓ Допомога')],
            [MenuButton['BACK_TO_MAIN_MENU']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_heroes_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='🛡️ Танки'), KeyboardButton(text='🧙‍♂️ Маги'), KeyboardButton(text='🏹 Стрільці')],
            [KeyboardButton(text='⚔️ Асасіни'), KeyboardButton(text='❤️ Сапорти'), KeyboardButton(text='🗡️ Бійці')],
            [KeyboardButton(text='⚖️ Порівняти'), KeyboardButton(text='🔎 Шукати')],
            [MenuButton['BACK']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_hero_class_menu(hero_class: str) -> ReplyKeyboardMarkup:
    # Можна додати додаткові кнопки залежно від обраного класу
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [MenuButton['BACK']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_guides_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='🆕 Нові'), KeyboardButton(text='🌟 Топ')],
            [KeyboardButton(text='📘 Новачкам'), KeyboardButton(text='🧙 Стратегії')],
            [KeyboardButton(text='🤝 Команда'), MenuButton['BACK']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_counter_picks_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='🔎 Шукати'), KeyboardButton(text='📄 Список')],
            [MenuButton['BACK']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_builds_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='🏗️ Новий'), KeyboardButton(text='📄 Збережені')],
            [KeyboardButton(text='🔥 Популярні'), MenuButton['BACK']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_voting_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='📍 Активні'), KeyboardButton(text='📋 Ваші')],
            [KeyboardButton(text='➕ Ідея'), MenuButton['BACK']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_statistics_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='📊 Активність'), KeyboardButton(text='🥇 Рейтинг'), KeyboardButton(text='🎮 Ігри')],
            [MenuButton['BACK_TO_PROFILE']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_achievements_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='🎖️ Бейджі'), KeyboardButton(text='🚀 Прогрес')],
            [KeyboardButton(text='🏅 Турніри'), KeyboardButton(text='🎟️ Нагороди')],
            [MenuButton['BACK_TO_PROFILE']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_settings_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='🌐 Мова'), KeyboardButton(text='ℹ️ Нік')],
            [KeyboardButton(text='🆔 ID'), KeyboardButton(text='🔔 Алєрти')],
            [MenuButton['BACK_TO_PROFILE']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_feedback_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='✏️ Пропозиція'), KeyboardButton(text='🐛 Помилка')],
            [MenuButton['BACK_TO_PROFILE']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_help_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text='📄 Гайд'), KeyboardButton(text='❔ FAQ')],
            [KeyboardButton(text='📞 Контакти'), MenuButton['BACK_TO_PROFILE']],
        ],
        resize_keyboard=True
    )
    return keyboard

# Функції для створення Inline Keyboards

def get_generic_inline_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("MLS Button", callback_data="mls_button"),
        InlineKeyboardButton("🔙 Назад", callback_data="menu_back"),
    ]
    keyboard.add(*buttons)
    return keyboard

def get_intro_page_1_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Далі", callback_data="intro_next_1")
    keyboard.add(button)
    return keyboard

def get_intro_page_2_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Далі", callback_data="intro_next_2")
    keyboard.add(button)
    return keyboard

def get_intro_page_3_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Розпочати", callback_data="intro_start")
    keyboard.add(button)
    return keyboard
