from enum import Enum
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class MenuButton(Enum):
    # Основне меню
    NAVIGATION = "🔧 Навігація"
    PROFILE = "👤 Профіль"

    # Навігаційне меню
    HEROES = "🦸‍♂️ Персонажі"
    BUILDS = "🔨 Білди"
    COUNTER_PICKS = "🔄 Контр-піки"
    GUIDES = "📚 Гайди"
    VOTING = "🗳️ Голосування"
    M6 = "⚔️ M6"
    GPT = "🤖 GPT"
    META = "📊 META"
    TOURNAMENTS = "🏆 Турніри"
    BACK = "🔙 Назад"

    # Меню Персонажів
    TANK = "🛡️ Танк"
    DAMAGER = "🔥 Дамагер"
    SUPPORT = "💧 Підтримка"

    # Інші кнопки (профіль, статистика тощо)
    STATISTICS = "📈 Статистика"
    ACHIEVEMENTS = "🏅 Досягнення"
    SETTINGS = "⚙️ Налаштування"
    FEEDBACK = "💬 Зворотний зв'язок"
    HELP = "❓ Допомога"
    BACK_TO_MAIN_MENU = "🏠 Головне меню"

    # Меню Статистика
    ACTIVITY = "📊 Активність"
    RANKING = "🏆 Рейтинг"
    GAME_STATS = "🎮 Ігрова Статистика"
    BACK_TO_PROFILE = "🔙 Назад до Профілю"

    # Меню Досягнення
    BADGES = "🏅 Бейджі"
    PROGRESS = "📈 Прогрес"
    TOURNAMENT_STATS = "📊 Турнірна Статистика"
    AWARDS = "🏆 Нагороди"
    BACK_TO_PROFILE_ACHIEVEMENTS = "🔙 Назад до Профілю"

    # Меню Налаштування
    LANGUAGE = "🌐 Мова Інтерфейсу"
    CHANGE_USERNAME = "✏️ Змінити Username"
    UPDATE_ID = "🔢 Оновити ID"
    NOTIFICATIONS = "🔔 Налаштування Сповіщень"
    BACK_TO_PROFILE_SETTINGS = "🔙 Назад до Профілю"

    # Меню Зворотного Зв'язку
    SEND_FEEDBACK = "✉️ Надіслати Відгук"
    REPORT_BUG = "🐞 Повідомити про Помилку"
    BACK_TO_PROFILE_FEEDBACK = "🔙 Назад до Профілю"

    # Меню Допомоги
    INSTRUCTIONS = "📖 Інструкції"
    FAQ = "❓ FAQ"
    HELP_SUPPORT = "🆘 Підтримка"
    BACK_TO_PROFILE_HELP = "🔙 Назад до Профілю"

    # Меню Голосування
    CURRENT_VOTES = "📊 Поточні Опитування"
    MY_VOTES = "✅ Мої Голосування"
    SUGGEST_TOPIC = "💡 Пропозиція Теми"
    BACK_TO_NAVIGATION = "🔙 Назад до Навігації"

    # Меню M6
    M6_TOURNAMENT_INFO = "📋 Інформація про Турніри"
    M6_STATISTICS = "📊 Статистика M6"
    M6_NEWS = "📰 Новини M6"
    BACK_M6 = "🔙 Назад до Навігації"

    # Меню GPT
    GPT_DATA_GENERATION = "📄 Генерація Даних"
    GPT_HINTS = "💡 Поради GPT"
    GPT_HERO_STATISTICS = "📊 Статистика Героїв GPT"
    BACK_GPT = "🔙 Назад до Навігації"

    # Меню META
    META_HERO_LIST = "🦸‍♂️ Перелік Героїв"
    META_RECOMMENDATIONS = "⭐ Рекомендації META"
    META_UPDATE = "🔄 Оновлення META"
    BACK_META = "🔙 Назад до Навігації"

    # Меню Турніри
    CREATE_TOURNAMENT = "🆕 Створити Турнір"
    VIEW_TOURNAMENTS = "👁️‍🗨️ Переглянути Турніри"

# Словник, який мапить кнопки класів героїв до їхніх назв
menu_button_to_class = {
    MenuButton.TANK.value: "Танк",
    MenuButton.DAMAGER.value: "Дамагер",
    MenuButton.SUPPORT.value: "Підтримка",
}

# Функція для клавіатури класів героїв
def get_hero_class_menu(hero_class: str) -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=f"Обрати героя з класу: {hero_class}"),
        KeyboardButton(text=MenuButton.BACK.value)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

# Інші функції меню
def get_main_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.NAVIGATION.value),
        KeyboardButton(text=MenuButton.PROFILE.value)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_navigation_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.HEROES.value),
        KeyboardButton(text=MenuButton.BUILDS.value),
        KeyboardButton(text=MenuButton.COUNTER_PICKS.value),
        KeyboardButton(text=MenuButton.GUIDES.value),
        KeyboardButton(text=MenuButton.VOTING.value),
        KeyboardButton(text=MenuButton.M6.value),
        KeyboardButton(text=MenuButton.GPT.value),
        KeyboardButton(text=MenuButton.META.value),
        KeyboardButton(text=MenuButton.TOURNAMENTS.value)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_heroes_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.TANK.value),
        KeyboardButton(text=MenuButton.DAMAGER.value),
        KeyboardButton(text=MenuButton.SUPPORT.value),
        KeyboardButton(text=MenuButton.BACK.value)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_builds_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text="Створити Білд"),
        KeyboardButton(text="Мої Білди"),
        KeyboardButton(text="Популярні Білди"),
        KeyboardButton(text=MenuButton.BACK.value)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_counter_picks_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text="Пошук Контр-піку"),
        KeyboardButton(text="Список Контр-піків"),
        KeyboardButton(text=MenuButton.BACK.value)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_guides_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text="Нові Гайди"),
        KeyboardButton(text="Популярні Гайди"),
        KeyboardButton(text="Гайди для Початківців"),
        KeyboardButton(text="Розширені Техніки"),
        KeyboardButton(text="Гайди для Командної Гри"),
        KeyboardButton(text=MenuButton.BACK.value)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_voting_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.CURRENT_VOTES.value),
        KeyboardButton(text=MenuButton.MY_VOTES.value),
        KeyboardButton(text=MenuButton.SUGGEST_TOPIC.value),
        KeyboardButton(text=MenuButton.BACK_TO_NAVIGATION.value)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_m6_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.M6_TOURNAMENT_INFO.value),
        KeyboardButton(text=MenuButton.M6_STATISTICS.value),
        KeyboardButton(text=MenuButton.M6_NEWS.value),
        KeyboardButton(text=MenuButton.BACK_M6.value)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_gpt_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.GPT_DATA_GENERATION.value),
        KeyboardButton(text=MenuButton.GPT_HINTS.value),
        KeyboardButton(text=MenuButton.GPT_HERO_STATISTICS.value),
        KeyboardButton(text=MenuButton.BACK_GPT.value)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_meta_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.META_HERO_LIST.value),
        KeyboardButton(text=MenuButton.META_RECOMMENDATIONS.value),
        KeyboardButton(text=MenuButton.META_UPDATE.value),
        KeyboardButton(text=MenuButton.BACK_META.value)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_tournaments_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.CREATE_TOURNAMENT.value),
        KeyboardButton(text=MenuButton.VIEW_TOURNAMENTS.value),
        KeyboardButton(text=MenuButton.BACK.value)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_profile_menu_buttons() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.STATISTICS.value),
        KeyboardButton(text=MenuButton.ACHIEVEMENTS.value),
        KeyboardButton(text=MenuButton.SETTINGS.value),
        KeyboardButton(text=MenuButton.FEEDBACK.value),
        KeyboardButton(text=MenuButton.HELP.value),
        KeyboardButton(text=MenuButton.BACK_TO_MAIN_MENU.value)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_statistics_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.ACTIVITY.value),
        KeyboardButton(text=MenuButton.RANKING.value),
        KeyboardButton(text=MenuButton.GAME_STATS.value),
        KeyboardButton(text=MenuButton.BACK_TO_PROFILE.value)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_achievements_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.BADGES.value),
        KeyboardButton(text=MenuButton.PROGRESS.value),
        KeyboardButton(text=MenuButton.TOURNAMENT_STATS.value),
        KeyboardButton(text=MenuButton.AWARDS.value),
        KeyboardButton(text=MenuButton.BACK.value)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_settings_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.LANGUAGE.value),
        KeyboardButton(text=MenuButton.CHANGE_USERNAME.value),
        KeyboardButton(text=MenuButton.UPDATE_ID.value),
        KeyboardButton(text=MenuButton.NOTIFICATIONS.value),
        KeyboardButton(text=MenuButton.BACK_TO_PROFILE_SETTINGS.value)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_feedback_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.SEND_FEEDBACK.value),
        KeyboardButton(text=MenuButton.REPORT_BUG.value),
        KeyboardButton(text=MenuButton.BACK_TO_PROFILE_FEEDBACK.value)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_help_menu() -> ReplyKeyboardMarkup:
