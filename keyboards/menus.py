# keyboards/menus.py

import logging
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

logger = logging.getLogger(__name__)

class MenuButton:
    # Головне меню
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Мій Профіль"
    
    # Меню Навігації
    HEROES = "🥷 Персонажі"
    BUILDS = "🛡️ Білди"
    COUNTER_PICKS = "⚖️ Контр-піки"
    GUIDES = "📚 Гайди"
    VOTING = "📊 Голосування"
    M6 = "🏆 M6"
    GPT = "👾 GPT"
    META = "🔥 META"
    TOURNAMENTS = "🏆 Турніри"
    BACK_NAVIGATION = "🔙 Назад"
    
    # Меню Профілю
    STATISTICS = "📈 Статистика"
    ACHIEVEMENTS = "🏆 Досягнення"
    SETTINGS = "⚙️ Налаштування"
    FEEDBACK = "💌 Зворотний Зв'язок"
    HELP = "❓ Допомога"
    BACK_TO_MAIN_MENU = "🔙 Назад до Головного Меню"
    
    # Підменю Статистики
    OVERALL_ACTIVITY = "📊 Загальна Активність"
    RATING = "🥇 Рейтинг"
    GAME_STATISTICS = "🎮 Ігрова Статистика"
    BACK_STATISTICS = "🔙 Назад"
    
    # Підменю Досягнень
    MY_BADGES = "🎖️ Мої Бейджі"
    PROGRESS = "🚀 Прогрес"
    TOURNAMENT_STATS = "🏅 Турнірна Статистика"
    RECEIVED_AWARDS = "🎟️ Отримані Нагороди"
    BACK_ACHIEVEMENTS = "🔙 Назад"
    
    # Підменю Налаштувань
    INTERFACE_LANGUAGE = "🌐 Мова Інтерфейсу"
    CHANGE_USERNAME = "ℹ️ Змінити Username"
    UPDATE_ID = "🆔 Оновити ID"
    NOTIFICATIONS = "🔔 Сповіщення"
    BACK_SETTINGS = "🔙 Назад"
    
    # Підменю Зворотного Зв'язку
    SEND_FEEDBACK = "✏️ Надіслати Відгук"
    REPORT_BUG = "🐛 Повідомити про Помилку"
    BACK_FEEDBACK = "🔙 Назад"
    
    # Підменю Допомоги
    INSTRUCTIONS = "📄 Інструкції"
    FAQ = "❔ FAQ"
    SUPPORT = "📞 Підтримка"
    BACK_HELP = "🔙 Назад"
    
    # Підменю Персонажів
    TANK = "🛡️ Танк"
    MAGE = "🧙‍♂️ Маг"
    ARCHER = "🏹 Стрілець"
    ASSASSIN = "⚔️ Асасін"
    SUPPORT = "❤️ Підтримка"
    FIGHTER = "🗡️ Боєць"
    COMPARISON = "⚖️ Порівняння"
    SEARCH_HERO = "🔎 Пошук"
    BACK_HEROES = "🔙 Назад"
    
    # Підменю Білд
    CREATE_BUILD = "🏗️ Створити"
    SELECTED_BUILDS = "📄 Обрані"
    POPULAR_BUILDS = "🔥 Популярні"
    BACK_BUILDS = "🔙 Назад"
    
    # Підменю Контр-піків
    SEARCH_COUNTER = "🔎 Пошук"
    HERO_LIST_COUNTER = "📝 Список Персонажів"
    BACK_COUNTER_PICKS = "🔙 Назад"
    
    # Підменю Гайд
    NEW_GUIDES = "🆕 Нові Гайди"
    TOP_GUIDES = "🌟 Топ Гайди"
    BEGINNER_GUIDES = "📘 Для Початківців"
    GAME_STRATEGIES = "🧙 Стратегії гри"
    TEAM_PLAY_GUIDES = "🤝 Командна Гра"
    BACK_GUIDES = "🔙 Назад"
    
    # Підменю Голосування
    CURRENT_POLLS = "📍 Поточні Опитування"
    MY_VOTINGS = "📋 Мої Голосування"
    SUGGEST_TOPIC = "➕ Запропонувати Тему"
    BACK_VOTING = "🔙 Назад"
    
    # Підменю M6
    M6_TOURNAMENT_INFO = "🏆 Турнірна Інформація"
    M6_STATISTICS = "📈 Статистика M6"
    M6_NEWS = "📰 Новини M6"
    BACK_M6 = "🔙 Назад"
    
    # Підменю GPT
    GPT_DATA_GENERATION = "🤖 Генерація Даних"
    GPT_HINTS = "📝 Підказки"
    GPT_HERO_STATISTICS = "📊 Статистика Героїв"
    BACK_GPT = "🔙 Назад"
    
    # Підменю META
    META_HERO_LIST = "📋 Список Героїв у Мету"
    META_RECOMMENDATIONS = "🌟 Рекомендації"
    META_UPDATE = "🔄 Оновлення Мети"
    BACK_META = "🔙 Назад"
    
    # Підменю Турнірів
    CREATE_TOURNAMENT = "🆕 Створити Турнір"
    VIEW_TOURNAMENTS = "📋 Переглянути Турніри"
    BACK_TOURNAMENTS = "🔙 Назад"
    
    # Сторінка пошуку героя або теми
    BACK_SEARCH = "🔙 Назад до Персонажів"
    
    # Загальні кнопки
    BACK_TO_NAVIGATION = "🔙 Назад до Меню Навігації"
    BACK_TO_PROFILE = "🔙 Назад до Меню Профілю"

# Функції для створення клавіатур

def get_main_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=MenuButton.NAVIGATION), KeyboardButton(text=MenuButton.PROFILE)]
    ]
    logger.info(f"Створення головного меню з кнопками: {[button.text for row in keyboard for button in row]}")
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_navigation_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=MenuButton.HEROES),
         KeyboardButton(text=MenuButton.BUILDS)],
        [KeyboardButton(text=MenuButton.COUNTER_PICKS),
         KeyboardButton(text=MenuButton.GUIDES)],
        [KeyboardButton(text=MenuButton.VOTING),
         KeyboardButton(text=MenuButton.M6)],
        [KeyboardButton(text=MenuButton.GPT),
         KeyboardButton(text=MenuButton.META)],
        [KeyboardButton(text=MenuButton.TOURNAMENTS),
         KeyboardButton(text=MenuButton.BACK_NAVIGATION)]
    ]
    logger.info(f"Створення меню навігації з кнопками: {[button.text for row in keyboard for button in row]}")
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_profile_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=MenuButton.STATISTICS),
         KeyboardButton(text=MenuButton.ACHIEVEMENTS)],
        [KeyboardButton(text=MenuButton.SETTINGS),
         KeyboardButton(text=MenuButton.FEEDBACK)],
        [KeyboardButton(text=MenuButton.HELP),
         KeyboardButton(text=MenuButton.BACK_TO_MAIN_MENU)]
    ]
    logger.info(f"Створення меню профілю з кнопками: {[button.text for row in keyboard for button in row]}")
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_statistics_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=MenuButton.OVERALL_ACTIVITY),
         KeyboardButton(text=MenuButton.RATING)],
        [KeyboardButton(text=MenuButton.GAME_STATISTICS),
         KeyboardButton(text=MenuButton.BACK_STATISTICS)]
    ]
    logger.info(f"Створення меню статистики з кнопками: {[button.text for row in keyboard for button in row]}")
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_achievements_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=MenuButton.MY_BADGES),
         KeyboardButton(text=MenuButton.PROGRESS)],
        [KeyboardButton(text=MenuButton.TOURNAMENT_STATS),
         KeyboardButton(text=MenuButton.RECEIVED_AWARDS)],
        [KeyboardButton(text=MenuButton.BACK_ACHIEVEMENTS)]
    ]
    logger.info(f"Створення меню досягнень з кнопками: {[button.text for row in keyboard for button in row]}")
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_settings_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=MenuButton.INTERFACE_LANGUAGE),
         KeyboardButton(text=MenuButton.CHANGE_USERNAME)],
        [KeyboardButton(text=MenuButton.UPDATE_ID),
         KeyboardButton(text=MenuButton.NOTIFICATIONS)],
        [KeyboardButton(text=MenuButton.BACK_SETTINGS)]
    ]
    logger.info(f"Створення меню налаштувань з кнопками: {[button.text for row in keyboard for button in row]}")
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_feedback_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=MenuButton.SEND_FEEDBACK),
         KeyboardButton(text=MenuButton.REPORT_BUG)],
        [KeyboardButton(text=MenuButton.BACK_FEEDBACK)]
    ]
    logger.info(f"Створення меню зворотного зв'язку з кнопками: {[button.text for row in keyboard for button in row]}")
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_help_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=MenuButton.INSTRUCTIONS),
         KeyboardButton(text=MenuButton.FAQ)],
        [KeyboardButton(text=MenuButton.SUPPORT),
         KeyboardButton(text=MenuButton.BACK_HELP)]
    ]
    logger.info(f"Створення меню допомоги з кнопками: {[button.text for row in keyboard for button in row]}")
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_heroes_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=MenuButton.TANK),
         KeyboardButton(text=MenuButton.MAGE),
         KeyboardButton(text=MenuButton.ARCHER)],
        [KeyboardButton(text=MenuButton.ASSASSIN),
         KeyboardButton(text=MenuButton.SUPPORT),
         KeyboardButton(text=MenuButton.FIGHTER)],
        [KeyboardButton(text=MenuButton.COMPARISON),
         KeyboardButton(text=MenuButton.SEARCH_HERO)],
        [KeyboardButton(text=MenuButton.BACK_HEROES)]
    ]
    logger.info(f"Створення меню Персонажів з кнопками: {[button.text for row in keyboard for button in row]}")
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_builds_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=MenuButton.CREATE_BUILD),
         KeyboardButton(text=MenuButton.SELECTED_BUILDS)],
        [KeyboardButton(text=MenuButton.POPULAR_BUILDS),
         KeyboardButton(text=MenuButton.BACK_BUILDS)]
    ]
    logger.info(f"Створення меню Білди з кнопками: {[button.text for row in keyboard for button in row]}")
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_counter_picks_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=MenuButton.SEARCH_COUNTER),
         KeyboardButton(text=MenuButton.HERO_LIST_COUNTER)],
        [KeyboardButton(text=MenuButton.BACK_COUNTER_PICKS)]
    ]
    logger.info(f"Створення меню Контр-піків з кнопками: {[button.text for row in keyboard for button in row]}")
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_guides_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=MenuButton.NEW_GUIDES),
         KeyboardButton(text=MenuButton.TOP_GUIDES)],
        [KeyboardButton(text=MenuButton.BEGINNER_GUIDES),
         KeyboardButton(text=MenuButton.GAME_STRATEGIES)],
        [KeyboardButton(text=MenuButton.TEAM_PLAY_GUIDES),
         KeyboardButton(text=MenuButton.BACK_GUIDES)]
    ]
    logger.info(f"Створення меню Гайди з кнопками: {[button.text for row in keyboard for button in row]}")
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_voting_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=MenuButton.CURRENT_POLLS),
         KeyboardButton(text=MenuButton.MY_VOTINGS)],
        [KeyboardButton(text=MenuButton.SUGGEST_TOPIC),
         KeyboardButton(text=MenuButton.BACK_VOTING)]
    ]
    logger.info(f"Створення меню Голосування з кнопками: {[button.text for row in keyboard for button in row]}")
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_m6_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=MenuButton.M6_TOURNAMENT_INFO),
         KeyboardButton(text=MenuButton.M6_STATISTICS)],
        [KeyboardButton(text=MenuButton.M6_NEWS),
         KeyboardButton(text=MenuButton.BACK_M6)]
    ]
    logger.info(f"Створення меню M6 з кнопками: {[button.text for row in keyboard for button in row]}")
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_gpt_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=MenuButton.GPT_DATA_GENERATION),
         KeyboardButton(text=MenuButton.GPT_HINTS)],
        [KeyboardButton(text=MenuButton.GPT_HERO_STATISTICS),
         KeyboardButton(text=MenuButton.BACK_GPT)]
    ]
    logger.info(f"Створення меню GPT з кнопками: {[button.text for row in keyboard for button in row]}")
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_meta_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=MenuButton.META_HERO_LIST),
         KeyboardButton(text=MenuButton.META_RECOMMENDATIONS)],
        [KeyboardButton(text=MenuButton.META_UPDATE),
         KeyboardButton(text=MenuButton.BACK_META)]
    ]
    logger.info(f"Створення меню META з кнопками: {[button.text for row in keyboard for button in row]}")
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_tournaments_menu() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text=MenuButton.CREATE_TOURNAMENT),
         KeyboardButton(text=MenuButton.VIEW_TOURNAMENTS)],
        [KeyboardButton(text=MenuButton.BACK_TOURNAMENTS)]
    ]
    logger.info(f"Створення меню Турнірів з кнопками: {[button.text for row in keyboard for button in row]}")
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_hero_class_menu(hero_class: str) -> ReplyKeyboardMarkup:
    # Приклад для класу Танк. Повторіть для інших класів, додаючи відповідні героїв.
    heroes = {
        "Танк": [
            "Alice",
            "Tigreal",
            "Akai",
            "Franco",
            "Minotaur",
            "Lolia",
            "Gatotkaca",
            "Grock",
            "Hylos",
            "Uranus",
            "Belerick",
            "Khufra",
            "Esmeralda",
            "Terizla",
            "Baxia",
            "Masha",
            "Atlas",
            "Barats",
            "Edith",
            "Fredrinn",
            "Johnson",
            "Hilda",
            "Carmilla",
            "Gloo",
            "Chip"
        ],
        "Маг": [
            "Lancelot",
            "Eudora",
            "Layla",
            "Valir",
            "Kaja",
            "Cyclops",
            "Harith",
            "Nana",
            "Esmeralda",
            "Pharsa",
            "Alice",
            "Kimmy",
            "Yve",
            "Harith",
            "Jawhead",
            "Paquito",
            "Kadita",
            "Vale",
            "Alucard",
            "Ruby",
            "Valir",
            "Ruby",
            "Franco",
            "Layla",
            "Yve"
            # Додайте інших магів
        ],
        # Додайте інші класи героїв з їхніми іменами
    }

    hero_list = heroes.get(hero_class, [])
    keyboard = []
    row = []
    for idx, hero in enumerate(hero_list, 1):
        row.append(KeyboardButton(text=hero))
        if idx % 3 == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    keyboard.append([KeyboardButton(text=MenuButton.BACK_HEROES)])

    logger.info(f"Створення меню класу героя '{hero_class}' з кнопками: {[button.text for row in keyboard for button in row]}")
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_generic_inline_keyboard() -> ReplyKeyboardMarkup:
    # Ця функція повинна бути визначена у вашому файлі inline_menus.py
    # Тут наведено простий приклад
    keyboard = [
        [KeyboardButton(text="🔄 Оновити")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Додайте інші функції для створення клавіатур відповідно до вашого меню