# keyboards/menus.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import List, Dict, Union
from texts.enums import MenuButton, LanguageButton
from texts.data import menu_button_to_class, heroes_by_class
from utils.logger_setup import setup_logger

logger = setup_logger(__name__)

def create_menu(
    buttons: List[Union[MenuButton, LanguageButton]],
    placeholder: str = "",
    row_width: int = 2
) -> ReplyKeyboardMarkup:
    """
    Створює меню з кнопками (ReplyKeyboardMarkup).

    :param buttons: Список кнопок (MenuButton або LanguageButton Enum).
    :param placeholder: Підказка для поля вводу.
    :param row_width: Кількість кнопок у рядку.
    :return: ReplyKeyboardMarkup об'єкт.
    """
    if not all(isinstance(button, (MenuButton, LanguageButton)) for button in buttons):
        logger.error("Усі елементи у списку кнопок повинні бути екземплярами MenuButton або LanguageButton Enum.")
        raise ValueError("Усі елементи у списку кнопок повинні бути екземплярами MenuButton або LanguageButton Enum.")

    button_texts = [button.value for button in buttons]
    logger.info(f"Створення меню з кнопками: {button_texts} та підказкою: '{placeholder}'")

    keyboard_buttons = [KeyboardButton(text=btn.value) for btn in buttons]

    keyboard_rows = [
        keyboard_buttons[i:i + row_width]
        for i in range(0, len(keyboard_buttons), row_width)
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard_rows,
        resize_keyboard=True,
        input_field_placeholder=placeholder
    )

# Приклади генерації меню

def get_main_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для головного меню з кнопками "Навігація" та "Профіль".
    """
    return create_menu(
        buttons=[MenuButton.NAVIGATION, MenuButton.PROFILE],
        placeholder="Оберіть одну з основних опцій",
        row_width=2
    )

def get_navigation_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для розділу Навігація з різними опціями.
    """
    return create_menu(
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
        placeholder="Виберіть розділ у навігації",
        row_width=3
    )

def get_heroes_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для розділу Персонажі з класами героїв.
    """
    return create_menu(
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
        placeholder="Виберіть клас персонажа",
        row_width=3
    )

def get_profile_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для розділу Профіль з різними опціями.
    """
    return create_menu(
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
        placeholder="Оберіть дію з профілем",
        row_width=3
    )

def get_language_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для вибору мови інтерфейсу.
    """
    return create_menu(
        buttons=[
            LanguageButton.UKRAINIAN,
            LanguageButton.ENGLISH,
            LanguageButton.BACK
        ],
        placeholder="Оберіть мову інтерфейсу",
        row_width=1
    )

def get_challenges_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для розділу Челенджі.
    """
    return create_menu(
        buttons=[
            MenuButton.CHALLENGES,
            MenuButton.BACK
        ],
        placeholder="Виберіть опцію челенджів",
        row_width=2
    )

def get_bust_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для розділу Бустів.
    """
    return create_menu(
        buttons=[
            MenuButton.BUST,
            MenuButton.BACK
        ],
        placeholder="Виберіть опцію бустів",
        row_width=2
    )

def get_my_team_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для розділу Моя команда.
    """
    return create_menu(
        buttons=[
            MenuButton.MY_TEAM,
            MenuButton.BACK
        ],
        placeholder="Виберіть опцію Моєї Команди",
        row_width=2
    )

def get_guides_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для розділу Гайди з різними категоріями.
    """
    return create_menu(
        buttons=[
            MenuButton.NEW_GUIDES,
            MenuButton.M6,
            MenuButton.POPULAR_GUIDES,
            MenuButton.BEGINNER_GUIDES,
            MenuButton.ADVANCED_TECHNIQUES,
            MenuButton.TEAMPLAY_GUIDES,
            MenuButton.BACK
        ],
        placeholder="Оберіть розділ гайдів",
        row_width=3
    )

def get_counter_picks_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для розділу Контр-піків.
    """
    return create_menu(
        buttons=[
            MenuButton.COUNTER_SEARCH,
            MenuButton.COUNTER_LIST,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію Контр-піків",
        row_width=3
    )

def get_builds_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для розділу Білди.
    """
    return create_menu(
        buttons=[
            MenuButton.CREATE_BUILD,
            MenuButton.MY_BUILDS,
            MenuButton.POPULAR_BUILDS,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію Білдів",
        row_width=3
    )

def get_voting_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для розділу Голосування.
    """
    return create_menu(
        buttons=[
            MenuButton.CURRENT_VOTES,
            MenuButton.MY_VOTES,
            MenuButton.SUGGEST_TOPIC,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію голосування",
        row_width=3
    )

def get_statistics_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для розділу Статистика з різними категоріями.
    """
    return create_menu(
        buttons=[
            MenuButton.ACTIVITY,
            MenuButton.RANKING,
            MenuButton.GAME_STATS,
            MenuButton.BACK
        ],
        placeholder="Оберіть тип статистики",
        row_width=3
    )

def get_achievements_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для розділу Досягнення.
    """
    return create_menu(
        buttons=[
            MenuButton.BADGES,
            MenuButton.PROGRESS,
            MenuButton.TOURNAMENT_STATS,
            MenuButton.AWARDS,
            MenuButton.BACK
        ],
        placeholder="Оберіть категорію досягнень",
        row_width=3
    )

def get_settings_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для розділу Налаштування.
    """
    return create_menu(
        buttons=[
            MenuButton.LANGUAGE,
            MenuButton.CHANGE_USERNAME,
            MenuButton.UPDATE_ID,
            MenuButton.NOTIFICATIONS,
            MenuButton.BACK
        ],
        placeholder="Налаштуйте свій профіль",
        row_width=3
    )

def get_feedback_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для розділу Зворотний зв'язок.
    """
    return create_menu(
        buttons=[
            MenuButton.SEND_FEEDBACK,
            MenuButton.REPORT_BUG,
            MenuButton.BACK
        ],
        placeholder="Виберіть тип зворотного зв'язку",
        row_width=3
    )

def get_help_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для розділу Допомога.
    """
    return create_menu(
        buttons=[
            MenuButton.INSTRUCTIONS,
            MenuButton.FAQ,
            MenuButton.HELP_SUPPORT,
            MenuButton.BACK
        ],
        placeholder="Оберіть розділ допомоги",
        row_width=3
    )

def get_tournaments_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для розділу Турніри.
    """
    return create_menu(
        buttons=[
            MenuButton.CREATE_TOURNAMENT,
            MenuButton.VIEW_TOURNAMENTS,
            MenuButton.BACK
        ],
        placeholder="Оберіть дію з турнірами",
        row_width=3
    )

def get_meta_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для розділу META.
    """
    return create_menu(
        buttons=[
            MenuButton.META_HERO_LIST,
            MenuButton.META_RECOMMENDATIONS,
            MenuButton.META_UPDATES,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію META",
        row_width=3
    )

def get_m6_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для розділу M6.
    """
    return create_menu(
        buttons=[
            MenuButton.M6_INFO,
            MenuButton.M6_STATS,
            MenuButton.M6_NEWS,
            MenuButton.BACK
        ],
        placeholder="Оберіть інформацію про M6",
        row_width=3
    )

def get_gpt_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для розділу GPT.
    """
    return create_menu(
        buttons=[
            MenuButton.GPT_DATA_GENERATION,
            MenuButton.GPT_HINTS,
            MenuButton.GPT_HERO_STATS,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію GPT",
        row_width=2
    )

def get_teams_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для розділу Команди.
    """
    return create_menu(
        buttons=[
            MenuButton.CREATE_TEAM,
            MenuButton.VIEW_TEAMS,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію Команди",
        row_width=2
    )

def get_trading_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для розділу Торгівлі.
    """
    return create_menu(
        buttons=[
            MenuButton.CREATE_TRADE,
            MenuButton.VIEW_TRADES,
            MenuButton.MANAGE_TRADES,
            MenuButton.BACK
        ],
        placeholder="Оберіть опцію Торгівлі",
        row_width=2
    )

def get_hero_class_menu() -> ReplyKeyboardMarkup:
    """
    Створює клавіатуру для вибору класу героя.
    """
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [
        KeyboardButton(text="Танк"),
        KeyboardButton(text="Маг"),
        KeyboardButton(text="Стрілець"),
        KeyboardButton(text="Асасін"),
        KeyboardButton(text="Підтримка"),
        KeyboardButton(text="Боєць"),
        KeyboardButton(text="🔙 Назад")
    ]
    keyboard.add(*buttons)
    return keyboard

def get_hero_class_reply_menu(hero_class: str) -> ReplyKeyboardMarkup:
    """
    Створює ЗВИЧАЙНУ клавіатуру (ReplyKeyboardMarkup) зі списком героїв обраного класу.

    :param hero_class: Напр. "Танк", "Маг", "Боєць" тощо.
    :return: ReplyKeyboardMarkup зі списком героїв, + кнопка Назад.
    """
    heroes = heroes_by_class.get(hero_class, [])
    logger.info(f"Створюємо звичайну клавіатуру для класу {hero_class}, героїв знайдено: {len(heroes)}")

    hero_buttons = [KeyboardButton(hero) for hero in heroes]

    # Додамо кнопку "Назад" (звичайну)
    hero_buttons.append(KeyboardButton("🔙 Назад"))

    # Наприклад, 3 герої в рядку
    row_width = 3
    keyboard_rows = [
        hero_buttons[i:i + row_width]
        for i in range(0, len(hero_buttons), row_width)
    ]

    return ReplyKeyboardMarkup(
        keyboard=keyboard_rows,
        resize_keyboard=True,
        input_field_placeholder=f"Оберіть героя з класу {hero_class}"
    )
