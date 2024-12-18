# base.py

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import types
from aiogram.enums import ParseMode
from handlers.profile import profile_router
from keyboards.menus import (
    MenuButton, menu_button_to_class, get_main_menu, get_navigation_menu, get_profile_menu,
    get_heroes_menu, get_hero_class_menu, get_guides_menu, get_counter_picks_menu,
    get_builds_menu, get_voting_menu, get_statistics_menu, get_achievements_menu,
    get_settings_menu, get_feedback_menu, get_help_menu, get_tournaments_menu,
    get_meta_menu, get_m6_menu, get_gpt_menu, heroes_by_class
)
from keyboards.inline_menus import (
    get_generic_inline_keyboard, get_intro_page_1_keyboard,
    get_intro_page_2_keyboard, get_intro_page_3_keyboard
)
from texts import (
    INTRO_PAGE_1_TEXT, INTRO_PAGE_2_TEXT, INTRO_PAGE_3_TEXT, MAIN_MENU_TEXT,
    MAIN_MENU_DESCRIPTION, MAIN_MENU_ERROR_TEXT, NAVIGATION_MENU_TEXT,
    NAVIGATION_INTERACTIVE_TEXT, PROFILE_MENU_TEXT, PROFILE_INTERACTIVE_TEXT,
    UNKNOWN_COMMAND_TEXT, ERROR_MESSAGE_TEXT, HEROES_MENU_TEXT,
    HEROES_INTERACTIVE_TEXT, HERO_CLASS_MENU_TEXT, HERO_CLASS_INTERACTIVE_TEXT,
    GUIDES_MENU_TEXT, GUIDES_INTERACTIVE_TEXT, NEW_GUIDES_TEXT,
    POPULAR_GUIDES_TEXT, BEGINNER_GUIDES_TEXT, ADVANCED_TECHNIQUES_TEXT,
    TEAMPLAY_GUIDES_TEXT, COUNTER_PICKS_MENU_TEXT, COUNTER_PICKS_INTERACTIVE_TEXT,
    COUNTER_SEARCH_TEXT, COUNTER_LIST_TEXT, BUILDS_MENU_TEXT,
    BUILDS_INTERACTIVE_TEXT, CREATE_BUILD_TEXT, MY_BUILDS_TEXT,
    POPULAR_BUILDS_TEXT, VOTING_MENU_TEXT, VOTING_INTERACTIVE_TEXT,
    CURRENT_VOTES_TEXT, MY_VOTES_TEXT, SUGGEST_TOPIC_TEXT,
    SUGGESTION_RESPONSE_TEXT, STATISTICS_MENU_TEXT, STATISTICS_INTERACTIVE_TEXT,
    ACTIVITY_TEXT, RANKING_TEXT, GAME_STATS_TEXT, ACHIEVEMENTS_MENU_TEXT,
    ACHIEVEMENTS_INTERACTIVE_TEXT, BADGES_TEXT, PROGRESS_TEXT,
    TOURNAMENT_STATS_TEXT, AWARDS_TEXT, SETTINGS_MENU_TEXT,
    SETTINGS_INTERACTIVE_TEXT, LANGUAGE_TEXT, CHANGE_USERNAME_TEXT,
    UPDATE_ID_TEXT, NOTIFICATIONS_TEXT, FEEDBACK_MENU_TEXT,
    FEEDBACK_INTERACTIVE_TEXT, SEND_FEEDBACK_TEXT, REPORT_BUG_TEXT,
    FEEDBACK_RECEIVED_TEXT, BUG_REPORT_RECEIVED_TEXT, HELP_MENU_TEXT,
    HELP_INTERACTIVE_TEXT, INSTRUCTIONS_TEXT, FAQ_TEXT, HELP_SUPPORT_TEXT,
    GENERIC_ERROR_MESSAGE_TEXT, USE_BUTTON_NAVIGATION_TEXT,
    SEARCH_HERO_RESPONSE_TEXT, CHANGE_USERNAME_RESPONSE_TEXT,
    MLS_BUTTON_RESPONSE_TEXT, UNHANDLED_INLINE_BUTTON_TEXT,
    MAIN_MENU_BACK_TO_PROFILE_TEXT, TOURNAMENT_CREATE_TEXT,
    TOURNAMENT_VIEW_TEXT, META_HERO_LIST_TEXT, META_RECOMMENDATIONS_TEXT,
    META_UPDATES_TEXT, M6_INFO_TEXT, M6_STATS_TEXT, M6_NEWS_TEXT
)
import logging
from database import get_user, create_user, async_session  # Заміна get_db_session на async_session
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram import BaseMiddleware
from typing import Any, Callable, Awaitable

from utils.message_formatter import safe_edit_message_text  # Доданий імпорт

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

# Визначення станів меню
class MenuStates(StatesGroup):
    INTRO_PAGE_1 = State()
    INTRO_PAGE_2 = State()
    INTRO_PAGE_3 = State()
    MAIN_MENU = State()
    NAVIGATION_MENU = State()
    HEROES_MENU = State()
    HERO_CLASS_MENU = State()
    GUIDES_MENU = State()
    COUNTER_PICKS_MENU = State()
    BUILDS_MENU = State()
    VOTING_MENU = State()
    PROFILE_MENU = State()
    STATISTICS_MENU = State()
    ACHIEVEMENTS_MENU = State()
    SETTINGS_MENU = State()
    FEEDBACK_MENU = State()
    HELP_MENU = State()
    SEARCH_HERO = State()
    SEARCH_TOPIC = State()
    CHANGE_USERNAME = State()
    RECEIVE_FEEDBACK = State()
    REPORT_BUG = State()
    TOURNAMENTS_MENU = State()
    META_MENU = State()
    M6_MENU = State()
    GPT_MENU = State()

# Middleware для додавання асинхронної сесії бази даних до обробників
class DatabaseMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[Any], Awaitable[Any]], event: Any, data: dict) -> Any:
        async with async_session() as session:  # Використання async_session
            data['db'] = session
            try:
                return await handler(event, data)
            finally:
                await session.close()  # Коректне закриття сесії

# Додавання middleware до роутера
router.message.middleware(DatabaseMiddleware())
router.callback_query.middleware(DatabaseMiddleware())

# Оновлена команда /start з реєстрацією користувача та логуванням
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name

    logger.info(f"User {user_id} invoked /start with username '{username}'")

    try:
        # Перевірка користувача
        user = await get_user(db, user_id)
        if not user:
            await create_user(db, user_id, username)
            welcome_text = "Ласкаво просимо! Ваш профіль створено."
            logger.info(f"Created new user: {user_id} with username: {username}")
        else:
            welcome_text = "Вітаємо вас знову!"
            logger.info(f"User {user_id} already exists.")

        # Відповідь користувачу
        try:
            await bot.send_message(chat_id=message.chat.id, text=welcome_text)
        except Exception as e:
            logger.error(f"Failed to send welcome message to {user_id}: {e}")

        # Видалення команди /start
        await message.delete()

        # Перехід до стану введення інтро
        await state.set_state(MenuStates.INTRO_PAGE_1)
        try:
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=INTRO_PAGE_1_TEXT,
                parse_mode=ParseMode.HTML,
                reply_markup=get_intro_page_1_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
        except Exception as e:
            logger.error(f"Failed to send intro page 1 to user {user_id}: {e}")
            await bot.send_message(
                chat_id=message.chat.id,
                text=GENERIC_ERROR_MESSAGE_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
    except Exception as e:
        logger.error(f"Error in /start command: {e}")
        await bot.send_message(chat_id=message.chat.id, text="Сталася помилка. Спробуйте пізніше.")

# Обробники переходів між інтро сторінками
@router.callback_query(F.data == "intro_next_1")
async def handle_intro_next_1(callback: CallbackQuery, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')
    if not interactive_message_id:
        logger.error("interactive_message_id not found in state_data")
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await callback.answer()
        return
    try:
        await safe_edit_message_text(
            message=callback.message,
            new_text=INTRO_PAGE_2_TEXT,
            reply_markup=get_intro_page_2_keyboard()
        )
        logger.info(f"Message {interactive_message_id} edited successfully.")
    except Exception as e:
        logger.error(f"Failed to edit intro page 1 to 2 for user {callback.from_user.id}: {e}")
        try:
            new_message = await bot.send_message(
                chat_id=callback.message.chat.id,
                text=GENERIC_ERROR_MESSAGE_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_message.message_id)
        except Exception as ex:
            logger.error(f"Failed to send fallback interactive message for user {callback.from_user.id}: {ex}")
    await state.set_state(MenuStates.INTRO_PAGE_2)
    await callback.answer()

@router.callback_query(F.data == "intro_next_2")
async def handle_intro_next_2(callback: CallbackQuery, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')
    if not interactive_message_id:
        logger.error("interactive_message_id not found in state_data")
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await callback.answer()
        return
    try:
        await safe_edit_message_text(
            message=callback.message,
            new_text=INTRO_PAGE_3_TEXT,
            reply_markup=get_intro_page_3_keyboard()
        )
        logger.info(f"Message {interactive_message_id} edited successfully.")
    except Exception as e:
        logger.error(f"Failed to edit intro page 2 to 3 for user {callback.from_user.id}: {e}")
        try:
            new_message = await bot.send_message(
                chat_id=callback.message.chat.id,
                text=GENERIC_ERROR_MESSAGE_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_message.message_id)
        except Exception as ex:
            logger.error(f"Failed to send fallback interactive message for user {callback.from_user.id}: {ex}")
    await state.set_state(MenuStates.INTRO_PAGE_3)
    await callback.answer()

@router.callback_query(F.data == "intro_start")
async def handle_intro_start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_first_name = callback.from_user.first_name
    main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
    try:
        main_menu_message = await bot.send_message(
            chat_id=callback.message.chat.id,
            text=main_menu_text_formatted,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_menu_message.message_id)
        logger.info(f"Main menu sent to user {callback.from_user.id}.")
    except Exception as e:
        logger.error(f"Failed to send main menu to user {callback.from_user.id}: {e}")

    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')
    if interactive_message_id:
        try:
            await safe_edit_message_text(
                message=callback.message,
                new_text=MAIN_MENU_DESCRIPTION,
                reply_markup=get_generic_inline_keyboard()
            )
            logger.info(f"Interactive message {interactive_message_id} edited successfully.")
        except Exception as e:
            logger.error(f"Failed to edit interactive message for user {callback.from_user.id}: {e}")
            try:
                new_message = await bot.send_message(
                    chat_id=callback.message.chat.id,
                    text=MAIN_MENU_DESCRIPTION,
                    reply_markup=get_generic_inline_keyboard()
                )
                await state.update_data(interactive_message_id=new_message.message_id)
                logger.info(f"Fallback interactive message sent to user {callback.from_user.id}.")
            except Exception as ex:
                logger.error(f"Failed to send fallback interactive message for user {callback.from_user.id}: {ex}")

    await state.set_state(MenuStates.MAIN_MENU)
    await callback.answer()

# Основні обробники меню
@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in main menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдені")
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            await state.update_data(bot_message_id=main_message.message_id)
            await state.set_state(MenuStates.MAIN_MENU)
            logger.info(f"Sent main menu error message to user {message.from_user.id}.")
        except Exception as e:
            logger.error(f"Не вдалося відправити повідомлення з помилкою головного меню користувачу {message.from_user.id}: {e}")
        return
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = None
    if user_choice == MenuButton.NAVIGATION.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    elif user_choice == MenuButton.PROFILE.value:
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    elif user_choice == MenuButton.TOURNAMENTS.value:
        new_main_text = "Меню Турніри"
        new_main_keyboard = get_tournaments_menu()
        new_interactive_text = "Меню Турніри"
        new_state = MenuStates.TOURNAMENTS_MENU
    elif user_choice == MenuButton.META.value:
        new_main_text = "Меню META"
        new_main_keyboard = get_meta_menu()
        new_interactive_text = "Меню META"
        new_state = MenuStates.META_MENU
    elif user_choice == MenuButton.M6.value:
        new_main_text = "Меню M6"
        new_main_keyboard = get_m6_menu()
        new_interactive_text = "Меню M6"
        new_state = MenuStates.M6_MENU
    elif user_choice == MenuButton.GPT.value:
        new_main_text = "Меню GPT"
        new_main_keyboard = get_gpt_menu()
        new_interactive_text = "Меню GPT"
        new_state = MenuStates.GPT_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Unknown command"
        new_state = MenuStates.MAIN_MENU
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
        logger.info(f"Sent new main menu message {new_bot_message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося відправити нове головне меню користувачу {message.from_user.id}: {e}")
        return
    # Видалення попереднього повідомлення
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
        logger.info(f"Deleted previous bot message {bot_message_id} for user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося видалити попереднє повідомлення бота для користувача {message.from_user.id}: {e}")
    await state.update_data(bot_message_id=new_bot_message_id)
    # Редагування інтерактивного повідомлення
    try:
        if interactive_message_id:
            await safe_edit_message_text(
                message=message,
                new_text=new_interactive_text,
                reply_markup=new_interactive_keyboard
            )
            logger.info(f"Interactive message {interactive_message_id} edited successfully for user {message.from_user.id}.")
        else:
            logger.warning("interactive_message_id not found. Sending a new message.")
            new_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=new_interactive_keyboard
            )
            await state.update_data(interactive_message_id=new_message.message_id)
            logger.info(f"Sent new interactive message {new_message.message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Failed to edit or send interactive message for user {message.from_user.id}: {e}")
        try:
            fallback_message = await bot.send_message(
                chat_id=message.chat.id,
                text="Не вдалося оновити повідомлення. Відправлено нове.",
                reply_markup=new_interactive_keyboard
            )
            await state.update_data(interactive_message_id=fallback_message.message_id)
            logger.info(f"Sent fallback interactive message {fallback_message.message_id} to user {message.from_user.id}.")
        except Exception as ex:
            logger.error(f"Не вдалося відправити резервне інтерактивне повідомлення для користувача {message.from_user.id}: {ex}")
    await state.set_state(new_state)

@router.message(MenuStates.FEEDBACK_MENU)
async def handle_feedback_menu_buttons(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Feedback Menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдені")
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            await state.update_data(bot_message_id=main_message.message_id)
            await state.set_state(MenuStates.MAIN_MENU)
            logger.info(f"Sent main menu error message to user {message.from_user.id}.")
        except Exception as e:
            logger.error(f"Не вдалося відправити повідомлення з помилкою головного меню користувачу {message.from_user.id}: {e}")
        return
    new_main_text = ""
    new_main_keyboard = get_feedback_menu()
    new_interactive_text = ""
    new_state = MenuStates.FEEDBACK_MENU
    if user_choice == MenuButton.SEND_FEEDBACK.value:
        new_main_text = SEND_FEEDBACK_TEXT
        new_interactive_text = "Sending feedback"
        new_state = MenuStates.RECEIVE_FEEDBACK
    elif user_choice == MenuButton.REPORT_BUG.value:
        new_main_text = REPORT_BUG_TEXT
        new_interactive_text = "Reporting a bug"
        new_state = MenuStates.REPORT_BUG
    elif user_choice == MenuButton.BACK.value:
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
        new_state = MenuStates.FEEDBACK_MENU
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
        logger.info(f"Sent feedback menu message {new_bot_message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося відправити меню зворотного зв'язку користувачу {message.from_user.id}: {e}")
        return
    # Видалення попереднього повідомлення
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
        logger.info(f"Deleted previous bot message {bot_message_id} for user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося видалити попереднє повідомлення бота для користувача {message.from_user.id}: {e}")
    await state.update_data(bot_message_id=new_bot_message_id)
    # Редагування інтерактивного повідомлення
    try:
        if interactive_message_id:
            await safe_edit_message_text(
                message=message,
                new_text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            logger.info(f"Interactive message {interactive_message_id} edited successfully for user {message.from_user.id}.")
        else:
            logger.warning("interactive_message_id not found. Sending a new message.")
            new_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_message.message_id)
            logger.info(f"Sent new interactive message {new_message.message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Failed to edit or send interactive message for user {message.from_user.id}: {e}")
        try:
            fallback_message = await bot.send_message(
                chat_id=message.chat.id,
                text="Не вдалося оновити повідомлення. Відправлено нове.",
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=fallback_message.message_id)
            logger.info(f"Sent fallback interactive message {fallback_message.message_id} to user {message.from_user.id}.")
        except Exception as ex:
            logger.error(f"Не вдалося відправити резервне інтерактивне повідомлення для користувача {message.from_user.id}: {ex}")
    await state.set_state(new_state)

@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Navigation Menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдені")
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            await state.update_data(bot_message_id=main_message.message_id)
            await state.set_state(MenuStates.MAIN_MENU)
            logger.info(f"Sent main menu error message to user {message.from_user.id}.")
        except Exception as e:
            logger.error(f"Не вдалося відправити повідомлення з помилкою головного меню користувачу {message.from_user.id}: {e}")
        return
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = None
    if user_choice == MenuButton.HEROES.value:
        new_main_text = HEROES_MENU_TEXT
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = HEROES_INTERACTIVE_TEXT
        new_state = MenuStates.HEROES_MENU
    elif user_choice == MenuButton.GUIDES.value:
        new_main_text = GUIDES_MENU_TEXT
        new_main_keyboard = get_guides_menu()
        new_interactive_text = GUIDES_INTERACTIVE_TEXT
        new_state = MenuStates.GUIDES_MENU
    elif user_choice == MenuButton.COUNTER_PICKS.value:
        new_main_text = COUNTER_PICKS_MENU_TEXT
        new_main_keyboard = get_counter_picks_menu()
        new_interactive_text = COUNTER_PICKS_INTERACTIVE_TEXT
        new_state = MenuStates.COUNTER_PICKS_MENU
    elif user_choice == MenuButton.BUILDS.value:
        new_main_text = BUILDS_MENU_TEXT
        new_main_keyboard = get_builds_menu()
        new_interactive_text = BUILDS_INTERACTIVE_TEXT
        new_state = MenuStates.BUILDS_MENU
    elif user_choice == MenuButton.VOTING.value:
        new_main_text = VOTING_MENU_TEXT
        new_main_keyboard = get_voting_menu()
        new_interactive_text = VOTING_INTERACTIVE_TEXT
        new_state = MenuStates.VOTING_MENU
    elif user_choice == MenuButton.TOURNAMENTS.value:
        new_main_text = "Меню Турніри"
        new_main_keyboard = get_tournaments_menu()
        new_interactive_text = "Меню Турніри"
        new_state = MenuStates.TOURNAMENTS_MENU
    elif user_choice == MenuButton.META.value:
        new_main_text = "Меню META"
        new_main_keyboard = get_meta_menu()
        new_interactive_text = "Меню META"
        new_state = MenuStates.META_MENU
    elif user_choice == MenuButton.M6.value:
        new_main_text = "Меню M6"
        new_main_keyboard = get_m6_menu()
        new_interactive_text = "Меню M6"
        new_state = MenuStates.M6_MENU
    elif user_choice == MenuButton.GPT.value:
        new_main_text = "Меню GPT"
        new_main_keyboard = get_gpt_menu()
        new_interactive_text = "Меню GPT"
        new_state = MenuStates.GPT_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Unknown command"
        new_state = MenuStates.NAVIGATION_MENU
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
        logger.info(f"Sent navigation menu message {new_bot_message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося відправити меню навігації користувачу {message.from_user.id}: {e}")
        return
    # Видалення попереднього повідомлення
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
        logger.info(f"Deleted previous bot message {bot_message_id} for user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося видалити попереднє повідомлення бота для користувача {message.from_user.id}: {e}")
    await state.update_data(bot_message_id=new_bot_message_id)
    # Редагування інтерактивного повідомлення
    try:
        if interactive_message_id:
            await safe_edit_message_text(
                message=message,
                new_text=new_interactive_text,
                reply_markup=new_interactive_keyboard
            )
            logger.info(f"Interactive message {interactive_message_id} edited successfully for user {message.from_user.id}.")
        else:
            logger.warning("interactive_message_id not found. Sending a new message.")
            new_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=new_interactive_keyboard
            )
            await state.update_data(interactive_message_id=new_message.message_id)
            logger.info(f"Sent new interactive message {new_message.message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Failed to edit or send interactive message for user {message.from_user.id}: {e}")
        try:
            fallback_message = await bot.send_message(
                chat_id=message.chat.id,
                text="Не вдалося оновити повідомлення. Відправлено нове.",
                reply_markup=new_interactive_keyboard
            )
            await state.update_data(interactive_message_id=fallback_message.message_id)
            logger.info(f"Sent fallback interactive message {fallback_message.message_id} to user {message.from_user.id}.")
        except Exception as ex:
            logger.error(f"Не вдалося відправити резервне інтерактивне повідомлення для користувача {message.from_user.id}: {ex}")
    await state.set_state(new_state)

@router.message(MenuStates.GPT_MENU)
async def handle_gpt_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected '{user_choice}' in GPT Menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдені")
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            await state.update_data(bot_message_id=main_message.message_id)
            await state.set_state(MenuStates.MAIN_MENU)
            logger.info(f"Sent main menu error message to user {message.from_user.id}.")
        except Exception as e:
            logger.error(f"Не вдалося відправити повідомлення з помилкою головного меню користувачу {message.from_user.id}: {e}")
        return
    new_main_text = ""
    new_main_keyboard = get_gpt_menu()
    new_interactive_text = ""
    new_state = MenuStates.GPT_MENU
    if user_choice == MenuButton.GPT_DATA_GENERATION.value:
        new_main_text = "Функціонал Генерації Даних GPT буде доступний пізніше."
        new_interactive_text = "GPT: Генерація Даних"
    elif user_choice == MenuButton.GPT_HINTS.value:
        new_main_text = "Функціонал Порад GPT буде доступний пізніше."
        new_interactive_text = "GPT: Поради"
    elif user_choice == MenuButton.GPT_HERO_STATS.value:
        new_main_text = "Функціонал Статистики Героїв GPT буде доступний пізніше."
        new_interactive_text = "GPT: Статистика Героїв"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
        logger.info(f"Sent GPT menu message {new_bot_message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося відправити GPT меню користувачу {message.from_user.id}: {e}")
        return
    # Видалення попереднього повідомлення
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
        logger.info(f"Deleted previous bot message {bot_message_id} for user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося видалити попереднє повідомлення бота для користувача {message.from_user.id}: {e}")
    await state.update_data(bot_message_id=new_bot_message_id)
    # Редагування інтерактивного повідомлення
    try:
        if interactive_message_id:
            await safe_edit_message_text(
                message=message,
                new_text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            logger.info(f"Interactive message {interactive_message_id} edited successfully for user {message.from_user.id}.")
        else:
            logger.warning("interactive_message_id not found. Sending a new message.")
            new_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_message.message_id)
            logger.info(f"Sent new interactive message {new_message.message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Failed to edit or send interactive message for user {message.from_user.id}: {e}")
        try:
            fallback_message = await bot.send_message(
                chat_id=message.chat.id,
                text="Не вдалося оновити повідомлення. Відправлено нове.",
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=fallback_message.message_id)
            logger.info(f"Sent fallback interactive message {fallback_message.message_id} to user {message.from_user.id}.")
        except Exception as ex:
            logger.error(f"Не вдалося відправити резервне інтерактивне повідомлення для користувача {message.from_user.id}: {ex}")
    await state.set_state(new_state)

@router.message(MenuStates.HEROES_MENU)
async def handle_heroes_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    data = await state.get_data()
    hero_class = data.get('hero_class', 'Unknown')
    heroes_list = data.get('heroes_list', 'No available heroes.')
    logger.info(f"User {message.from_user.id} selected '{user_choice}' in Heroes Menu for class {hero_class}")
    await message.delete()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    if user_choice == MenuButton.BACK.value:
        new_main_text = HEROES_MENU_TEXT
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = HEROES_INTERACTIVE_TEXT
        new_state = MenuStates.HEROES_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = f"Hero Class Menu for {hero_class}. Heroes: {heroes_list}"
        new_state = MenuStates.HERO_CLASS_MENU
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
        logger.info(f"Sent heroes menu message {new_bot_message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося відправити меню героїв користувачу {message.from_user.id}: {e}")
        return
    # Видалення попереднього повідомлення
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
        logger.info(f"Deleted previous bot message {bot_message_id} for user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося видалити попереднє повідомлення бота для користувача {message.from_user.id}: {e}")
    await state.update_data(bot_message_id=new_bot_message_id)
    # Редагування інтерактивного повідомлення
    try:
        if interactive_message_id:
            await safe_edit_message_text(
                message=message,
                new_text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            logger.info(f"Interactive message {interactive_message_id} edited successfully for user {message.from_user.id}.")
        else:
            logger.warning("interactive_message_id not found. Sending a new message.")
            new_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_message.message_id)
            logger.info(f"Sent new interactive message {new_message.message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Failed to edit or send interactive message for user {message.from_user.id}: {e}")
        try:
            fallback_message = await bot.send_message(
                chat_id=message.chat.id,
                text="Не вдалося оновити повідомлення. Відправлено нове.",
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=fallback_message.message_id)
            logger.info(f"Sent fallback interactive message {fallback_message.message_id} to user {message.from_user.id}.")
        except Exception as ex:
            logger.error(f"Не вдалося відправити резервне інтерактивне повідомлення для користувача {message.from_user.id}: {ex}")
    await state.set_state(new_state)

@router.message(MenuStates.GUIDES_MENU)
async def handle_guides_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Guides Menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдені")
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            await state.update_data(bot_message_id=main_message.message_id)
            await state.set_state(MenuStates.MAIN_MENU)
            logger.info(f"Sent main menu error message to user {message.from_user.id}.")
        except Exception as e:
            logger.error(f"Не вдалося відправити повідомлення з помилкою головного меню користувачу {message.from_user.id}: {e}")
        return
    new_main_text = ""
    new_main_keyboard = get_guides_menu()
    new_interactive_text = ""
    new_state = MenuStates.GUIDES_MENU
    if user_choice == MenuButton.NEW_GUIDES.value:
        new_main_text = NEW_GUIDES_TEXT
        new_interactive_text = "New Guides"
    elif user_choice == MenuButton.POPULAR_GUIDES.value:
        new_main_text = POPULAR_GUIDES_TEXT
        new_interactive_text = "Popular Guides"
    elif user_choice == MenuButton.BEGINNER_GUIDES.value:
        new_main_text = BEGINNER_GUIDES_TEXT
        new_interactive_text = "Beginner Guides"
    elif user_choice == MenuButton.ADVANCED_TECHNIQUES.value:
        new_main_text = ADVANCED_TECHNIQUES_TEXT
        new_interactive_text = "Advanced Techniques"
    elif user_choice == MenuButton.TEAMPLAY_GUIDES.value:
        new_main_text = TEAMPLAY_GUIDES_TEXT
        new_interactive_text = "Teamplay Guides"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
        logger.info(f"Sent guides menu message {new_bot_message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося відправити меню гідів користувачу {message.from_user.id}: {e}")
        return
    # Видалення попереднього повідомлення
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
        logger.info(f"Deleted previous bot message {bot_message_id} for user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося видалити попереднє повідомлення бота для користувача {message.from_user.id}: {e}")
    await state.update_data(bot_message_id=new_bot_message_id)
    # Редагування інтерактивного повідомлення
    try:
        if interactive_message_id:
            await safe_edit_message_text(
                message=message,
                new_text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            logger.info(f"Interactive message {interactive_message_id} edited successfully for user {message.from_user.id}.")
        else:
            logger.warning("interactive_message_id not found. Sending a new message.")
            new_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_message.message_id)
            logger.info(f"Sent new interactive message {new_message.message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Failed to edit or send interactive message for user {message.from_user.id}: {e}")
        try:
            fallback_message = await bot.send_message(
                chat_id=message.chat.id,
                text="Не вдалося оновити повідомлення. Відправлено нове.",
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=fallback_message.message_id)
            logger.info(f"Sent fallback interactive message {fallback_message.message_id} to user {message.from_user.id}.")
        except Exception as ex:
            logger.error(f"Не вдалося відправити резервне інтерактивне повідомлення для користувача {message.from_user.id}: {ex}")
    await state.set_state(new_state)

@router.message(MenuStates.COUNTER_PICKS_MENU)
async def handle_counter_picks_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Counter Picks Menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдені")
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            await state.update_data(bot_message_id=main_message.message_id)
            await state.set_state(MenuStates.MAIN_MENU)
            logger.info(f"Sent main menu error message to user {message.from_user.id}.")
        except Exception as e:
            logger.error(f"Не вдалося відправити повідомлення з помилкою головного меню користувачу {message.from_user.id}: {e}")
        return
    new_main_text = ""
    new_main_keyboard = get_counter_picks_menu()
    new_interactive_text = ""
    new_state = MenuStates.COUNTER_PICKS_MENU
    if user_choice == MenuButton.COUNTER_SEARCH.value:
        new_main_text = COUNTER_SEARCH_TEXT
        new_main_keyboard = types.ReplyKeyboardRemove()
        new_interactive_text = "Counter Pick Search"
        new_state = MenuStates.SEARCH_HERO
    elif user_choice == MenuButton.COUNTER_LIST.value:
        new_main_text = COUNTER_LIST_TEXT
        new_interactive_text = "Counter Pick List"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
        logger.info(f"Sent counter picks menu message {new_bot_message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося відправити меню counter picks користувачу {message.from_user.id}: {e}")
        return
    # Видалення попереднього повідомлення
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
        logger.info(f"Deleted previous bot message {bot_message_id} for user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося видалити попереднє повідомлення бота для користувача {message.from_user.id}: {e}")
    await state.update_data(bot_message_id=new_bot_message_id)
    # Редагування інтерактивного повідомлення
    try:
        if interactive_message_id:
            await safe_edit_message_text(
                message=message,
                new_text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            logger.info(f"Interactive message {interactive_message_id} edited successfully for user {message.from_user.id}.")
        else:
            logger.warning("interactive_message_id not found. Sending a new message.")
            new_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_message.message_id)
            logger.info(f"Sent new interactive message {new_message.message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Failed to edit or send interactive message for user {message.from_user.id}: {e}")
        try:
            fallback_message = await bot.send_message(
                chat_id=message.chat.id,
                text="Не вдалося оновити повідомлення. Відправлено нове.",
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=fallback_message.message_id)
            logger.info(f"Sent fallback interactive message {fallback_message.message_id} to user {message.from_user.id}.")
        except Exception as ex:
            logger.error(f"Не вдалося відправити резервне інтерактивне повідомлення для користувача {message.from_user.id}: {ex}")
    await state.set_state(new_state)

@router.message(MenuStates.BUILDS_MENU)
async def handle_builds_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Builds Menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id or interactive_message_id не знайдені")
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            await state.update_data(bot_message_id=main_message.message_id)
            await state.set_state(MenuStates.MAIN_MENU)
            logger.info(f"Sent main menu error message to user {message.from_user.id}.")
        except Exception as e:
            logger.error(f"Не вдалося відправити повідомлення з помилкою головного меню користувачу {message.from_user.id}: {e}")
        return
    new_main_text = ""
    new_main_keyboard = get_builds_menu()
    new_interactive_text = ""
    new_state = MenuStates.BUILDS_MENU
    if user_choice == MenuButton.CREATE_BUILD.value:
        new_main_text = CREATE_BUILD_TEXT
        new_interactive_text = "Creating a build"
    elif user_choice == MenuButton.MY_BUILDS.value:
        new_main_text = MY_BUILDS_TEXT
        new_interactive_text = "My builds"
    elif user_choice == MenuButton.POPULAR_BUILDS.value:
        new_main_text = POPULAR_BUILDS_TEXT
        new_interactive_text = "Popular builds"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
        new_state = MenuStates.BUILDS_MENU
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
        logger.info(f"Sent builds menu message {new_bot_message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося відправити меню builds користувачу {message.from_user.id}: {e}")
        return
    # Видалення попереднього повідомлення
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
        logger.info(f"Deleted previous bot message {bot_message_id} for user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося видалити попереднє повідомлення бота для користувача {message.from_user.id}: {e}")
    await state.update_data(bot_message_id=new_bot_message_id)
    # Редагування інтерактивного повідомлення
    try:
        if interactive_message_id:
            await safe_edit_message_text(
                message=message,
                new_text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            logger.info(f"Interactive message {interactive_message_id} edited successfully for user {message.from_user.id}.")
        else:
            logger.warning("interactive_message_id not found. Sending a new message.")
            new_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_message.message_id)
            logger.info(f"Sent new interactive message {new_message.message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Failed to edit or send interactive message for user {message.from_user.id}: {e}")
        try:
            fallback_message = await bot.send_message(
                chat_id=message.chat.id,
                text="Не вдалося оновити повідомлення. Відправлено нове.",
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=fallback_message.message_id)
            logger.info(f"Sent fallback interactive message {fallback_message.message_id} to user {message.from_user.id}.")
        except Exception as ex:
            logger.error(f"Не вдалося відправити резервне інтерактивне повідомлення для користувача {message.from_user.id}: {ex}")
    await state.set_state(new_state)

@router.message(MenuStates.VOTING_MENU)
async def handle_voting_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Voting Menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдені")
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            await state.update_data(bot_message_id=main_message.message_id)
            await state.set_state(MenuStates.MAIN_MENU)
            logger.info(f"Sent main menu error message to user {message.from_user.id}.")
        except Exception as e:
            logger.error(f"Не вдалося відправити повідомлення з помилкою головного меню користувачу {message.from_user.id}: {e}")
        return
    new_main_text = ""
    new_main_keyboard = get_voting_menu()
    new_interactive_text = ""
    new_state = MenuStates.VOTING_MENU
    if user_choice == MenuButton.CURRENT_VOTES.value:
        new_main_text = CURRENT_VOTES_TEXT
        new_interactive_text = "Current polls"
    elif user_choice == MenuButton.MY_VOTES.value:
        new_main_text = MY_VOTES_TEXT
        new_interactive_text = "My votes"
    elif user_choice == MenuButton.SUGGEST_TOPIC.value:
        new_main_text = SUGGEST_TOPIC_TEXT
        new_main_keyboard = types.ReplyKeyboardRemove()
        new_interactive_text = "Suggest a topic"
        new_state = MenuStates.SEARCH_TOPIC
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
        logger.info(f"Sent voting menu message {new_bot_message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося відправити меню голосувань користувачу {message.from_user.id}: {e}")
        return
    # Видалення попереднього повідомлення
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
        logger.info(f"Deleted previous bot message {bot_message_id} for user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося видалити попереднє повідомлення бота для користувача {message.from_user.id}: {e}")
    await state.update_data(bot_message_id=new_bot_message_id)
    # Редагування інтерактивного повідомлення
    try:
        if interactive_message_id:
            await safe_edit_message_text(
                message=message,
                new_text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            logger.info(f"Interactive message {interactive_message_id} edited successfully for user {message.from_user.id}.")
        else:
            logger.warning("interactive_message_id not found. Sending a new message.")
            new_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_message.message_id)
            logger.info(f"Sent new interactive message {new_message.message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Failed to edit or send interactive message for user {message.from_user.id}: {e}")
        try:
            fallback_message = await bot.send_message(
                chat_id=message.chat.id,
                text="Не вдалося оновити повідомлення. Відправлено нове.",
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=fallback_message.message_id)
            logger.info(f"Sent fallback interactive message {fallback_message.message_id} to user {message.from_user.id}.")
        except Exception as ex:
            logger.error(f"Не вдалося відправити резервне інтерактивне повідомлення для користувача {message.from_user.id}: {ex}")
    await state.set_state(new_state)

@profile_router.message(Command("profile"))
async def show_profile(message: Message, db: AsyncSession, bot: Bot):
    try:
        user = await get_user(db, message.from_user.id)
        if user:
            profile_text = f"Ваш профіль:\nID: {user.id}\nUsername: {user.username}"
        else:
            profile_text = "Ваш профіль порожній або не знайдений."
        try:
            await message.answer(profile_text)
            logger.info(f"Sent profile information to user {message.from_user.id}.")
        except Exception as e:
            logger.error(f"Не вдалося відправити інформацію про профіль користувачу {message.from_user.id}: {e}")
    except Exception as e:
        logger.error(f"Failed to fetch profile for user {message.from_user.id}: {e}")
        try:
            await bot.send_message(chat_id=message.chat.id, text="Сталася помилка при отриманні вашого профілю. Спробуйте пізніше.")
        except Exception as ex:
            logger.error(f"Не вдалося відправити повідомлення про помилку профілю користувачу {message.from_user.id}: {ex}")

@router.message(MenuStates.PROFILE_MENU)
async def handle_profile_menu_buttons(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Profile Menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдені")
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            await state.update_data(bot_message_id=main_message.message_id)
            await state.set_state(MenuStates.MAIN_MENU)
            logger.info(f"Sent main menu error message to user {message.from_user.id}.")
        except Exception as e:
            logger.error(f"Не вдалося відправити повідомлення з помилкою головного меню користувачу {message.from_user.id}: {e}")
        return
    new_main_text = ""
    new_main_keyboard = get_profile_menu()
    new_interactive_text = ""
    new_state = MenuStates.PROFILE_MENU
    if user_choice == MenuButton.STATISTICS.value:
        new_main_text = STATISTICS_MENU_TEXT
        new_main_keyboard = get_statistics_menu()
        new_interactive_text = STATISTICS_INTERACTIVE_TEXT
        new_state = MenuStates.STATISTICS_MENU
    elif user_choice == MenuButton.ACHIEVEMENTS.value:
        new_main_text = ACHIEVEMENTS_MENU_TEXT
        new_main_keyboard = get_achievements_menu()
        new_interactive_text = ACHIEVEMENTS_INTERACTIVE_TEXT
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif user_choice == MenuButton.SETTINGS.value:
        new_main_text = SETTINGS_MENU_TEXT
        new_main_keyboard = get_settings_menu()
        new_interactive_text = SETTINGS_INTERACTIVE_TEXT
        new_state = MenuStates.SETTINGS_MENU
    elif user_choice == MenuButton.FEEDBACK.value:
        new_main_text = FEEDBACK_MENU_TEXT
        new_main_keyboard = get_feedback_menu()
        new_interactive_text = FEEDBACK_INTERACTIVE_TEXT
        new_state = MenuStates.FEEDBACK_MENU
    elif user_choice == MenuButton.HELP.value:
        new_main_text = HELP_MENU_TEXT
        new_main_keyboard = get_help_menu()
        new_interactive_text = HELP_INTERACTIVE_TEXT
        new_state = MenuStates.HELP_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
        new_state = MenuStates.PROFILE_MENU
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
        logger.info(f"Sent profile menu message {new_bot_message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося відправити меню профілю користувачу {message.from_user.id}: {e}")
        return
    # Видалення попереднього повідомлення
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
        logger.info(f"Deleted previous bot message {bot_message_id} for user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося видалити попереднє повідомлення бота для користувача {message.from_user.id}: {e}")
    await state.update_data(bot_message_id=new_bot_message_id)
    # Редагування інтерактивного повідомлення
    try:
        if interactive_message_id:
            await safe_edit_message_text(
                message=message,
                new_text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            logger.info(f"Interactive message {interactive_message_id} edited successfully for user {message.from_user.id}.")
        else:
            logger.warning("interactive_message_id not found. Sending a new message.")
            new_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_message.message_id)
            logger.info(f"Sent new interactive message {new_message.message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Failed to edit or send interactive message for user {message.from_user.id}: {e}")
        try:
            fallback_message = await bot.send_message(
                chat_id=message.chat.id,
                text="Не вдалося оновити повідомлення. Відправлено нове.",
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=fallback_message.message_id)
            logger.info(f"Sent fallback interactive message {fallback_message.message_id} to user {message.from_user.id}.")
        except Exception as ex:
            logger.error(f"Не вдалося відправити резервне інтерактивне повідомлення для користувача {message.from_user.id}: {ex}")
    await state.set_state(new_state)

@router.message(MenuStates.STATISTICS_MENU)
async def handle_statistics_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Statistics Menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдені")
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            await state.update_data(bot_message_id=main_message.message_id)
            await state.set_state(MenuStates.MAIN_MENU)
            logger.info(f"Sent main menu error message to user {message.from_user.id}.")
        except Exception as e:
            logger.error(f"Не вдалося відправити повідомлення з помилкою головного меню користувачу {message.from_user.id}: {e}")
        return
    new_main_text = ""
    new_main_keyboard = get_statistics_menu()
    new_interactive_text = ""
    new_state = MenuStates.STATISTICS_MENU
    if user_choice == MenuButton.ACTIVITY.value:
        new_main_text = ACTIVITY_TEXT
        new_interactive_text = "General Activity"
    elif user_choice == MenuButton.RANKING.value:
        new_main_text = RANKING_TEXT
        new_interactive_text = "Ranking"
    elif user_choice == MenuButton.GAME_STATS.value:
        new_main_text = GAME_STATS_TEXT
        new_interactive_text = "Game Statistics"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
        logger.info(f"Sent statistics menu message {new_bot_message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося відправити меню статистики користувачу {message.from_user.id}: {e}")
        return
    # Видалення попереднього повідомлення
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
        logger.info(f"Deleted previous bot message {bot_message_id} for user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося видалити попереднє повідомлення бота для користувача {message.from_user.id}: {e}")
    await state.update_data(bot_message_id=new_bot_message_id)
    # Редагування інтерактивного повідомлення
    try:
        if interactive_message_id:
            await safe_edit_message_text(
                message=message,
                new_text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            logger.info(f"Interactive message {interactive_message_id} edited successfully for user {message.from_user.id}.")
        else:
            logger.warning("interactive_message_id not found. Sending a new message.")
            new_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_message.message_id)
            logger.info(f"Sent new interactive message {new_message.message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Failed to edit or send interactive message for user {message.from_user.id}: {e}")
        try:
            fallback_message = await bot.send_message(
                chat_id=message.chat.id,
                text="Не вдалося оновити повідомлення. Відправлено нове.",
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=fallback_message.message_id)
            logger.info(f"Sent fallback interactive message {fallback_message.message_id} to user {message.from_user.id}.")
        except Exception as ex:
            logger.error(f"Не вдалося відправити резервне інтерактивне повідомлення для користувача {message.from_user.id}: {ex}")
    await state.set_state(new_state)

@router.message(MenuStates.ACHIEVEMENTS_MENU)
async def handle_achievements_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Achievements Menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдені")
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            await state.update_data(bot_message_id=main_message.message_id)
            await state.set_state(MenuStates.MAIN_MENU)
            logger.info(f"Sent main menu error message to user {message.from_user.id}.")
        except Exception as e:
            logger.error(f"Не вдалося відправити повідомлення з помилкою головного меню користувачу {message.from_user.id}: {e}")
        return
    new_main_text = ""
    new_main_keyboard = get_achievements_menu()
    new_interactive_text = ""
    new_state = MenuStates.ACHIEVEMENTS_MENU
    if user_choice == MenuButton.BADGES.value:
        new_main_text = BADGES_TEXT
        new_interactive_text = "My Badges"
    elif user_choice == MenuButton.PROGRESS.value:
        new_main_text = PROGRESS_TEXT
        new_interactive_text = "Progress"
    elif user_choice == MenuButton.TOURNAMENT_STATS.value:
        new_main_text = TOURNAMENT_STATS_TEXT
        new_interactive_text = "Tournament Statistics"
    elif user_choice == MenuButton.AWARDS.value:
        new_main_text = AWARDS_TEXT
        new_interactive_text = "Received Awards"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
        logger.info(f"Sent achievements menu message {new_bot_message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося відправити меню досягнень користувачу {message.from_user.id}: {e}")
        return
    # Видалення попереднього повідомлення
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
        logger.info(f"Deleted previous bot message {bot_message_id} for user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося видалити попереднє повідомлення бота для користувача {message.from_user.id}: {e}")
    await state.update_data(bot_message_id=new_bot_message_id)
    # Редагування інтерактивного повідомлення
    try:
        if interactive_message_id:
            await safe_edit_message_text(
                message=message,
                new_text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            logger.info(f"Interactive message {interactive_message_id} edited successfully for user {message.from_user.id}.")
        else:
            logger.warning("interactive_message_id not found. Sending a new message.")
            new_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_message.message_id)
            logger.info(f"Sent new interactive message {new_message.message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Failed to edit or send interactive message for user {message.from_user.id}: {e}")
        try:
            fallback_message = await bot.send_message(
                chat_id=message.chat.id,
                text="Не вдалося оновити повідомлення. Відправлено нове.",
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=fallback_message.message_id)
            logger.info(f"Sent fallback interactive message {fallback_message.message_id} to user {message.from_user.id}.")
        except Exception as ex:
            logger.error(f"Не вдалося відправити резервне інтерактивне повідомлення для користувача {message.from_user.id}: {ex}")
    await state.set_state(new_state)

@router.message(MenuStates.SETTINGS_MENU)
async def handle_settings_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Settings Menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдені")
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            await state.update_data(bot_message_id=main_message.message_id)
            await state.set_state(MenuStates.MAIN_MENU)
            logger.info(f"Sent main menu error message to user {message.from_user.id}.")
        except Exception as e:
            logger.error(f"Не вдалося відправити повідомлення з помилкою головного меню користувачу {message.from_user.id}: {e}")
        return
    new_main_text = ""
    new_main_keyboard = get_settings_menu()
    new_interactive_text = ""
    new_state = MenuStates.SETTINGS_MENU
    if user_choice == MenuButton.LANGUAGE.value:
        new_main_text = LANGUAGE_TEXT
        new_interactive_text = "Interface Language"
    elif user_choice == MenuButton.CHANGE_USERNAME.value:
        new_main_text = CHANGE_USERNAME_TEXT
        new_main_keyboard = types.ReplyKeyboardRemove()
        new_interactive_text = "Change Username"
        new_state = MenuStates.CHANGE_USERNAME
    elif user_choice == MenuButton.UPDATE_ID.value:
        new_main_text = UPDATE_ID_TEXT
        new_interactive_text = "Update Player ID"
    elif user_choice == MenuButton.NOTIFICATIONS.value:
        new_main_text = NOTIFICATIONS_TEXT
        new_interactive_text = "Notifications"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
        logger.info(f"Sent settings menu message {new_bot_message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося відправити меню налаштувань користувачу {message.from_user.id}: {e}")
        return
    # Видалення попереднього повідомлення
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
        logger.info(f"Deleted previous bot message {bot_message_id} for user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося видалити попереднє повідомлення бота для користувача {message.from_user.id}: {e}")
    await state.update_data(bot_message_id=new_bot_message_id)
    # Редагування інтерактивного повідомлення
    try:
        if interactive_message_id:
            await safe_edit_message_text(
                message=message,
                new_text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            logger.info(f"Interactive message {interactive_message_id} edited successfully for user {message.from_user.id}.")
        else:
            logger.warning("interactive_message_id not found. Sending a new message.")
            new_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_message.message_id)
            logger.info(f"Sent new interactive message {new_message.message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Failed to edit or send interactive message for user {message.from_user.id}: {e}")
        try:
            fallback_message = await bot.send_message(
                chat_id=message.chat.id,
                text="Не вдалося оновити повідомлення. Відправлено нове.",
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=fallback_message.message_id)
            logger.info(f"Sent fallback interactive message {fallback_message.message_id} to user {message.from_user.id}.")
        except Exception as ex:
            logger.error(f"Не вдалося відправити резервне інтерактивне повідомлення для користувача {message.from_user.id}: {ex}")
    await state.set_state(new_state)

# Обробник CallbackQuery
@router.callback_query()
async def handle_inline_buttons(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = callback.data
    logger.info(f"User {callback.from_user.id} pressed inline button: {data}")
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')
    if interactive_message_id:
        if data == "mls_button":
            try:
                await bot.answer_callback_query(callback.id, text=MLS_BUTTON_RESPONSE_TEXT)
                logger.info(f"Answered MLS button callback for user {callback.from_user.id}.")
            except Exception as e:
                logger.error(f"Не вдалося відповісти на callback query для користувача {callback.from_user.id}: {e}")
        elif data == "menu_back":
            await state.set_state(MenuStates.MAIN_MENU)
            new_interactive_text = MAIN_MENU_DESCRIPTION
            new_interactive_keyboard = get_generic_inline_keyboard()
            try:
                await safe_edit_message_text(
                    message=callback.message,
                    new_text=new_interactive_text,
                    reply_markup=new_interactive_keyboard
                )
                logger.info(f"Edited interactive message {interactive_message_id} to main menu description for user {callback.from_user.id}.")
            except Exception as e:
                logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            try:
                main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=callback.from_user.first_name)
                main_menu_message = await bot.send_message(
                    chat_id=callback.message.chat.id,
                    text=main_menu_text_formatted,
                    reply_markup=get_main_menu()
                )
                await state.update_data(bot_message_id=main_menu_message.message_id)
                logger.info(f"Sent main menu message {main_menu_message.message_id} to user {callback.from_user.id}.")
            except Exception as e:
                logger.error(f"Не вдалося відправити повідомлення головного меню: {e}")
            old_bot_message_id = state_data.get('bot_message_id')
            if old_bot_message_id:
                try:
                    await bot.delete_message(
                        chat_id=callback.message.chat.id,
                        message_id=old_bot_message_id
                    )
                    logger.info(f"Deleted old bot message {old_bot_message_id} for user {callback.from_user.id}.")
                except Exception as e:
                    logger.error(f"Не вдалося видалити старе повідомлення бота: {e}")
        else:
            try:
                await bot.answer_callback_query(callback.id, text=UNHANDLED_INLINE_BUTTON_TEXT)
                logger.info(f"Answered unhandled inline button callback for user {callback.from_user.id}.")
            except Exception as e:
                logger.error(f"Не вдалося відповісти на непередбачену callback query для користувача {callback.from_user.id}: {e}")
    else:
        logger.error("interactive_message_id не знайдено")
        try:
            await bot.answer_callback_query(callback.id, text=GENERIC_ERROR_MESSAGE_TEXT)
            logger.info(f"Answered generic error callback for user {callback.from_user.id}.")
        except Exception as e:
            logger.error(f"Не вдалося відповісти на загальну помилку callback query для користувача {callback.from_user.id}: {e}")
    await callback.answer()

@router.message(MenuStates.SEARCH_HERO)
async def handle_search_hero(message: Message, state: FSMContext, bot: Bot):
    hero_name = message.text.strip()
    logger.info(f"User {message.from_user.id} is searching for hero: {hero_name}")
    await message.delete()
    if hero_name:
        response_text = SEARCH_HERO_RESPONSE_TEXT.format(hero_name=hero_name)
    else:
        response_text = "Будь ласка, введіть ім'я героя, якого ви хочете шукати."
    try:
        await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
        logger.info(f"Sent search hero response to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося відправити відповідь на пошук героя користувачу {message.from_user.id}: {e}")
    await state.set_state(MenuStates.HEROES_MENU)

@router.message(MenuStates.SEARCH_TOPIC)
async def handle_search_topic(message: Message, state: FSMContext, bot: Bot):
    topic = message.text.strip()
    logger.info(f"User {message.from_user.id} is suggesting a topic: {topic}")
    await message.delete()
    if topic:
        response_text = SUGGESTION_RESPONSE_TEXT.format(topic=topic)
    else:
        response_text = "Будь ласка, введіть тему, яку ви хочете запропонувати."
    try:
        await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
        logger.info(f"Sent topic suggestion response to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося відправити відповідь на пропозицію теми користувачу {message.from_user.id}: {e}")
    await state.set_state(MenuStates.FEEDBACK_MENU)

@router.message(MenuStates.CHANGE_USERNAME)
async def handle_change_username(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    new_username = message.text.strip()
    logger.info(f"User {message.from_user.id} is changing username to: {new_username}")
    await message.delete()
    if new_username:
        try:
            # Оновлення імені користувача в базі даних
            await update_username(db, message.from_user.id, new_username)  # Передбачається, що функція update_username існує
            response_text = CHANGE_USERNAME_RESPONSE_TEXT.format(new_username=new_username)
            logger.info(f"User {message.from_user.id} changed username to: {new_username}")
        except Exception as e:
            logger.error(f"Failed to update username for user {message.from_user.id}: {e}")
            response_text = "Не вдалося оновити ваше ім'я користувача. Спробуйте пізніше."
    else:
        response_text = "Будь ласка, введіть нове ім'я користувача."
    try:
        await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
        logger.info(f"Sent change username response to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося відправити відповідь на зміну імені користувача користувачу {message.from_user.id}: {e}")
    await state.set_state(MenuStates.SETTINGS_MENU)

@router.message(MenuStates.RECEIVE_FEEDBACK)
async def handle_receive_feedback(message: Message, state: FSMContext, bot: Bot):
    feedback = message.text.strip()
    logger.info(f"User {message.from_user.id} sent feedback: {feedback}")
    await message.delete()
    if feedback:
        try:
            # Збереження зворотного зв'язку в базі даних або відправка адміністратору
            await save_feedback(message.from_user.id, feedback)  # Передбачається, що функція save_feedback існує
            response_text = FEEDBACK_RECEIVED_TEXT
            logger.info(f"Feedback from user {message.from_user.id} saved successfully.")
        except Exception as e:
            logger.error(f"Failed to save feedback from user {message.from_user.id}: {e}")
            response_text = "Не вдалося зберегти ваш зворотний зв'язок. Спробуйте пізніше."
    else:
        response_text = "Будь ласка, надайте свій зворотний зв'язок."
    try:
        await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
        logger.info(f"Sent feedback received message to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося відправити відповідь на зворотний зв'язок користувачу {message.from_user.id}: {e}")
    await state.set_state(MenuStates.FEEDBACK_MENU)

@router.message(MenuStates.REPORT_BUG)
async def handle_report_bug(message: Message, state: FSMContext, bot: Bot):
    bug_report = message.text.strip()
    logger.info(f"User {message.from_user.id} reported a bug: {bug_report}")
    await message.delete()
    if bug_report:
        try:
            # Збереження звіту про помилку в базі даних або відправка адміністратору
            await save_bug_report(message.from_user.id, bug_report)  # Передбачається, що функція save_bug_report існує
            response_text = BUG_REPORT_RECEIVED_TEXT
            logger.info(f"Bug report from user {message.from_user.id} saved successfully.")
        except Exception as e:
            logger.error(f"Failed to save bug report from user {message.from_user.id}: {e}")
            response_text = "Не вдалося зберегти ваш звіт про помилку. Спробуйте пізніше."
    else:
        response_text = "Будь ласка, опишіть помилку, яку ви зустріли."
    try:
        await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
        logger.info(f"Sent bug report received message to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося відправити відповідь на звіт про помилку користувачу {message.from_user.id}: {e}")
    await state.set_state(MenuStates.FEEDBACK_MENU)

# Обробник невідомих команд
@router.message()
async def unknown_command(message: Message, state: FSMContext, bot: Bot):
    logger.warning(f"Unknown message from {message.from_user.id}: {message.text}")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    current_state = await state.get_state()
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None
    if current_state == MenuStates.MAIN_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Main Menu"
        new_state = MenuStates.MAIN_MENU
    elif current_state == MenuStates.NAVIGATION_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Navigation Screen"
        new_state = MenuStates.NAVIGATION_MENU
    elif current_state == MenuStates.HEROES_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = "Heroes Menu"
        new_state = MenuStates.HEROES_MENU
    elif current_state == MenuStates.HERO_CLASS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        hero_class = data.get('hero_class', 'Tank')
        heroes_list = data.get('heroes_list', 'No available heroes.')
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = f"Hero Class Menu for {hero_class}. Heroes: {heroes_list}"
        new_state = MenuStates.HERO_CLASS_MENU
    elif current_state == MenuStates.GUIDES_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_guides_menu()
        new_interactive_text = "Guides Menu"
        new_state = MenuStates.GUIDES_MENU
    elif current_state == MenuStates.COUNTER_PICKS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_counter_picks_menu()
        new_interactive_text = "Counter Picks Menu"
        new_state = MenuStates.COUNTER_PICKS_MENU
    elif current_state == MenuStates.BUILDS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_builds_menu()
        new_interactive_text = "Builds Menu"
        new_state = MenuStates.BUILDS_MENU
    elif current_state == MenuStates.VOTING_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_voting_menu()
        new_interactive_text = "Voting Menu"
        new_state = MenuStates.VOTING_MENU
    elif current_state == MenuStates.PROFILE_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "Profile Menu"
        new_state = MenuStates.PROFILE_MENU
    elif current_state == MenuStates.STATISTICS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_statistics_menu()
        new_interactive_text = "Statistics Menu"
        new_state = MenuStates.STATISTICS_MENU
    elif current_state == MenuStates.ACHIEVEMENTS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_achievements_menu()
        new_interactive_text = "Achievements Menu"
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif current_state == MenuStates.SETTINGS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_settings_menu()
        new_interactive_text = "Settings Menu"
        new_state = MenuStates.SETTINGS_MENU
    elif current_state in [
        MenuStates.SEARCH_HERO.state,
        MenuStates.SEARCH_TOPIC.state,
        MenuStates.CHANGE_USERNAME.state,
        MenuStates.RECEIVE_FEEDBACK.state,
        MenuStates.REPORT_BUG.state
    ]:
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=USE_BUTTON_NAVIGATION_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            logger.info(f"Sent navigation suggestion to user {message.from_user.id}.")
        except Exception as e:
            logger.error(f"Не вдалося відправити пропозицію навігації користувачу {message.from_user.id}: {e}")
        await state.set_state(current_state)
        return
    else:
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
        logger.info(f"Sent unknown command main menu message {new_bot_message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Не вдалося відправити головне меню користувачу {message.from_user.id}: {e}")
        return
    # Видалення попереднього повідомлення
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
            logger.info(f"Deleted old bot message {bot_message_id} for user {message.from_user.id}.")
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота для користувача {message.from_user.id}: {e}")
    # Редагування інтерактивного повідомлення
    try:
        if interactive_message_id:
            await safe_edit_message_text(
                message=message,
                new_text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            logger.info(f"Interactive message {interactive_message_id} edited successfully for user {message.from_user.id}.")
        else:
            logger.warning("interactive_message_id not found. Sending a new message.")
            new_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_message.message_id)
            logger.info(f"Sent new interactive message {new_message.message_id} to user {message.from_user.id}.")
    except Exception as e:
        logger.error(f"Failed to edit or send interactive message for user {message.from_user.id}: {e}")
        try:
            fallback_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=fallback_message.message_id)
            logger.info(f"Sent fallback interactive message {fallback_message.message_id} to user {message.from_user.id}.")
        except Exception as ex:
            logger.error(f"Не вдалося відправити інтерактивне повідомлення для користувача {message.from_user.id}: {ex}")
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

# Реєстрація обробників
def setup_handlers(dp: Router):
    dp.include_router(router)
    dp.include_router(profile_router)
