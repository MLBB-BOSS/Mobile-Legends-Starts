# handlers/base.py

import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import types
from aiogram.enums import ParseMode

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from utils.db import get_user_profile  # Імпорт функції для отримання профілю
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

# Допоміжні функції для спрощення коду
async def send_new_bot_message(bot: Bot, chat_id: int, text: str, reply_markup: types.ReplyKeyboardMarkup):
    """Відправляє нове бот-повідомлення з клавіатурою."""
    return await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)

async def edit_interactive_message(bot: Bot, chat_id: int, message_id: int, text: str, reply_markup: types.InlineKeyboardMarkup):
    """Редагує інтерактивне повідомлення з інлайн-клавіатурою."""
    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Failed to edit interactive message: {e}")
        # Якщо редагування не вдалося, відправляємо нове інтерактивне повідомлення
        new_message = await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup
        )
        return new_message.message_id
    return message_id

async def delete_message_safe(bot: Bot, chat_id: int, message_id: int):
    """Безпечно видаляє повідомлення, обробляючи можливі помилки."""
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        logger.error(f"Failed to delete message {message_id} in chat {chat_id}: {e}")

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
    logger.info(f"Sent INTRO_PAGE_1 to user {user_id}")

# Обробники вступних сторінок
@router.callback_query(Text(equals="intro_next_1"))
async def handle_intro_next_1(callback: CallbackQuery, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')
    chat_id = callback.message.chat.id

    new_text = INTRO_PAGE_2_TEXT
    new_keyboard = get_intro_page_2_keyboard()

    # Редагування інтерактивного повідомлення
    new_interactive_message_id = await edit_interactive_message(
        bot=bot,
        chat_id=chat_id,
        message_id=interactive_message_id,
        text=new_text,
        reply_markup=new_keyboard
    )

    # Оновлення state даних
    await state.update_data(interactive_message_id=new_interactive_message_id)
    await state.set_state(MenuStates.INTRO_PAGE_2)
    await callback.answer()
    logger.info(f"User {callback.from_user.id} moved to INTRO_PAGE_2")

@router.callback_query(Text(equals="intro_next_2"))
async def handle_intro_next_2(callback: CallbackQuery, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')
    chat_id = callback.message.chat.id

    new_text = INTRO_PAGE_3_TEXT
    new_keyboard = get_intro_page_3_keyboard()

    # Редагування інтерактивного повідомлення
    new_interactive_message_id = await edit_interactive_message(
        bot=bot,
        chat_id=chat_id,
        message_id=interactive_message_id,
        text=new_text,
        reply_markup=new_keyboard
    )

    # Оновлення state даних
    await state.update_data(interactive_message_id=new_interactive_message_id)
    await state.set_state(MenuStates.INTRO_PAGE_3)
    await callback.answer()
    logger.info(f"User {callback.from_user.id} moved to INTRO_PAGE_3")

@router.callback_query(Text(equals="intro_start"))
async def handle_intro_start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_first_name = callback.from_user.first_name
    chat_id = callback.message.chat.id

    main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
    main_menu_keyboard = get_main_menu()

    # Відправка нового бот-повідомлення з головним меню
    new_bot_message = await send_new_bot_message(
        bot=bot,
        chat_id=chat_id,
        text="🔰 Оберіть опцію для профілю:",
        reply_markup=get_profile_menu()
    )
    new_bot_message_id = new_bot_message.message_id

    # Видалення старого інтерактивного повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')
    if interactive_message_id:
        await delete_message_safe(bot, chat_id, interactive_message_id)

    # Відправка інтерактивного повідомлення з описом головного меню
    new_interactive_message = await bot.send_message(
        chat_id=chat_id,
        text=MAIN_MENU_DESCRIPTION,
        parse_mode=ParseMode.HTML,
        reply_markup=get_generic_inline_keyboard()
    )
    new_interactive_message_id = new_interactive_message.message_id

    # Оновлення state даних
    await state.update_data(
        bot_message_id=new_bot_message_id,
        interactive_message_id=new_interactive_message_id
    )
    await state.set_state(MenuStates.MAIN_MENU)
    await callback.answer()
    logger.info(f"User {callback.from_user.id} entered MAIN_MENU")

# Обробник кнопки "🪪 Мій Профіль"
@router.message(Text(equals="🪪 Мій Профіль"))
async def handle_my_profile(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_id = message.from_user.id
    profile_data = await get_user_profile(db, user_id)  # Отримання профілю з БД

    chat_id = message.chat.id
    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    interactive_message_id = state_data.get('interactive_message_id')

    if profile_data:
        profile_message = (
            f"🔍 <b>Ваш Профіль:</b>\n\n"
            f"• 🏅 Ім'я користувача: {profile_data['username']}\n"
            f"• 🧬 Рівень: {profile_data['level']}\n"
            f"• 📈 Рейтинг: {profile_data['rating']}\n"
            f"• 🎯 Досягнення: {profile_data['achievements_count']} досягнень\n"
            f"• 📸 Скріншоти: {profile_data['screenshots_count']}\n"
            f"• 🎯 Місії: {profile_data['missions_count']}\n"
            f"• 🧩 Вікторини: {profile_data['quizzes_count']}\n"
            f"• 🏆 Загальні матчі: {profile_data['total_matches']}\n"
            f"• 🥇 Виграші: {profile_data['total_wins']}\n"
            f"• 🥈 Поразки: {profile_data['total_losses']}\n"
            f"• 🌟 Турнірні Участі: {profile_data['tournament_participations']}\n"
            f"• 🏅 Бейджів: {profile_data['badges_count']}\n"
            f"• 📅 Останнє оновлення: {profile_data['last_update'].strftime('%d.%m.%Y %H:%M')}\n\n"
            f"Оберіть опцію, щоб редагувати свій профіль чи переглянути статистику."
        )

        # Видалення старого бот-повідомлення
        if bot_message_id:
            await delete_message_safe(bot, chat_id, bot_message_id)

        # Відправка нового бот-повідомлення з меню профілю
        profile_menu_message = await send_new_bot_message(
            bot=bot,
            chat_id=chat_id,
            text="🔰 Оберіть опцію для профілю:",
            reply_markup=get_profile_menu()
        )
        new_bot_message_id = profile_menu_message.message_id

        # Редагування інтерактивного повідомлення з інформацією про профіль
        if interactive_message_id:
            updated_interactive_message_id = await edit_interactive_message(
                bot=bot,
                chat_id=chat_id,
                message_id=interactive_message_id,
                text=profile_message,
                reply_markup=get_generic_inline_keyboard()
            )
        else:
            # Відправка нового інтерактивного повідомлення, якщо його не існує
            new_interactive_message = await bot.send_message(
                chat_id=chat_id,
                text=profile_message,
                parse_mode=ParseMode.HTML,
                reply_markup=get_generic_inline_keyboard()
            )
            updated_interactive_message_id = new_interactive_message.message_id

        # Оновлення state даних
        await state.update_data(
            bot_message_id=new_bot_message_id,
            interactive_message_id=updated_interactive_message_id
        )

        # Встановлення нового стану
        await state.set_state(MenuStates.PROFILE_MENU)
        logger.info(f"User {user_id} viewed their profile")
    else:
        # Обробка випадку, коли дані профілю не знайдено
        if bot_message_id:
            await delete_message_safe(bot, chat_id, bot_message_id)

        # Відправка повідомлення з помилкою
        error_message = await send_new_bot_message(
            bot=bot,
            chat_id=chat_id,
            text="❌ Дані профілю не знайдено. Зареєструйтесь, щоб переглянути статистику.",
            reply_markup=get_generic_inline_keyboard()
        )
        new_bot_message_id = error_message.message_id

        # Видалення старого інтерактивного повідомлення, якщо існує
        if interactive_message_id:
            await delete_message_safe(bot, chat_id, interactive_message_id)

        # Оновлення state даних
        await state.update_data(
            bot_message_id=new_bot_message_id,
            interactive_message_id=None
        )

        # Встановлення стану на MAIN_MENU
        await state.set_state(MenuStates.MAIN_MENU)
        logger.warning(f"Profile data not found for user {user_id}")

# Обробник меню "Main Menu"
@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"User {user_id} selected {user_choice} in main menu")
    await message.delete()

    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    interactive_message_id = state_data.get('interactive_message_id')

    # Видалення старого бот-повідомлення
    if bot_message_id:
        await delete_message_safe(bot, chat_id, bot_message_id)

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
        new_interactive_text = UNKNOWN_COMMAND_TEXT
        new_state = MenuStates.MAIN_MENU

    # Відправка нового бот-повідомлення з відповідним меню
    new_bot_message = await send_new_bot_message(
        bot=bot,
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = new_bot_message.message_id

    # Оновлення state даних з новим bot_message_id
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагування інтерактивного повідомлення
    if interactive_message_id:
        updated_interactive_message_id = await edit_interactive_message(
            bot=bot,
            chat_id=chat_id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    else:
        # Відправка нового інтерактивного повідомлення, якщо його не існує
        new_interactive_message = await bot.send_message(
            chat_id=chat_id,
            text=new_interactive_text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_generic_inline_keyboard()
        )
        updated_interactive_message_id = new_interactive_message.message_id

    # Оновлення state даних з новим interactive_message_id
    await state.update_data(interactive_message_id=updated_interactive_message_id)

    # Встановлення нового стану
    await state.set_state(new_state)
    logger.info(f"User {user_id} navigated to {new_state}")

# Обробник меню "Feedback Menu"
@router.message(MenuStates.FEEDBACK_MENU)
async def handle_feedback_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"User {user_id} selected {user_choice} in Feedback Menu")
    await message.delete()

    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    interactive_message_id = state_data.get('interactive_message_id')

    # Видалення старого бот-повідомлення
    if bot_message_id:
        await delete_message_safe(bot, chat_id, bot_message_id)

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = None

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

    # Відправка нового бот-повідомлення з відповідним меню
    new_bot_message = await send_new_bot_message(
        bot=bot,
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = new_bot_message.message_id

    # Оновлення state даних з новим bot_message_id
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагування інтерактивного повідомлення
    if interactive_message_id:
        updated_interactive_message_id = await edit_interactive_message(
            bot=bot,
            chat_id=chat_id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    else:
        # Відправка нового інтерактивного повідомлення, якщо його не існує
        new_interactive_message = await bot.send_message(
            chat_id=chat_id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        updated_interactive_message_id = new_interactive_message.message_id

    # Оновлення state даних з новим interactive_message_id
    await state.update_data(interactive_message_id=updated_interactive_message_id)

    # Встановлення нового стану
    await state.set_state(new_state)
    logger.info(f"User {user_id} navigated to {new_state}")

# Обробник меню "Navigation Menu"
@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"User {user_id} selected {user_choice} in Navigation Menu")
    await message.delete()

    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    interactive_message_id = state_data.get('interactive_message_id')

    # Видалення старого бот-повідомлення
    if bot_message_id:
        await delete_message_safe(bot, chat_id, bot_message_id)

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = None
    hero_classes = [
        MenuButton.TANK.value,
        MenuButton.MAGE.value,
        MenuButton.MARKSMAN.value,
        MenuButton.ASSASSIN.value,
        MenuButton.SUPPORT.value,
        MenuButton.FIGHTER.value
    ]

    if user_choice in hero_classes:
        hero_class = MenuButton(user_choice).name  # Перетворення значення кнопки на ім'я
        heroes_list = heroes_by_class.get(hero_class, [])
        heroes_formatted = ", ".join(heroes_list) if heroes_list else "No available heroes."
        new_main_text = HERO_CLASS_MENU_TEXT.format(hero_class=hero_class)
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = HERO_CLASS_INTERACTIVE_TEXT.format(hero_class=hero_class, heroes_list=heroes_formatted)
        new_state = MenuStates.HERO_CLASS_MENU
        await state.update_data(hero_class=hero_class, heroes_list=heroes_formatted)
    elif user_choice == MenuButton.SEARCH_HERO.value:
        new_main_text = SEARCH_HERO_RESPONSE_TEXT.format(hero_name="")
        new_main_keyboard = types.ReplyKeyboardRemove()
        new_interactive_text = "Search Hero"
        new_state = MenuStates.SEARCH_HERO
    elif user_choice == MenuButton.COMPARISON.value:
        new_main_text = "Hero comparison feature is under development."
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = "Compare Heroes"
        new_state = MenuStates.HEROES_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        hero_class = data.get('hero_class', 'Tank')
        heroes_list = data.get('heroes_list', 'No available heroes.')
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = "Unknown command"
        new_state = MenuStates.HEROES_MENU

    # Відправка нового бот-повідомлення з відповідним меню
    new_bot_message = await send_new_bot_message(
        bot=bot,
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = new_bot_message.message_id

    # Оновлення state даних з новим bot_message_id
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагування інтерактивного повідомлення
    if interactive_message_id:
        updated_interactive_message_id = await edit_interactive_message(
            bot=bot,
            chat_id=chat_id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    else:
        # Відправка нового інтерактивного повідомлення, якщо його не існує
        new_interactive_message = await bot.send_message(
            chat_id=chat_id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        updated_interactive_message_id = new_interactive_message.message_id

    # Оновлення state даних з новим interactive_message_id
    await state.update_data(interactive_message_id=updated_interactive_message_id)

    # Встановлення нового стану
    await state.set_state(new_state)
    logger.info(f"User {user_id} navigated to {new_state}")

# Обробник меню "GPT Menu"
@router.message(MenuStates.GPT_MENU)
async def handle_gpt_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"User {user_id} selected '{user_choice}' in GPT Menu")
    await message.delete()

    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    interactive_message_id = state_data.get('interactive_message_id')

    # Видалення старого бот-повідомлення
    if bot_message_id:
        await delete_message_safe(bot, chat_id, bot_message_id)

    new_main_text = ""
    new_main_keyboard = get_gpt_menu()
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
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

    # Відправка нового бот-повідомлення з відповідним меню
    new_bot_message = await send_new_bot_message(
        bot=bot,
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = new_bot_message.message_id

    # Оновлення state даних з новим bot_message_id
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагування інтерактивного повідомлення
    if interactive_message_id:
        updated_interactive_message_id = await edit_interactive_message(
            bot=bot,
            chat_id=chat_id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    else:
        # Відправка нового інтерактивного повідомлення, якщо його не існує
        new_interactive_message = await bot.send_message(
            chat_id=chat_id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        updated_interactive_message_id = new_interactive_message.message_id

    # Оновлення state даних з новим interactive_message_id
    await state.update_data(interactive_message_id=updated_interactive_message_id)

    # Встановлення нового стану
    await state.set_state(new_state)
    logger.info(f"User {user_id} navigated to {new_state}")

# Обробник меню "Heroes Menu"
@router.message(MenuStates.HEROES_MENU)
async def handle_heroes_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"User {user_id} selected {user_choice} in Heroes Menu")
    await message.delete()

    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    interactive_message_id = state_data.get('interactive_message_id')

    # Видалення старого бот-повідомлення
    if bot_message_id:
        await delete_message_safe(bot, chat_id, bot_message_id)

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = MenuStates.HEROES_MENU
    hero_classes = [
        MenuButton.TANK.value,
        MenuButton.MAGE.value,
        MenuButton.MARKSMAN.value,
        MenuButton.ASSASSIN.value,
        MenuButton.SUPPORT.value,
        MenuButton.FIGHTER.value
    ]

    if user_choice in hero_classes:
        hero_class = MenuButton(user_choice).name  # Перетворення значення кнопки на ім'я
        heroes_list = heroes_by_class.get(hero_class, [])
        heroes_formatted = ", ".join(heroes_list) if heroes_list else "No available heroes."
        new_main_text = HERO_CLASS_MENU_TEXT.format(hero_class=hero_class)
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = HERO_CLASS_INTERACTIVE_TEXT.format(hero_class=hero_class, heroes_list=heroes_formatted)
        new_state = MenuStates.HERO_CLASS_MENU
        await state.update_data(hero_class=hero_class, heroes_list=heroes_formatted)
    elif user_choice == MenuButton.SEARCH_HERO.value:
        new_main_text = SEARCH_HERO_RESPONSE_TEXT.format(hero_name="")
        new_main_keyboard = types.ReplyKeyboardRemove()
        new_interactive_text = "Search Hero"
        new_state = MenuStates.SEARCH_HERO
    elif user_choice == MenuButton.COMPARISON.value:
        new_main_text = "Hero comparison feature is under development."
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = "Compare Heroes"
        new_state = MenuStates.HEROES_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        hero_class = state_data.get('hero_class', 'Tank')
        heroes_list = state_data.get('heroes_list', 'No available heroes.')
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = "Unknown command"
        new_state = MenuStates.HEROES_MENU

    # Відправка нового бот-повідомлення з відповідним меню
    new_bot_message = await send_new_bot_message(
        bot=bot,
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = new_bot_message.message_id

    # Оновлення state даних з новим bot_message_id
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагування інтерактивного повідомлення
    if interactive_message_id:
        updated_interactive_message_id = await edit_interactive_message(
            bot=bot,
            chat_id=chat_id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    else:
        # Відправка нового інтерактивного повідомлення, якщо його не існує
        new_interactive_message = await bot.send_message(
            chat_id=chat_id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        updated_interactive_message_id = new_interactive_message.message_id

    # Оновлення state даних з новим interactive_message_id
    await state.update_data(interactive_message_id=updated_interactive_message_id)

    # Встановлення нового стану
    await state.set_state(new_state)
    logger.info(f"User {user_id} navigated to {new_state}")

# Обробник меню "Guides Menu"
@router.message(MenuStates.GUIDES_MENU)
async def handle_guides_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"User {user_id} selected {user_choice} in Guides Menu")
    await message.delete()

    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    interactive_message_id = state_data.get('interactive_message_id')

    # Видалення старого бот-повідомлення
    if bot_message_id:
        await delete_message_safe(bot, chat_id, bot_message_id)

    new_main_text = ""
    new_main_keyboard = get_guides_menu()
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
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

    # Відправка нового бот-повідомлення з відповідним меню
    new_bot_message = await send_new_bot_message(
        bot=bot,
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = new_bot_message.message_id

    # Оновлення state даних з новим bot_message_id
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагування інтерактивного повідомлення
    if interactive_message_id:
        updated_interactive_message_id = await edit_interactive_message(
            bot=bot,
            chat_id=chat_id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    else:
        # Відправка нового інтерактивного повідомлення, якщо його не існує
        new_interactive_message = await bot.send_message(
            chat_id=chat_id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        updated_interactive_message_id = new_interactive_message.message_id

    # Оновлення state даних з новим interactive_message_id
    await state.update_data(interactive_message_id=updated_interactive_message_id)

    # Встановлення нового стану
    await state.set_state(new_state)
    logger.info(f"User {user_id} navigated to {new_state}")

# Обробник меню "Counter Picks Menu"
@router.message(MenuStates.COUNTER_PICKS_MENU)
async def handle_counter_picks_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"User {user_id} selected {user_choice} in Counter Picks Menu")
    await message.delete()

    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    interactive_message_id = state_data.get('interactive_message_id')

    # Видалення старого бот-повідомлення
    if bot_message_id:
        await delete_message_safe(bot, chat_id, bot_message_id)

    new_main_text = ""
    new_main_keyboard = get_counter_picks_menu()
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
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

    # Відправка нового бот-повідомлення з відповідним меню
    new_bot_message = await send_new_bot_message(
        bot=bot,
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = new_bot_message.message_id

    # Оновлення state даних з новим bot_message_id
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагування інтерактивного повідомлення
    if interactive_message_id:
        updated_interactive_message_id = await edit_interactive_message(
            bot=bot,
            chat_id=chat_id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    else:
        # Відправка нового інтерактивного повідомлення, якщо його не існує
        new_interactive_message = await bot.send_message(
            chat_id=chat_id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        updated_interactive_message_id = new_interactive_message.message_id

    # Оновлення state даних з новим interactive_message_id
    await state.update_data(interactive_message_id=updated_interactive_message_id)

    # Встановлення нового стану
    await state.set_state(new_state)
    logger.info(f"User {user_id} navigated to {new_state}")

# Обробник меню "Builds Menu"
@router.message(MenuStates.BUILDS_MENU)
async def handle_builds_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"User {user_id} selected {user_choice} in Builds Menu")
    await message.delete()

    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    interactive_message_id = state_data.get('interactive_message_id')

    # Видалення старого бот-повідомлення
    if bot_message_id:
        await delete_message_safe(bot, chat_id, bot_message_id)

    new_main_text = ""
    new_main_keyboard = get_builds_menu()
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
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

    # Відправка нового бот-повідомлення з відповідним меню
    new_bot_message = await send_new_bot_message(
        bot=bot,
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = new_bot_message.message_id

    # Оновлення state даних з новим bot_message_id
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагування інтерактивного повідомлення
    if interactive_message_id:
        updated_interactive_message_id = await edit_interactive_message(
            bot=bot,
            chat_id=chat_id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    else:
        # Відправка нового інтерактивного повідомлення, якщо його не існує
        new_interactive_message = await bot.send_message(
            chat_id=chat_id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        updated_interactive_message_id = new_interactive_message.message_id

    # Оновлення state даних з новим interactive_message_id
    await state.update_data(interactive_message_id=updated_interactive_message_id)

    # Встановлення нового стану
    await state.set_state(new_state)
    logger.info(f"User {user_id} navigated to {new_state}")

# Обробник меню "Voting Menu"
@router.message(MenuStates.VOTING_MENU)
async def handle_voting_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"User {user_id} selected {user_choice} in Voting Menu")
    await message.delete()

    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    interactive_message_id = state_data.get('interactive_message_id')

    # Видалення старого бот-повідомлення
    if bot_message_id:
        await delete_message_safe(bot, chat_id, bot_message_id)

    new_main_text = ""
    new_main_keyboard = get_voting_menu()
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
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

    # Відправка нового бот-повідомлення з відповідним меню
    new_bot_message = await send_new_bot_message(
        bot=bot,
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = new_bot_message.message_id

    # Оновлення state даних з новим bot_message_id
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагування інтерактивного повідомлення
    if interactive_message_id:
        updated_interactive_message_id = await edit_interactive_message(
            bot=bot,
            chat_id=chat_id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    else:
        # Відправка нового інтерактивного повідомлення, якщо його не існує
        new_interactive_message = await bot.send_message(
            chat_id=chat_id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        updated_interactive_message_id = new_interactive_message.message_id

    # Оновлення state даних з новим interactive_message_id
    await state.update_data(interactive_message_id=updated_interactive_message_id)

    # Встановлення нового стану
    await state.set_state(new_state)
    logger.info(f"User {user_id} navigated to {new_state}")

# Обробник меню "Profile Menu"
@router.message(MenuStates.PROFILE_MENU)
async def handle_profile_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"User {user_id} selected {user_choice} in Profile Menu")
    await message.delete()

    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    interactive_message_id = state_data.get('interactive_message_id')

    # Видалення старого бот-повідомлення
    if bot_message_id:
        await delete_message_safe(bot, chat_id, bot_message_id)

    new_main_text = ""
    new_main_keyboard = get_profile_menu()
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
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

    # Відправка нового бот-повідомлення з відповідним меню
    new_bot_message = await send_new_bot_message(
        bot=bot,
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = new_bot_message.message_id

    # Оновлення state даних з новим bot_message_id
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагування інтерактивного повідомлення
    if interactive_message_id:
        updated_interactive_message_id = await edit_interactive_message(
            bot=bot,
            chat_id=chat_id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    else:
        # Відправка нового інтерактивного повідомлення, якщо його не існує
        new_interactive_message = await bot.send_message(
            chat_id=chat_id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        updated_interactive_message_id = new_interactive_message.message_id

    # Оновлення state даних з новим interactive_message_id
    await state.update_data(interactive_message_id=updated_interactive_message_id)

    # Встановлення нового стану
    await state.set_state(new_state)
    logger.info(f"User {user_id} navigated to {new_state}")

# Обробник меню "Statistics Menu"
@router.message(MenuStates.STATISTICS_MENU)
async def handle_statistics_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"User {user_id} selected {user_choice} in Statistics Menu")
    await message.delete()

    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    interactive_message_id = state_data.get('interactive_message_id')

    # Видалення старого бот-повідомлення
    if bot_message_id:
        await delete_message_safe(bot, chat_id, bot_message_id)

    new_main_text = ""
    new_main_keyboard = get_statistics_menu()
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
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
        new_state = MenuStates.STATISTICS_MENU

    # Відправка нового бот-повідомлення з відповідним меню
    new_bot_message = await send_new_bot_message(
        bot=bot,
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = new_bot_message.message_id

    # Оновлення state даних з новим bot_message_id
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагування інтерактивного повідомлення
    if interactive_message_id:
        updated_interactive_message_id = await edit_interactive_message(
            bot=bot,
            chat_id=chat_id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    else:
        # Відправка нового інтерактивного повідомлення, якщо його не існує
        new_interactive_message = await bot.send_message(
            chat_id=chat_id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        updated_interactive_message_id = new_interactive_message.message_id

    # Оновлення state даних з новим interactive_message_id
    await state.update_data(interactive_message_id=updated_interactive_message_id)

    # Встановлення нового стану
    await state.set_state(new_state)
    logger.info(f"User {user_id} navigated to {new_state}")

# Обробник меню "Achievements Menu"
@router.message(MenuStates.ACHIEVEMENTS_MENU)
async def handle_achievements_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"User {user_id} selected {user_choice} in Achievements Menu")
    await message.delete()

    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    interactive_message_id = state_data.get('interactive_message_id')

    # Видалення старого бот-повідомлення
    if bot_message_id:
        await delete_message_safe(bot, chat_id, bot_message_id)

    new_main_text = ""
    new_main_keyboard = get_achievements_menu()
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
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

    # Відправка нового бот-повідомлення з відповідним меню
    new_bot_message = await send_new_bot_message(
        bot=bot,
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = new_bot_message.message_id

    # Оновлення state даних з новим bot_message_id
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагування інтерактивного повідомлення
    if interactive_message_id:
        updated_interactive_message_id = await edit_interactive_message(
            bot=bot,
            chat_id=chat_id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    else:
        # Відправка нового інтерактивного повідомлення, якщо його не існує
        new_interactive_message = await bot.send_message(
            chat_id=chat_id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        updated_interactive_message_id = new_interactive_message.message_id

    # Оновлення state даних з новим interactive_message_id
    await state.update_data(interactive_message_id=updated_interactive_message_id)

    # Встановлення нового стану
    await state.set_state(new_state)
    logger.info(f"User {user_id} navigated to {new_state}")

# Обробник меню "Settings Menu"
@router.message(MenuStates.SETTINGS_MENU)
async def handle_settings_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"User {user_id} selected {user_choice} in Settings Menu")
    await message.delete()

    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    interactive_message_id = state_data.get('interactive_message_id')

    # Видалення старого бот-повідомлення
    if bot_message_id:
        await delete_message_safe(bot, chat_id, bot_message_id)

    new_main_text = ""
    new_main_keyboard = get_settings_menu()
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
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

    # Відправка нового бот-повідомлення з відповідним меню
    new_bot_message = await send_new_bot_message(
        bot=bot,
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = new_bot_message.message_id

    # Оновлення state даних з новим bot_message_id
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагування інтерактивного повідомлення
    if interactive_message_id:
        updated_interactive_message_id = await edit_interactive_message(
            bot=bot,
            chat_id=chat_id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    else:
        # Відправка нового інтерактивного повідомлення, якщо його не існує
        new_interactive_message = await bot.send_message(
            chat_id=chat_id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        updated_interactive_message_id = new_interactive_message.message_id

    # Оновлення state даних з новим interactive_message_id
    await state.update_data(interactive_message_id=updated_interactive_message_id)

    # Встановлення нового стану
    await state.set_state(new_state)
    logger.info(f"User {user_id} navigated to {new_state}")

# Обробник зміни імені користувача
@router.message(MenuStates.CHANGE_USERNAME)
async def handle_change_username(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    new_username = message.text.strip()
    user_id = message.from_user.id
    chat_id = message.chat.id
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

    # Видалення старого бот-повідомлення
    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    if bot_message_id:
        await delete_message_safe(bot, chat_id, bot_message_id)

    # Відправка повідомлення про результат зміни
    result_message = await send_new_bot_message(
        bot=bot,
        chat_id=chat_id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard()
    )
    new_bot_message_id = result_message.message_id

    # Оновлення state даних з новим bot_message_id
    await state.update_data(bot_message_id=new_bot_message_id)

    # Видалення старого інтерактивного повідомлення, якщо необхідно
    interactive_message_id = state_data.get('interactive_message_id')
    if interactive_message_id:
        await delete_message_safe(bot, chat_id, interactive_message_id)

    # Відправка інтерактивного повідомлення з меню налаштувань
    new_interactive_message = await bot.send_message(
        chat_id=chat_id,
        text=SETTINGS_INTERACTIVE_TEXT,
        reply_markup=get_generic_inline_keyboard()
    )
    new_interactive_message_id = new_interactive_message.message_id

    # Оновлення state даних з новим interactive_message_id
    await state.update_data(interactive_message_id=new_interactive_message_id)

    # Встановлення стану назад до SETTINGS_MENU
    await state.set_state(MenuStates.SETTINGS_MENU)
    logger.info(f"User {user_id} completed username change")

# Обробник отримання зворотного зв'язку
@router.message(MenuStates.RECEIVE_FEEDBACK)
async def handle_receive_feedback(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    feedback = message.text.strip()
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"User {user_id} sent feedback: {feedback}")
    await message.delete()

    if feedback:
        try:
            # Припустимо, що є модель Feedback
            # from models.feedback import Feedback
            # new_feedback = Feedback(user_id=user_id, feedback=feedback)
            # db.add(new_feedback)
            # await db.commit()
            # Можна також надсилати зворотний зв'язок адміністратору
            response_text = FEEDBACK_RECEIVED_TEXT
            logger.info(f"Feedback received from user {user_id}")
        except Exception as e:
            logger.error(f"Error saving feedback from user_id {user_id}: {e}")
            response_text = "❌ Виникла помилка при збереженні вашого зворотного зв'язку."
    else:
        response_text = "❌ Будь ласка, надайте ваш зворотний зв'язок."

    # Видалення старого бот-повідомлення
    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    if bot_message_id:
        await delete_message_safe(bot, chat_id, bot_message_id)

    # Відправка повідомлення про отримання зворотного зв'язку
    feedback_received_message = await send_new_bot_message(
        bot=bot,
        chat_id=chat_id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard()
    )
    new_bot_message_id = feedback_received_message.message_id

    # Оновлення state даних з новим bot_message_id
    await state.update_data(bot_message_id=new_bot_message_id)

    # Видалення старого інтерактивного повідомлення, якщо необхідно
    interactive_message_id = state_data.get('interactive_message_id')
    if interactive_message_id:
        await delete_message_safe(bot, chat_id, interactive_message_id)

    # Відправка інтерактивного повідомлення з меню зворотного зв'язку
    new_interactive_message = await bot.send_message(
        chat_id=chat_id,
        text=FEEDBACK_INTERACTIVE_TEXT,
        reply_markup=get_generic_inline_keyboard()
    )
    new_interactive_message_id = new_interactive_message.message_id

    # Оновлення state даних з новим interactive_message_id
    await state.update_data(interactive_message_id=new_interactive_message_id)

    # Встановлення стану назад до FEEDBACK_MENU
    await state.set_state(MenuStates.FEEDBACK_MENU)
    logger.info(f"User {user_id} completed sending feedback")

# Обробник повідомлення про помилку
@router.message(MenuStates.REPORT_BUG)
async def handle_report_bug(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    bug_report = message.text.strip()
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"User {user_id} reported a bug: {bug_report}")
    await message.delete()

    if bug_report:
        try:
            # Припустимо, що є модель BugReport
            # from models.bug_report import BugReport
            # new_bug = BugReport(user_id=user_id, report=bug_report)
            # db.add(new_bug)
            # await db.commit()
            response_text = BUG_REPORT_RECEIVED_TEXT
            logger.info(f"Bug report received from user {user_id}")
        except Exception as e:
            logger.error(f"Error saving bug report from user_id {user_id}: {e}")
            response_text = "❌ Виникла помилка при збереженні вашого звіту про помилку."
    else:
        response_text = "❌ Будь ласка, опишіть помилку, яку ви зустріли."

    # Видалення старого бот-повідомлення
    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    if bot_message_id:
        await delete_message_safe(bot, chat_id, bot_message_id)

    # Відправка повідомлення про отримання звіту про помилку
    bug_report_received_message = await send_new_bot_message(
        bot=bot,
        chat_id=chat_id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard()
    )
    new_bot_message_id = bug_report_received_message.message_id

    # Оновлення state даних з новим bot_message_id
    await state.update_data(bot_message_id=new_bot_message_id)

    # Видалення старого інтерактивного повідомлення, якщо необхідно
    interactive_message_id = state_data.get('interactive_message_id')
    if interactive_message_id:
        await delete_message_safe(bot, chat_id, interactive_message_id)

    # Відправка інтерактивного повідомлення з меню зворотного зв'язку
    new_interactive_message = await bot.send_message(
        chat_id=chat_id,
        text=FEEDBACK_INTERACTIVE_TEXT,
        reply_markup=get_generic_inline_keyboard()
    )
    new_interactive_message_id = new_interactive_message.message_id

    # Оновлення state даних з новим interactive_message_id
    await state.update_data(interactive_message_id=new_interactive_message_id)

    # Встановлення стану назад до FEEDBACK_MENU
    await state.set_state(MenuStates.FEEDBACK_MENU)
    logger.info(f"User {user_id} completed reporting a bug")

# Обробник меню "Tournaments Menu"
@router.message(MenuStates.TOURNAMENTS_MENU)
async def handle_tournaments_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"User {user_id} selected '{user_choice}' in Tournaments Menu")
    await message.delete()

    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    interactive_message_id = state_data.get('interactive_message_id')

    # Видалення старого бот-повідомлення
    if bot_message_id:
        await delete_message_safe(bot, chat_id, bot_message_id)

    new_main_text = ""
    new_main_keyboard = get_tournaments_menu()
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = MenuStates.TOURNAMENTS_MENU

    if user_choice == MenuButton.CREATE_TOURNAMENT.value:
        new_main_text = TOURNAMENT_CREATE_TEXT
        new_interactive_text = "Tournament Creation"
    elif user_choice == MenuButton.VIEW_TOURNAMENTS.value:
        new_main_text = TOURNAMENT_VIEW_TEXT
        new_interactive_text = "View Tournaments"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"

    # Відправка нового бот-повідомлення з відповідним меню
    new_bot_message = await send_new_bot_message(
        bot=bot,
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = new_bot_message.message_id

    # Оновлення state даних з новим bot_message_id
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагування інтерактивного повідомлення
    if interactive_message_id:
        updated_interactive_message_id = await edit_interactive_message(
            bot=bot,
            chat_id=chat_id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    else:
        # Відправка нового інтерактивного повідомлення, якщо його не існує
        new_interactive_message = await bot.send_message(
            chat_id=chat_id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        updated_interactive_message_id = new_interactive_message.message_id

    # Оновлення state даних з новим interactive_message_id
    await state.update_data(interactive_message_id=updated_interactive_message_id)

    # Встановлення нового стану
    await state.set_state(new_state)
    logger.info(f"User {user_id} navigated to {new_state}")

# Обробник меню "META Menu"
@router.message(MenuStates.META_MENU)
async def handle_meta_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"User {user_id} selected '{user_choice}' in META Menu")
    await message.delete()

    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    interactive_message_id = state_data.get('interactive_message_id')

    # Видалення старого бот-повідомлення
    if bot_message_id:
        await delete_message_safe(bot, chat_id, bot_message_id)

    new_main_text = ""
    new_main_keyboard = get_meta_menu()
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = MenuStates.META_MENU

    if user_choice == MenuButton.META_HERO_LIST.value:
        new_main_text = META_HERO_LIST_TEXT
        new_interactive_text = "META: Hero List"
    elif user_choice == MenuButton.META_RECOMMENDATIONS.value:
        new_main_text = META_RECOMMENDATIONS_TEXT
        new_interactive_text = "META: Recommendations"
    elif user_choice == MenuButton.META_UPDATES.value:
        new_main_text = META_UPDATES_TEXT
        new_interactive_text = "META: Updates"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"

    # Відправка нового бот-повідомлення з відповідним меню
    new_bot_message = await send_new_bot_message(
        bot=bot,
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = new_bot_message.message_id

    # Оновлення state даних з новим bot_message_id
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагування інтерактивного повідомлення
    if interactive_message_id:
        updated_interactive_message_id = await edit_interactive_message(
            bot=bot,
            chat_id=chat_id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    else:
        # Відправка нового інтерактивного повідомлення, якщо його не існує
        new_interactive_message = await bot.send_message(
            chat_id=chat_id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        updated_interactive_message_id = new_interactive_message.message_id

    # Оновлення state даних з новим interactive_message_id
    await state.update_data(interactive_message_id=updated_interactive_message_id)

    # Встановлення нового стану
    await state.set_state(new_state)
    logger.info(f"User {user_id} navigated to {new_state}")

# Обробник Inline кнопок
@router.callback_query()
async def handle_inline_buttons(callback: CallbackQuery, state: FSMContext, db: AsyncSession, bot: Bot):
    data = callback.data
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    logger.info(f"User {user_id} pressed inline button: {data}")

    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if not interactive_message_id:
        logger.error("interactive_message_id not found")
        await bot.answer_callback_query(callback.id, text=GENERIC_ERROR_MESSAGE_TEXT)
        return

    if data == "mls_button":
        await bot.answer_callback_query(callback.id, text=MLS_BUTTON_RESPONSE_TEXT)
        logger.info(f"User {user_id} pressed 'mls_button'")
    elif data == "menu_back":
        # Перехід назад до головного меню
        user_first_name = callback.from_user.first_name
        main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
        main_menu_keyboard = get_main_menu()

        # Видалення старого бот-повідомлення
        bot_message_id = state_data.get('bot_message_id')
        if bot_message_id:
            await delete_message_safe(bot, chat_id, bot_message_id)

        # Відправка нового бот-повідомлення з головним меню
        new_bot_message = await send_new_bot_message(
            bot=bot,
            chat_id=chat_id,
            text="🔰 Оберіть опцію для профілю:",
            reply_markup=get_profile_menu()
        )
        new_bot_message_id = new_bot_message.message_id

        # Оновлення state даних з новим bot_message_id
        await state.update_data(bot_message_id=new_bot_message_id)

        # Редагування інтерактивного повідомлення з описом головного меню
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_interactive_keyboard = get_generic_inline_keyboard()
        updated_interactive_message_id = await edit_interactive_message(
            bot=bot,
            chat_id=chat_id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )

        # Оновлення state даних з новим interactive_message_id
        await state.update_data(interactive_message_id=updated_interactive_message_id)

        # Встановлення стану на MAIN_MENU
        await state.set_state(MenuStates.MAIN_MENU)
        logger.info(f"User {user_id} navigated back to MAIN_MENU")
    else:
        await bot.answer_callback_query(callback.id, text=UNHANDLED_INLINE_BUTTON_TEXT)
        logger.warning(f"Unhandled inline button pressed by user {user_id}: {data}")

    await callback.answer()

# Обробник пошуку героя
@router.message(MenuStates.SEARCH_HERO)
async def handle_search_hero(message: Message, state: FSMContext, bot: Bot):
    hero_name = message.text.strip()
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"User {user_id} is searching for hero: {hero_name}")
    await message.delete()

    if hero_name:
        response_text = SEARCH_HERO_RESPONSE_TEXT.format(hero_name=hero_name)
    else:
        response_text = "❌ Будь ласка, введіть назву героя, якого ви хочете знайти."

    # Видалення старого бот-повідомлення
    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    if bot_message_id:
        await delete_message_safe(bot, chat_id, bot_message_id)

    # Відправка повідомлення з результатом пошуку
    search_result_message = await send_new_bot_message(
        bot=bot,
        chat_id=chat_id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard()
    )
    new_bot_message_id = search_result_message.message_id

    # Оновлення state даних з новим bot_message_id
    await state.update_data(bot_message_id=new_bot_message_id)

    # Видалення старого інтерактивного повідомлення, якщо необхідно
    interactive_message_id = state_data.get('interactive_message_id')
    if interactive_message_id:
        await delete_message_safe(bot, chat_id, interactive_message_id)

    # Відправка інтерактивного повідомлення з меню героїв
    new_interactive_message = await bot.send_message(
        chat_id=chat_id,
        text="🔍 Результати пошуку:",
        reply_markup=get_generic_inline_keyboard()
    )
    new_interactive_message_id = new_interactive_message.message_id

    # Оновлення state даних з новим interactive_message_id
    await state.update_data(interactive_message_id=new_interactive_message_id)

    # Встановлення стану назад до HEROES_MENU
    await state.set_state(MenuStates.HEROES_MENU)
    logger.info(f"User {user_id} completed hero search")

# Обробник пропозиції теми
@router.message(MenuStates.SEARCH_TOPIC)
async def handle_search_topic(message: Message, state: FSMContext, bot: Bot):
    topic = message.text.strip()
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"User {user_id} is suggesting a topic: {topic}")
    await message.delete()

    if topic:
        response_text = SUGGESTION_RESPONSE_TEXT.format(topic=topic)
    else:
        response_text = "❌ Будь ласка, введіть тему, яку ви хочете запропонувати."

    # Видалення старого бот-повідомлення
    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    if bot_message_id:
        await delete_message_safe(bot, chat_id, bot_message_id)

    # Відправка повідомлення з результатом пропозиції
    suggestion_response_message = await send_new_bot_message(
        bot=bot,
        chat_id=chat_id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard()
    )
    new_bot_message_id = suggestion_response_message.message_id

    # Оновлення state даних з новим bot_message_id
    await state.update_data(bot_message_id=new_bot_message_id)

    # Видалення старого інтерактивного повідомлення, якщо необхідно
    interactive_message_id = state_data.get('interactive_message_id')
    if interactive_message_id:
        await delete_message_safe(bot, chat_id, interactive_message_id)

    # Відправка інтерактивного повідомлення з меню зворотного зв'язку
    new_interactive_message = await bot.send_message(
        chat_id=chat_id,
        text=FEEDBACK_INTERACTIVE_TEXT,
        reply_markup=get_generic_inline_keyboard()
    )
    new_interactive_message_id = new_interactive_message.message_id

    # Оновлення state даних з новим interactive_message_id
    await state.update_data(interactive_message_id=new_interactive_message_id)

    # Встановлення стану назад до FEEDBACK_MENU
    await state.set_state(MenuStates.FEEDBACK_MENU)
    logger.info(f"User {user_id} completed topic suggestion")

# Обробник невідомих команд
@router.message()
async def unknown_command(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_id = message.from_user.id
    chat_id = message.chat.id
    user_text = message.text
    logger.warning(f"Unknown message from {user_id}: {user_text}")
    await message.delete()

    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    interactive_message_id = state_data.get('interactive_message_id')
    current_state = await state.get_state()

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
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
        hero_class = state_data.get('hero_class', 'Tank')
        heroes_list = state_data.get('heroes_list', 'No available heroes.')
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
        # Для станів, де очікуються текстові введення, пропонуємо використовувати кнопки навігації
        error_response = USE_BUTTON_NAVIGATION_TEXT
        new_bot_message = await send_new_bot_message(
            bot=bot,
            chat_id=chat_id,
            text=error_response,
            reply_markup=get_generic_inline_keyboard()
        )
        new_bot_message_id = new_bot_message.message_id
        await state.update_data(bot_message_id=new_bot_message_id)
        # Не змінюємо стан
        return
    else:
        # Для будь-яких інших станів переходимо до головного меню
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU

    # Видалення старого бот-повідомлення
    if bot_message_id:
        await delete_message_safe(bot, chat_id, bot_message_id)

    # Відправка нового бот-повідомлення з відповідним меню
    new_bot_message = await send_new_bot_message(
        bot=bot,
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = new_bot_message.message_id

    # Оновлення state даних з новим bot_message_id
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагування інтерактивного повідомлення
    if interactive_message_id:
        updated_interactive_message_id = await edit_interactive_message(
            bot=bot,
            chat_id=chat_id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    else:
        # Відправка нового інтерактивного повідомлення, якщо його не існує
        new_interactive_message = await bot.send_message(
            chat_id=chat_id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        updated_interactive_message_id = new_interactive_message.message_id

    # Оновлення state даних з новим interactive_message_id
    await state.update_data(interactive_message_id=updated_interactive_message_id)

    # Встановлення нового стану
    await state.set_state(new_state)
    logger.info(f"User {user_id} navigated to {new_state}")

# Інтеграція обробників з Dispatcher
def setup_handlers(dp: Router):
    dp.include_router(router)
    # Якщо у вас є інші роутери, включіть їх тут, наприклад:
    # dp.include_router(profile_router)