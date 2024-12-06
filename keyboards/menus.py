# keyboards/menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from enum import Enum
import logging

# Налаштування логування
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MenuButton(Enum):
    # Головне Меню
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Мій Профіль"

    # Розділ Навігація
    HEROES = "🥷 Персонажі"
    GUIDES = "📚 Гайди"
    COUNTER_PICKS = "⚖️ Контр-піки"
    BUILDS = "🛡️ Білди"
    VOTING = "📊 Голосування"
    GPT_SUPPORT = "👾 GPT Підтримка"
    M6_ANALYTICS = "🏆 М6 Аналітика"
    META = "🔮 Мета"  # Додано кнопку Мета
    BACK_NAV = "🔙 Назад"  # Назва змінена для консистентності

    # Розділ Персонажі
    TANK = "🛡️ Танк"
    MAGE = "🧙‍♂️ Маг"
    MARKSMAN = "🏹 Стрілець"
    ASSASSIN = "⚔️ Асасін"
    SUPPORT = "❤️ Підтримка"
    FIGHTER = "🗡️ Боєць"
    COMPARE = "⚖️ Порівняння"
    SEARCH_HERO = "🔎 Пошук"

    # Розділ Гайди
    NEW_GUIDES = "🆕 Нові Гайди"
    POPULAR_GUIDES = "🌟 Популярні Гайди"
    BEGINNER_GUIDES = "📘 Для Початківців"
    ADVANCED_TECHNIQUES = "🧙 Стратегії гри"
    TEAMPLAY_GUIDES = "🤝 Командна Гра"

    # Розділ Контр-піки
    COUNTER_SEARCH = "🔎 Пошук Контр-піку"
    COUNTER_LIST = "📝 Список Контр-піків"

    # Розділ Білди
    CREATE_BUILD = "🏗️ Створити Білд"
    MY_BUILDS = "📄 Мої Білди"
    POPULAR_BUILDS = "🔥 Популярні Білди"

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
    BACK_TO_MAIN_MENU = "🔙 Назад до Головного Меню"

    # Підрозділ Статистика
    ACTIVITY = "📊 Загальна Активність"
    RANKING = "🥇 Рейтинг"
    GAME_STATS = "🎮 Ігрова Статистика"
    BACK_TO_PROFILE = "🔙 Назад до Профілю"

    # Підрозділ Досягнення
    BADGES = "🎖️ Мої Бейджі"
    PROGRESS = "🚀 Прогрес"
    TOURNAMENT_STATS = "🏅 Турнірна Статистика"
    AWARDS = "🎟️ Отримані Нагороди"
    BACK_TO_PROFILE_FROM_ACHIEVEMENTS = "🔙 Назад до Профілю"

    # Підрозділ Налаштування
    LANGUAGE = "🌐 Мова Інтерфейсу"
    CHANGE_USERNAME = "ℹ️ Змінити Username"
    UPDATE_ID = "🆔 Оновити ID"
    NOTIFICATIONS = "🔔 Сповіщення"
    BACK_TO_PROFILE_FROM_SETTINGS = "🔙 Назад до Профілю"

    # Підрозділ Зворотний Зв'язок
    SEND_FEEDBACK = "✏️ Надіслати Відгук"
    REPORT_BUG = "🐛 Повідомити про Помилку"
    BACK_TO_PROFILE_FROM_FEEDBACK = "🔙 Назад до Профілю"

    # Підрозділ Допомога
    INSTRUCTIONS = "📄 Інструкції"
    FAQ = "❔ FAQ"
    HELP_SUPPORT = "📞 Підтримка"
    BACK_TO_PROFILE_FROM_HELP = "🔙 Назад до Профілю"


# Відповідність кнопок класам героїв
menu_button_to_class = {
    MenuButton.TANK.value: "Танк",
    MenuButton.MAGE.value: "Маг",
    MenuButton.MARKSMAN.value: "Стрілець",
    MenuButton.ASSASSIN.value: "Асасін",
    MenuButton.SUPPORT.value: "Підтримка",
    MenuButton.FIGHTER.value: "Боєць",
    MenuButton.META.value: "Мета",  # Додано відповідність для Мета
}

# Повний список героїв за класами
heroes_by_class = {
    "Боєць": [
        "Aldous", "Alpha", "Arlott", "Aulus", "Badang", "Balmond",
        "Bane", "Barats", "Dyrroth", "Fredrinn", "Freya", "Guinevere",
        "Jawhead", "Khaleed", "Leomord", "Martis", "Masha", "Minsitthar",
        "Paquito", "Phoveus", "Roger", "Ruby", "Silvanna", "Terizla",
        "Thamuz", "Xborg", "YuZhong", "Zilong"
    ],
    "Танк": [
        "Akai", "Atlas", "Barats", "Baxia", "Belerick", "Chip",
        "Edith", "Esmeralda", "Franco", "Gatotkaca", "Gloo", "Grock",
        "Hilda", "Hylos", "Johnson", "Khufra", "Lolita", "Minotaur",
        "Tigreal", "Uranus"
    ],
    "Асасін": [
        "Alucard", "Aamon", "Arlott", "Benedetta", "Fanny", "Gusion",
        "Hanzo", "Helcurt", "Lancelot", "Ling", "Natalia", "Saber",
        "Selena", "Yin"
    ],
    "Стрілець": [
        "Beatrix", "Brody", "Bruno", "Claude", "Clint", "Granger",
        "Hanabi", "Irithel", "Ixia", "Karrie", "Kimmy", "Layla",
        "Lesley", "Melissa", "Miya", "Moskov", "Natan", "PopolAndKupa",
        "Wanwan", "YiSunShin"
    ],
    "Маг": [
        "Aurora", "Cecilion", "Change", "Cyclops", "Eudora", "Gord",
        "Harith", "Kadita", "Kagura", "Lunox", "LuoYi", "Lylia",
        "Nana", "Odette", "Pharsa", "Vale", "Valentina", "Valir",
        "Vexana", "Xavier", "Yve", "Zhask"
    ],
    "Підтримка": [
        "Angela", "Carmilla", "Diggie", "Estes", "Faramis", "Floryn",
        "Rafaela"
    ],
    "Мета": [
        # Додайте тут Метових персонажів, якщо вони існують
        # Наприклад:
        "MetaHero1", "MetaHero2"
    ],
}

# Загальна функція створення меню
def create_menu(buttons, row_width=3):
    """
    Створює клавіатуру з кнопками.
    :param buttons: Список кнопок (MenuButton або str).
    :param row_width: Кількість кнопок у рядку.
    :return: ReplyKeyboardMarkup
    """
    if not all(isinstance(button, (MenuButton, str)) for button in buttons):
        raise ValueError("Усі елементи повинні бути MenuButton або str.")
    logger.info(f"Створення меню з кнопками: {[button.value if isinstance(button, MenuButton) else button for button in buttons]}")
    keyboard_buttons = [
        KeyboardButton(text=button.value if isinstance(button, MenuButton) else button) for button in buttons
    ]
    keyboard = [
        keyboard_buttons[i:i + row_width] for i in range(0, len(keyboard_buttons), row_width)
    ]
    keyboard.append([KeyboardButton(text="🔙 Назад")])  # Смайлик для повернення
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Функції для отримання конкретних меню
def get_main_menu():
    return create_menu([MenuButton.NAVIGATION, MenuButton.PROFILE])

def get_navigation_menu():
    return create_menu([
        MenuButton.HEROES, MenuButton.BUILDS, MenuButton.COUNTER_PICKS,
        MenuButton.GUIDES, MenuButton.VOTING, MenuButton.GPT_SUPPORT,
        MenuButton.M6_ANALYTICS, MenuButton.META  # Додано кнопку Мета
    ])

def get_heroes_menu():
    return create_menu([
        MenuButton.TANK, MenuButton.MAGE, MenuButton.MARKSMAN,
        MenuButton.ASSASSIN, MenuButton.SUPPORT, MenuButton.FIGHTER,
        MenuButton.COMPARE, MenuButton.SEARCH_HERO
    ])

def get_hero_class_menu(hero_class):
    heroes = heroes_by_class.get(hero_class, [])
    buttons = [MenuButton(hero) if hero in MenuButton.__members__ else hero for hero in heroes]
    # Створюємо кнопки для героїв
    keyboard_buttons = [
        KeyboardButton(text=hero) for hero in heroes
    ]
    # Розбиваємо кнопки на рядки по 3
    keyboard = [keyboard_buttons[i:i + 3] for i in range(0, len(keyboard_buttons), 3)]
    # Додаємо кнопку назад
    keyboard.append([KeyboardButton(text="🔙 Назад")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_guides_menu():
    return create_menu([
        MenuButton.NEW_GUIDES, MenuButton.POPULAR_GUIDES,
        MenuButton.BEGINNER_GUIDES, MenuButton.ADVANCED_TECHNIQUES,
        MenuButton.TEAMPLAY_GUIDES
    ])

def get_counter_picks_menu():
    return create_menu([
        MenuButton.COUNTER_SEARCH, MenuButton.COUNTER_LIST
    ])

def get_builds_menu():
    return create_menu([
        MenuButton.CREATE_BUILD, MenuButton.MY_BUILDS, MenuButton.POPULAR_BUILDS
    ])

def get_voting_menu():
    return create_menu([
        MenuButton.CURRENT_VOTES, MenuButton.MY_VOTES, MenuButton.SUGGEST_TOPIC
    ])

def get_profile_menu():
    return create_menu([
        MenuButton.STATISTICS, MenuButton.ACHIEVEMENTS,
        MenuButton.SETTINGS, MenuButton.FEEDBACK, MenuButton.HELP
    ])

def get_statistics_menu():
    return create_menu([
        MenuButton.ACTIVITY, MenuButton.RANKING, MenuButton.GAME_STATS
    ])

def get_achievements_menu():
    return create_menu([
        MenuButton.BADGES, MenuButton.PROGRESS,
        MenuButton.TOURNAMENT_STATS, MenuButton.AWARDS
    ])

def get_settings_menu():
    return create_menu([
        MenuButton.LANGUAGE, MenuButton.CHANGE_USERNAME,
        MenuButton.UPDATE_ID, MenuButton.NOTIFICATIONS
    ])

def get_feedback_menu():
    return create_menu([
        MenuButton.SEND_FEEDBACK, MenuButton.REPORT_BUG
    ])

def get_help_menu():
    return create_menu([
        MenuButton.INSTRUCTIONS, MenuButton.FAQ, MenuButton.HELP_SUPPORT
    ])
