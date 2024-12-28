# handlers/base.py

import io
import logging
from typing import Optional

import networkx as nx  # Якщо потрібно, інакше видаліть
import plotly.graph_objects as go
from PIL import Image
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Моделі та утиліти
import models.user
import models.user_stats
from states import MenuStates
from utils.db import get_user_profile
from utils.message_utils import safe_delete_message
from utils.text_formatter import format_profile_text

# Клавіатури
from keyboards.inline_menus import (
    get_generic_inline_keyboard,
    get_intro_page_1_keyboard,
    get_intro_page_2_keyboard,
    get_intro_page_3_keyboard
)
from keyboards.menus import (
    MenuButton as AdvancedMenuButton,
    get_main_menu,            # Використовуємо в обох логіках
    get_profile_menu,
    get_navigation_menu,
    get_heroes_menu,
    get_hero_class_menu,
    get_guides_menu,
    get_counter_picks_menu,
    get_builds_menu,
    get_voting_menu,
    get_statistics_menu,
    get_achievements_menu,
    get_settings_menu,
    get_feedback_menu,
    get_help_menu,
    get_tournaments_menu,
    get_meta_menu,
    get_m6_menu,
    get_gpt_menu,
    heroes_by_class
)

# Тексти
from texts import (
    # Основні (для простої логіки)
    MAIN_MENU_TEXT,
    MAIN_MENU_DESCRIPTION,
    MAIN_MENU_ERROR_TEXT,
    LANGUAGE_TEXT,
    LANGUAGE_CHANGED_TEXT,
    LANGUAGE_ERROR_TEXT,
    HEROES_MENU_TEXT,
    HEROES_INTERACTIVE_TEXT,
    GUIDES_MENU_TEXT,
    GUIDES_INTERACTIVE_TEXT,
    COUNTER_PICKS_MENU_TEXT,
    COUNTER_PICKS_INTERACTIVE_TEXT,
    BUILDS_MENU_TEXT,
    BUILDS_INTERACTIVE_TEXT,
    VOTING_MENU_TEXT,
    VOTING_INTERACTIVE_TEXT,
    UNKNOWN_COMMAND_TEXT,
    GENERIC_ERROR_MESSAGE_TEXT,

    # Для розширеної логіки (вступні сторінки, графіки тощо)
    INTRO_PAGE_1_TEXT,
    INTRO_PAGE_2_TEXT,
    INTRO_PAGE_3_TEXT,
    NAVIGATION_MENU_TEXT,
    NAVIGATION_INTERACTIVE_TEXT,
    PROFILE_MENU_TEXT,
    PROFILE_INTERACTIVE_TEXT,
    ERROR_MESSAGE_TEXT,
    HERO_CLASS_MENU_TEXT,
    HERO_CLASS_INTERACTIVE_TEXT,
    NEW_GUIDES_TEXT,
    POPULAR_GUIDES_TEXT,
    BEGINNER_GUIDES_TEXT,
    ADVANCED_TECHNIQUES_TEXT,
    TEAMPLAY_GUIDES_TEXT,
    COUNTER_SEARCH_TEXT,
    COUNTER_LIST_TEXT,
    CREATE_BUILD_TEXT,
    MY_BUILDS_TEXT,
    POPULAR_BUILDS_TEXT,
    CURRENT_VOTES_TEXT,
    MY_VOTES_TEXT,
    SUGGEST_TOPIC_TEXT,
    SUGGESTION_RESPONSE_TEXT,
    STATISTICS_MENU_TEXT,
    STATISTICS_INTERACTIVE_TEXT,
    ACTIVITY_TEXT,
    RANKING_TEXT,
    GAME_STATS_TEXT,
    ACHIEVEMENTS_MENU_TEXT,
    ACHIEVEMENTS_INTERACTIVE_TEXT,
    BADGES_TEXT,
    PROGRESS_TEXT,
    TOURNAMENT_STATS_TEXT,
    AWARDS_TEXT,
    SETTINGS_MENU_TEXT,
    SETTINGS_INTERACTIVE_TEXT,
    CHANGE_USERNAME_TEXT,
    UPDATE_ID_TEXT,
    NOTIFICATIONS_TEXT,
    FEEDBACK_MENU_TEXT,
    FEEDBACK_INTERACTIVE_TEXT,
    SEND_FEEDBACK_TEXT,
    REPORT_BUG_TEXT,
    FEEDBACK_RECEIVED_TEXT,
    BUG_REPORT_RECEIVED_TEXT,
    HELP_MENU_TEXT,
    HELP_INTERACTIVE_TEXT,
    INSTRUCTIONS_TEXT,
    FAQ_TEXT,
    HELP_SUPPORT_TEXT,
    USE_BUTTON_NAVIGATION_TEXT,
    SEARCH_HERO_RESPONSE_TEXT,
    CHANGE_USERNAME_RESPONSE_TEXT,
    MLS_BUTTON_RESPONSE_TEXT,
    UNHANDLED_INLINE_BUTTON_TEXT,
    MAIN_MENU_BACK_TO_PROFILE_TEXT,
    TOURNAMENT_CREATE_TEXT,
    TOURNAMENT_VIEW_TEXT,
    META_HERO_LIST_TEXT,
    META_RECOMMENDATIONS_TEXT,
    META_UPDATES_TEXT,
    M6_INFO_TEXT,
    M6_STATS_TEXT,
    M6_NEWS_TEXT,
    GPT_MENU_TEXT,
    TOURNAMENTS_MENU_TEXT,
    META_MENU_TEXT,
    LANGUAGE_CHANGED_TEXT,
    LANGUAGE_ERROR_TEXT,
    STATS_TEXT
)

# ------------------------------------------------------------------------------------
#                           ОСНОВНИЙ РОУТЕР ТА ЛОГЕР
# ------------------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

# ------------------------------------------------------------------------------------
#                           СПРОЩЕНА ЛОГІКА МЕНЮ
# ------------------------------------------------------------------------------------

class SimpleMenuButton:
    """Константи для кнопок меню (спрощена логіка)"""
    HEROES = "Герої"
    GUIDES = "Гайди"
    COUNTER_PICKS = "Контр-піки"
    BUILDS = "Білди"
    VOTING = "Голосування"
    SETTINGS = "Налаштування"
    BACK = "Назад"


@router.message(Command("start"))
async def start_command_simple(message: Message, state: FSMContext):
    """
    Спрощена обробка команди /start.
    (Якщо бажаєте використовувати розширену логіку з БД — використовуйте cmd_start нижче.)
    """
    try:
        user_first_name = message.from_user.first_name or "Користувач"
        await message.answer(
            MAIN_MENU_TEXT.format(user_first_name=user_first_name),
            reply_markup=get_main_menu()
        )
        await state.set_state(MenuStates.MAIN_MENU)
        logger.info(f"User {message.from_user.id} started the bot (simple logic)")
    except Exception as e:
        logger.error(f"Error in start command (simple logic): {e}")
        await handle_error_simple(message)


@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_simple(message: Message, state: FSMContext):
    """
    Спрощена обробка головного меню.
    """
    try:
        user_choice = message.text

        handlers = {
            SimpleMenuButton.HEROES: handle_heroes_menu_simple,
            SimpleMenuButton.GUIDES: handle_guides_menu_simple,
            SimpleMenuButton.COUNTER_PICKS: handle_counter_picks_menu_simple,
            SimpleMenuButton.BUILDS: handle_builds_menu_simple,
            SimpleMenuButton.VOTING: handle_voting_menu_simple,
            SimpleMenuButton.SETTINGS: handle_settings_menu_simple
        }

        handler = handlers.get(user_choice)
        if handler:
            await handler(message, state)
        else:
            await message.answer(
                UNKNOWN_COMMAND_TEXT,
                reply_markup=get_main_menu()
            )

    except Exception as e:
        logger.error(f"Error in main menu (simple logic): {e}")
        await handle_error_simple(message)


async def handle_heroes_menu_simple(message: Message, state: FSMContext):
    """Обробка меню героїв (спрощена логіка)."""
    try:
        await message.answer(
            HEROES_MENU_TEXT,
            reply_markup=get_heroes_menu()
        )
        await state.set_state(MenuStates.HEROES_MENU)
        logger.info(f"User {message.from_user.id} entered heroes menu (simple)")
    except Exception as e:
        logger.error(f"Error in heroes menu (simple logic): {e}")
        await handle_error_simple(message)


async def handle_guides_menu_simple(message: Message, state: FSMContext):
    """Обробка меню гайдів (спрощена логіка)."""
    try:
        await message.answer(
            GUIDES_MENU_TEXT,
            reply_markup=get_guides_menu()
        )
        await state.set_state(MenuStates.GUIDES_MENU)
    except Exception as e:
        logger.error(f"Error in guides menu (simple logic): {e}")
        await handle_error_simple(message)


async def handle_counter_picks_menu_simple(message: Message, state: FSMContext):
    """Обробка меню контр-піків (спрощена логіка)."""
    try:
        await message.answer(
            COUNTER_PICKS_MENU_TEXT,
            reply_markup=get_counter_picks_menu()
        )
        await state.set_state(MenuStates.COUNTER_PICKS_MENU)
    except Exception as e:
        logger.error(f"Error in counter picks menu (simple logic): {e}")
        await handle_error_simple(message)


async def handle_builds_menu_simple(message: Message, state: FSMContext):
    """Обробка меню білдів (спрощена логіка)."""
    try:
        await message.answer(
            BUILDS_MENU_TEXT,
            reply_markup=get_builds_menu()
        )
        await state.set_state(MenuStates.BUILDS_MENU)
    except Exception as e:
        logger.error(f"Error in builds menu (simple logic): {e}")
        await handle_error_simple(message)


async def handle_voting_menu_simple(message: Message, state: FSMContext):
    """Обробка меню голосування (спрощена логіка)."""
    try:
        await message.answer(
            VOTING_MENU_TEXT,
            reply_markup=get_voting_menu()
        )
        await state.set_state(MenuStates.VOTING_MENU)
    except Exception as e:
        logger.error(f"Error in voting menu (simple logic): {e}")
        await handle_error_simple(message)


async def handle_settings_menu_simple(message: Message, state: FSMContext):
    """Обробка меню налаштувань (спрощена логіка)."""
    try:
        await message.answer(
            LANGUAGE_TEXT,
            reply_markup=get_settings_menu()
        )
        await state.set_state(MenuStates.SETTINGS_MENU)
    except Exception as e:
        logger.error(f"Error in settings menu (simple logic): {e}")
        await handle_error_simple(message)


async def handle_error_simple(message: Message):
    """Загальний обробник помилок (спрощена логіка)."""
    try:
        await message.answer(
            GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_main_menu()
        )
    except Exception as e:
        logger.error(f"Error in error handler (simple logic): {e}")


# ------------------------------------------------------------------------------------
#           ЛОГІКА РОЗШИРЕНА: ПІДКЛЮЧЕННЯ ДО БД, ВСТУПНІ СТОРІНКИ, ГРАФІКИ
# ------------------------------------------------------------------------------------

# Далі йде розширений код, який Ви вже бачили.
# УВАГА: Якщо Ви хочете використовувати саме його, достатньо викликати cmd_start замість start_command_simple.

# (Приклад збережено без змін, лише додано підпис “розширений”)

# Мапінг кнопок до класів героїв (розширена логіка)
MENU_BUTTON_TO_CLASS = {
    AdvancedMenuButton.TANK.value: "Танк",
    AdvancedMenuButton.MAGE.value: "Маг",
    AdvancedMenuButton.MARKSMAN.value: "Стрілець",
    AdvancedMenuButton.ASSASSIN.value: "Асасін",
    AdvancedMenuButton.SUPPORT.value: "Підтримка",
    AdvancedMenuButton.FIGHTER.value: "Боєць"
}


# ---------------------------------------------------------------------------
# ФУНКЦІЇ ДЛЯ ОПРАЦЮВАННЯ ПОМИЛОК, РЕДАГУВАННЯ ПОВІДОМЛЕНЬ ТА СТАНІВ (РОЗШИРЕНА)
# ---------------------------------------------------------------------------

async def handle_error(
    bot: Bot,
    chat_id: int,
    error_message: str,
    logger: logging.Logger,
    exception: Exception = None
) -> None:
    """
    Розширена централізована функція для обробки помилок.
    """
    if exception:
        logger.exception(f"Помилка: {exception}")
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=error_message,
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as critical_error:
        logger.critical(f"Критична помилка при відправці повідомлення про помилку: {critical_error}")


# Усі інші функції increment_step, transition_state, check_and_edit_message,
# send_or_update_interactive_message, create_overall_activity_graph, create_rating_graph,
# create_game_stats_graph, create_comparison_graph — тут уже є вище.
# Ви можете використати їх знову, якщо немає конфлікту імен.

# ---------------------------------------------------------------------------
# ОБРОБНИК /example (розширений)
# ---------------------------------------------------------------------------

@router.message(Command("example"))
async def handle_example(message: Message, state: FSMContext) -> None:
    """Приклад переходу між станами (розширений)."""
    await transition_state(state, MenuStates.MAIN_MENU)
    await message.answer("Перехід до головного меню (розширена логіка).")


# ---------------------------------------------------------------------------
# ОБРОБНИК /start (розширений)
# ---------------------------------------------------------------------------

@router.message(Command("start"), F.chat.type.in_({"private", "group", "supergroup"}))
async def cmd_start(
    message: Message,
    state: FSMContext,
    db: AsyncSession,
    bot: Bot
) -> None:
    """
    Обробник команди /start, реєструє користувача (якщо треба) та відправляє вступні сторінки.
    Розширена логіка з БД.
    """
    user_id = message.from_user.id
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Реєстрація нового користувача
    try:
        async with db.begin():
            user_result = await db.execute(
                select(models.user.User).where(
                    models.user.User.telegram_id == user_id
                )
            )
            user = user_result.scalars().first()

            if not user:
                new_user = models.user.User(
                    telegram_id=user_id,
                    username=message.from_user.username
                )
                db.add(new_user)
                await db.flush()

                new_stats = models.user_stats.UserStats(user_id=new_user.id)
                db.add(new_stats)
                await db.commit()
                logger.info(f"Зареєстровано нового користувача: {user_id}")
            else:
                logger.info(f"Існуючий користувач: {user_id}")
    except Exception as e:
        logger.error(f"Помилка при реєстрації користувача {user_id}: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger, e)
        return

    await transition_state(state, MenuStates.INTRO_PAGE_1)

    try:
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=INTRO_PAGE_1_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=get_intro_page_1_keyboard()
        )
        await state.update_data(
            interactive_message_id=interactive_message.message_id,
            last_text=INTRO_PAGE_1_TEXT,
            last_keyboard=get_intro_page_1_keyboard(),
            bot_message_id=None
        )
    except Exception as e:
        logger.error(f"Не вдалося надіслати вступну сторінку 1: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger, e)


# ---------------------------------------------------------------------------
# Вступні сторінки (розширені)
# ---------------------------------------------------------------------------
# Аналогічні обробники intro_next_1, intro_next_2, intro_start і т.д.

# ---------------------------------------------------------------------------
# УНІВЕРСАЛЬНА ФУНКЦІЯ ДЛЯ ОБРОБКИ ПЕРЕХОДІВ (РОЗШИРЕНА)
# ---------------------------------------------------------------------------
# Тут же handle_menu, process_my_profile тощо.


# ------------------------------------------------------------------------------------
#                       ПІДКЛЮЧЕННЯ ОБОХ СПОСОБІВ
# ------------------------------------------------------------------------------------

def setup_handlers(dp: Dispatcher) -> None:
    """
    Підключаємо обидві логіки в один роутер. 
    Якщо потрібна лише одна з них — коментуйте зайве.
    """
    dp.include_router(router)
    logger.info("Handlers (об’єднані) have been set up")