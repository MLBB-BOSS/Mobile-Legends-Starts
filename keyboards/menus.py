# keyboards.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

# Визначення кнопок для Reply Keyboards
MenuButton = {
    # Головне меню
    'NAVIGATION': KeyboardButton(text='🧭 Навігація'),
    'PROFILE': KeyboardButton(text='🪪 Профіль'),
    'META': KeyboardButton(text='🔥 META'),
    'M6': KeyboardButton(text='🏆 M6'),
    'GPT': KeyboardButton(text='👾 GPT'),

    # Розділ Навігація
    'HEROES': KeyboardButton(text='🥷 Персонажі'),
    'GUIDES': KeyboardButton(text='📚 Гайди'),
    'COUNTER_PICKS': KeyboardButton(text='⚖️ Контр-піки'),
    'BUILDS': KeyboardButton(text='🛡️ Білди'),
    'VOTING': KeyboardButton(text='📊 Голосування'),
    'BACK': KeyboardButton(text='🔙 Назад'),

    # Розділ Персонажі
    'TANK': KeyboardButton(text='🛡️ Танки'),
    'MAGE': KeyboardButton(text='🧙‍♂️ Маги'),
    'MARKSMAN': KeyboardButton(text='🏹 Стрільці'),
    'ASSASSIN': KeyboardButton(text='⚔️ Асасіни'),
    'SUPPORT': KeyboardButton(text='❤️ Сапорти'),
    'FIGHTER': KeyboardButton(text='🗡️ Бійці'),
    'COMPARISON': KeyboardButton(text='⚖️ Порівняти'),
    'SEARCH_HERO': KeyboardButton(text='🔎 Шукати'),

    # Розділ Гайди
    'NEW_GUIDES': KeyboardButton(text='🆕 Нові'),
    'POPULAR_GUIDES': KeyboardButton(text='🌟 Топ'),
    'BEGINNER_GUIDES': KeyboardButton(text='📘 Новачкам'),
    'ADVANCED_TECHNIQUES': KeyboardButton(text='🧙 Стратегії'),
    'TEAMPLAY_GUIDES': KeyboardButton(text='🤝 Команда'),

    # Розділ Контр-піки
    'COUNTER_SEARCH': KeyboardButton(text='🔎 Шукати'),
    'COUNTER_LIST': KeyboardButton(text='📄 Список'),

    # Розділ Білди
    'CREATE_BUILD': KeyboardButton(text='🏗️ Новий'),
    'MY_BUILDS': KeyboardButton(text='📄 Збережені'),
    'POPULAR_BUILDS': KeyboardButton(text='🔥 Популярні'),

    # Розділ Голосування
    'CURRENT_VOTES': KeyboardButton(text='📍 Активні'),
    'MY_VOTES': KeyboardButton(text='📋 Ваші'),
    'SUGGEST_TOPIC': KeyboardButton(text='➕ Ідея'),

    # Розділ Профіль
    'STATISTICS': KeyboardButton(text='📈 Дані'),
    'ACHIEVEMENTS': KeyboardButton(text='🏆 Успіхи'),
    'SETTINGS': KeyboardButton(text='⚙️ Опції'),
    'FEEDBACK': KeyboardButton(text='💌 Відгук'),
    'HELP': KeyboardButton(text='❓ Питання'),
    'BACK_TO_MAIN_MENU': KeyboardButton(text='🔙 Меню'),

    # Підрозділ Статистика
    'ACTIVITY': KeyboardButton(text='📊 Активність'),
    'RANKING': KeyboardButton(text='🥇 Рейтинг'),
    'GAME_STATS': KeyboardButton(text='🎮 Ігри'),
    'BACK_TO_PROFILE': KeyboardButton(text='🔙 Назад'),

    # Підрозділ Досягнення
    'BADGES': KeyboardButton(text='🎖️ Бейджі'),
    'PROGRESS': KeyboardButton(text='🚀 Прогрес'),
    'TOURNAMENT_STATS': KeyboardButton(text='🏅 Турніри'),
    'AWARDS': KeyboardButton(text='🎟️ Нагороди'),

    # Підрозділ Налаштування
    'LANGUAGE': KeyboardButton(text='🌐 Мова'),
    'CHANGE_USERNAME': KeyboardButton(text='ℹ️ Нік'),
    'UPDATE_ID': KeyboardButton(text='🆔 ID'),
    'NOTIFICATIONS': KeyboardButton(text='🔔 Алєрти'),

    # Підрозділ Зворотний Зв'язок
    'SEND_FEEDBACK': KeyboardButton(text='✏️ Пропозиція'),
    'REPORT_BUG': KeyboardButton(text='🐛 Помилка'),

    # Підрозділ Допомога
    'INSTRUCTIONS': KeyboardButton(text='📄 Гайд'),
    'FAQ': KeyboardButton(text='❔ FAQ'),
    'HELP_SUPPORT': KeyboardButton(text='📞 Контакти'),
}

# Функції для створення Reply Keyboards

def get_main_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [MenuButton['NAVIGATION'], MenuButton['PROFILE']],
            [MenuButton['META'], MenuButton['M6'], MenuButton['GPT']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_navigation_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [MenuButton['HEROES'], MenuButton['GUIDES']],
            [MenuButton['COUNTER_PICKS'], MenuButton['BUILDS']],
            [MenuButton['VOTING'], MenuButton['BACK']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_profile_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [MenuButton['STATISTICS'], MenuButton['ACHIEVEMENTS']],
            [MenuButton['SETTINGS'], MenuButton['FEEDBACK']],
            [MenuButton['HELP'], MenuButton['BACK_TO_MAIN_MENU']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_heroes_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [MenuButton['TANK'], MenuButton['MAGE'], MenuButton['MARKSMAN']],
            [MenuButton['ASSASSIN'], MenuButton['SUPPORT'], MenuButton['FIGHTER']],
            [MenuButton['COMPARISON'], MenuButton['SEARCH_HERO']],
            [MenuButton['BACK']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_hero_class_menu(hero_class: str):
    # Можна додати додаткові кнопки залежно від обраного класу
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [MenuButton['BACK']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_guides_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [MenuButton['NEW_GUIDES'], MenuButton['POPULAR_GUIDES']],
            [MenuButton['BEGINNER_GUIDES'], MenuButton['ADVANCED_TECHNIQUES']],
            [MenuButton['TEAMPLAY_GUIDES'], MenuButton['BACK']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_counter_picks_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [MenuButton['COUNTER_SEARCH'], MenuButton['COUNTER_LIST']],
            [MenuButton['BACK']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_builds_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [MenuButton['CREATE_BUILD'], MenuButton['MY_BUILDS']],
            [MenuButton['POPULAR_BUILDS'], MenuButton['BACK']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_voting_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [MenuButton['CURRENT_VOTES'], MenuButton['MY_VOTES']],
            [MenuButton['SUGGEST_TOPIC'], MenuButton['BACK']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_statistics_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [MenuButton['ACTIVITY'], MenuButton['RANKING'], MenuButton['GAME_STATS']],
            [MenuButton['BACK_TO_PROFILE']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_achievements_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [MenuButton['BADGES'], MenuButton['PROGRESS']],
            [MenuButton['TOURNAMENT_STATS'], MenuButton['AWARDS']],
            [MenuButton['BACK_TO_PROFILE']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_settings_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [MenuButton['LANGUAGE'], MenuButton['CHANGE_USERNAME']],
            [MenuButton['UPDATE_ID'], MenuButton['NOTIFICATIONS']],
            [MenuButton['BACK_TO_PROFILE']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_feedback_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [MenuButton['SEND_FEEDBACK'], MenuButton['REPORT_BUG']],
            [MenuButton['BACK_TO_PROFILE']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_help_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [MenuButton['INSTRUCTIONS'], MenuButton['FAQ']],
            [MenuButton['HELP_SUPPORT'], MenuButton['BACK_TO_PROFILE']],
        ],
        resize_keyboard=True
    )
    return keyboard

# Функції для створення Inline Keyboards

def get_generic_inline_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("MLS Button", callback_data="mls_button"),
        InlineKeyboardButton("🔙 Назад", callback_data="menu_back"),
    ]
    keyboard.add(*buttons)
    return keyboard

def get_intro_page_1_keyboard():
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Далі", callback_data="intro_next_1")
    keyboard.add(button)
    return keyboard

def get_intro_page_2_keyboard():
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Далі", callback_data="intro_next_2")
    keyboard.add(button)
    return keyboard

def get_intro_page_3_keyboard():
    keyboard = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Розпочати", callback_data="intro_start")
    keyboard.add(button)
    return keyboard
