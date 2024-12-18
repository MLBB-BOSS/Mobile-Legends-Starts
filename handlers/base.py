# handlers/base.py

import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import types
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest  # Оновлено для обробки специфічних виключень

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from utils.db import get_user_profile  # Функція для отримання профілю
import models.user
import models.user_stats

from keyboards.menus import (
    MenuButton, get_main_menu, get_profile_menu, get_navigation_menu,
    get_heroes_menu, get_hero_class_menu, get_guides_menu,
    get_counter_picks_menu, get_builds_menu, get_voting_menu, get_statistics_menu,
    get_achievements_menu, get_settings_menu, get_feedback_menu, get_help_menu,
    get_tournaments_menu, get_meta_menu, get_m6_menu, get_gpt_menu, heroes_by_class
)
from keyboards.inline_menus import (
    get_generic_inline_keyboard,
    get_intro_page_1_keyboard,
    get_intro_page_2_keyboard,
    get_intro_page_3_keyboard
)
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
    SEARCH_HERO_RESPONSE_TEXT, CHANGE_USERNAME_RESPONSE_TEXT, MLS_BUTTON_RESPONSE_TEXT,
    UNHANDLED_INLINE_BUTTON_TEXT, MAIN_MENU_BACK_TO_PROFILE_TEXT,
    TOURNAMENT_CREATE_TEXT, TOURNAMENT_VIEW_TEXT, META_HERO_LIST_TEXT,
    META_RECOMMENDATIONS_TEXT, META_UPDATES_TEXT, M6_INFO_TEXT, M6_STATS_TEXT,
    M6_NEWS_TEXT
)

# Ініціалізація логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

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

# Допоміжні функції для надсилання та редагування повідомлень
async def send_new_message(chat_id: int, text: str, reply_markup, state: FSMContext, key: str, bot: Bot):
    try:
        message = await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
        await state.update_data(**{key: message.message_id})
        return message.message_id
    except Exception as e:
        logger.error(f"Failed to send new message: {e}")
        await bot.send_message(chat_id=chat_id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=get_generic_inline_keyboard())
        return None

async def edit_interactive_message(chat_id: int, message_id: int, text: str, reply_markup, state: FSMContext, bot: Bot):
    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )
    except TelegramBadRequest as e:  # Оновлено
        if "message is not modified" in str(e):
            logger.info("Message is not modified. Skipping edit.")
        else:
            logger.error(f"Failed to edit interactive message: {e}")
            interactive_message = await bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=reply_markup
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
    except Exception as e:
        logger.error(f"Failed to edit interactive message: {e}")
        interactive_message = await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

# Обробник команди /start з реєстрацією користувача
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_id = message.from_user.id
    user = await db.execute(select(models.user.User).where(models.user.User.telegram_id == user_id))
    user = user.scalars().first()
    if not user:
        # Створення нового користувача
        new_user = models.user.User(telegram_id=user_id, username=message.from_user.username)
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        # Створення статистики користувача
        new_stats = models.user_stats.UserStats(user_id=new_user.id)
        db.add(new_stats)
        await db.commit()
        logger.info(f"Registered new user: {user_id}")
    else:
        logger.info(f"Existing user: {user_id}")

    # Продовження зі встановленням стану та відправкою вступних сторінок
    await message.delete()
    await state.set_state(MenuStates.INTRO_PAGE_1)
    interactive_message = await bot.send_message(
        chat_id=message.chat.id,
        text=INTRO_PAGE_1_TEXT,
        parse_mode=ParseMode.HTML,
        reply_markup=get_intro_page_1_keyboard()
    )
    await state.update_data(interactive_message_id=interactive_message.message_id)

# Обробники вступних сторінок
@router.callback_query(F.data == "intro_next_1")
async def handle_intro_next_1(callback: CallbackQuery, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')
    chat_id = callback.message.chat.id
    try:
        await edit_interactive_message(
            chat_id=chat_id,
            message_id=interactive_message_id,
            text=INTRO_PAGE_2_TEXT,
            reply_markup=get_intro_page_2_keyboard(),
            state=state,
            bot=bot
        )
    except Exception as e:
        logger.error(f"Failed to edit interactive message: {e}")
        await bot.send_message(
            chat_id=chat_id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
    await state.set_state(MenuStates.INTRO_PAGE_2)
    await callback.answer()

@router.callback_query(F.data == "intro_next_2")
async def handle_intro_next_2(callback: CallbackQuery, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')
    chat_id = callback.message.chat.id
    try:
        await edit_interactive_message(
            chat_id=chat_id,
            message_id=interactive_message_id,
            text=INTRO_PAGE_3_TEXT,
            reply_markup=get_intro_page_3_keyboard(),
            state=state,
            bot=bot
        )
    except Exception as e:
        logger.error(f"Failed to edit interactive message: {e}")
        await bot.send_message(
            chat_id=chat_id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
    await state.set_state(MenuStates.INTRO_PAGE_3)
    await callback.answer()

@router.callback_query(F.data == "intro_start")
async def handle_intro_start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_first_name = callback.from_user.first_name
    main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
    chat_id = callback.message.chat.id

    # Надсилання нового main_message
    main_menu_message_id = await send_new_message(
        chat_id=chat_id,
        text=main_menu_text_formatted,
        reply_markup=get_main_menu(),
        state=state,
        key="bot_message_id",
        bot=bot
    )

    # Редагування interactive_message або надсилання нового
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if interactive_message_id:
        try:
            await edit_interactive_message(
                chat_id=chat_id,
                message_id=interactive_message_id,
                text=MAIN_MENU_DESCRIPTION,
                reply_markup=get_generic_inline_keyboard(),
                state=state,
                bot=bot
            )
        except Exception as e:
            logger.error(f"Failed to edit interactive message: {e}")
            new_message = await bot.send_message(
                chat_id=chat_id,
                text=MAIN_MENU_DESCRIPTION,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_message.message_id)
    else:
        # Якщо interactive_message_id ще не збережено, надсилається нове повідомлення
        new_message = await bot.send_message(
            chat_id=chat_id,
            text=MAIN_MENU_DESCRIPTION,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=new_message.message_id)

    await state.set_state(MenuStates.MAIN_MENU)
    await callback.answer()

# 🔴 **Об'єднаний Обробник Inline кнопок 🔴**

@router.callback_query()
async def handle_inline_buttons(callback: CallbackQuery, state: FSMContext, db: AsyncSession, bot: Bot):
    data = callback.data
    logger.info(f"User {callback.from_user.id} pressed inline button: {data}")
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')
    chat_id = callback.message.chat.id

    if interactive_message_id:
        if data == "mls_button":
            await bot.answer_callback_query(callback.id, text=MLS_BUTTON_RESPONSE_TEXT)
        elif data == "menu_back":
            await state.set_state(MenuStates.MAIN_MENU)
            new_interactive_text = MAIN_MENU_DESCRIPTION
            new_interactive_keyboard = get_generic_inline_keyboard()
            try:
                await edit_interactive_message(
                    chat_id=chat_id,
                    message_id=interactive_message_id,
                    text=new_interactive_text,
                    reply_markup=new_interactive_keyboard,
                    state=state,
                    bot=bot
                )
            except Exception as e:
                logger.error(f"Failed to edit interactive message: {e}")
            main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=callback.from_user.first_name)
            main_menu_message_id = await send_new_message(
                chat_id=chat_id,
                text=main_menu_text_formatted,
                reply_markup=get_main_menu(),
                state=state,
                key="bot_message_id",
                bot=bot
            )
            old_bot_message_id = state_data.get('bot_message_id')
            if old_bot_message_id:
                try:
                    await bot.delete_message(chat_id=chat_id, message_id=old_bot_message_id)
                except Exception as e:
                    logger.error(f"Failed to delete old bot message: {e}")
        else:
            await bot.answer_callback_query(callback.id, text=UNHANDLED_INLINE_BUTTON_TEXT)
    else:
        logger.error("interactive_message_id not found")
        await bot.answer_callback_query(callback.id, text=GENERIC_ERROR_MESSAGE_TEXT)
    
    await callback.answer()

# 🔴 **Уніфіковані Обробники Меню 🔴**

# Функція для обробки переходів між меню
async def handle_menu_transition(
    user_choice: str,
    current_state: str,
    state: FSMContext,
    db: AsyncSession,
    bot: Bot,
    message: Message,
    get_new_menu: callable,
    new_state: str,
    new_interactive_text: str,
    parse_mode: str = ParseMode.HTML
):
    logger.info(f"User {message.from_user.id} selected {user_choice} in {current_state}")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id or interactive_message_id not found")
        main_message_id = await send_new_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu(),
            state=state,
            key="bot_message_id",
            bot=bot
        )
        await state.set_state(MenuStates.MAIN_MENU)
        return

    try:
        # Надсилання нового main_message
        new_bot_message_id = await send_new_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_new_menu(),
            state=state,
            key="bot_message_id",
            bot=bot
        )

        # Видалення старого повідомлення
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Failed to send new message or delete old message: {e}")

    # Редагування interactive_message або надсилання нового
    try:
        await edit_interactive_message(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard(),
            state=state,
            bot=bot
        )
    except Exception as e:
        logger.error(f"Failed to edit interactive message: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    # Встановлення нового стану
    await state.set_state(new_state)

# Обробник меню "Main Menu"
@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in main menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id or interactive_message_id not found")
        main_message_id = await send_new_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu(),
            state=state,
            key="bot_message_id",
            bot=bot
        )
        await state.set_state(MenuStates.MAIN_MENU)
        return

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
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
        new_main_keyboard = get_main_menu()
        new_interactive_text = UNKNOWN_COMMAND_TEXT
        new_state = MenuStates.MAIN_MENU

    # Виклик уніфікованої функції для обробки переходу
    await handle_menu_transition(
        user_choice=user_choice,
        current_state="Main Menu",
        state=state,
        db=db,
        bot=bot,
        message=message,
        get_new_menu=lambda: get_main_menu(),
        new_state=new_state,
        new_interactive_text=new_interactive_text
    )

# Подібні уніфіковані обробники для інших меню
# Наприклад, для Feedback Menu

@router.message(MenuStates.FEEDBACK_MENU)
async def handle_feedback_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Feedback Menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id or interactive_message_id not found")
        main_message_id = await send_new_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu(),
            state=state,
            key="bot_message_id",
            bot=bot
        )
        await state.set_state(MenuStates.MAIN_MENU)
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

    # Виклик уніфікованої функції для обробки переходу
    await handle_menu_transition(
        user_choice=user_choice,
        current_state="Feedback Menu",
        state=state,
        db=db,
        bot=bot,
        message=message,
        get_new_menu=lambda: get_feedback_menu(),
        new_state=new_state,
        new_interactive_text=new_interactive_text
    )

# Аналогічно можна створити уніфіковані обробники для інших меню:
# NAVIGATION_MENU, HEROES_MENU, GUIDES_MENU, COUNTER_PICKS_MENU, BUILDS_MENU,
# VOTING_MENU, PROFILE_MENU, STATISTICS_MENU, ACHIEVEMENTS_MENU, SETTINGS_MENU,
# TOURNAMENTS_MENU, META_MENU, M6_MENU, GPT_MENU

# Обробник зміни імені користувача
@router.message(MenuStates.CHANGE_USERNAME)
async def handle_change_username(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    new_username = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"User {user_id} is changing username to: {new_username}")
    await message.delete()
    if new_username:
        try:
            # Оновлення імені користувача у базі даних
            result = await db.execute(select(models.user.User).where(models.user.User.telegram_id == user_id))
            user = result.scalars().first()
            if user:
                user.username = new_username
                await db.commit()
                response_text = CHANGE_USERNAME_RESPONSE_TEXT.format(new_username=new_username)
                logger.info(f"User {user_id} changed username to: {new_username}")
            else:
                response_text = "❌ Користувача не знайдено. Зареєструйтесь, щоб змінити ім'я."
        except Exception as e:
            logger.error(f"Error updating username for user_id {user_id}: {e}")
            response_text = "❌ Виникла помилка при зміні імені користувача."
    else:
        response_text = "❌ Будь ласка, введіть нове ім'я користувача."
    
    await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
    await state.set_state(MenuStates.SETTINGS_MENU)

# Обробник отримання зворотного зв'язку
@router.message(MenuStates.RECEIVE_FEEDBACK)
async def handle_receive_feedback(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    feedback = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"User {user_id} sent feedback: {feedback}")
    await message.delete()
    if feedback:
        # Збереження зворотного зв'язку у базі даних або надсилання адміністратору
        # Наприклад, збереження у таблиці Feedback
        # from models.feedback import Feedback
        # new_feedback = Feedback(user_id=user_id, feedback=feedback)
        # db.add(new_feedback)
        # await db.commit()
        
        response_text = FEEDBACK_RECEIVED_TEXT
        logger.info(f"Feedback received from user {user_id}")
    else:
        response_text = "❌ Будь ласка, надайте ваш зворотний зв'язок."
    
    await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
    await state.set_state(MenuStates.FEEDBACK_MENU)

# Обробник повідомлення про помилку
@router.message(MenuStates.REPORT_BUG)
async def handle_report_bug(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    bug_report = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"User {user_id} reported a bug: {bug_report}")
    await message.delete()
    if bug_report:
        # Збереження звіту про помилку у базі даних або надсилання адміністратору
        # Наприклад, збереження у таблиці BugReports
        # from models.bug_report import BugReport
        # new_bug = BugReport(user_id=user_id, report=bug_report)
        # db.add(new_bug)
        # await db.commit()
        
        response_text = BUG_REPORT_RECEIVED_TEXT
        logger.info(f"Bug report received from user {user_id}")
    else:
        response_text = "❌ Будь ласка, опишіть помилку, яку ви зустріли."
    
    await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
    await state.set_state(MenuStates.FEEDBACK_MENU)

# Обробник пошуку героя
@router.message(MenuStates.SEARCH_HERO)
async def handle_search_hero(message: Message, state: FSMContext, bot: Bot):
    hero_name = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"User {user_id} is searching for hero: {hero_name}")
    await message.delete()
    if hero_name:
        response_text = SEARCH_HERO_RESPONSE_TEXT.format(hero_name=hero_name)
    else:
        response_text = "❌ Будь ласка, введіть назву героя, якого ви хочете знайти."
    await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
    await state.set_state(MenuStates.HEROES_MENU)

# Обробник пропозиції теми
@router.message(MenuStates.SEARCH_TOPIC)
async def handle_search_topic(message: Message, state: FSMContext, bot: Bot):
    topic = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"User {user_id} is suggesting a topic: {topic}")
    await message.delete()
    if topic:
        response_text = SUGGESTION_RESPONSE_TEXT.format(topic=topic)
    else:
        response_text = "❌ Будь ласка, введіть тему, яку ви хочете запропонувати."
    await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
    await state.set_state(MenuStates.FEEDBACK_MENU)

# Обробник невідомих команд
@router.message()
async def unknown_command(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
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
        await bot.send_message(chat_id=message.chat.id, text=USE_BUTTON_NAVIGATION_TEXT, reply_markup=get_generic_inline_keyboard())
        await state.set_state(current_state)
        return
    else:
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU

    # Надсилання нового main_message
    new_bot_message_id = await send_new_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        state=state,
        key="bot_message_id",
        bot=bot
    )

    # Видалення старого повідомлення, якщо існує
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Failed to delete bot message: {e}")

    # Редагування interactive_message або надсилання нового
    if interactive_message_id:
        try:
            await edit_interactive_message(
                chat_id=message.chat.id,
                message_id=interactive_message_id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard(),
                state=state,
                bot=bot
            )
        except Exception as e:
            logger.error(f"Failed to edit interactive message: {e}")
            interactive_message = await bot.send_message(chat_id=message.chat.id, text=new_interactive_text, reply_markup=get_generic_inline_keyboard())
            await state.update_data(interactive_message_id=interactive_message.message_id)
    else:
        interactive_message = await bot.send_message(chat_id=message.chat.id, text=new_interactive_text, reply_markup=get_generic_inline_keyboard())
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Інтеграція обробників з Dispatcher
def setup_handlers(dp: Router):
    dp.include_router(router)
    # Якщо у вас є інші роутери, включіть їх тут, наприклад:
    # dp.include_router(profile_router)