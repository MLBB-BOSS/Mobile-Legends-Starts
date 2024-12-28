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
    CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup,
    Message, ReplyKeyboardRemove
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

import models.user
import models.user_stats
from keyboards.inline_menus import (
    get_generic_inline_keyboard,
    get_intro_page_1_keyboard,
    get_intro_page_2_keyboard,
    get_intro_page_3_keyboard
)
from keyboards.menus import (
    MenuButton, get_main_menu, get_profile_menu, get_navigation_menu,
    get_heroes_menu, get_hero_class_menu, get_guides_menu,
    get_counter_picks_menu, get_builds_menu, get_voting_menu, get_statistics_menu,
    get_achievements_menu, get_settings_menu, get_feedback_menu, get_help_menu,
    get_tournaments_menu, get_meta_menu, get_m6_menu, get_gpt_menu, heroes_by_class
)
from states import MenuStates
from texts import (
    INTRO_PAGE_1_TEXT, INTRO_PAGE_2_TEXT, INTRO_PAGE_3_TEXT, MAIN_MENU_TEXT,
    MAIN_MENU_DESCRIPTION, MAIN_MENU_ERROR_TEXT, NAVIGATION_MENU_TEXT,
    NAVIGATION_INTERACTIVE_TEXT, PROFILE_MENU_TEXT, PROFILE_INTERACTIVE_TEXT,
    UNKNOWN_COMMAND_TEXT, ERROR_MESSAGE_TEXT, HEROES_MENU_TEXT,
    HEROES_INTERACTIVE_TEXT, HERO_CLASS_MENU_TEXT, HERO_CLASS_INTERACTIVE_TEXT,
    GUIDES_MENU_TEXT, GUIDES_INTERACTIVE_TEXT, NEW_GUIDES_TEXT, POPULAR_GUIDES_TEXT,
    BEGINNER_GUIDES_TEXT, ADVANCED_TECHNIQUES_TEXT, TEAMPLAY_GUIDES_TEXT,
    COUNTER_PICKS_MENU_TEXT, COUNTER_PICKS_INTERACTIVE_TEXT, COUNTER_SEARCH_TEXT,
    COUNTER_LIST_TEXT, BUILDS_MENU_TEXT, BUILDS_INTERACTIVE_TEXT, CREATE_BUILD_TEXT,
    MY_BUILDS_TEXT, POPULAR_BUILDS_TEXT, VOTING_MENU_TEXT, VOTING_INTERACTIVE_TEXT,
    CURRENT_VOTES_TEXT, MY_VOTES_TEXT, SUGGEST_TOPIC_TEXT, SUGGESTION_RESPONSE_TEXT,
    STATISTICS_MENU_TEXT, STATISTICS_INTERACTIVE_TEXT, ACTIVITY_TEXT, RANKING_TEXT,
    GAME_STATS_TEXT, ACHIEVEMENTS_MENU_TEXT, ACHIEVEMENTS_INTERACTIVE_TEXT,
    BADGES_TEXT, PROGRESS_TEXT, TOURNAMENT_STATS_TEXT, AWARDS_TEXT,
    SETTINGS_MENU_TEXT, SETTINGS_INTERACTIVE_TEXT, LANGUAGE_TEXT,
    CHANGE_USERNAME_TEXT, UPDATE_ID_TEXT, NOTIFICATIONS_TEXT,
    FEEDBACK_MENU_TEXT, FEEDBACK_INTERACTIVE_TEXT, SEND_FEEDBACK_TEXT,
    REPORT_BUG_TEXT, FEEDBACK_RECEIVED_TEXT, BUG_REPORT_RECEIVED_TEXT,
    HELP_MENU_TEXT, HELP_INTERACTIVE_TEXT, INSTRUCTIONS_TEXT, FAQ_TEXT,
    HELP_SUPPORT_TEXT, GENERIC_ERROR_MESSAGE_TEXT, USE_BUTTON_NAVIGATION_TEXT,
    SEARCH_HERO_RESPONSE_TEXT, CHANGE_USERNAME_RESPONSE_TEXT,
    MLS_BUTTON_RESPONSE_TEXT, UNHANDLED_INLINE_BUTTON_TEXT,
    MAIN_MENU_BACK_TO_PROFILE_TEXT, TOURNAMENT_CREATE_TEXT,
    TOURNAMENT_VIEW_TEXT, META_HERO_LIST_TEXT, META_RECOMMENDATIONS_TEXT,
    META_UPDATES_TEXT, M6_INFO_TEXT, M6_STATS_TEXT, M6_NEWS_TEXT,
    GPT_MENU_TEXT, TOURNAMENTS_MENU_TEXT, META_MENU_TEXT,
    LANGUAGE_CHANGED_TEXT, LANGUAGE_ERROR_TEXT, STATS_TEXT
)
from utils.db import get_user_profile
from utils.message_utils import safe_delete_message
from utils.text_formatter import format_profile_text

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

# Мапінг кнопок до класів героїв
MENU_BUTTON_TO_CLASS = {
    MenuButton.TANK.value: "Танк",
    MenuButton.MAGE.value: "Маг",
    MenuButton.MARKSMAN.value: "Стрілець",
    MenuButton.ASSASSIN.value: "Асасін",
    MenuButton.SUPPORT.value: "Підтримка",
    MenuButton.FIGHTER.value: "Боєць"
}

# ---------------------------------------------------------------------------
# ФУНКЦІЇ ДЛЯ ОПРАЦЮВАННЯ ПОМИЛОК, РЕДАГУВАННЯ ПОВІДОМЛЕНЬ І ПЕРЕХОДУ СТАНІВ
# ---------------------------------------------------------------------------

async def handle_error(
    bot: Bot,
    chat_id: int,
    error_message: str,
    logger: logging.Logger,
    exception: Exception = None
) -> None:
    """
    Централізована функція для обробки помилок: повідомлення логеру та відправка
    повідомлення з помилкою користувачеві.
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


async def increment_step(state: FSMContext) -> None:
    """
    Інкрементує крок у FSM. Якщо крок досягає 3, не очищає стан.
    """
    data = await state.get_data()
    step_count = data.get("step_count", 0) + 1
    await state.update_data(step_count=step_count)
    logger.debug(f"Крок інкрементовано до {step_count}")


async def transition_state(state: FSMContext, new_state: State) -> None:
    """
    Встановлення нового стану без очищення існуючих даних.
    """
    await state.set_state(new_state)
    logger.debug(f"Стан встановлено на {new_state}")


async def check_and_edit_message(
    bot: Bot,
    chat_id: int,
    message_id: int,
    new_text: str,
    new_keyboard,
    state: FSMContext,
    parse_mode: str = ParseMode.HTML
) -> None:
    """
    Перевіряє, чи змінився текст або клавіатура, і якщо так — редагує повідомлення.
    """
    state_data = await state.get_data()
    last_text = state_data.get('last_text')
    last_keyboard = state_data.get('last_keyboard')

    if last_text != new_text or last_keyboard != new_keyboard:
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=new_text,
                reply_markup=new_keyboard,
                parse_mode=parse_mode
            )
            await state.update_data(last_text=new_text, last_keyboard=new_keyboard)
            logger.info(f"Повідомлення {message_id} успішно оновлено.")
        except Exception as e:
            logger.error(f"Не вдалося редагувати повідомлення {message_id}: {e}")
            await handle_error(bot, chat_id, GENERIC_ERROR_MESSAGE_TEXT, logger, e)


async def send_or_update_interactive_message(
    bot: Bot,
    chat_id: int,
    text: str,
    keyboard,
    message_id: Optional[int] = None,
    state: Optional[FSMContext] = None,
    parse_mode: str = ParseMode.HTML
) -> Optional[int]:
    """
    Відправляє нове або оновлює існуюче повідомлення (якщо message_id вказано).
    Повертає ID оновленого чи створеного повідомлення.
    """
    if message_id:
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=text,
                reply_markup=keyboard,
                parse_mode=parse_mode
            )
            logger.info(f"Повідомлення {message_id} успішно відредаговано.")
            return message_id
        except Exception as e:
            logger.warning(f"Не вдалося редагувати повідомлення {message_id}: {e}")

    try:
        new_message = await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=keyboard,
            parse_mode=parse_mode
        )
        logger.info(f"Відправлено нове повідомлення {new_message.message_id}.")
        if state:
            await state.update_data(interactive_message_id=new_message.message_id)
        return new_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося відправити повідомлення: {e}")
        return None

# ---------------------------------------------------------------------------
# ФУНКЦІЇ ДЛЯ ГЕНЕРАЦІЇ РІЗНИХ ГРАФІКІВ
# ---------------------------------------------------------------------------

def create_overall_activity_graph() -> bytes:
    """Генерація графіка загальної активності за місяць (умовні дані)."""
    days = list(range(1, 31))
    activity = [i + (i % 5) * 10 for i in days]
    fig = go.Figure(data=go.Bar(x=days, y=activity))
    fig.update_layout(
        title="📊 Загальна Активність за Місяць",
        xaxis_title="Дні",
        yaxis_title="Активність",
        template="plotly_white"
    )
    return fig.to_image(format="png")


def create_rating_graph() -> bytes:
    """Генерація графіка рейтингу за місяць (умовні дані)."""
    months = ['Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень']
    ratings = [1500, 2000, 1800, 2200, 2100, 2300]
    fig = go.Figure(data=go.Scatter(x=months, y=ratings, mode='lines+markers'))
    fig.update_layout(
        title="🥇 Ваш Рейтинг за Місяць",
        xaxis_title="Місяці",
        yaxis_title="Рейтинг",
        template="plotly_white"
    )
    return fig.to_image(format="png")


def create_game_stats_graph() -> bytes:
    """Генерація графіка ігрової статистики героїв (умовні дані)."""
    heroes = ['Hero A', 'Hero B', 'Hero C', 'Hero D', 'Hero E']
    kills = [50, 70, 60, 80, 90]
    deaths = [30, 40, 35, 45, 50]
    assists = [100, 120, 110, 130, 140]
    fig = go.Figure(data=[
        go.Bar(name='Вбивства', x=heroes, y=kills),
        go.Bar(name='Смерті', x=heroes, y=deaths),
        go.Bar(name='Допомоги', x=heroes, y=assists)
    ])
    fig.update_layout(
        barmode='group',
        title="🎮 Ігрова Статистика Героїв",
        xaxis_title="Герої",
        yaxis_title="Кількість",
        template="plotly_white"
    )
    return fig.to_image(format="png")


def create_comparison_graph(
    hero1_stats: dict,
    hero2_stats: dict,
    hero1_name: str,
    hero2_name: str
) -> bytes:
    """
    Генерація графіка порівняння двох героїв.
    Параметри hero1_stats та hero2_stats — словники зі статистикою.
    """
    categories = ['Вбивства', 'Смерті', 'Допомоги']
    hero1_values = [
        hero1_stats.get('kills', 0),
        hero1_stats.get('deaths', 0),
        hero1_stats.get('assists', 0)
    ]
    hero2_values = [
        hero2_stats.get('kills', 0),
        hero2_stats.get('deaths', 0),
        hero2_stats.get('assists', 0)
    ]

    fig = go.Figure(data=[
        go.Bar(name=hero1_name, x=categories, y=hero1_values),
        go.Bar(name=hero2_name, x=categories, y=hero2_values)
    ])
    fig.update_layout(
        barmode='group',
        title=f"⚔️ Порівняння: {hero1_name} vs {hero2_name}",
        xaxis_title="Категорії",
        yaxis_title="Кількість",
        template="plotly_white"
    )
    return fig.to_image(format="png")


# ---------------------------------------------------------------------------
# ОСНОВНИЙ РОУТЕР ТА ОБРОБНИКИ КОМАНД /START, /EXAMPLE, ТА ОПЕРАТОРИ СТАНІВ
# ---------------------------------------------------------------------------

@router.message(Command("example"))
async def handle_example(message: Message, state: FSMContext) -> None:
    """
    Обробник для демонстрації переходу між станами (тільки приклад).
    """
    await transition_state(state, MenuStates.MAIN_MENU)
    await message.answer("Перехід до головного меню.")


@router.message(Command("start"))
async def cmd_start(
    message: Message,
    state: FSMContext,
    db: AsyncSession,
    bot: Bot
) -> None:
    """
    Обробник команди /start, реєструє користувача та відправляє вступні сторінки.
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
# ВСТУПНІ СТОРІНКИ (INTRO_PAGE_1, INTRO_PAGE_2, INTRO_PAGE_3) ТА ЇХ ПЕРЕХОДИ
# ---------------------------------------------------------------------------

@router.callback_query(F.data == "intro_next_1")
async def handle_intro_next_1(
    callback: CallbackQuery,
    state: FSMContext,
    bot: Bot
) -> None:
    """
    Обробник для переходу від INTRO_PAGE_1 до INTRO_PAGE_2.
    """
    current_state = await state.get_state()
    if current_state != MenuStates.INTRO_PAGE_1.state:
        logger.warning(f"Некоректний стан для 'intro_next_1': {current_state}")
        await bot.answer_callback_query(
            callback.id,
            text="Некоректна дія для цього стану.",
            show_alert=True
        )
        return

    await increment_step(state)
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')
    new_text = INTRO_PAGE_2_TEXT
    new_keyboard = get_intro_page_2_keyboard()
    new_state = MenuStates.INTRO_PAGE_2

    await check_and_edit_message(
        bot=bot,
        chat_id=callback.message.chat.id,
        message_id=interactive_message_id,
        new_text=new_text,
        new_keyboard=new_keyboard,
        state=state,
        parse_mode=ParseMode.HTML
    )
    await transition_state(state, new_state)
    await callback.answer()


@router.callback_query(F.data == "intro_next_2")
async def handle_intro_next_2(
    callback: CallbackQuery,
    state: FSMContext,
    bot: Bot
) -> None:
    """
    Обробник для переходу від INTRO_PAGE_2 до INTRO_PAGE_3.
    """
    current_state = await state.get_state()
    if current_state != MenuStates.INTRO_PAGE_2.state:
        logger.warning(f"Некоректний стан для 'intro_next_2': {current_state}")
        await bot.answer_callback_query(
            callback.id,
            text="Некоректна дія для цього стану.",
            show_alert=True
        )
        return

    await increment_step(state)
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')
    new_text = INTRO_PAGE_3_TEXT
    new_keyboard = get_intro_page_3_keyboard()
    new_state = MenuStates.INTRO_PAGE_3

    await check_and_edit_message(
        bot=bot,
        chat_id=callback.message.chat.id,
        message_id=interactive_message_id,
        new_text=new_text,
        new_keyboard=new_keyboard,
        state=state,
        parse_mode=ParseMode.HTML
    )
    await transition_state(state, new_state)
    await callback.answer()


@router.callback_query(F.data == "intro_start")
async def handle_intro_start(
    callback: CallbackQuery,
    state: FSMContext,
    bot: Bot,
    db: AsyncSession
) -> None:
    """
    Обробник для завершення вступних сторінок та переходу до головного меню.
    """
    current_state = await state.get_state()
    if current_state not in [
        MenuStates.INTRO_PAGE_1.state,
        MenuStates.INTRO_PAGE_2.state,
        MenuStates.INTRO_PAGE_3.state
    ]:
        logger.warning(f"Некоректний стан для 'intro_start': {current_state}")
        await bot.answer_callback_query(
            callback.id,
            text="Некоректна дія для цього стану.",
            show_alert=True
        )
        return

    await increment_step(state)
    user_first_name = callback.from_user.first_name or "Користувач"
    main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=user_first_name)

    # Редагуємо існуюче інтерактивне повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')
    new_interactive_text = MAIN_MENU_DESCRIPTION
    new_interactive_keyboard = get_generic_inline_keyboard()

    try:
        await check_and_edit_message(
            bot=bot,
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            new_text=new_interactive_text,
            new_keyboard=new_interactive_keyboard,
            state=state,
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        await handle_error(bot, callback.message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger, e)

    # Відправляємо нове звичайне повідомлення з головним меню
    try:
        main_menu_message = await bot.send_message(
            chat_id=callback.message.chat.id,
            text=main_menu_text_formatted,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_menu_message.message_id)
    except Exception as e:
        logger.error(f"Не вдалося надіслати головне меню: {e}")
        await handle_error(bot, callback.message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger, e)
        return

    # Видаляємо попереднє повідомлення
    old_bot_message_id = state_data.get('bot_message_id')
    if old_bot_message_id:
        await safe_delete_message(bot, callback.message.chat.id, old_bot_message_id)

    await transition_state(state, MenuStates.MAIN_MENU)
    await callback.answer()

# ---------------------------------------------------------------------------
# УНІВЕРСАЛЬНА ФУНКЦІЯ ДЛЯ ОБРОБКИ ПЕРЕХОДІВ МІЖ РІЗНИМИ МЕНЮ
# ---------------------------------------------------------------------------

async def handle_menu(
    user_choice: str,
    message: Message,
    state: FSMContext,
    db: AsyncSession,
    bot: Bot,
    chat_id: int,
    main_menu_error: str,
    main_menu_keyboard_func,
    main_menu_text: str,
    interactive_text: str,
    new_state: State
) -> None:
    """
    Уніфікована функція для обробки різних меню.
    """
    logger.info(f"Користувач обрав '{user_choice}' в меню")
    await increment_step(state)
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        try:
            main_message = await bot.send_message(
                chat_id=chat_id,
                text=main_menu_error,
                reply_markup=main_menu_keyboard_func()
            )
            await state.update_data(bot_message_id=main_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку головного меню: {e}")
            await handle_error(bot, chat_id, GENERIC_ERROR_MESSAGE_TEXT, logger, e)
        return

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    updated_state = new_state

    # Логіка головного меню або будь-яких підменю
    if user_choice == MenuButton.NAVIGATION.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        updated_state = MenuStates.NAVIGATION_MENU
    elif user_choice == MenuButton.PROFILE.value:
        await process_my_profile(message=message, state=state, db=db, bot=bot)
        return
    elif user_choice == MenuButton.TOURNAMENTS.value:
        new_main_text = TOURNAMENTS_MENU_TEXT
        new_main_keyboard = get_tournaments_menu()
        new_interactive_text = TOURNAMENTS_MENU_TEXT
        updated_state = MenuStates.TOURNAMENTS_MENU
    elif user_choice == MenuButton.META.value:
        new_main_text = META_MENU_TEXT
        new_main_keyboard = get_meta_menu()
        new_interactive_text = META_MENU_TEXT
        updated_state = MenuStates.META_MENU
    elif user_choice == MenuButton.M6.value:
        new_main_text = M6_MENU_TEXT
        new_main_keyboard = get_m6_menu()
        new_interactive_text = M6_MENU_TEXT
        updated_state = MenuStates.M6_MENU
    elif user_choice == MenuButton.GPT.value:
        new_main_text = GPT_MENU_TEXT
        new_main_keyboard = get_gpt_menu()
        new_interactive_text = GPT_MENU_TEXT
        updated_state = MenuStates.GPT_MENU
    elif user_choice == MenuButton.BACK.value:
        user_first_name = message.from_user.first_name or "Користувач"
        new_main_text = main_menu_text.format(user_first_name=user_first_name)
        new_main_keyboard = main_menu_keyboard_func()
        new_interactive_text = interactive_text
        updated_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = main_menu_keyboard_func()
        new_interactive_text = "Невідома команда"
        updated_state = MenuStates.MAIN_MENU

    try:
        main_message = await bot.send_message(
            chat_id=chat_id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося надіслати нове повідомлення: {e}")
        await handle_error(bot, chat_id, GENERIC_ERROR_MESSAGE_TEXT, logger, e)
        return

    await safe_delete_message(bot, chat_id, bot_message_id)

    await check_and_edit_message(
        bot=bot,
        chat_id=chat_id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, updated_state)

# ---------------------------------------------------------------------------
# ФУНКЦІЯ ДЛЯ ПЕРЕГЛЯДУ ПРОФІЛЮ
# ---------------------------------------------------------------------------

async def process_my_profile(
    message: Message,
    state: FSMContext,
    db: AsyncSession,
    bot: Bot
) -> None:
    """
    Обробка відображення профілю користувача (швидка демонстрація).
    """
    user_id = message.from_user.id
    profile_data = await get_user_profile(db, user_id)

    await safe_delete_message(bot, message.chat.id, message.message_id)

    if profile_data:
        profile_info = {
            "username": profile_data.get('username', 'N/A'),
            "level": profile_data.get('level', 'N/A'),
            "rating": profile_data.get('rating', 'N/A'),
            "achievements_count": profile_data.get('achievements_count', 'N/A'),
            "screenshots_count": profile_data.get('screenshots_count', 'N/A'),
            "missions_count": profile_data.get('missions_count', 'N/A'),
            "quizzes_count": profile_data.get('quizzes_count', 'N/A'),
            "total_matches": profile_data.get('total_matches', 'N/A'),
            "total_wins": profile_data.get('total_wins', 'N/A'),
            "total_losses": profile_data.get('total_losses', 'N/A'),
            "tournament_participations": profile_data.get('tournament_participations', 'N/A'),
            "badges_count": profile_data.get('badges_count', 'N/A'),
            "last_update": (
                profile_data.get('last_update').strftime('%d.%m.%Y %H:%M')
                if profile_data.get('last_update')
                else 'N/A'
            )
        }

        try:
            formatted_profile_text = format_profile_text(PROFILE_INTERACTIVE_TEXT, profile_info)
        except ValueError as e:
            logger.error(f"Помилка форматування профілю: {e}")
            formatted_profile_text = GENERIC_ERROR_MESSAGE_TEXT

        data = await state.get_data()
        old_bot_message_id = data.get('bot_message_id')
        interactive_message_id = data.get('interactive_message_id')

        try:
            overall_activity_bytes = create_overall_activity_graph()
            rating_bytes = create_rating_graph()
            game_stats_bytes = create_game_stats_graph()
        except Exception as e:
            logger.error(f"Помилка при генерації графіків профілю: {e}")
            overall_activity_bytes = rating_bytes = game_stats_bytes = None

        combined_image_bytes = None
        if overall_activity_bytes and rating_bytes and game_stats_bytes:
            try:
                img1 = Image.open(io.BytesIO(overall_activity_bytes))
                img2 = Image.open(io.BytesIO(rating_bytes))
                img3 = Image.open(io.BytesIO(game_stats_bytes))

                img1 = img1.resize((600, 400))
                img2 = img2.resize((600, 400))
                img3 = img3.resize((600, 400))

                combined_width = max(img1.width, img2.width, img3.width)
                combined_height = img1.height + img2.height + img3.height
                combined_image = Image.new('RGB', (combined_width, combined_height), (255, 255, 255))

                combined_image.paste(img1, (0, 0))
                combined_image.paste(img2, (0, img1.height))
                combined_image.paste(img3, (0, img1.height + img2.height))

                buffer = io.BytesIO()
                combined_image.save(buffer, format="PNG")
                combined_image_bytes = buffer.getvalue()
            except Exception as e:
                logger.error(f"Помилка при об'єднанні графіків: {e}")

        if combined_image_bytes:
            try:
                await bot.edit_message_media(
                    media=types.InputMediaPhoto(
                        media=combined_image_bytes,
                        caption=formatted_profile_text
                    ),
                    chat_id=message.chat.id,
                    message_id=interactive_message_id,
                    reply_markup=get_generic_inline_keyboard()
                )
                logger.info(f"Профіль оновлено (з графіками) для {message.from_user.id}")
            except Exception as e:
                logger.error(f"Не вдалося відредагувати повідомлення профілю: {e}")
                interactive_message_id = await send_or_update_interactive_message(
                    bot=bot,
                    chat_id=message.chat.id,
                    text=formatted_profile_text,
                    keyboard=get_generic_inline_keyboard(),
                    message_id=None,
                    state=state,
                    parse_mode=ParseMode.HTML
                )
        else:
            try:
                await check_and_edit_message(
                    bot=bot,
                    chat_id=message.chat.id,
                    message_id=interactive_message_id,
                    new_text=formatted_profile_text,
                    new_keyboard=get_generic_inline_keyboard(),
                    state=state,
                    parse_mode=ParseMode.HTML
                )
                logger.info(f"Профіль оновлено (без зображення) для {message.from_user.id}")
            except Exception as e:
                logger.error(f"Не вдалося відредагувати повідомлення профілю: {e}")
                interactive_message_id = await send_or_update_interactive_message(
                    bot=bot,
                    chat_id=message.chat.id,
                    text=formatted_profile_text,
                    keyboard=get_generic_inline_keyboard(),
                    message_id=None,
                    state=state,
                    parse_mode=ParseMode.HTML
                )

        try:
            my_profile_message = await bot.send_message(
                chat_id=message.chat.id,
                text="🪪 Мій Профіль\nОберіть опцію для перегляду:",
                reply_markup=get_profile_menu()
            )
            new_bot_message_id = my_profile_message.message_id
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення профілю: {e}")
            await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger, e)
            new_bot_message_id = None

        if old_bot_message_id:
            await safe_delete_message(bot, message.chat.id, old_bot_message_id)

        if new_bot_message_id:
            await state.update_data(bot_message_id=new_bot_message_id)

        await transition_state(state, MenuStates.PROFILE_MENU)
    else:
        error_message = "❌ Дані профілю не знайдено. Зареєструйтесь, щоб переглянути статистику."
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=error_message,
                reply_markup=get_generic_inline_keyboard()
            )
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку: {e}")

        await transition_state(state, MenuStates.MAIN_MENU)


@router.message(F.text == "🪪 Мій Профіль")
async def handle_my_profile_handler(
    message: Message,
    state: FSMContext,
    db: AsyncSession,
    bot: Bot
) -> None:
    """
    Обробник кнопки "🪪 Мій Профіль".
    """
    await increment_step(state)
    await process_my_profile(message, state, db, bot)


# ---------------------------------------------------------------------------
# РЕЄСТРАЦІЯ В РОУТЕРІ
# ---------------------------------------------------------------------------

def setup_handlers(dp: Dispatcher) -> None:
    """
    Функція для підключення всіх описаних у цьому файлі обробників.
    """
    dp.include_router(router)
    # Якщо будуть додаткові роутери, підключайте їх тут, наприклад:
    # dp.include_router(some_other_router)