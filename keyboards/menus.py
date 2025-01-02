# keyboards/menus.py

from typing import List, Union, Dict
from enum import Enum, unique
import logging
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.logger_setup import setup_logger
from texts.data import heroes_by_class

# Налаштування логування
logger = setup_logger(__name__)

@unique
class MenuButton(Enum):
    # Головне Меню
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Мій Профіль"

    # Розділ Навігація
    TOURNAMENTS = "🏆 Турніри"
    HEROES = "🥷 Персонажі"
    CHALLENGES = "🧩 Челендж"
    GUIDES = "📚 Гайди"
    BUILDS = "🛡️ Білди"
    BUST = "🚀 Буст"
    TEAMS = "🧑‍🤝‍🧑 Команди"
    TRADING = "💰 Торгівля"
    BACK = "🔙 Назад"

    # Додані константи для Турнірів та M6
    CREATE_TOURNAMENT = "➕ Створити Турнір"
    VIEW_TOURNAMENTS = "🔍 Переглянути Турніри"

    M6_INFO = "ℹ️ Інфо M6"
    M6_STATS = "📊 Статистика M6"
    M6_NEWS = "📰 Новини M6"

    # Розділ Персонажі
    TANK = "🛡️ Танк"
    MAGE = "🧙‍♂️ Маг"
    MARKSMAN = "🏹 Стрілець"
    ASSASSIN = "⚔️ Асасін"
    SUPPORT = "❤️ Підтримка"
    FIGHTER = "🗡️ Боєць"
    COMPARISON = "⚖️ Порівняй"
    SEARCH_HERO = "🔎 Пошук"
    VOTING = "🗳️ Голосуй"

    # Розділ Контр-піки
    COUNTER_SEARCH = "🔎 Пошук Контр-піка"
    COUNTER_LIST = "📝 Список Персонажів"
    COUNTER_PICKS = "♻️ Контр-пік"

    # Розділ META
    META_HERO_LIST = "🔍 Список Героїв META"
    META_RECOMMENDATIONS = "☑️ Рекомендації META"
    META_UPDATES = "📈 Оновлення META"
    META = "🔥 МЕТА"

    # Розділ Гайди
    NEW_GUIDES = "🆕 Нові Гайди"
    M6 = "🏆 M6"
    POPULAR_GUIDES = "🌟 Популярні Гайди"
    BEGINNER_GUIDES = "📘 Для Початківців"
    ADVANCED_TECHNIQUES = "🧙 Стратегії Гри"
    TEAMPLAY_GUIDES = "🤝 Командна Гра"

    # Розділ Білди
    CREATE_BUILD = "🏗️ Створити Білд"
    MY_BUILDS = "📄 Мої Білди"
    POPULAR_BUILDS = "🔝 Популярні Білди"

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
    MY_TEAM = "🧍 Моя команда"
    GPT = "👾 GPT"

    # Підрозділ Статистика
    ACTIVITY = "📊 Загальна Активність"
    RANKING = "🥇 Рейтинг"
    GAME_STATS = "🎮 Ігрова Статистика"

    # Підрозділ Досягнення
    BADGES = "🎖️ Мої Бейджі"
    PROGRESS = "🚀 Прогрес"
    TOURNAMENT_STATS = "🏅 Турнірна Статистика"
    AWARDS = "🎟️ Отримані Нагороди"

    # Підрозділ Налаштування
    LANGUAGE = "🌐 Мова Інтерфейсу"
    CHANGE_USERNAME = "ℹ️ Змінити Username"
    UPDATE_ID = "🆔 Оновити ID"
    NOTIFICATIONS = "🔔 Сповіщення"

    # Підрозділ Зворотний зв'язок
    SEND_FEEDBACK = "✏️ Надіслати Відгук"
    REPORT_BUG = "🐛 Повідомити про Помилку"

    # Підрозділ Допомога
    INSTRUCTIONS = "📄 Інструкції"
    FAQ = "❔ FAQ"
    HELP_SUPPORT = "📞 Підтримка"

    # Новий розділ Команди
    CREATE_TEAM = "➕ Створити Команду"
    VIEW_TEAMS = "👀 Переглянути Команди"

    # Нові константи для Торгівлі
    CREATE_TRADE = "➕ Створити Торгівлю"
    VIEW_TRADES = "👀 Переглянути Торгівлі"
    MANAGE_TRADES = "🔧 Управління Торгівлями"

    # GPT Меню
    GPT_DATA_GENERATION = "📊 Генерація Даних"
    GPT_HINTS = "💡 Поради"
    GPT_HERO_STATS = "📈 Статистика Героїв"


@unique
class LanguageButton(Enum):
    UKRAINIAN = "🇺🇦 Українська"
    ENGLISH = "🇬🇧 English"
    BACK = "🔙 Назад"


class MenuBuilder:
    def __init__(self, row_width: int = 2):
        self.row_width = row_width

    def create_menu(
        self,
        buttons: List[Union[MenuButton, LanguageButton]],
        placeholder: str = ""
    ) -> ReplyKeyboardMarkup:
        """
        Створює меню з кнопками (ReplyKeyboardMarkup).

        :param buttons: Список кнопок (MenuButton або LanguageButton Enum).
        :param placeholder: Підказка для поля вводу.
        :return: ReplyKeyboardMarkup об'єкт.
        """
        if not all(isinstance(button, (MenuButton, LanguageButton)) for button in buttons):
            logger.error("Усі елементи у списку кнопок повинні бути екземплярами MenuButton або LanguageButton Enum.")
            raise ValueError("Усі елементи у списку кнопок повинні бути екземплярами MenuButton або LanguageButton Enum.")

        button_texts = [button.value for button in buttons]
        logger.info(f"Створення меню з кнопками: {button_texts} та підказкою: '{placeholder}'")

        keyboard_buttons = [KeyboardButton(text=btn.value) for btn in buttons]
        keyboard_rows = [
            keyboard_buttons[i:i + self.row_width]
            for i in range(0, len(keyboard_buttons), self.row_width)
        ]

        return ReplyKeyboardMarkup(
            keyboard=keyboard_rows,
            resize_keyboard=True,
            input_field_placeholder=placeholder
        )

    def get_main_menu(self) -> ReplyKeyboardMarkup:
        """Головне меню"""
        return self.create_menu(
            buttons=[MenuButton.NAVIGATION, MenuButton.PROFILE],
            placeholder="Оберіть одну з основних опцій"
        )

        from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu_keyboard():
    """
    Генерує клавіатуру головного меню.
    """
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("🧭 Навігація"), KeyboardButton("🪪 Профіль")],
            [KeyboardButton("⚔️ Герої"), KeyboardButton("🏆 Турніри")],
            [KeyboardButton("📚 Гайди"), KeyboardButton("⚡️ Буст")]
        ],
        resize_keyboard=True
    )

    def get_navigation_menu(self) -> ReplyKeyboardMarkup:
        """Меню навігації"""
        return self.create_menu(
            buttons=[
                MenuButton.HEROES,
                MenuButton.BUILDS,
                MenuButton.GUIDES,
                MenuButton.TOURNAMENTS,
                MenuButton.TEAMS,
                MenuButton.CHALLENGES,
                MenuButton.BUST,
                MenuButton.TRADING,
                MenuButton.BACK
            ],
            placeholder="Виберіть розділ у навігації"
        )

    def get_heroes_menu(self) -> ReplyKeyboardMarkup:
        """Меню героїв"""
        return self.create_menu(
            buttons=[
                MenuButton.TANK,
                MenuButton.MAGE,
                MenuButton.MARKSMAN,
                MenuButton.ASSASSIN,
                MenuButton.FIGHTER,
                MenuButton.SUPPORT,
                MenuButton.META,
                MenuButton.COUNTER_PICKS,
                MenuButton.COMPARISON,
                MenuButton.VOTING,
                MenuButton.SEARCH_HERO,
                MenuButton.BACK
            ],
            placeholder="Виберіть клас персонажа"
        )

    def get_profile_menu(self) -> ReplyKeyboardMarkup:
        """Меню профілю"""
        return self.create_menu(
            buttons=[
                MenuButton.STATISTICS,
                MenuButton.MY_TEAM,
                MenuButton.ACHIEVEMENTS,
                MenuButton.SETTINGS,
                MenuButton.FEEDBACK,
                MenuButton.HELP,
                MenuButton.GPT,
                MenuButton.BACK
            ],
            placeholder="Оберіть дію з профілем"
        )

    def get_language_menu(self) -> ReplyKeyboardMarkup:
        """Меню вибору мови"""
        return self.create_menu(
            buttons=[
                LanguageButton.UKRAINIAN,
                LanguageButton.ENGLISH,
                LanguageButton.BACK
            ],
            placeholder="Оберіть мову інтерфейсу"
        )

    def get_challenges_menu(self) -> ReplyKeyboardMarkup:
        """Меню челенджів"""
        return self.create_menu(
            buttons=[
                MenuButton.CHALLENGES,
                MenuButton.BACK
            ],
            placeholder="Виберіть опцію челенджів"
        )

    def get_bust_menu(self) -> ReplyKeyboardMarkup:
        """Меню бустів"""
        return self.create_menu(
            buttons=[
                MenuButton.BUST,
                MenuButton.BACK
            ],
            placeholder="Виберіть опцію бустів"
        )

    def get_my_team_menu(self) -> ReplyKeyboardMarkup:
        """Меню моєї команди"""
        return self.create_menu(
            buttons=[
                MenuButton.MY_TEAM,
                MenuButton.BACK
            ],
            placeholder="Виберіть опцію Моєї Команди"
        )

    def get_guides_menu(self) -> ReplyKeyboardMarkup:
        """Меню гайдів"""
        return self.create_menu(
            buttons=[
                MenuButton.NEW_GUIDES,
                MenuButton.M6,
                MenuButton.POPULAR_GUIDES,
                MenuButton.BEGINNER_GUIDES,
                MenuButton.ADVANCED_TECHNIQUES,
                MenuButton.TEAMPLAY_GUIDES,
                MenuButton.BACK
            ],
            placeholder="Оберіть розділ гайдів"
        )

    def get_counter_picks_menu(self) -> ReplyKeyboardMarkup:
        """Меню контр-піків"""
        return self.create_menu(
            buttons=[
                MenuButton.COUNTER_SEARCH,
                MenuButton.COUNTER_LIST,
                MenuButton.BACK
            ],
            placeholder="Виберіть опцію Контр-піків"
        )

    def get_builds_menu(self) -> ReplyKeyboardMarkup:
        """Меню білдів"""
        return self.create_menu(
            buttons=[
                MenuButton.CREATE_BUILD,
                MenuButton.MY_BUILDS,
                MenuButton.POPULAR_BUILDS,
                MenuButton.BACK
            ],
            placeholder="Виберіть опцію Білдів"
        )

    def get_voting_menu(self) -> ReplyKeyboardMarkup:
        """Меню голосування"""
        return self.create_menu(
            buttons=[
                MenuButton.CURRENT_VOTES,
                MenuButton.MY_VOTES,
                MenuButton.SUGGEST_TOPIC,
                MenuButton.BACK
            ],
            placeholder="Виберіть опцію голосування"
        )

    def get_statistics_menu(self) -> ReplyKeyboardMarkup:
        """Меню статистики"""
        return self.create_menu(
            buttons=[
                MenuButton.ACTIVITY,
                MenuButton.RANKING,
                MenuButton.GAME_STATS,
                MenuButton.BACK
            ],
            placeholder="Оберіть тип статистики"
        )

    def get_achievements_menu(self) -> ReplyKeyboardMarkup:
        """Меню досягнень"""
        return self.create_menu(
            buttons=[
                MenuButton.BADGES,
                MenuButton.PROGRESS,
                MenuButton.TOURNAMENT_STATS,
                MenuButton.AWARDS,
                MenuButton.BACK
            ],
            placeholder="Оберіть категорію досягнень"
        )

    def get_settings_menu(self) -> ReplyKeyboardMarkup:
        """Меню налаштувань"""
        return self.create_menu(
            buttons=[
                MenuButton.LANGUAGE,
                MenuButton.CHANGE_USERNAME,
                MenuButton.UPDATE_ID,
                MenuButton.NOTIFICATIONS,
                MenuButton.BACK
            ],
            placeholder="Налаштуйте свій профіль"
        )

    def get_feedback_menu(self) -> ReplyKeyboardMarkup:
        """Меню зворотного зв'язку"""
        return self.create_menu(
            buttons=[
                MenuButton.SEND_FEEDBACK,
                MenuButton.REPORT_BUG,
                MenuButton.BACK
            ],
            placeholder="Виберіть тип зворотного зв'язку"
        )

    def get_help_menu(self) -> ReplyKeyboardMarkup:
        """Меню допомоги"""
        return self.create_menu(
            buttons=[
                MenuButton.INSTRUCTIONS,
                MenuButton.FAQ,
                MenuButton.HELP_SUPPORT,
                MenuButton.BACK
            ],
            placeholder="Оберіть розділ допомоги"
        )

    def get_tournaments_menu(self) -> ReplyKeyboardMarkup:
        """Меню турнірів"""
        return self.create_menu(
            buttons=[
                MenuButton.CREATE_TOURNAMENT,
                MenuButton.VIEW_TOURNAMENTS,
                MenuButton.BACK
            ],
            placeholder="Оберіть дію з турнірами"
        )

    def get_meta_menu(self) -> ReplyKeyboardMarkup:
        """Меню META"""
        return self.create_menu(
            buttons=[
                MenuButton.META_HERO_LIST,
                MenuButton.META_RECOMMENDATIONS,
                MenuButton.META_UPDATES,
                MenuButton.BACK
            ],
            placeholder="Оберіть опцію META"
        )

    def get_m6_menu(self) -> ReplyKeyboardMarkup:
        """Меню M6"""
        return self.create_menu(
            buttons=[
                MenuButton.M6_INFO,
                MenuButton.M6_STATS,
                MenuButton.M6_NEWS,
                MenuButton.BACK
            ],
            placeholder="Оберіть інформацію про M6"
        )

    def get_gpt_menu(self) -> ReplyKeyboardMarkup:
        """Меню GPT"""
        return self.create_menu(
            buttons=[
                MenuButton.GPT_DATA_GENERATION,
                MenuButton.GPT_HINTS,
                MenuButton.GPT_HERO_STATS,
                MenuButton.BACK
            ],
            placeholder="Оберіть опцію GPT"
        )

    def get_teams_menu(self) -> ReplyKeyboardMarkup:
        """Меню команд"""
        return self.create_menu(
            buttons=[
                MenuButton.CREATE_TEAM,
                MenuButton.VIEW_TEAMS,
                MenuButton.BACK
            ],
            placeholder="Оберіть опцію Команди"
        )

    def get_trading_menu(self) -> ReplyKeyboardMarkup:
        """Меню торгівлі"""
        return self.create_menu(
            buttons=[
                MenuButton.CREATE_TRADE,
                MenuButton.VIEW_TRADES,
                MenuButton.MANAGE_TRADES,
                MenuButton.BACK
            ],
            placeholder="Оберіть опцію Торгівлі"
        )

    def get_hero_class_menu(self) -> ReplyKeyboardMarkup:
        """Меню вибору класу героя"""
        buttons = [
            MenuButton.TANK,
            MenuButton.MAGE,
            MenuButton.MARKSMAN,
            MenuButton.ASSASSIN,
            MenuButton.SUPPORT,
            MenuButton.FIGHTER,
            MenuButton.BACK
        ]
        return self.create_menu(
            buttons=buttons,
            placeholder="Оберіть клас героя"
        )

    def get_hero_class_reply_menu(self, hero_class: str) -> ReplyKeyboardMarkup:
        """
        Створює клавіатуру зі списком героїв обраного класу.

        :param hero_class: Напр. "Танк", "Маг", "Боєць" тощо.
        :return: ReplyKeyboardMarkup зі списком героїв + кнопка "Назад".
        """
        heroes = heroes_by_class.get(hero_class, [])
        logger.info(f"Створюємо клавіатуру для класу {hero_class}, героїв знайдено: {len(heroes)}")

        # Створюємо кнопки для кожного героя
        hero_buttons = [KeyboardButton(text=hero) for hero in heroes]
        hero_buttons.append(KeyboardButton(text=MenuButton.BACK.value))

        # Розділяємо кнопки на рядки
        keyboard_rows = [
            hero_buttons[i:i + self.row_width]
            for i in range(0, len(hero_buttons), self.row_width)
        ]

        return ReplyKeyboardMarkup(
            keyboard=keyboard_rows,
            resize_keyboard=True,
            input_field_placeholder=f"Оберіть героя з класу {hero_class}"
        )

    # Налаштування логування
logger = setup_logger(__name__)

class Keyboards:
    """Клас для централізованого доступу до всіх клавіатур"""
    
    def __init__(self):
        self.builder = MenuBuilder()
        logger.info("Keyboards class initialized")

    def main_menu(self) -> ReplyKeyboardMarkup:
        """Головне меню"""
        return self.builder.get_main_menu()

    def navigation_menu(self) -> ReplyKeyboardMarkup:
        """Меню навігації"""
        return self.builder.get_navigation_menu()

    def heroes_menu(self) -> ReplyKeyboardMarkup:
        """Меню героїв"""
        return self.builder.get_heroes_menu()

    def profile_menu(self) -> ReplyKeyboardMarkup:
        """Меню профілю"""
        return self.builder.get_profile_menu()

    def language_menu(self) -> ReplyKeyboardMarkup:
        """Меню вибору мови"""
        return self.builder.get_language_menu()

    def challenges_menu(self) -> ReplyKeyboardMarkup:
        """Меню челенджів"""
        return self.builder.get_challenges_menu()

    def bust_menu(self) -> ReplyKeyboardMarkup:
        """Меню бустів"""
        return self.builder.get_bust_menu()

    def my_team_menu(self) -> ReplyKeyboardMarkup:
        """Меню моєї команди"""
        return self.builder.get_my_team_menu()

    def guides_menu(self) -> ReplyKeyboardMarkup:
        """Меню гайдів"""
        return self.builder.get_guides_menu()

    def counter_picks_menu(self) -> ReplyKeyboardMarkup:
        """Меню контр-піків"""
        return self.builder.get_counter_picks_menu()

    def builds_menu(self) -> ReplyKeyboardMarkup:
        """Меню білдів"""
        return self.builder.get_builds_menu()

    def voting_menu(self) -> ReplyKeyboardMarkup:
        """Меню голосування"""
        return self.builder.get_voting_menu()

    def statistics_menu(self) -> ReplyKeyboardMarkup:
        """Меню статистики"""
        return self.builder.get_statistics_menu()

    def achievements_menu(self) -> ReplyKeyboardMarkup:
        """Меню досягнень"""
        return self.builder.get_achievements_menu()

    def settings_menu(self) -> ReplyKeyboardMarkup:
        """Меню налаштувань"""
        return self.builder.get_settings_menu()

    def feedback_menu(self) -> ReplyKeyboardMarkup:
        """Меню зворотного зв'язку"""
        return self.builder.get_feedback_menu()

    def help_menu(self) -> ReplyKeyboardMarkup:
        """Меню допомоги"""
        return self.builder.get_help_menu()

    def tournaments_menu(self) -> ReplyKeyboardMarkup:
        """Меню турнірів"""
        return self.builder.get_tournaments_menu()

    def meta_menu(self) -> ReplyKeyboardMarkup:
        """Меню META"""
        return self.builder.get_meta_menu()

    def m6_menu(self) -> ReplyKeyboardMarkup:
        """Меню M6"""
        return self.builder.get_m6_menu()

    def gpt_menu(self) -> ReplyKeyboardMarkup:
        """Меню GPT"""
        return self.builder.get_gpt_menu()

    def teams_menu(self) -> ReplyKeyboardMarkup:
        """Меню команд"""
        return self.builder.get_teams_menu()

    def trading_menu(self) -> ReplyKeyboardMarkup:
        """Меню торгівлі"""
        return self.builder.get_trading_menu()

    def hero_class_menu(self) -> ReplyKeyboardMarkup:
        """Меню вибору класу героя"""
        return self.builder.get_hero_class_menu()

    def hero_class_reply_menu(self, hero_class: str) -> ReplyKeyboardMarkup:
        """Меню вибору героя з конкретного класу"""
        return self.builder.get_hero_class_reply_menu(hero_class)

    @property
    def back_button(self) -> str:
        """Кнопка 'Назад'"""
        return MenuButton.BACK.value

# Створюємо глобальний екземпляр MenuBuilder
menu_builder = MenuBuilder()

# Експортуємо функції для зворотної сумісності
def get_main_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_main_menu()

def get_navigation_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_navigation_menu()

def get_heroes_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_heroes_menu()

def get_profile_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_profile_menu()

def get_language_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_language_menu()

def get_challenges_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_challenges_menu()

def get_bust_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_bust_menu()

def get_my_team_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_my_team_menu()

def get_guides_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_guides_menu()

def get_counter_picks_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_counter_picks_menu()

def get_builds_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_builds_menu()

def get_voting_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_voting_menu()

def get_statistics_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_statistics_menu()

def get_achievements_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_achievements_menu()

def get_settings_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_settings_menu()

def get_feedback_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_feedback_menu()

def get_help_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_help_menu()

def get_tournaments_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_tournaments_menu()

def get_meta_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_meta_menu()

def get_m6_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_m6_menu()

def get_gpt_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_gpt_menu()

def get_teams_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_teams_menu()

def get_trading_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_trading_menu()

def get_hero_class_menu() -> ReplyKeyboardMarkup:
    return menu_builder.get_hero_class_menu()

def get_hero_class_reply_menu(hero_class: str) -> ReplyKeyboardMarkup:
    return menu_builder.get_hero_class_reply_menu(hero_class)
