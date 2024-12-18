import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode
from aiogram import types

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
    get_tournaments_menu, get_meta_menu, get_m6_menu, get_gpt_menu, heroes_by_class,
    menu_button_to_class  # Додано припущення, що ця змінна визначена тут
)
from keyboards.inline_menus import (
    get_generic_inline_keyboard,
    get_intro_page_1_keyboard,
    get_intro_page_2_keyboard,
    get_intro_page_3_keyboard,
    get_profile_submenu_inline_keyboard,
    get_navigation_submenu_inline_keyboard,
    get_gpt_submenu_inline_keyboard,
    # Додайте інші інлайн-клавіатури за потреби
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
    M6_NEWS_TEXT, GPT_MENU_TEXT  # Додано припущення, що GPT_MENU_TEXT визначено
)
from utils.helpers import (
    generate_profile_message,
    generate_statistics_message,
    generate_achievements_message
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

# Допоміжні функції для управління повідомленнями
async def send_new_message(chat_id: int, text: str, reply_markup: types.ReplyKeyboardMarkup | types.InlineKeyboardMarkup | None, state: FSMContext, key: str):
    try:
        message = await bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )
        await state.update_data(**{key: message.message_id})
        return message.message_id
    except Exception as e:
        logger.error(f"Failed to send new message: {e}")
        return None

async def edit_interactive_message(bot: Bot, chat_id: int, message_id: int, text: str, reply_markup: types.InlineKeyboardMarkup | None, state: FSMContext):
    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )
        logger.info("Successfully edited interactive message.")
    except Exception as e:
        logger.error(f"Failed to edit interactive message: {e}")
        # Надсилання нового інтерактивного повідомлення та оновлення interactive_message_id
        new_message = await bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=ParseMode.HTML,
            reply_markup=reply_markup
        )
        await state.update_data(interactive_message_id=new_message.message_id)

async def delete_message(bot: Bot, chat_id: int, message_id: int):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        logger.info(f"Deleted message {message_id} from chat {chat_id}.")
    except Exception as e:
        logger.error(f"Failed to delete message {message_id} from chat {chat_id}: {e}")

# Обробник команди /start з реєстрацією користувача та початковим меню
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
    if not interactive_message_id:
        logger.error("interactive_message_id not found in state data")
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await callback.answer()
        return

    await state.set_state(MenuStates.INTRO_PAGE_2)
    await callback.answer()

    # Редагування існуючого повідомлення або надсилання нового
    await edit_interactive_message(
        bot=bot,
        chat_id=callback.message.chat.id,
        message_id=interactive_message_id,
        text=INTRO_PAGE_2_TEXT,
        reply_markup=get_intro_page_2_keyboard(),
        state=state
    )

@router.callback_query(F.data == "intro_next_2")
async def handle_intro_next_2(callback: CallbackQuery, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')
    if not interactive_message_id:
        logger.error("interactive_message_id not found in state data")
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await callback.answer()
        return

    await state.set_state(MenuStates.INTRO_PAGE_3)
    await callback.answer()

    # Редагування існуючого повідомлення або надсилання нового
    await edit_interactive_message(
        bot=bot,
        chat_id=callback.message.chat.id,
        message_id=interactive_message_id,
        text=INTRO_PAGE_3_TEXT,
        reply_markup=get_intro_page_3_keyboard(),
        state=state
    )

@router.callback_query(F.data == "intro_start")
async def handle_intro_start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_first_name = callback.from_user.first_name
    main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=user_first_name)

    # Надсилання основного меню
    main_menu_message_id = await send_new_message(
        chat_id=callback.message.chat.id,
        text=main_menu_text_formatted,
        reply_markup=get_main_menu(),
        state=state,
        key="bot_message_id"
    )

    # Отримання interactive_message_id зі стану FSM
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if interactive_message_id:
        await edit_interactive_message(
            bot=bot,
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=MAIN_MENU_DESCRIPTION,
            reply_markup=get_generic_inline_keyboard(),
            state=state
        )
    else:
        logger.warning("interactive_message_id not found, sending MAIN_MENU_DESCRIPTION as new message")
        # Якщо interactive_message_id не знайдено, надсилання нового повідомлення
        interactive_message = await bot.send_message(
            chat_id=callback.message.chat.id,
            text=MAIN_MENU_DESCRIPTION,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    # Видалення попереднього інтерактивного повідомлення, якщо потрібно
    # Наприклад, якщо у вас є старий bot_message_id, який потрібно видалити

    await state.set_state(MenuStates.MAIN_MENU)
    await callback.answer()

# Допоміжні функції для обробки переходів між меню
async def transition_to_state(message: Message | CallbackQuery, state: FSMContext, bot: Bot, new_state: State, new_main_text: str, new_main_keyboard, new_interactive_text: str):
    """
    Допоміжна функція для переходу до нового стану:
    - Видаляє попереднє bot_message.
    - Редагує або надсилає нове interactive_message.
    - Відправляє нове main_message.
    """
    # Отримання chat_id та user_first_name
    if isinstance(message, Message):
        chat_id = message.chat.id
        user_first_name = message.from_user.first_name
    else:
        chat_id = message.message.chat.id
        user_first_name = message.from_user.first_name

    # Отримання bot_message_id та interactive_message_id зі стану
    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    interactive_message_id = state_data.get('interactive_message_id')

    # Видалення старого bot_message
    if bot_message_id:
        await delete_message(bot, chat_id, bot_message_id)

    # Відправка нового main_message
    new_main_message_id = await send_new_message(
        chat_id=chat_id,
        text=new_main_text.format(user_first_name=user_first_name) if "{user_first_name}" in new_main_text else new_main_text,
        reply_markup=new_main_keyboard,
        state=state,
        key="bot_message_id"
    )

    # Редагування або надсилання нового interactive_message
    if interactive_message_id:
        await edit_interactive_message(
            bot=bot,
            chat_id=chat_id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard(),
            state=state
        )
    else:
        interactive_message = await bot.send_message(
            chat_id=chat_id,
            text=new_interactive_text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    # Встановлення нового стану
    await state.set_state(new_state)

# 🔴 **Оновлена Функція `handle_my_profile` 🔴**

@router.message(F.text == "🪪 Мій Профіль")
async def handle_my_profile(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_id = message.from_user.id
    profile_data = await get_user_profile(db, user_id)  # Отримання профілю з БД

    if profile_data:
        profile_message = generate_profile_message(profile_data)

        # Отримання interactive_message_id зі стану FSM
        data = await state.get_data()
        interactive_message_id = data.get("interactive_message_id")

        if interactive_message_id:
            try:
                # Редагування існуючого повідомлення з використанням InlineKeyboardMarkup
                await bot.edit_message_text(
                    chat_id=message.chat.id,
                    message_id=interactive_message_id,
                    text=profile_message,
                    parse_mode="HTML",
                    reply_markup=get_profile_submenu_inline_keyboard()
                )
            except Exception as e:
                # Якщо редагування не вдається, надіслати нове повідомлення та оновити interactive_message_id
                logger.error(f"Failed to edit interactive message: {e}")
                new_message = await bot.send_message(
                    chat_id=message.chat.id,
                    text=profile_message,
                    parse_mode="HTML",
                    reply_markup=get_profile_submenu_inline_keyboard()
                )
                await state.update_data(interactive_message_id=new_message.message_id)
        else:
            # Якщо interactive_message_id ще не збережено, надсилається нове повідомлення
            new_message = await bot.send_message(
                chat_id=message.chat.id,
                text=profile_message,
                parse_mode="HTML",
                reply_markup=get_profile_submenu_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_message.message_id)

        # Видалення попереднього bot_message, якщо необхідно
        bot_message_id = data.get('bot_message_id')
        if bot_message_id:
            await delete_message(bot, message.chat.id, bot_message_id)

        # Встановлення стану
        await state.set_state(MenuStates.PROFILE_MENU)
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="❌ Дані профілю не знайдено. Зареєструйтесь, щоб переглянути статистику.",
            reply_markup=get_generic_inline_keyboard()
        )
        await state.set_state(MenuStates.MAIN_MENU)

# Обробник меню "Main Menu"
@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in main menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice == MenuButton.NAVIGATION.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_submenu_inline_keyboard()  # InlineKeyboardMarkup
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    elif user_choice == MenuButton.PROFILE.value:
        # Використання допоміжної функції для генерації профілю
        profile_data = await get_user_profile(db, message.from_user.id)
        if profile_data:
            profile_message = generate_profile_message(profile_data)
            new_main_text = profile_message
            new_main_keyboard = get_profile_submenu_inline_keyboard()  # InlineKeyboardMarkup
            new_interactive_text = "Profile Overview"
            new_state = MenuStates.PROFILE_MENU
        else:
            new_main_text = "❌ Дані профілю не знайдено."
            new_interactive_text = "Profile Overview"
            new_state = MenuStates.PROFILE_MENU
    elif user_choice == MenuButton.TOURNAMENTS.value:
        new_main_text = TOURNAMENT_CREATE_TEXT  # Початковий текст для турнірів
        new_main_keyboard = get_tournaments_menu()  # ReplyKeyboardMarkup
        new_interactive_text = "Tournaments Menu"
        new_state = MenuStates.TOURNAMENTS_MENU
    elif user_choice == MenuButton.META.value:
        new_main_text = META_MENU_TEXT
        new_main_keyboard = get_meta_menu()  # ReplyKeyboardMarkup
        new_interactive_text = "META Menu"
        new_state = MenuStates.META_MENU
    elif user_choice == MenuButton.M6.value:
        new_main_text = M6_INFO_TEXT  # Можливо, потрібно вибрати певну опцію
        new_main_keyboard = get_m6_menu()  # ReplyKeyboardMarkup
        new_interactive_text = "M6 Menu"
        new_state = MenuStates.M6_MENU
    elif user_choice == MenuButton.GPT.value:
        new_main_text = GPT_MENU_TEXT
        new_main_keyboard = get_gpt_menu()  # ReplyKeyboardMarkup
        new_interactive_text = "GPT Menu"
        new_state = MenuStates.GPT_MENU
    else:
        new_main_keyboard = get_main_menu()
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
        new_state = MenuStates.MAIN_MENU

    # Перехід до нового стану
    await transition_to_state(
        message=message,
        state=state,
        bot=bot,
        new_state=new_state,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text
    )

# Обробник меню "Navigation Menu"
@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Navigation Menu")
    await message.delete()

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice == MenuButton.HEROES.value:
        new_main_text = HEROES_MENU_TEXT
        new_main_keyboard = get_heroes_menu()  # ReplyKeyboardMarkup
        new_interactive_text = HEROES_INTERACTIVE_TEXT
        new_state = MenuStates.HEROES_MENU
    elif user_choice == MenuButton.GUIDES.value:
        new_main_text = GUIDES_MENU_TEXT
        new_main_keyboard = get_guides_menu()  # ReplyKeyboardMarkup
        new_interactive_text = GUIDES_INTERACTIVE_TEXT
        new_state = MenuStates.GUIDES_MENU
    elif user_choice == MenuButton.COUNTER_PICKS.value:
        new_main_text = COUNTER_PICKS_MENU_TEXT
        new_main_keyboard = get_counter_picks_menu()  # ReplyKeyboardMarkup
        new_interactive_text = COUNTER_PICKS_INTERACTIVE_TEXT
        new_state = MenuStates.COUNTER_PICKS_MENU
    elif user_choice == MenuButton.BUILDS.value:
        new_main_text = BUILDS_MENU_TEXT
        new_main_keyboard = get_builds_menu()  # ReplyKeyboardMarkup
        new_interactive_text = BUILDS_INTERACTIVE_TEXT
        new_state = MenuStates.BUILDS_MENU
    elif user_choice == MenuButton.VOTING.value:
        new_main_text = VOTING_MENU_TEXT
        new_main_keyboard = get_voting_menu()  # ReplyKeyboardMarkup
        new_interactive_text = VOTING_INTERACTIVE_TEXT
        new_state = MenuStates.VOTING_MENU
    elif user_choice == MenuButton.TOURNAMENTS.value:
        new_main_text = TOURNAMENT_CREATE_TEXT  # Початковий текст для турнірів
        new_main_keyboard = get_tournaments_menu()  # ReplyKeyboardMarkup
        new_interactive_text = "Tournaments Menu"
        new_state = MenuStates.TOURNAMENTS_MENU
    elif user_choice == MenuButton.META.value:
        new_main_text = META_MENU_TEXT
        new_main_keyboard = get_meta_menu()  # ReplyKeyboardMarkup
        new_interactive_text = "META Menu"
        new_state = MenuStates.META_MENU
    elif user_choice == MenuButton.M6.value:
        new_main_text = M6_INFO_TEXT  # Можливо, потрібно вибрати певну опцію
        new_main_keyboard = get_m6_menu()  # ReplyKeyboardMarkup
        new_interactive_text = "M6 Menu"
        new_state = MenuStates.M6_MENU
    elif user_choice == MenuButton.GPT.value:
        new_main_text = GPT_MENU_TEXT
        new_main_keyboard = get_gpt_menu()  # ReplyKeyboardMarkup
        new_interactive_text = "GPT Menu"
        new_state = MenuStates.GPT_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = get_main_menu_text(message.from_user.first_name)
        new_main_keyboard = get_main_menu()  # ReplyKeyboardMarkup для основного меню
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_keyboard = get_navigation_menu()  # ReplyKeyboardMarkup
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
        new_state = MenuStates.NAVIGATION_MENU

    # Перехід до нового стану
    await transition_to_state(
        message=message,
        state=state,
        bot=bot,
        new_state=new_state,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text
    )

# Обробник меню "Profile Menu"
@router.message(MenuStates.PROFILE_MENU)
async def handle_profile_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Profile Menu")
    await message.delete()

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice == MenuButton.STATISTICS.value:
        statistics_data = {
            'activity': 'Active',  # Це потрібно замінити на реальні дані
            'ranking': 'Gold',     # Це потрібно замінити на реальні дані
            'game_stats': 'Detailed stats here'  # Це потрібно замінити на реальні дані
        }
        statistics_message = generate_statistics_message(statistics_data)
        new_main_text = statistics_message
        new_interactive_text = "Statistics Overview"
        new_state = MenuStates.STATISTICS_MENU
    elif user_choice == MenuButton.ACHIEVEMENTS.value:
        achievements_data = {
            'badges': 5,                  # Це потрібно замінити на реальні дані
            'progress': '50%',            # Це потрібно замінити на реальні дані
            'tournament_stats': 'Participated in 3 tournaments',  # Це потрібно замінити на реальні дані
            'awards': 'Winner of MVP award'  # Це потрібно замінити на реальні дані
        }
        achievements_message = generate_achievements_message(achievements_data)
        new_main_text = achievements_message
        new_interactive_text = "Achievements Overview"
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif user_choice == MenuButton.SETTINGS.value:
        new_main_text = SETTINGS_MENU_TEXT
        new_main_keyboard = get_settings_menu()  # ReplyKeyboardMarkup
        new_interactive_text = SETTINGS_INTERACTIVE_TEXT
        new_state = MenuStates.SETTINGS_MENU
    elif user_choice == MenuButton.FEEDBACK.value:
        new_main_text = FEEDBACK_MENU_TEXT
        new_main_keyboard = get_feedback_menu()  # ReplyKeyboardMarkup
        new_interactive_text = FEEDBACK_INTERACTIVE_TEXT
        new_state = MenuStates.FEEDBACK_MENU
    elif user_choice == MenuButton.HELP.value:
        new_main_text = HELP_MENU_TEXT
        new_main_keyboard = get_help_menu()  # ReplyKeyboardMarkup
        new_interactive_text = HELP_INTERACTIVE_TEXT
        new_state = MenuStates.HELP_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = get_main_menu_text(message.from_user.first_name)
        new_main_keyboard = get_main_menu()  # ReplyKeyboardMarkup для основного меню
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
        new_state = MenuStates.PROFILE_MENU

    # Перехід до нового стану
    await transition_to_state(
        message=message,
        state=state,
        bot=bot,
        new_state=new_state,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text
    )

# Обробник меню "Statistics Menu"
@router.message(MenuStates.STATISTICS_MENU)
async def handle_statistics_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Statistics Menu")
    await message.delete()

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice == MenuButton.ACTIVITY.value:
        new_main_text = ACTIVITY_TEXT
        new_interactive_text = "General Activity Statistics"
        new_state = MenuStates.STATISTICS_MENU
    elif user_choice == MenuButton.RANKING.value:
        new_main_text = RANKING_TEXT
        new_interactive_text = "Ranking Statistics"
        new_state = MenuStates.STATISTICS_MENU
    elif user_choice == MenuButton.GAME_STATS.value:
        new_main_text = GAME_STATS_TEXT
        new_interactive_text = "Game Statistics"
        new_state = MenuStates.STATISTICS_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()  # ReplyKeyboardMarkup
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
        new_state = MenuStates.STATISTICS_MENU

    # Перехід до нового стану
    await transition_to_state(
        message=message,
        state=state,
        bot=bot,
        new_state=new_state,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text
    )

# Обробник меню "Achievements Menu"
@router.message(MenuStates.ACHIEVEMENTS_MENU)
async def handle_achievements_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Achievements Menu")
    await message.delete()

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice == MenuButton.BADGES.value:
        new_main_text = BADGES_TEXT
        new_interactive_text = "My Badges"
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif user_choice == MenuButton.PROGRESS.value:
        new_main_text = PROGRESS_TEXT
        new_interactive_text = "Progress Overview"
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif user_choice == MenuButton.TOURNAMENT_STATS.value:
        new_main_text = TOURNAMENT_STATS_TEXT
        new_interactive_text = "Tournament Statistics"
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif user_choice == MenuButton.AWARDS.value:
        new_main_text = AWARDS_TEXT
        new_interactive_text = "Received Awards"
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()  # ReplyKeyboardMarkup
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
        new_state = MenuStates.ACHIEVEMENTS_MENU

    # Перехід до нового стану
    await transition_to_state(
        message=message,
        state=state,
        bot=bot,
        new_state=new_state,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text
    )

# Обробник меню "Settings Menu"
@router.message(MenuStates.SETTINGS_MENU)
async def handle_settings_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Settings Menu")
    await message.delete()

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice == MenuButton.LANGUAGE.value:
        new_main_text = LANGUAGE_TEXT
        new_interactive_text = "Language Settings"
        new_state = MenuStates.SETTINGS_MENU
    elif user_choice == MenuButton.CHANGE_USERNAME.value:
        new_main_text = CHANGE_USERNAME_TEXT
        new_interactive_text = "Change Username"
        new_state = MenuStates.CHANGE_USERNAME
    elif user_choice == MenuButton.UPDATE_ID.value:
        new_main_text = UPDATE_ID_TEXT
        new_interactive_text = "Update ID"
        new_state = MenuStates.SETTINGS_MENU
    elif user_choice == MenuButton.NOTIFICATIONS.value:
        new_main_text = NOTIFICATIONS_TEXT
        new_interactive_text = "Notification Settings"
        new_state = MenuStates.SETTINGS_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = get_main_menu_text(message.from_user.first_name)
        new_main_keyboard = get_main_menu()  # ReplyKeyboardMarkup для основного меню
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
        new_state = MenuStates.SETTINGS_MENU

    # Перехід до нового стану
    await transition_to_state(
        message=message,
        state=state,
        bot=bot,
        new_state=new_state,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text
    )

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
    
    # Перехід до стану "Settings Menu" після зміни імені
    await transition_to_state(
        message=message,
        state=state,
        bot=bot,
        new_state=MenuStates.SETTINGS_MENU,
        new_main_text=MAIN_MENU_DESCRIPTION,
        new_main_keyboard=get_generic_inline_keyboard(),
        new_interactive_text=MAIN_MENU_DESCRIPTION
    )

    await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())

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
    
    # Перехід до стану "Feedback Menu"
    await transition_to_state(
        message=message,
        state=state,
        bot=bot,
        new_state=MenuStates.FEEDBACK_MENU,
        new_main_text=response_text,
        new_main_keyboard=get_generic_inline_keyboard(),
        new_interactive_text="Feedback Menu"
    )

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
    
    # Перехід до стану "Feedback Menu"
    await transition_to_state(
        message=message,
        state=state,
        bot=bot,
        new_state=MenuStates.FEEDBACK_MENU,
        new_main_text=response_text,
        new_main_keyboard=get_generic_inline_keyboard(),
        new_interactive_text="Feedback Menu"
    )

# Обробник меню "Feedback Menu"
@router.message(MenuStates.FEEDBACK_MENU)
async def handle_feedback_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Feedback Menu")
    await message.delete()

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
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
        new_main_text = get_main_menu_text(message.from_user.first_name)
        new_main_keyboard = get_main_menu()  # ReplyKeyboardMarkup для основного меню
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
        new_state = MenuStates.FEEDBACK_MENU

    # Перехід до нового стану
    await transition_to_state(
        message=message,
        state=state,
        bot=bot,
        new_state=new_state,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text
    )

# Обробник меню "Help Menu"
@router.message(MenuStates.HELP_MENU)
async def handle_help_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Help Menu")
    await message.delete()

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice == MenuButton.INSTRUCTIONS.value:
        new_main_text = INSTRUCTIONS_TEXT
        new_interactive_text = "Instructions"
        new_state = MenuStates.HELP_MENU
    elif user_choice == MenuButton.FAQ.value:
        new_main_text = FAQ_TEXT
        new_interactive_text = "Frequently Asked Questions"
        new_state = MenuStates.HELP_MENU
    elif user_choice == MenuButton.HELP_SUPPORT.value:
        new_main_text = HELP_SUPPORT_TEXT
        new_interactive_text = "Support"
        new_state = MenuStates.HELP_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = get_main_menu_text(message.from_user.first_name)
        new_main_keyboard = get_main_menu()  # ReplyKeyboardMarkup для основного меню
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
        new_state = MenuStates.HELP_MENU

    # Перехід до нового стану
    await transition_to_state(
        message=message,
        state=state,
        bot=bot,
        new_state=new_state,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text
    )

# Обробник меню "Heroes Menu"
@router.message(MenuStates.HEROES_MENU)
async def handle_heroes_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Heroes Menu")
    await message.delete()

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice in menu_button_to_class.keys():
        hero_class = menu_button_to_class[user_choice]
        heroes_list = heroes_by_class.get(hero_class, [])
        heroes_formatted = "\n".join([f"• <b>{hero}</b>: Короткий опис здібностей." for hero in heroes_list]) if heroes_list else "Немає доступних героїв."
        new_main_text = HERO_CLASS_MENU_TEXT.format(hero_class=hero_class)
        new_main_keyboard = get_hero_class_menu(hero_class)  # ReplyKeyboardMarkup
        new_interactive_text = HERO_CLASS_INTERACTIVE_TEXT.format(hero_class=hero_class, heroes_list=heroes_formatted)
        new_state = MenuStates.HERO_CLASS_MENU
        await state.update_data(hero_class=hero_class, heroes_list=heroes_formatted)
    elif user_choice == MenuButton.COMPARISON.value:
        new_main_text = "⚖️ Функціонал порівняння героїв буде доступний пізніше."
        new_interactive_text = "Compare Heroes"
        new_state = MenuStates.HEROES_MENU
    elif user_choice == MenuButton.SEARCH_HERO.value:
        new_main_text = "🔎 Будь ласка, введіть назву героя, якого ви хочете знайти."
        new_main_keyboard = types.ReplyKeyboardRemove()
        new_interactive_text = "Search Hero"
        new_state = MenuStates.SEARCH_HERO
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_submenu_inline_keyboard()  # ReplyKeyboardMarkup
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
        new_state = MenuStates.HEROES_MENU

    # Перехід до нового стану
    await transition_to_state(
        message=message,
        state=state,
        bot=bot,
        new_state=new_state,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text
    )

# Обробник пошуку героя
@router.message(MenuStates.SEARCH_HERO)
async def handle_search_hero(message: Message, state: FSMContext, bot: Bot):
    hero_name = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"User {user_id} is searching for hero: {hero_name}")
    await message.delete()
    if hero_name:
        # Тут можна реалізувати логіку пошуку героя в базі даних або API
        # Наприклад, перевірка наявності героя
        response_text = SEARCH_HERO_RESPONSE_TEXT.format(hero_name=hero_name)
    else:
        response_text = "❌ Будь ласка, введіть назву героя, якого ви хочете знайти."

    # Перехід до стану "Heroes Menu"
    await transition_to_state(
        message=message,
        state=state,
        bot=bot,
        new_state=MenuStates.HEROES_MENU,
        new_main_text=response_text,
        new_main_keyboard=get_generic_inline_keyboard(),
        new_interactive_text="Heroes Menu"
    )

# Обробник меню "Guides Menu"
@router.message(MenuStates.GUIDES_MENU)
async def handle_guides_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Guides Menu")
    await message.delete()

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice == MenuButton.NEW_GUIDES.value:
        new_main_text = NEW_GUIDES_TEXT
        new_interactive_text = "New Guides"
        new_state = MenuStates.GUIDES_MENU
    elif user_choice == MenuButton.POPULAR_GUIDES.value:
        new_main_text = POPULAR_GUIDES_TEXT
        new_interactive_text = "Popular Guides"
        new_state = MenuStates.GUIDES_MENU
    elif user_choice == MenuButton.BEGINNER_GUIDES.value:
        new_main_text = BEGINNER_GUIDES_TEXT
        new_interactive_text = "Beginner Guides"
        new_state = MenuStates.GUIDES_MENU
    elif user_choice == MenuButton.ADVANCED_TECHNIQUES.value:
        new_main_text = ADVANCED_TECHNIQUES_TEXT
        new_interactive_text = "Advanced Techniques"
        new_state = MenuStates.GUIDES_MENU
    elif user_choice == MenuButton.TEAMPLAY_GUIDES.value:
        new_main_text = TEAMPLAY_GUIDES_TEXT
        new_interactive_text = "Teamplay Guides"
        new_state = MenuStates.GUIDES_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_submenu_inline_keyboard()  # ReplyKeyboardMarkup
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
        new_state = MenuStates.GUIDES_MENU

    # Перехід до нового стану
    await transition_to_state(
        message=message,
        state=state,
        bot=bot,
        new_state=new_state,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text
    )

# Обробник меню "Counter Picks Menu"
@router.message(MenuStates.COUNTER_PICKS_MENU)
async def handle_counter_picks_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Counter Picks Menu")
    await message.delete()

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice == MenuButton.COUNTER_SEARCH.value:
        new_main_text = COUNTER_SEARCH_TEXT
        new_interactive_text = "Counter Pick Search"
        new_state = MenuStates.COUNTER_PICKS_MENU
    elif user_choice == MenuButton.COUNTER_LIST.value:
        new_main_text = COUNTER_LIST_TEXT
        new_interactive_text = "Counter Picks List"
        new_state = MenuStates.COUNTER_PICKS_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_submenu_inline_keyboard()  # ReplyKeyboardMarkup
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
        new_state = MenuStates.COUNTER_PICKS_MENU

    # Перехід до нового стану
    await transition_to_state(
        message=message,
        state=state,
        bot=bot,
        new_state=new_state,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text
    )

# Обробник меню "Builds Menu"
@router.message(MenuStates.BUILDS_MENU)
async def handle_builds_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Builds Menu")
    await message.delete()

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice == MenuButton.CREATE_BUILD.value:
        new_main_text = CREATE_BUILD_TEXT
        new_interactive_text = "Creating a build"
        new_state = MenuStates.BUILDS_MENU
    elif user_choice == MenuButton.MY_BUILDS.value:
        new_main_text = MY_BUILDS_TEXT
        new_interactive_text = "My Builds"
        new_state = MenuStates.BUILDS_MENU
    elif user_choice == MenuButton.POPULAR_BUILDS.value:
        new_main_text = POPULAR_BUILDS_TEXT
        new_interactive_text = "Popular Builds"
        new_state = MenuStates.BUILDS_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_submenu_inline_keyboard()  # ReplyKeyboardMarkup
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
        new_state = MenuStates.BUILDS_MENU

    # Перехід до нового стану
    await transition_to_state(
        message=message,
        state=state,
        bot=bot,
        new_state=new_state,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text
    )

# Обробник меню "Voting Menu"
@router.message(MenuStates.VOTING_MENU)
async def handle_voting_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Voting Menu")
    await message.delete()

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice == MenuButton.CURRENT_VOTES.value:
        new_main_text = CURRENT_VOTES_TEXT
        new_interactive_text = "Current Polls"
        new_state = MenuStates.VOTING_MENU
    elif user_choice == MenuButton.MY_VOTES.value:
        new_main_text = MY_VOTES_TEXT
        new_interactive_text = "My Votes"
        new_state = MenuStates.VOTING_MENU
    elif user_choice == MenuButton.SUGGEST_TOPIC.value:
        new_main_text = SUGGEST_TOPIC_TEXT
        new_interactive_text = "Suggest a Topic"
        new_state = MenuStates.SEARCH_TOPIC
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_submenu_inline_keyboard()  # ReplyKeyboardMarkup
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
        new_state = MenuStates.VOTING_MENU

    # Перехід до нового стану
    await transition_to_state(
        message=message,
        state=state,
        bot=bot,
        new_state=new_state,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text
    )

# Обробник меню "Tournaments Menu"
@router.message(MenuStates.TOURNAMENTS_MENU)
async def handle_tournaments_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Tournaments Menu")
    await message.delete()

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice == MenuButton.CREATE_TOURNAMENT.value:
        new_main_text = TOURNAMENT_CREATE_TEXT
        new_interactive_text = "Creating a Tournament"
        new_state = MenuStates.TOURNAMENTS_MENU
    elif user_choice == MenuButton.VIEW_TOURNAMENTS.value:
        new_main_text = TOURNAMENT_VIEW_TEXT
        new_interactive_text = "Viewing Tournaments"
        new_state = MenuStates.TOURNAMENTS_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_submenu_inline_keyboard()  # ReplyKeyboardMarkup
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
        new_state = MenuStates.TOURNAMENTS_MENU

    # Перехід до нового стану
    await transition_to_state(
        message=message,
        state=state,
        bot=bot,
        new_state=new_state,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text
    )

# Обробник меню "META Menu"
@router.message(MenuStates.META_MENU)
async def handle_meta_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in META Menu")
    await message.delete()

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice == MenuButton.META_HERO_LIST.value:
        new_main_text = META_HERO_LIST_TEXT
        new_interactive_text = "META Hero List"
        new_state = MenuStates.META_MENU
    elif user_choice == MenuButton.META_RECOMMENDATIONS.value:
        new_main_text = META_RECOMMENDATIONS_TEXT
        new_interactive_text = "META Recommendations"
        new_state = MenuStates.META_MENU
    elif user_choice == MenuButton.META_UPDATES.value:
        new_main_text = META_UPDATES_TEXT
        new_interactive_text = "META Updates"
        new_state = MenuStates.META_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = get_main_menu_text(message.from_user.first_name)
        new_main_keyboard = get_main_menu()  # ReplyKeyboardMarkup для основного меню
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
        new_state = MenuStates.META_MENU

    # Перехід до нового стану
    await transition_to_state(
        message=message,
        state=state,
        bot=bot,
        new_state=new_state,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text
    )

# Обробник меню "M6 Menu"
@router.message(MenuStates.M6_MENU)
async def handle_m6_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in M6 Menu")
    await message.delete()

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice == MenuButton.M6_INFO.value:
        new_main_text = M6_INFO_TEXT
        new_interactive_text = "M6 Information"
        new_state = MenuStates.M6_MENU
    elif user_choice == MenuButton.M6_STATS.value:
        new_main_text = M6_STATS_TEXT
        new_interactive_text = "M6 Statistics"
        new_state = MenuStates.M6_MENU
    elif user_choice == MenuButton.M6_NEWS.value:
        new_main_text = M6_NEWS_TEXT
        new_interactive_text = "M6 News"
        new_state = MenuStates.M6_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_submenu_inline_keyboard()  # ReplyKeyboardMarkup
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
        new_state = MenuStates.M6_MENU

    # Перехід до нового стану
    await transition_to_state(
        message=message,
        state=state,
        bot=bot,
        new_state=new_state,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text
    )

# Обробник меню "GPT Menu"
@router.message(MenuStates.GPT_MENU)
async def handle_gpt_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in GPT Menu")
    await message.delete()

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice == MenuButton.GPT_DATA_GENERATION.value:
        new_main_text = "📊 Data Generation Functionality Coming Soon."
        new_interactive_text = "GPT Data Generation"
        new_state = MenuStates.GPT_MENU
    elif user_choice == MenuButton.GPT_HINTS.value:
        new_main_text = "💡 GPT Hints Functionality Coming Soon."
        new_interactive_text = "GPT Hints"
        new_state = MenuStates.GPT_MENU
    elif user_choice == MenuButton.GPT_HERO_STATS.value:
        new_main_text = "📈 GPT Hero Statistics Functionality Coming Soon."
        new_interactive_text = "GPT Hero Statistics"
        new_state = MenuStates.GPT_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = get_main_menu_text(message.from_user.first_name)
        new_main_keyboard = get_main_menu()  # ReplyKeyboardMarkup для основного меню
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Unknown command"
        new_state = MenuStates.GPT_MENU

    # Перехід до нового стану
    await transition_to_state(
        message=message,
        state=state,
        bot=bot,
        new_state=new_state,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text
    )

# Обробник Inline кнопок
@router.callback_query()
async def handle_inline_buttons(callback: CallbackQuery, state: FSMContext, db: AsyncSession, bot: Bot):
    data = callback.data
    logger.info(f"User {callback.from_user.id} pressed inline button: {data}")
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if interactive_message_id:
        if data == "mls_button":
            await bot.answer_callback_query(callback.id, text=MLS_BUTTON_RESPONSE_TEXT)
        elif data == "menu_back":
            await state.set_state(MenuStates.MAIN_MENU)
            new_interactive_text = MAIN_MENU_DESCRIPTION
            new_interactive_keyboard = get_generic_inline_keyboard()
            await edit_interactive_message(
                bot=bot,
                chat_id=callback.message.chat.id,
                message_id=interactive_message_id,
                text=new_interactive_text,
                reply_markup=new_interactive_keyboard,
                state=state
            )
            main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=callback.from_user.first_name)
            main_menu_message_id = await send_new_message(
                chat_id=callback.message.chat.id,
                text=main_menu_text_formatted,
                reply_markup=get_main_menu(),
                state=state,
                key="bot_message_id"
            )
            # Видалення старого bot_message, якщо необхідно
            old_bot_message_id = state_data.get('bot_message_id')
            if old_bot_message_id:
                await delete_message(bot, callback.message.chat.id, old_bot_message_id)
        else:
            await bot.answer_callback_query(callback.id, text=UNHANDLED_INLINE_BUTTON_TEXT)
    else:
        logger.error("interactive_message_id not found")
        await bot.answer_callback_query(callback.id, text=GENERIC_ERROR_MESSAGE_TEXT)
    
    await callback.answer()

# Обробник невідомих команд
@router.message(F.text)
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
        new_main_keyboard = get_navigation_submenu_inline_keyboard()
        new_interactive_text = "Navigation Screen"
        new_state = MenuStates.NAVIGATION_MENU
    elif current_state == MenuStates.HEROES_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = "Heroes Menu"
        new_state = MenuStates.HEROES_MENU
    elif current_state == MenuStates.HERO_CLASS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        state_data = await state.get_data()
        hero_class = state_data.get('hero_class', 'Tank')
        heroes_list = state_data.get('heroes_list', 'No available heroes.')
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = f"Hero Class Menu for {hero_class}. Heroes:\n{heroes_list}"
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
    elif current_state == MenuStates.FEEDBACK_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_feedback_menu()
        new_interactive_text = "Feedback Menu"
        new_state = MenuStates.FEEDBACK_MENU
    elif current_state == MenuStates.HELP_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_help_menu()
        new_interactive_text = "Help Menu"
        new_state = MenuStates.HELP_MENU
    elif current_state in [
        MenuStates.SEARCH_HERO.state,
        MenuStates.SEARCH_TOPIC.state,
        MenuStates.CHANGE_USERNAME.state,
        MenuStates.RECEIVE_FEEDBACK.state,
        MenuStates.REPORT_BUG.state
    ]:
        await bot.send_message(
            chat_id=message.chat.id,
            text=USE_BUTTON_NAVIGATION_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.set_state(current_state)
        return
    else:
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU

    # Перехід до нового стану
    await transition_to_state(
        message=message,
        state=state,
        bot=bot,
        new_state=new_state,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text
    )

# Інтеграція обробників з Dispatcher
def setup_handlers(dp: Router):
    dp.include_router(router)
    # Якщо у вас є інші роутери, включіть їх тут, наприклад:
    # dp.include_router(profile_router)

# Допоміжна функція для генерації тексту основного меню з ім'ям користувача
def get_main_menu_text(user_first_name: str) -> str:
    return MAIN_MENU_TEXT.format(user_first_name=user_first_name)