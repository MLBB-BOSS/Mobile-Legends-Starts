# keyboards/menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from constants.characters import Characters

MenuButton = {
    'NAVIGATION': KeyboardButton(text='🧭 Навігація'),
    'PROFILE': KeyboardButton(text='🪪 Профіль'),
    'HEROES': KeyboardButton(text='🥷 Персонажі'),
    'GUIDES': KeyboardButton(text='📚 Гайди'),
    'COUNTER_PICKS': KeyboardButton(text='⚖️ Контр-піки'),
    'BUILDS': KeyboardButton(text='🛡️ Білди'),
    'VOTING': KeyboardButton(text='📊 Голосування'),
    'META': KeyboardButton(text='🔥 META'),
    'M6': KeyboardButton(text='🏆 M6'),
    'GPT': KeyboardButton(text='👾 GPT'),
    'BACK': KeyboardButton(text='🔙'),
    'TANK': KeyboardButton(text='🛡️ Танк'),
    'MAGE': KeyboardButton(text='🧙‍♂️ Маг'),
    'MARKSMAN': KeyboardButton(text='🏹 Стрілець'),
    'ASSASSIN': KeyboardButton(text='⚔️ Асасін'),
    'SUPPORT': KeyboardButton(text='❤️ Підтримка'),
    'FIGHTER': KeyboardButton(text='🗡️ Боєць'),
    'COMPARISON': KeyboardButton(text='⚖️ Порівняння'),
    'SEARCH_HERO': KeyboardButton(text='🔎 Пошук'),
    'NEW_GUIDES': KeyboardButton(text='Нові гайди'),
    'POPULAR_GUIDES': KeyboardButton(text='Популярні гайди'),
    'BEGINNER_GUIDES': KeyboardButton(text='Гайди для початківців'),
    'ADVANCED_TECHNIQUES': KeyboardButton(text='Просунуті техніки'),
    'TEAMPLAY_GUIDES': KeyboardButton(text='Командна гра'),
    'COUNTER_SEARCH': KeyboardButton(text='Пошук контр-піку'),
    'COUNTER_LIST': KeyboardButton(text='Список контр-піків'),
    'CREATE_BUILD': KeyboardButton(text='Створення білду'),
    'MY_BUILDS': KeyboardButton(text='Мої білди'),
    'POPULAR_BUILDS': KeyboardButton(text='Популярні білди'),
    'CURRENT_VOTES': KeyboardButton(text='Поточні опитування'),
    'MY_VOTES': KeyboardButton(text='Мої голосування'),
    'SUGGEST_TOPIC': KeyboardButton(text='Пропозиція теми'),
    'SEND_FEEDBACK': KeyboardButton(text='Надіслати відгук'),
    'REPORT_BUG': KeyboardButton(text='Повідомити про помилку'),
    'LANGUAGE': KeyboardButton(text='Мова'),
    'CHANGE_USERNAME': KeyboardButton(text='Змінити Username'),
    'UPDATE_ID': KeyboardButton(text='Оновити ID'),
    'NOTIFICATIONS': KeyboardButton(text='Сповіщення'),
    'INSTRUCTIONS': KeyboardButton(text='Інструкції'),
    'FAQ': KeyboardButton(text='FAQ'),
    'HELP_SUPPORT': KeyboardButton(text='Підтримка'),

    # Додаткові кнопки, що використовуються в меню Профіль, Статистика та Досягнення
    'STATISTICS': KeyboardButton(text='Статистика'),
    'ACHIEVEMENTS': KeyboardButton(text='Досягнення'),
    'SETTINGS': KeyboardButton(text='Налаштування'),
    'FEEDBACK': KeyboardButton(text='Зворотний зв\'язок'),
    'HELP': KeyboardButton(text='Допомога'),

    # Додаткові кнопки для меню Статистика
    'ACTIVITY': KeyboardButton(text='Загальна активність'),
    'RANKING': KeyboardButton(text='Рейтинг'),
    'GAME_STATS': KeyboardButton(text='Ігрова статистика'),

    # Додаткові кнопки для меню Досягнення
    'BADGES': KeyboardButton(text='Бейджі'),
    'PROGRESS': KeyboardButton(text='Прогрес'),
    'TOURNAMENT_STATS': KeyboardButton(text='Турнірна статистика'),
    'AWARDS': KeyboardButton(text='Отримані нагороди'),
}

# Відповідність кнопок класам героїв
menu_button_to_class = {
    "🛡️ Танк": "Танк",
    "🧙‍♂️ Маг": "Маг",
    "🏹 Стрілець": "Стрілець",
    "⚔️ Асасін": "Асасін",
    "❤️ Підтримка": "Підтримка",
    "🗡️ Боєць": "Боєць",
    "🔥 META": "META",
}

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
            [MenuButton['HELP'], MenuButton['BACK']],
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
    # Тут ви можете додати перелік героїв за класом, використовуючи змінну 'hero_class'
    # Для прикладу, просто повертаємо кнопку BACK.
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
            [MenuButton['BACK']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_achievements_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [MenuButton['BADGES'], MenuButton['PROGRESS']],
            [MenuButton['TOURNAMENT_STATS'], MenuButton['AWARDS']],
            [MenuButton['BACK']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_settings_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [MenuButton['LANGUAGE'], MenuButton['CHANGE_USERNAME']],
            [MenuButton['UPDATE_ID'], MenuButton['NOTIFICATIONS']],
            [MenuButton['BACK']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_feedback_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [MenuButton['SEND_FEEDBACK'], MenuButton['REPORT_BUG']],
            [MenuButton['BACK']],
        ],
        resize_keyboard=True
    )
    return keyboard

def get_help_menu():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [MenuButton['INSTRUCTIONS'], MenuButton['FAQ']],
            [MenuButton['HELP_SUPPORT'], MenuButton['BACK']],
        ],
        resize_keyboard=True
    )
    return keyboard
