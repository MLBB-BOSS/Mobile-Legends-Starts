# handlers/base.py

import logging
from aiogram import Router, F, Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode
from aiogram.exceptions import BadRequest

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

# Визначаємо стани меню
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

# Централізована функція для оновлення повідомлень
async def update_messages(
    bot: Bot,
    chat_id: int,
    new_main_text: str,
    new_main_keyboard: types.ReplyKeyboardMarkup | types.InlineKeyboardMarkup | None,
    new_interactive_text: str,
    interactive_message_id: int,
    state: FSMContext
):
    """
    Функція для оновлення повідомлень бота та інтерактивного повідомлення.
    """
    try:
        # Редагуємо інтерактивне повідомлення
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_generic_inline_keyboard()
        )
    except BadRequest as e:
        if "message is not modified" in str(e):
            logger.warning("Спроба редагувати повідомлення без змін.")
        else:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            # Відправляємо нове інтерактивне повідомлення
            interactive_message = await bot.send_message(
                chat_id=chat_id,
                text=new_interactive_text,
                parse_mode=ParseMode.HTML,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
    
    # Видаляємо старе bot-повідомлення
    # Перевірка, чи існує старе повідомлення
    data = await state.get_data()
    old_bot_message_id = data.get('bot_message_id')
    if old_bot_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=old_bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити старе bot-повідомлення: {e}")
    
    # Відправляємо нове bot-повідомлення
    main_message = await bot.send_message(
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id
    await state.update_data(bot_message_id=new_bot_message_id)

# Команда /start з реєстрацією користувача
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
    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=INTRO_PAGE_2_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=get_intro_page_2_keyboard()
        )
    except BadRequest as e:
        if "message is not modified" not in str(e):
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text=GENERIC_ERROR_MESSAGE_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
    await state.set_state(MenuStates.INTRO_PAGE_2)
    await callback.answer()

@router.callback_query(F.data == "intro_next_2")
async def handle_intro_next_2(callback: CallbackQuery, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')
    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=INTRO_PAGE_3_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=get_intro_page_3_keyboard()
        )
    except BadRequest as e:
        if "message is not modified" not in str(e):
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text=GENERIC_ERROR_MESSAGE_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
    await state.set_state(MenuStates.INTRO_PAGE_3)
    await callback.answer()

@router.callback_query(F.data == "intro_start")
async def handle_intro_start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_first_name = callback.from_user.first_name
    main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
    main_menu_message = await bot.send_message(
        chat_id=callback.message.chat.id,
        text=main_menu_text_formatted,
        reply_markup=get_main_menu()
    )
    await state.update_data(bot_message_id=main_menu_message.message_id)
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')
    if interactive_message_id:
        try:
            await bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=interactive_message_id,
                text=MAIN_MENU_DESCRIPTION,
                parse_mode=ParseMode.HTML,
                reply_markup=get_generic_inline_keyboard()
            )
        except BadRequest as e:
            if "message is not modified" not in str(e):
                logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
                # Відправка нового інтерактивного повідомлення
                interactive_message = await bot.send_message(
                    chat_id=callback.message.chat.id,
                    text=MAIN_MENU_DESCRIPTION,
                    parse_mode=ParseMode.HTML,
                    reply_markup=get_generic_inline_keyboard()
                )
                await state.update_data(interactive_message_id=interactive_message.message_id)
    await state.set_state(MenuStates.MAIN_MENU)
    await callback.answer()

# Обробник кнопки "🪪 Мій Профіль"
@router.message(F.text == "🪪 Мій Профіль")
async def handle_my_profile(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_id = message.from_user.id
    profile_data = await get_user_profile(db, user_id)  # Отримання профілю з БД

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
        await message.answer(profile_message, parse_mode="HTML", reply_markup=get_profile_menu())
        await state.set_state(MenuStates.PROFILE_MENU)
    else:
        await message.answer("❌ Дані профілю не знайдено. Зареєструйтесь, щоб переглянути статистику.")

# Централізований обробник для меню (опціонально)
# Можна використовувати централізований обробник для спрощення коду.
# Проте у даному випадку всі обробники вже включені окремо.

# Обробчик невідомих команд
@router.message()
async def unknown_command(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_id = message.from_user.id
    logger.warning(f"Unknown message from {user_id}: {message.text}")
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
        hero_class = data.get('hero_class', 'Танк')
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
        # Якщо користувач перебуває в процесі введення, надсилаємо підказку
        await bot.send_message(chat_id=message.chat.id, text=USE_BUTTON_NAVIGATION_TEXT, reply_markup=get_generic_inline_keyboard())
        await state.set_state(current_state)
        return
    else:
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU

    main_message = await bot.send_message(chat_id=message.chat.id, text=new_main_text, reply_markup=new_main_keyboard)
    new_bot_message_id = main_message.message_id
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Failed to delete bot message: {e}")
    if interactive_message_id:
        try:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=interactive_message_id,
                text=new_interactive_text,
                parse_mode=ParseMode.HTML,
                reply_markup=get_generic_inline_keyboard()
            )
        except Exception as e:
            logger.error(f"Failed to edit interactive message: {e}")
            interactive_message = await bot.send_message(chat_id=message.chat.id, text=new_interactive_text, reply_markup=get_generic_inline_keyboard())
            await state.update_data(interactive_message_id=interactive_message.message_id)
    else:
        interactive_message = await bot.send_message(chat_id=message.chat.id, text=new_interactive_text, reply_markup=get_generic_inline_keyboard())
        await state.update_data(interactive_message_id=interactive_message.message_id)
    await state.set_state(new_state)

# Обробник Inline кнопок
@router.callback_query()
async def handle_inline_buttons(callback: CallbackQuery, state: FSMContext, db: AsyncSession, bot: Bot):
    data = callback.data
    user_id = callback.from_user.id
    logger.info(f"User {user_id} pressed inline button: {data}")
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')
    if interactive_message_id:
        if data == "mls_button":
            await bot.answer_callback_query(callback.id, text=MLS_BUTTON_RESPONSE_TEXT)
        elif data == "menu_back":
            user_first_name = callback.from_user.first_name
            main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
            main_menu_message = await bot.send_message(
                chat_id=callback.message.chat.id,
                text=main_menu_text_formatted,
                reply_markup=get_main_menu()
            )
            await state.update_data(bot_message_id=main_menu_message.message_id)
            new_interactive_text = MAIN_MENU_DESCRIPTION
            new_interactive_keyboard = get_generic_inline_keyboard()
            try:
                await bot.edit_message_text(
                    chat_id=callback.message.chat.id,
                    message_id=interactive_message_id,
                    text=new_interactive_text,
                    parse_mode=ParseMode.HTML,
                    reply_markup=new_interactive_keyboard
                )
            except BadRequest as e:
                if "message is not modified" not in str(e):
                    logger.error(f"Failed to edit interactive message: {e}")
                    # Відправка нового інтерактивного повідомлення
                    interactive_message = await bot.send_message(
                        chat_id=callback.message.chat.id,
                        text=new_interactive_text,
                        parse_mode=ParseMode.HTML,
                        reply_markup=get_generic_inline_keyboard()
                    )
                    await state.update_data(interactive_message_id=interactive_message.message_id)
            # Видалення попереднього повідомлення з клавіатурою
            old_bot_message_id = state_data.get('bot_message_id')
            if old_bot_message_id:
                try:
                    await bot.delete_message(chat_id=callback.message.chat.id, message_id=old_bot_message_id)
                except Exception as e:
                    logger.error(f"Failed to delete old bot message: {e}")
        else:
            await bot.answer_callback_query(callback.id, text=UNHANDLED_INLINE_BUTTON_TEXT)
    else:
        logger.error("interactive_message_id not found")
        await bot.answer_callback_query(callback.id, text=GENERIC_ERROR_MESSAGE_TEXT)
    await callback.answer()

# Обробчик пошуку героя
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

# Обробчик пропозиції теми
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

# Обробчик зміни імені користувача
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

# Обробчик отримання зворотного зв'язку
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

# Обробчик повідомлення про помилку
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

# Обробчик меню "Main Menu"
@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    user_id = message.from_user.id
    logger.info(f"User {user_id} selected '{user_choice}' in Main Menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначення текстів та клавіатур для вибраних опцій
    menu_texts = {
        MenuButton.NAVIGATION.value: NAVIGATION_MENU_TEXT,
        MenuButton.PROFILE.value: PROFILE_MENU_TEXT,
        MenuButton.TOURNAMENTS.value: "Меню Турніри",
        MenuButton.META.value: "Меню META",
        MenuButton.M6.value: "Меню M6",
        MenuButton.GPT.value: "Меню GPT",
        'default': UNKNOWN_COMMAND_TEXT
    }

    menu_keyboards = {
        MenuButton.NAVIGATION.value: get_navigation_menu(),
        MenuButton.PROFILE.value: get_profile_menu(),
        MenuButton.TOURNAMENTS.value: get_tournaments_menu(),
        MenuButton.META.value: get_meta_menu(),
        MenuButton.M6.value: get_m6_menu(),
        MenuButton.GPT.value: get_gpt_menu(),
        'default': get_main_menu()
    }

    interactive_texts = {
        MenuButton.NAVIGATION.value: NAVIGATION_INTERACTIVE_TEXT,
        MenuButton.PROFILE.value: PROFILE_INTERACTIVE_TEXT,
        MenuButton.TOURNAMENTS.value: "Меню Турніри",
        MenuButton.META.value: "Меню META",
        MenuButton.M6.value: "Меню M6",
        MenuButton.GPT.value: "Меню GPT",
        'default': "Невідома команда"
    }

    next_states = {
        MenuButton.NAVIGATION.value: MenuStates.NAVIGATION_MENU,
        MenuButton.PROFILE.value: MenuStates.PROFILE_MENU,
        MenuButton.TOURNAMENTS.value: MenuStates.TOURNAMENTS_MENU,
        MenuButton.META.value: MenuStates.META_MENU,
        MenuButton.M6.value: MenuStates.M6_MENU,
        MenuButton.GPT.value: MenuStates.GPT_MENU,
        'default': MenuStates.MAIN_MENU
    }

    new_state = next_states.get(user_choice, MenuStates.MAIN_MENU)
    new_main_text = menu_texts.get(user_choice, UNKNOWN_COMMAND_TEXT)
    new_main_keyboard = menu_keyboards.get(user_choice, get_main_menu())
    new_interactive_text = interactive_texts.get(user_choice, "Невідома команда")

    # Виклик централізованої функції для оновлення повідомлень
    await update_messages(
        bot=bot,
        chat_id=message.chat.id,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text,
        interactive_message_id=interactive_message_id,
        state=state
    )

    # Встановлення нового стану
    await state.set_state(new_state)

# Обробчик меню "Navigation Menu"
@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    user_id = message.from_user.id
    logger.info(f"User {user_id} selected '{user_choice}' in Navigation Menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначення текстів та клавіатур для вибраних опцій
    menu_texts = {
        MenuButton.HEROES.value: HEROES_MENU_TEXT,
        MenuButton.GUIDES.value: GUIDES_MENU_TEXT,
        MenuButton.COUNTER_PICKS.value: COUNTER_PICKS_MENU_TEXT,
        MenuButton.BUILDS.value: BUILDS_MENU_TEXT,
        MenuButton.VOTING.value: VOTING_MENU_TEXT,
        MenuButton.TOURNAMENTS.value: "Меню Турніри",
        MenuButton.META.value: "Меню META",
        MenuButton.M6.value: "Меню M6",
        MenuButton.GPT.value: "Меню GPT",
        MenuButton.BACK.value: MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name),
        'default': UNKNOWN_COMMAND_TEXT
    }

    menu_keyboards = {
        MenuButton.HEROES.value: get_heroes_menu(),
        MenuButton.GUIDES.value: get_guides_menu(),
        MenuButton.COUNTER_PICKS.value: get_counter_picks_menu(),
        MenuButton.BUILDS.value: get_builds_menu(),
        MenuButton.VOTING.value: get_voting_menu(),
        MenuButton.TOURNAMENTS.value: get_tournaments_menu(),
        MenuButton.META.value: get_meta_menu(),
        MenuButton.M6.value: get_m6_menu(),
        MenuButton.GPT.value: get_gpt_menu(),
        MenuButton.BACK.value: get_main_menu(),
        'default': get_navigation_menu()
    }

    interactive_texts = {
        MenuButton.HEROES.value: HEROES_INTERACTIVE_TEXT,
        MenuButton.GUIDES.value: GUIDES_INTERACTIVE_TEXT,
        MenuButton.COUNTER_PICKS.value: COUNTER_PICKS_INTERACTIVE_TEXT,
        MenuButton.BUILDS.value: BUILDS_INTERACTIVE_TEXT,
        MenuButton.VOTING.value: VOTING_INTERACTIVE_TEXT,
        MenuButton.TOURNAMENTS.value: "Меню Турніри",
        MenuButton.META.value: "Меню META",
        MenuButton.M6.value: "Меню M6",
        MenuButton.GPT.value: "Меню GPT",
        MenuButton.BACK.value: MAIN_MENU_DESCRIPTION,
        'default': "Невідома команда"
    }

    next_states = {
        MenuButton.HEROES.value: MenuStates.HEROES_MENU,
        MenuButton.GUIDES.value: MenuStates.GUIDES_MENU,
        MenuButton.COUNTER_PICKS.value: MenuStates.COUNTER_PICKS_MENU,
        MenuButton.BUILDS.value: MenuStates.BUILDS_MENU,
        MenuButton.VOTING.value: MenuStates.VOTING_MENU,
        MenuButton.TOURNAMENTS.value: MenuStates.TOURNAMENTS_MENU,
        MenuButton.META.value: MenuStates.META_MENU,
        MenuButton.M6.value: MenuStates.M6_MENU,
        MenuButton.GPT.value: MenuStates.GPT_MENU,
        MenuButton.BACK.value: MenuStates.MAIN_MENU,
        'default': MenuStates.NAVIGATION_MENU
    }

    new_state = next_states.get(user_choice, MenuStates.NAVIGATION_MENU)
    new_main_text = menu_texts.get(user_choice, UNKNOWN_COMMAND_TEXT)
    new_main_keyboard = menu_keyboards.get(user_choice, get_navigation_menu())
    new_interactive_text = interactive_texts.get(user_choice, "Невідома команда")

    # Виклик централізованої функції для оновлення повідомлень
    await update_messages(
        bot=bot,
        chat_id=message.chat.id,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text,
        interactive_message_id=interactive_message_id,
        state=state
    )

    # Встановлення нового стану
    await state.set_state(new_state)

# Обробчик меню "Feedback Menu"
@router.message(MenuStates.FEEDBACK_MENU)
async def handle_feedback_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    user_id = message.from_user.id
    logger.info(f"User {user_id} selected '{user_choice}' in Feedback Menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначення текстів та клавіатур для вибраних опцій
    menu_texts = {
        MenuButton.SEND_FEEDBACK.value: SEND_FEEDBACK_TEXT,
        MenuButton.REPORT_BUG.value: REPORT_BUG_TEXT,
        MenuButton.BACK.value: PROFILE_MENU_TEXT,
        'default': UNKNOWN_COMMAND_TEXT
    }

    menu_keyboards = {
        MenuButton.SEND_FEEDBACK.value: types.ReplyKeyboardRemove(),
        MenuButton.REPORT_BUG.value: types.ReplyKeyboardRemove(),
        MenuButton.BACK.value: get_profile_menu(),
        'default': get_feedback_menu()
    }

    interactive_texts = {
        MenuButton.SEND_FEEDBACK.value: "Sending feedback",
        MenuButton.REPORT_BUG.value: "Reporting a bug",
        MenuButton.BACK.value: PROFILE_INTERACTIVE_TEXT,
        'default': "Unknown command"
    }

    next_states = {
        MenuButton.SEND_FEEDBACK.value: MenuStates.RECEIVE_FEEDBACK,
        MenuButton.REPORT_BUG.value: MenuStates.REPORT_BUG,
        MenuButton.BACK.value: MenuStates.PROFILE_MENU,
        'default': MenuStates.FEEDBACK_MENU
    }

    new_state = next_states.get(user_choice, MenuStates.FEEDBACK_MENU)
    new_main_text = menu_texts.get(user_choice, UNKNOWN_COMMAND_TEXT)
    new_main_keyboard = menu_keyboards.get(user_choice, get_feedback_menu())
    new_interactive_text = interactive_texts.get(user_choice, "Unknown command")

    # Виклик централізованої функції для оновлення повідомлень
    await update_messages(
        bot=bot,
        chat_id=message.chat.id,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text,
        interactive_message_id=interactive_message_id,
        state=state
    )

    # Встановлення нового стану
    await state.set_state(new_state)

# Обробчик меню "Tournaments Menu"
@router.message(MenuStates.TOURNAMENTS_MENU)
async def handle_tournaments_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    user_id = message.from_user.id
    logger.info(f"User {user_id} selected '{user_choice}' in Tournaments Menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначення текстів та клавіатур для вибраних опцій
    menu_texts = {
        MenuButton.CREATE_TOURNAMENT.value: TOURNAMENT_CREATE_TEXT,
        MenuButton.VIEW_TOURNAMENTS.value: TOURNAMENT_VIEW_TEXT,
        MenuButton.BACK.value: NAVIGATION_MENU_TEXT,
        'default': UNKNOWN_COMMAND_TEXT
    }

    menu_keyboards = {
        MenuButton.CREATE_TOURNAMENT.value: get_tournaments_menu(),
        MenuButton.VIEW_TOURNAMENTS.value: get_tournaments_menu(),
        MenuButton.BACK.value: get_navigation_menu(),
        'default': get_tournaments_menu()
    }

    interactive_texts = {
        MenuButton.CREATE_TOURNAMENT.value: "Creating a tournament",
        MenuButton.VIEW_TOURNAMENTS.value: "Viewing tournaments",
        MenuButton.BACK.value: NAVIGATION_INTERACTIVE_TEXT,
        'default': "Unknown command"
    }

    next_states = {
        MenuButton.CREATE_TOURNAMENT.value: MenuStates.TOURNAMENTS_MENU,  # Можна змінити стан, якщо потрібно
        MenuButton.VIEW_TOURNAMENTS.value: MenuStates.TOURNAMENTS_MENU,  # Можна змінити стан, якщо потрібно
        MenuButton.BACK.value: MenuStates.NAVIGATION_MENU,
        'default': MenuStates.TOURNAMENTS_MENU
    }

    new_state = next_states.get(user_choice, MenuStates.TOURNAMENTS_MENU)
    new_main_text = menu_texts.get(user_choice, UNKNOWN_COMMAND_TEXT)
    new_main_keyboard = menu_keyboards.get(user_choice, get_tournaments_menu())
    new_interactive_text = interactive_texts.get(user_choice, "Unknown command")

    # Виклик централізованої функції для оновлення повідомлень
    await update_messages(
        bot=bot,
        chat_id=message.chat.id,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text,
        interactive_message_id=interactive_message_id,
        state=state
    )

    # Встановлення нового стану
    await state.set_state(new_state)

# Обробчик меню "META Menu"
@router.message(MenuStates.META_MENU)
async def handle_meta_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    user_id = message.from_user.id
    logger.info(f"User {user_id} selected '{user_choice}' in META Menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначення текстів та клавіатур для вибраних опцій
    menu_texts = {
        MenuButton.META_HERO_LIST.value: META_HERO_LIST_TEXT,
        MenuButton.META_RECOMMENDATIONS.value: META_RECOMMENDATIONS_TEXT,
        MenuButton.META_UPDATES.value: META_UPDATES_TEXT,
        MenuButton.BACK.value: NAVIGATION_MENU_TEXT,
        'default': UNKNOWN_COMMAND_TEXT
    }

    menu_keyboards = {
        MenuButton.META_HERO_LIST.value: get_meta_menu(),
        MenuButton.META_RECOMMENDATIONS.value: get_meta_menu(),
        MenuButton.META_UPDATES.value: get_meta_menu(),
        MenuButton.BACK.value: get_navigation_menu(),
        'default': get_meta_menu()
    }

    interactive_texts = {
        MenuButton.META_HERO_LIST.value: "META Hero List",
        MenuButton.META_RECOMMENDATIONS.value: "META Recommendations",
        MenuButton.META_UPDATES.value: "META Updates",
        MenuButton.BACK.value: NAVIGATION_INTERACTIVE_TEXT,
        'default': "Unknown command"
    }

    next_states = {
        MenuButton.META_HERO_LIST.value: MenuStates.META_MENU,  # Можна змінити стан, якщо потрібно
        MenuButton.META_RECOMMENDATIONS.value: MenuStates.META_MENU,  # Можна змінити стан, якщо потрібно
        MenuButton.META_UPDATES.value: MenuStates.META_MENU,  # Можна змінити стан, якщо потрібно
        MenuButton.BACK.value: MenuStates.NAVIGATION_MENU,
        'default': MenuStates.META_MENU
    }

    new_state = next_states.get(user_choice, MenuStates.META_MENU)
    new_main_text = menu_texts.get(user_choice, UNKNOWN_COMMAND_TEXT)
    new_main_keyboard = menu_keyboards.get(user_choice, get_meta_menu())
    new_interactive_text = interactive_texts.get(user_choice, "Unknown command")

    # Виклик централізованої функції для оновлення повідомлень
    await update_messages(
        bot=bot,
        chat_id=message.chat.id,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text,
        interactive_message_id=interactive_message_id,
        state=state
    )

    # Встановлення нового стану
    await state.set_state(new_state)

# Обробчик меню "M6 Menu"
@router.message(MenuStates.M6_MENU)
async def handle_m6_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    user_id = message.from_user.id
    logger.info(f"User {user_id} selected '{user_choice}' in M6 Menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначення текстів та клавіатур для вибраних опцій
    menu_texts = {
        MenuButton.M6_INFO.value: M6_INFO_TEXT,
        MenuButton.M6_STATS.value: M6_STATS_TEXT,
        MenuButton.M6_NEWS.value: M6_NEWS_TEXT,
        MenuButton.BACK.value: NAVIGATION_MENU_TEXT,
        'default': UNKNOWN_COMMAND_TEXT
    }

    menu_keyboards = {
        MenuButton.M6_INFO.value: get_m6_menu(),
        MenuButton.M6_STATS.value: get_m6_menu(),
        MenuButton.M6_NEWS.value: get_m6_menu(),
        MenuButton.BACK.value: get_navigation_menu(),
        'default': get_m6_menu()
    }

    interactive_texts = {
        MenuButton.M6_INFO.value: "M6 Info",
        MenuButton.M6_STATS.value: "M6 Stats",
        MenuButton.M6_NEWS.value: "M6 News",
        MenuButton.BACK.value: NAVIGATION_INTERACTIVE_TEXT,
        'default': "Unknown command"
    }

    next_states = {
        MenuButton.M6_INFO.value: MenuStates.M6_MENU,  # Можна змінити стан, якщо потрібно
        MenuButton.M6_STATS.value: MenuStates.M6_MENU,  # Можна змінити стан, якщо потрібно
        MenuButton.M6_NEWS.value: MenuStates.M6_MENU,  # Можна змінити стан, якщо потрібно
        MenuButton.BACK.value: MenuStates.NAVIGATION_MENU,
        'default': MenuStates.M6_MENU
    }

    new_state = next_states.get(user_choice, MenuStates.M6_MENU)
    new_main_text = menu_texts.get(user_choice, UNKNOWN_COMMAND_TEXT)
    new_main_keyboard = menu_keyboards.get(user_choice, get_m6_menu())
    new_interactive_text = interactive_texts.get(user_choice, "Unknown command")

    # Виклик централізованої функції для оновлення повідомлень
    await update_messages(
        bot=bot,
        chat_id=message.chat.id,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text,
        interactive_message_id=interactive_message_id,
        state=state
    )

    # Встановлення нового стану
    await state.set_state(new_state)

# Обробчик меню "GPT Menu"
@router.message(MenuStates.GPT_MENU)
async def handle_gpt_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    user_id = message.from_user.id
    logger.info(f"User {user_id} selected '{user_choice}' in GPT Menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначення текстів та клавіатур для вибраних опцій
    menu_texts = {
        MenuButton.GPT_DATA_GENERATION.value: "Функціонал Генерації Даних GPT буде доступний пізніше.",
        MenuButton.GPT_HINTS.value: "Функціонал Порад GPT буде доступний пізніше.",
        MenuButton.GPT_HERO_STATS.value: "Функціонал Статистики Героїв GPT буде доступний пізніше.",
        MenuButton.BACK.value: NAVIGATION_MENU_TEXT,
        'default': UNKNOWN_COMMAND_TEXT
    }

    menu_keyboards = {
        MenuButton.GPT_DATA_GENERATION.value: get_gpt_menu(),
        MenuButton.GPT_HINTS.value: get_gpt_menu(),
        MenuButton.GPT_HERO_STATS.value: get_gpt_menu(),
        MenuButton.BACK.value: get_navigation_menu(),
        'default': get_gpt_menu()
    }

    interactive_texts = {
        MenuButton.GPT_DATA_GENERATION.value: "GPT: Генерація Даних",
        MenuButton.GPT_HINTS.value: "GPT: Поради",
        MenuButton.GPT_HERO_STATS.value: "GPT: Статистика Героїв",
        MenuButton.BACK.value: NAVIGATION_INTERACTIVE_TEXT,
        'default': "Unknown command"
    }

    next_states = {
        MenuButton.GPT_DATA_GENERATION.value: MenuStates.GPT_MENU,  # Можна змінити стан, якщо потрібно
        MenuButton.GPT_HINTS.value: MenuStates.GPT_MENU,  # Можна змінити стан, якщо потрібно
        MenuButton.GPT_HERO_STATS.value: MenuStates.GPT_MENU,  # Можна змінити стан, якщо потрібно
        MenuButton.BACK.value: MenuStates.NAVIGATION_MENU,
        'default': MenuStates.GPT_MENU
    }

    new_state = next_states.get(user_choice, MenuStates.GPT_MENU)
    new_main_text = menu_texts.get(user_choice, UNKNOWN_COMMAND_TEXT)
    new_main_keyboard = menu_keyboards.get(user_choice, get_gpt_menu())
    new_interactive_text = interactive_texts.get(user_choice, "Unknown command")

    # Виклик централізованої функції для оновлення повідомлень
    await update_messages(
        bot=bot,
        chat_id=message.chat.id,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text,
        interactive_message_id=interactive_message_id,
        state=state
    )

    # Встановлення нового стану
    await state.set_state(new_state)

# Обробчик меню "Heroes Menu"
@router.message(MenuStates.HEROES_MENU)
async def handle_heroes_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    user_id = message.from_user.id
    logger.info(f"User {user_id} selected '{user_choice}' in Heroes Menu")
    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначення текстів та клавіатур для вибраних опцій
    menu_texts = {
        **heroes_by_class,
        MenuButton.SEARCH_HERO.value: SEARCH_HERO_RESPONSE_TEXT,
        MenuButton.COMPARISON.value: "Hero comparison feature is under development.",
        MenuButton.BACK.value: NAVIGATION_MENU_TEXT,
        'default': UNKNOWN_COMMAND_TEXT
    }

    menu_keyboards = {
        MenuButton.TANK.value: get_hero_class_menu("Танк"),
        MenuButton.MAGE.value: get_hero_class_menu("Маг"),
        MenuButton.MARKSMAN.value: get_hero_class_menu("Стрілець"),
        MenuButton.ASSASSIN.value: get_hero_class_menu("Асасін"),
        MenuButton.FIGHTER.value: get_hero_class_menu("Боєць"),
        MenuButton.SUPPORT.value: get_hero_class_menu("Підтримка"),
        MenuButton.SEARCH_HERO.value: types.ReplyKeyboardRemove(),
        MenuButton.COMPARISON.value: get_heroes_menu(),
        MenuButton.BACK.value: get_navigation_menu(),
        'default': get_heroes_menu()
    }

    interactive_texts = {
        **{cls: HERO_CLASS_INTERACTIVE_TEXT.format(hero_class=cls, heroes_list=", ".join(heroes_by_class.get(cls, [])))
           for cls in heroes_by_class},
        MenuButton.SEARCH_HERO.value: "Search Hero",
        MenuButton.COMPARISON.value: "Compare Heroes",
        MenuButton.BACK.value: NAVIGATION_INTERACTIVE_TEXT,
        'default': "Unknown command"
    }

    next_states = {
        **{cls: MenuStates.HERO_CLASS_MENU for cls in heroes_by_class},
        MenuButton.SEARCH_HERO.value: MenuStates.SEARCH_HERO,
        MenuButton.COMPARISON.value: MenuStates.HEROES_MENU,
        MenuButton.BACK.value: MenuStates.NAVIGATION_MENU,
        'default': MenuStates.HEROES_MENU
    }

    new_state = next_states.get(user_choice, MenuStates.HEROES_MENU)
    new_main_text = menu_texts.get(user_choice, UNKNOWN_COMMAND_TEXT)
    new_main_keyboard = menu_keyboards.get(user_choice, get_heroes_menu())
    new_interactive_text = interactive_texts.get(user_choice, "Unknown command")

    # Якщо обрано клас героя, зберігаємо вибір у стані
    if user_choice in heroes_by_class:
        await state.update_data(hero_class=user_choice, heroes_list=", ".join(heroes_by_class.get(user_choice, [])))

    # Виклик централізованої функції для оновлення повідомлень
    await update_messages(
        bot=bot,
        chat_id=message.chat.id,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text,
        interactive_message_id=interactive_message_id,
        state=state
    )

    # Встановлення нового стану
    await state.set_state(new_state)

# Інші обробники меню можна додати аналогічним чином, використовуючи централізовану функцію `update_messages`

# Інтеграція обробників з Dispatcher
def setup_handlers(dp: Dispatcher):
    dp.include_router(router)
    # Якщо у вас є інші роутери, включіть їх тут, наприклад:
    # dp.include_router(profile_router)