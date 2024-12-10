#keyboards/menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from constants.characters import Characters

MenuButton = {
    'NAVIGATION': KeyboardButton('🧭 Навігація'),
    'PROFILE': KeyboardButton('🪪 Профіль'),
    'HEROES': KeyboardButton('🥷 Персонажі'),
    'GUIDES': KeyboardButton('📚 Гайди'),
    'COUNTER_PICKS': KeyboardButton('⚖️ Контр-піки'),
    'BUILDS': KeyboardButton('🛡️ Білди'),
    'VOTING': KeyboardButton('📊 Голосування'),
    'META': KeyboardButton('🔥 META'),
    'M6': KeyboardButton('🏆 M6'),
    'GPT': KeyboardButton('👾 GPT'),
    'BACK': KeyboardButton('🔙'),
    'TANK': KeyboardButton('🛡️ Танк'),
    'MAGE': KeyboardButton('🧙‍♂️ Маг'),
    'MARKSMAN': KeyboardButton('🏹 Стрілець'),
    'ASSASSIN': KeyboardButton('⚔️ Асасін'),
    'SUPPORT': KeyboardButton('❤️ Підтримка'),
    'FIGHTER': KeyboardButton('🗡️ Боєць'),
    'COMPARISON': KeyboardButton('⚖️ Порівняння'),
    'SEARCH_HERO': KeyboardButton('🔎 Пошук'),
    'NEW_GUIDES': KeyboardButton('Нові гайди'),
    'POPULAR_GUIDES': KeyboardButton('Популярні гайди'),
    'BEGINNER_GUIDES': KeyboardButton('Гайди для початківців'),
    'ADVANCED_TECHNIQUES': KeyboardButton('Просунуті техніки'),
    'TEAMPLAY_GUIDES': KeyboardButton('Командна гра'),
    'COUNTER_SEARCH': KeyboardButton('Пошук контр-піку'),
    'COUNTER_LIST': KeyboardButton('Список контр-піків'),
    'CREATE_BUILD': KeyboardButton('Створення білду'),
    'MY_BUILDS': KeyboardButton('Мої білди'),
    'POPULAR_BUILDS': KeyboardButton('Популярні білди'),
    'CURRENT_VOTES': KeyboardButton('Поточні опитування'),
    'MY_VOTES': KeyboardButton('Мої голосування'),
    'SUGGEST_TOPIC': KeyboardButton('Пропозиція теми'),
    'SEND_FEEDBACK': KeyboardButton('Надіслати відгук'),
    'REPORT_BUG': KeyboardButton('Повідомити про помилку'),
    'LANGUAGE': KeyboardButton('Мова'),
    'CHANGE_USERNAME': KeyboardButton('Змінити Username'),
    'UPDATE_ID': KeyboardButton('Оновити ID'),
    'NOTIFICATIONS': KeyboardButton('Сповіщення'),
    'INSTRUCTIONS': KeyboardButton('Інструкції'),
    'FAQ': KeyboardButton('FAQ'),
    'HELP_SUPPORT': KeyboardButton('Підтримка'),
    # Додайте інші кнопки за потребою
}

# Функції для створення меню

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