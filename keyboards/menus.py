# keyboards/menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from enum import Enum, auto


class MainMenuButtons(Enum):
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Мій Профіль"


class NavigationMenuButtons(Enum):
    CHARACTERS = "🥷 Персонажі"
    BUILDS = "🛡️ Білди"
    COUNTER_PICKS = "⚖️ Контр-піки"
    GUIDES = "📚 Гайди"
    VOTING = "📊 Голосування"
    M6 = "🏆 M6"
    GPT = "👾 GPT"
    META = "🔥 META"
    BACK = "🔙 Назад"


class CharactersMenuButtons(Enum):
    TANK = "🛡️ Танк"
    MAGE = "🧙‍♂️ Маг"
    MARKSMAN = "🏹 Стрілець"
    ASSASSIN = "⚔️ Асасін"
    SUPPORT = "❤️ Підтримка"
    FIGHTER = "🗡️ Боєць"
    COMPARISON = "⚖️ Порівняння"
    SEARCH_HERO = "🔎 Пошук"
    BACK = "🔙 Назад"


class BuildsMenuButtons(Enum):
    CREATE_BUILD = "🏗️ Створити"
    MY_BUILDS = "📄 Обрані"
    POPULAR_BUILDS = "🔥 Популярні"
    BACK = "🔙 Назад"


class CounterPicksMenuButtons(Enum):
    COUNTER_SEARCH = "🔎 Пошук"
    COUNTER_LIST = "📝 Список Персонажів"
    BACK = "🔙 Назад"


class GuidesMenuButtons(Enum):
    NEW_GUIDES = "🆕 Нові Гайди"
    TOP_GUIDES = "🌟 Топ Гайди"
    BEGINNER_GUIDES = "📘 Для Початківців"
    ADVANCED_GUIDES = "🧙 Стратегії гри"
    TEAMPLAY_GUIDES = "🤝 Командна Гра"
    BACK = "🔙 Назад"


class VotingMenuButtons(Enum):
    CURRENT_VOTES = "📍 Поточні Опитування"
    MY_VOTES = "📋 Мої Голосування"
    SUGGEST_TOPIC = "➕ Запропонувати Тему"
    BACK = "🔙 Назад"


class M6MenuButtons(Enum):
    TOURNAMENT_INFO = "🏆 Турнірна Інформація"
    STATISTICS_M6 = "📈 Статистика M6"
    NEWS_M6 = "📰 Новини M6"
    BACK = "🔙 Назад"


class GPTMenuButtons(Enum):
    GENERATE_DATA = "🤖 Генерація Даних"
    GPT_HINTS = "📝 Підказки"
    HERO_STATS_GPT = "📊 Статистика Героїв"
    BACK = "🔙 Назад"


class MetaMenuButtons(Enum):
    META_HERO_LIST = "📋 Список Героїв у Мету"
    RECOMMENDATIONS = "🌟 Рекомендації"
    UPDATE_META = "🔄 Оновлення Мети"
    BACK = "🔙 Назад"


class ProfileMenuButtons(Enum):
    STATISTICS = "📈 Статистика"
    ACHIEVEMENTS = "🏆 Досягнення"
    SETTINGS = "⚙️ Налаштування"
    FEEDBACK = "💌 Зворотний Зв'язок"
    HELP = "❓ Допомога"
    BACK_TO_MAIN = "🔙 Назад до Головного Меню"


class StatisticsMenuButtons(Enum):
    ACTIVITY = "📊 Загальна Активність"
    RANKING = "🥇 Рейтинг"
    GAME_STATS = "🎮 Ігрова Статистика"
    BACK = "🔙 Назад"


class AchievementsMenuButtons(Enum):
    BADGES = "🎖️ Мої Бейджі"
    PROGRESS = "🚀 Прогрес"
    TOURNAMENT_STATS = "🏅 Турнірна Статистика"
    AWARDS = "🎟️ Отримані Нагороди"
    BACK = "🔙 Назад"


class SettingsMenuButtons(Enum):
    LANGUAGE = "🌐 Мова Інтерфейсу"
    CHANGE_USERNAME = "ℹ️ Змінити Username"
    UPDATE_ID = "🆔 Оновити ID"
    NOTIFICATIONS = "🔔 Сповіщення"
    BACK = "🔙 Назад"


class FeedbackMenuButtons(Enum):
    SEND_FEEDBACK = "✏️ Надіслати Відгук"
    REPORT_BUG = "🐛 Повідомити про Помилку"
    BACK = "🔙 Назад"


class HelpMenuButtons(Enum):
    INSTRUCTIONS = "📄 Інструкції"
    FAQ = "❔ FAQ"
    HELP_SUPPORT = "📞 Підтримка"
    BACK = "🔙 Назад"


def create_reply_keyboard(buttons: list, row_width: int = 2, resize_keyboard: bool = True) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(resize_keyboard=resize_keyboard, row_width=row_width)
    keyboard.add(*[KeyboardButton(text=button.value) for button in buttons])
    return keyboard


def get_main_menu() -> ReplyKeyboardMarkup:
    return create_reply_keyboard([MainMenuButtons.NAVIGATION, MainMenuButtons.PROFILE], row_width=2)


def get_navigation_menu() -> ReplyKeyboardMarkup:
    return create_reply_keyboard([
        NavigationMenuButtons.CHARACTERS,
        NavigationMenuButtons.BUILDS,
        NavigationMenuButtons.COUNTER_PICKS,
        NavigationMenuButtons.GUIDES,
        NavigationMenuButtons.VOTING,
        NavigationMenuButtons.M6,
        NavigationMenuButtons.GPT,
        NavigationMenuButtons.META,
        NavigationMenuButtons.BACK
    ], row_width=3)


def get_characters_menu() -> ReplyKeyboardMarkup:
    return create_reply_keyboard([
        CharactersMenuButtons.TANK,
        CharactersMenuButtons.MAGE,
        CharactersMenuButtons.MARKSMAN,
        CharactersMenuButtons.ASSASSIN,
        CharactersMenuButtons.SUPPORT,
        CharactersMenuButtons.FIGHTER,
        CharactersMenuButtons.COMPARISON,
        CharactersMenuButtons.SEARCH_HERO,
        CharactersMenuButtons.BACK
    ], row_width=3)


def get_builds_menu() -> ReplyKeyboardMarkup:
    return create_reply_keyboard([
        BuildsMenuButtons.CREATE_BUILD,
        BuildsMenuButtons.MY_BUILDS,
        BuildsMenuButtons.POPULAR_BUILDS,
        BuildsMenuButtons.BACK
    ], row_width=2)


def get_counter_picks_menu() -> ReplyKeyboardMarkup:
    return create_reply_keyboard([
        CounterPicksMenuButtons.COUNTER_SEARCH,
        CounterPicksMenuButtons.COUNTER_LIST,
        CounterPicksMenuButtons.BACK
    ], row_width=2)


def get_guides_menu() -> ReplyKeyboardMarkup:
    return create_reply_keyboard([
        GuidesMenuButtons.NEW_GUIDES,
        GuidesMenuButtons.TOP_GUIDES,
        GuidesMenuButtons.BEGINNER_GUIDES,
        GuidesMenuButtons.ADVANCED_GUIDES,
        GuidesMenuButtons.TEAMPLAY_GUIDES,
        GuidesMenuButtons.BACK
    ], row_width=2)


def get_voting_menu() -> ReplyKeyboardMarkup:
    return create_reply_keyboard([
        VotingMenuButtons.CURRENT_VOTES,
        VotingMenuButtons.MY_VOTES,
        VotingMenuButtons.SUGGEST_TOPIC,
        VotingMenuButtons.BACK
    ], row_width=2)


def get_m6_menu() -> ReplyKeyboardMarkup:
    return create_reply_keyboard([
        M6MenuButtons.TOURNAMENT_INFO,
        M6MenuButtons.STATISTICS_M6,
        M6MenuButtons.NEWS_M6,
        M6MenuButtons.BACK
    ], row_width=2)


def get_gpt_menu() -> ReplyKeyboardMarkup:
    return create_reply_keyboard([
        GPTMenuButtons.GENERATE_DATA,
        GPTMenuButtons.GPT_HINTS,
        GPTMenuButtons.HERO_STATS_GPT,
        GPTMenuButtons.BACK
    ], row_width=2)


def get_meta_menu() -> ReplyKeyboardMarkup:
    return create_reply_keyboard([
        MetaMenuButtons.META_HERO_LIST,
        MetaMenuButtons.RECOMMENDATIONS,
        MetaMenuButtons.UPDATE_META,
        MetaMenuButtons.BACK
    ], row_width=2)


def get_profile_menu() -> ReplyKeyboardMarkup:
    return create_reply_keyboard([
        ProfileMenuButtons.STATISTICS,
        ProfileMenuButtons.ACHIEVEMENTS,
        ProfileMenuButtons.SETTINGS,
        ProfileMenuButtons.FEEDBACK,
        ProfileMenuButtons.HELP,
        ProfileMenuButtons.BACK_TO_MAIN
    ], row_width=2)


def get_statistics_menu() -> ReplyKeyboardMarkup:
    return create_reply_keyboard([
        StatisticsMenuButtons.ACTIVITY,
        StatisticsMenuButtons.RANKING,
        StatisticsMenuButtons.GAME_STATS,
        StatisticsMenuButtons.BACK
    ], row_width=2)


def get_achievements_menu() -> ReplyKeyboardMarkup:
    return create_reply_keyboard([
        AchievementsMenuButtons.BADGES,
        AchievementsMenuButtons.PROGRESS,
        AchievementsMenuButtons.TOURNAMENT_STATS,
        AchievementsMenuButtons.AWARDS,
        AchievementsMenuButtons.BACK
    ], row_width=2)


def get_settings_menu() -> ReplyKeyboardMarkup:
    return create_reply_keyboard([
        SettingsMenuButtons.LANGUAGE,
        SettingsMenuButtons.CHANGE_USERNAME,
        SettingsMenuButtons.UPDATE_ID,
        SettingsMenuButtons.NOTIFICATIONS,
        SettingsMenuButtons.BACK
    ], row_width=2)


def get_feedback_menu() -> ReplyKeyboardMarkup:
    return create_reply_keyboard([
        FeedbackMenuButtons.SEND_FEEDBACK,
        FeedbackMenuButtons.REPORT_BUG,
        FeedbackMenuButtons.BACK
    ], row_width=2)


def get_help_menu() -> ReplyKeyboardMarkup:
    return create_reply_keyboard([
        HelpMenuButtons.INSTRUCTIONS,
        HelpMenuButtons.FAQ,
        HelpMenuButtons.HELP_SUPPORT,
        HelpMenuButtons.BACK
    ], row_width=2)


# Інлайн-клавіатури

class InlineMenuButtons(Enum):
    ADDITIONAL_INFO = "Додаткова Інформація"
    BACK_TO_MENU = "🔙 Назад до Меню"
    NEXT_CHARACTER = "➡️ Наступний"
    PREV_CHARACTER = "⬅️ Попередній"
    MORE_GUIDES = "📝 Більше Гайдів"


def get_generic_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Генерична інлайн-клавіатура для додаткових функцій.
    """
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text=InlineMenuButtons.ADDITIONAL_INFO.value, callback_data="additional_info"),
        InlineKeyboardButton(text=InlineMenuButtons.BACK_TO_MENU.value, callback_data="back_to_menu"),
    ]
    keyboard.add(*buttons)
    return keyboard


def get_character_inline_keyboard(character_id: int) -> InlineKeyboardMarkup:
    """
    Інлайн-клавіатура для перегляду персонажа з кнопками для гайдів та навігації.
    """
    keyboard = InlineKeyboardMarkup(row_width=3)
    buttons = [
        InlineKeyboardButton(text="📝 Гайди", callback_data=f"guides_{character_id}"),
        InlineKeyboardButton(text="➡️ Наступний", callback_data=f"next_{character_id}"),
        InlineKeyboardButton(text="⬅️ Попередній", callback_data=f"prev_{character_id}"),
    ]
    keyboard.add(*buttons)
    return keyboard


def get_guide_inline_keyboard(guide_id: int) -> InlineKeyboardMarkup:
    """
    Інлайн-клавіатура для гайдів з кнопками для повернення або переходу до іншого гайду.
    """
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="🔙 Повернутись", callback_data="back_to_guides"),
        InlineKeyboardButton(text="➡️ Наступний Гайд", callback_data=f"next_guide_{guide_id}"),
    ]
    keyboard.add(*buttons)
    return keyboard