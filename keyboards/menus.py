# keyboards/menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class MenuButton:
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

    # Меню Профіль
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
    BACK_TO_PROFILE = "🔙 Назад до Профілю"

    # Меню Налаштування
    LANGUAGE = "🌐 Мова Інтерфейсу"
    CHANGE_USERNAME = "✏️ Змінити Username"
    UPDATE_ID = "🔢 Оновити ID"
    NOTIFICATIONS = "🔔 Налаштування Сповіщень"
    BACK_TO_PROFILE = "🔙 Назад до Профілю"

    # Меню Зворотного Зв'язку
    SEND_FEEDBACK = "✉️ Надіслати Відгук"
    REPORT_BUG = "🐞 Повідомити про Помилку"
    BACK_TO_PROFILE = "🔙 Назад до Профілю"

    # Меню Допомоги
    INSTRUCTIONS = "📖 Інструкції"
    FAQ = "❓ FAQ"
    HELP_SUPPORT = "🆘 Підтримка"
    BACK_TO_PROFILE = "🔙 Назад до Профілю"

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

def get_main_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.NAVIGATION),
        KeyboardButton(text=MenuButton.PROFILE)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_navigation_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.HEROES),
        KeyboardButton(text=MenuButton.BUILDS),
        KeyboardButton(text=MenuButton.COUNTER_PICKS),
        KeyboardButton(text=MenuButton.GUIDES),
        KeyboardButton(text=MenuButton.VOTING),
        KeyboardButton(text=MenuButton.M6),
        KeyboardButton(text=MenuButton.GPT),
        KeyboardButton(text=MenuButton.META),
        KeyboardButton(text=MenuButton.TOURNAMENTS)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_tournaments_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.CREATE_TOURNAMENT),
        KeyboardButton(text=MenuButton.VIEW_TOURNAMENTS),
        KeyboardButton(text=MenuButton.BACK)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_m6_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.M6_TOURNAMENT_INFO),
        KeyboardButton(text=MenuButton.M6_STATISTICS),
        KeyboardButton(text=MenuButton.M6_NEWS),
        KeyboardButton(text=MenuButton.BACK_M6)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_gpt_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.GPT_DATA_GENERATION),
        KeyboardButton(text=MenuButton.GPT_HINTS),
        KeyboardButton(text=MenuButton.GPT_HERO_STATISTICS),
        KeyboardButton(text=MenuButton.BACK_GPT)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_meta_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.META_HERO_LIST),
        KeyboardButton(text=MenuButton.META_RECOMMENDATIONS),
        KeyboardButton(text=MenuButton.META_UPDATE),
        KeyboardButton(text=MenuButton.BACK_META)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_profile_menu_buttons() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.STATISTICS),
        KeyboardButton(text=MenuButton.ACHIEVEMENTS),
        KeyboardButton(text=MenuButton.SETTINGS),
        KeyboardButton(text=MenuButton.FEEDBACK),
        KeyboardButton(text=MenuButton.HELP),
        KeyboardButton(text=MenuButton.BACK_TO_MAIN_MENU)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_statistics_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.ACTIVITY),
        KeyboardButton(text=MenuButton.RANKING),
        KeyboardButton(text=MenuButton.GAME_STATS),
        KeyboardButton(text=MenuButton.BACK_TO_PROFILE)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_achievements_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.BADGES),
        KeyboardButton(text=MenuButton.PROGRESS),
        KeyboardButton(text=MenuButton.TOURNAMENT_STATS),
        KeyboardButton(text=MenuButton.AWARDS),
        KeyboardButton(text=MenuButton.BACK)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_settings_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.LANGUAGE),
        KeyboardButton(text=MenuButton.CHANGE_USERNAME),
        KeyboardButton(text=MenuButton.UPDATE_ID),
        KeyboardButton(text=MenuButton.NOTIFICATIONS),
        KeyboardButton(text=MenuButton.BACK)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_feedback_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.SEND_FEEDBACK),
        KeyboardButton(text=MenuButton.REPORT_BUG),
        KeyboardButton(text=MenuButton.BACK)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_help_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.INSTRUCTIONS),
        KeyboardButton(text=MenuButton.FAQ),
        KeyboardButton(text=MenuButton.HELP_SUPPORT),
        KeyboardButton(text=MenuButton.BACK)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_voting_menu() -> ReplyKeyboardMarkup:
    buttons = [
        KeyboardButton(text=MenuButton.CURRENT_VOTES),
        KeyboardButton(text=MenuButton.MY_VOTES),
        KeyboardButton(text=MenuButton.SUGGEST_TOPIC),
        KeyboardButton(text=MenuButton.BACK)
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=[buttons],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

# Додайте інші функції для створення меню за потребою