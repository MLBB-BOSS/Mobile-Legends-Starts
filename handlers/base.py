# handlers/base.py

import logging
import io
from typing import Optional, Dict
from datetime import datetime
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
    ReplyKeyboardRemove
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from states import MenuStates
from utils.db import async_session, get_user_profile
from utils.models import User, UserStats, Feedback, BugReport
from utils.keyboards import (
    get_main_menu_keyboard, get_profile_keyboard, get_generic_inline_keyboard,
    get_intro_page_1_keyboard, get_intro_page_2_keyboard, get_intro_page_3_keyboard,
    get_navigation_menu, get_heroes_menu, get_hero_class_menu, get_guides_menu,
    get_counter_picks_menu, get_builds_menu, get_voting_menu, get_statistics_menu,
    get_achievements_menu, get_settings_menu, get_feedback_menu, get_help_menu,
    get_tournaments_menu, get_meta_menu, get_m6_menu, get_gpt_menu
)
from utils.message_utils import safe_delete_message, check_and_edit_message
from utils.text_formatter import format_profile_text
from utils.graph_utils import (
    create_overall_activity_graph, create_rating_graph,
    create_game_stats_graph, create_comparison_graph
)
from texts import (
    INTRO_PAGE_1_TEXT, INTRO_PAGE_2_TEXT, INTRO_PAGE_3_TEXT, MAIN_MENU_TEXT,
    MAIN_MENU_DESCRIPTION, MAIN_MENU_ERROR_TEXT, NAVIGATION_MENU_TEXT,
    NAVIGATION_INTERACTIVE_TEXT, PROFILE_MENU_TEXT, PROFILE_INTERACTIVE_TEXT,
    UNKNOWN_COMMAND_TEXT, GENERIC_ERROR_MESSAGE_TEXT, HEROES_MENU_TEXT,
    HEROES_INTERACTIVE_TEXT, HERO_CLASS_MENU_TEXT, HERO_CLASS_INTERACTIVE_TEXT,
    GUIDES_MENU_TEXT, GUIDES_INTERACTIVE_TEXT, POPULAR_GUIDES_TEXT,
    SEND_FEEDBACK_TEXT, BUG_REPORT_RECEIVED_TEXT, CHANGE_USERNAME_RESPONSE_TEXT,
    FEEDBACK_RECEIVED_TEXT, REPORT_BUG_TEXT, SUGGESTION_RESPONSE_TEXT,
    SEARCH_HERO_RESPONSE_TEXT, MAIN_MENU_BACK_TO_PROFILE_TEXT,
    TOURNAMENT_CREATE_TEXT, TOURNAMENT_VIEW_TEXT, META_HERO_LIST_TEXT,
    META_RECOMMENDATIONS_TEXT, META_UPDATES_TEXT, M6_INFO_TEXT, M6_STATS_TEXT,
    M6_NEWS_TEXT, GPT_MENU_TEXT, UNHANDLED_INLINE_BUTTON_TEXT,
    MLS_BUTTON_RESPONSE_TEXT, USE_BUTTON_NAVIGATION_TEXT
)
from keyboards.menus import (
    MenuButton, get_main_menu, get_profile_menu, get_generic_inline_keyboard
)

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізація роутера
router = Router()

# Мапінг кнопок до класів героїв
MENU_BUTTON_TO_CLASS: Dict[str, str] = {
    MenuButton.TANK.value: "Танк",
    MenuButton.MAGE.value: "Маг",
    MenuButton.MARKSMAN.value: "Стрілець",
    MenuButton.ASSASSIN.value: "Асасін",
    MenuButton.SUPPORT.value: "Підтримка",
    MenuButton.FIGHTER.value: "Боєць"
}

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка команди /start
# --------------------------------------------------------------------------------
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, db: AsyncSession, bot: Bot) -> None:
    """
    Обробник команди /start, реєструє користувача та відправляє вступні сторінки.
    """
    user_id = message.from_user.id

    # Видаляємо повідомлення з командою /start
    await safe_delete_message(bot, message.chat.id, message.message_id)

    try:
        async with db.begin():
            user_result = await db.execute(
                select(User).where(User.telegram_id == user_id)
            )
            user = user_result.scalars().first()

            if not user:
                # Створення нового користувача
                new_user = User(
                    telegram_id=user_id,
                    username=message.from_user.username or message.from_user.full_name,
                    created_at=datetime.utcnow()
                )
                db.add(new_user)
                await db.flush()

                new_stats = UserStats(user_id=new_user.id)
                db.add(new_stats)

                await db.commit()
                logger.info(f"Зареєстровано нового користувача: {user_id}")

            else:
                logger.info(f"Існуючий користувач: {user_id}")

    except Exception as e:
        logger.error(f"Помилка при реєстрації користувача {user_id}: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger)
        return

    # Встановлення стану на INTRO_PAGE_1 без очищення стану
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
            bot_message_id=None  # Оскільки це інтерактивне повідомлення
        )
    except Exception as e:
        logger.error(f"Не вдалося надіслати вступну сторінку 1: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger)

# --------------------------------------------------------------------------------
# XOMO-Handler: Показ профілю користувача
# --------------------------------------------------------------------------------
@router.callback_query(F.data == "profile")
async def show_profile(callback: CallbackQuery, db: AsyncSession, bot: Bot) -> None:
    """Показує профіль користувача"""
    try:
        user_id = callback.from_user.id

        async with db.begin():
            user = await db.get(User, user_id)

            if not user:
                await callback.answer("Профіль не знайдено", show_alert=True)
                return

            profile_text = (
                f"👤 Профіль гравця\n\n"
                f"Нікнейм: {user.username}\n"
                f"Дата реєстрації: {user.created_at.strftime('%Y-%m-%d')}\n"
                f"Рейтинг: {user.rating or 0}\n"
                f"Турнірів: {user.tournaments_count or 0}\n"
                f"Перемог: {user.wins or 0}\n"
                f"Всього матчів: {user.matches_count or 0}"
            )

            await callback.message.edit_text(
                profile_text,
                reply_markup=get_profile_keyboard()
            )

    except Exception as e:
        error_msg = f"Помилка при показі профілю: {e}"
        logger.error(error_msg)
        await callback.answer(
            "Сталася помилка при завантаженні профілю",
            show_alert=True
        )

# --------------------------------------------------------------------------------
# XOMO-Handler: Повернення до головного меню
# --------------------------------------------------------------------------------
@router.callback_query(F.data == "menu_main")
async def return_to_main_menu(callback: CallbackQuery, bot: Bot) -> None:
    """Повертає користувача до головного меню"""
    try:
        await callback.message.edit_text(
            "Головне меню:",
            reply_markup=get_main_menu_keyboard()
        )
    except Exception as e:
        logger.error(f"Помилка при поверненні до головного меню: {e}")
        await callback.answer("Сталася помилка", show_alert=True)

# --------------------------------------------------------------------------------
# XOMO-Handler: Глобальний обробник помилок
# --------------------------------------------------------------------------------
@router.errors()
async def error_handler(update: types.Update, exception: Exception) -> None:
    """Глобальний обробник помилок"""
    logger.error(f"Помилка при обробці оновлення {update}: {exception}")

    if isinstance(update.event, Message):
        await update.event.answer(
            "Сталася помилка при обробці вашого запиту. Спробуйте пізніше або зверніться до адміністратора."
        )
    elif isinstance(update.event, CallbackQuery):
        await update.event.answer(
            "Сталася помилка. Спробуйте пізніше.",
            show_alert=True
        )

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробник натискання кнопки "🪪 Мій Профіль"
# --------------------------------------------------------------------------------
@router.message(F.text == "🪪 Мій Профіль")
async def handle_my_profile_handler(message: Message, state: FSMContext, db: AsyncSession, bot: Bot) -> None:
    """
    Обробчик натискання кнопки "🪪 Мій Профіль".
    """
    await increment_step(state)
    await process_my_profile(message=message, state=state, db=db, bot=bot)

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка головного меню
# --------------------------------------------------------------------------------
@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot) -> None:
    """
    Обробчик кнопок у головному меню.
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в головному меню")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    await handle_menu(
        user_choice=user_choice,
        message=message,
        state=state,
        db=db,
        bot=bot,
        chat_id=message.chat.id,
        main_menu_error=MAIN_MENU_ERROR_TEXT,
        main_menu_keyboard_func=get_main_menu,
        main_menu_text=MAIN_MENU_TEXT,
        interactive_text=MAIN_MENU_DESCRIPTION,
        new_state=MenuStates.MAIN_MENU
    )

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка меню Зворотний Зв'язок
# --------------------------------------------------------------------------------
@router.message(MenuStates.FEEDBACK_MENU)
async def handle_feedback_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot) -> None:
    """
    Обробчик кнопок у меню Зворотний Зв'язок.
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Зворотний Зв'язок")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            await state.update_data(bot_message_id=main_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку головного меню: {e}")
            await handle_error(bot, chat_id=message.chat.id, error_message=MAIN_MENU_ERROR_TEXT, logger=logger)
        return

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_feedback_menu()
    new_interactive_text = ""
    new_state = MenuStates.FEEDBACK_MENU

    if user_choice == MenuButton.SEND_FEEDBACK.value:
        new_main_text = SEND_FEEDBACK_TEXT
        new_interactive_text = "Надсилання зворотного зв'язку"
        new_state = MenuStates.RECEIVE_FEEDBACK
    elif user_choice == MenuButton.REPORT_BUG.value:
        new_main_text = REPORT_BUG_TEXT
        new_interactive_text = "Повідомлення про помилку"
        new_state = MenuStates.REPORT_BUG
    elif user_choice == MenuButton.BACK.value:
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.FEEDBACK_MENU

    # Відправка нового звичайного повідомлення
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося надіслати нове повідомлення: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)
        return

    # Видалення старого звичайного повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану користувача
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка зміни імені користувача
# --------------------------------------------------------------------------------
@router.message(MenuStates.CHANGE_USERNAME)
async def handle_change_username(message: Message, state: FSMContext, db: AsyncSession, bot: Bot) -> None:
    """
    Обробчик для зміни імені користувача.
    """
    new_username = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"Користувач {user_id} змінює ім'я на: {new_username}")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    if new_username:
        try:
            async with db.begin():
                user_result = await db.execute(
                    select(User).where(User.telegram_id == user_id)
                )
                user = user_result.scalars().first()
                if user:
                    user.username = new_username
                    await db.commit()
                    response_text = CHANGE_USERNAME_RESPONSE_TEXT.format(new_username=new_username)
                    logger.info(f"Користувач {user_id} змінив ім'я на: {new_username}")
                else:
                    response_text = "❌ Користувача не знайдено. Зареєструйтесь, щоб змінити ім'я."
        except Exception as e:
            logger.error(f"Помилка при оновленні імені користувача {user_id}: {e}")
            response_text = "❌ Виникла помилка при зміні імені користувача."
    else:
        response_text = "❌ Будь ласка, введіть нове ім'я користувача."

    try:
        await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
    except Exception as e:
        logger.error(f"Не вдалося надіслати повідомлення про зміну імені: {e}")

    await transition_state(state, MenuStates.SETTINGS_MENU)

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка отримання зворотного зв'язку
# --------------------------------------------------------------------------------
@router.message(MenuStates.RECEIVE_FEEDBACK)
async def handle_receive_feedback(message: Message, state: FSMContext, db: AsyncSession, bot: Bot) -> None:
    """
    Обробчик для прийому зворотного зв'язку від користувача.
    """
    feedback = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"Користувач {user_id} надав зворотний зв'язок: {feedback}")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    if feedback:
        try:
            async with db.begin():
                new_feedback = Feedback(user_id=user_id, feedback=feedback, created_at=datetime.utcnow())
                db.add(new_feedback)
                await db.commit()
            response_text = FEEDBACK_RECEIVED_TEXT
            logger.info(f"Зворотний зв'язок отримано від користувача {user_id}")
        except Exception as e:
            logger.error(f"Помилка при збереженні зворотного зв'язку від користувача {user_id}: {e}")
            response_text = "❌ Виникла помилка при збереженні вашого зворотного зв'язку."
    else:
        response_text = "❌ Будь ласка, надайте ваш зворотний зв'язок."

    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=response_text,
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося надіслати повідомлення про отримання зворотного зв'язку: {e}")

    await transition_state(state, MenuStates.FEEDBACK_MENU)

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка отримання звіту про помилку
# --------------------------------------------------------------------------------
@router.message(MenuStates.REPORT_BUG)
async def handle_report_bug(message: Message, state: FSMContext, db: AsyncSession, bot: Bot) -> None:
    """
    Обробчик для прийому звіту про помилку від користувача.
    """
    bug_report = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"Користувач {user_id} повідомив про помилку: {bug_report}")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    if bug_report:
        try:
            async with db.begin():
                new_bug = BugReport(user_id=user_id, report=bug_report, created_at=datetime.utcnow())
                db.add(new_bug)
                await db.commit()
            response_text = BUG_REPORT_RECEIVED_TEXT
            logger.info(f"Звіт про помилку отримано від користувача {user_id}")
        except Exception as e:
            logger.error(f"Помилка при збереженні звіту про помилку від користувача {user_id}: {e}")
            response_text = "❌ Виникла помилка при збереженні вашого звіту про помилку."
    else:
        response_text = "❌ Будь ласка, опишіть помилку, яку ви зустріли."

    try:
        await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
    except Exception as e:
        logger.error(f"Не вдалося надіслати повідомлення про отримання звіту про помилку: {e}")

    await transition_state(state, MenuStates.FEEDBACK_MENU)

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка меню Турніри
# --------------------------------------------------------------------------------
@router.message(MenuStates.TOURNAMENTS_MENU)
async def handle_tournaments_menu_buttons(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Обробчик кнопок у меню Турніри.
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Турніри")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            await state.update_data(bot_message_id=main_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку головного меню: {e}")
            await handle_error(bot, chat_id=message.chat.id, error_message=MAIN_MENU_ERROR_TEXT, logger=logger)
        return

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_tournaments_menu()
    new_interactive_text = ""
    new_state = MenuStates.TOURNAMENTS_MENU

    if user_choice == MenuButton.CREATE_TOURNAMENT.value:
        new_main_text = TOURNAMENT_CREATE_TEXT
        new_interactive_text = "Створення турніру"
    elif user_choice == MenuButton.VIEW_TOURNAMENTS.value:
        new_main_text = TOURNAMENT_VIEW_TEXT
        new_interactive_text = "Перегляд турнірів"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.TOURNAMENTS_MENU

    # Відправка нового повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося надіслати нове повідомлення: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)
        return

    # Видалення старого звичайного повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану користувача
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка меню META
# --------------------------------------------------------------------------------
@router.message(MenuStates.META_MENU)
async def handle_meta_menu_buttons(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Обробчик кнопок у меню META.
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню META")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            await state.update_data(bot_message_id=main_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку головного меню: {e}")
            await handle_error(bot, chat_id=message.chat.id, error_message=MAIN_MENU_ERROR_TEXT, logger=logger)
        return

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_meta_menu()
    new_interactive_text = ""
    new_state = MenuStates.META_MENU

    if user_choice == MenuButton.HERO_LIST.value:
        new_main_text = META_HERO_LIST_TEXT
        new_interactive_text = "Список героїв META"
    elif user_choice == MenuButton.RECOMMENDATIONS.value:
        new_main_text = META_RECOMMENDATIONS_TEXT
        new_interactive_text = "Рекомендації META"
    elif user_choice == MenuButton.UPDATES.value:
        new_main_text = META_UPDATES_TEXT
        new_interactive_text = "Оновлення META"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.META_MENU

    # Відправка нового повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося надіслати нове повідомлення: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану користувача
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка меню M6
# --------------------------------------------------------------------------------
@router.message(MenuStates.M6_MENU)
async def handle_m6_menu_buttons(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Обробчик кнопок у меню M6.
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню M6")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            await state.update_data(bot_message_id=main_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку головного меню: {e}")
            await handle_error(bot, chat_id=message.chat.id, error_message=MAIN_MENU_ERROR_TEXT, logger=logger)
        return

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_m6_menu()
    new_interactive_text = ""
    new_state = MenuStates.M6_MENU

    if user_choice == MenuButton.INFO.value:
        new_main_text = M6_INFO_TEXT
        new_interactive_text = "Інформація про M6"
    elif user_choice == MenuButton.STATS.value:
        new_main_text = M6_STATS_TEXT
        new_interactive_text = "Статистика M6"
    elif user_choice == MenuButton.NEWS.value:
        new_main_text = M6_NEWS_TEXT
        new_interactive_text = "Новини M6"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"

    # Відправка нового повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося надіслати нове повідомлення: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану користувача
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка меню GPT
# --------------------------------------------------------------------------------
@router.message(MenuStates.GPT_MENU)
async def handle_gpt_menu_buttons(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Обробчик кнопок у меню GPT.
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню GPT")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            await state.update_data(bot_message_id=main_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку головного меню: {e}")
            await handle_error(bot, chat_id=message.chat.id, error_message=MAIN_MENU_ERROR_TEXT, logger=logger)
        return

    new_main_text = ""
    new_main_keyboard = get_gpt_menu()
    new_interactive_text = ""
    new_state = MenuStates.GPT_MENU

    if user_choice == MenuButton.CHAT.value:
        new_main_text = "🤖 GPT Chat ще в розробці."
        new_interactive_text = "GPT Chat"
    elif user_choice == MenuButton.ASSIST.value:
        new_main_text = "🤖 GPT Assist ще в розробці."
        new_interactive_text = "GPT Assist"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"

    # Відправка нового повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося надіслати нове повідомлення: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану користувача
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка меню Навігація
# --------------------------------------------------------------------------------
@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu_buttons(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Обробчик кнопок у меню Навігація.
    """
    try:
        user_choice = message.text
        logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Навігація")

        # Видалення старого повідомлення
        await safe_delete_message(bot, message.chat.id, message.message_id)

        # Отримуємо дані стану
        data = await state.get_data()
        bot_message_id = data.get('bot_message_id')
        interactive_message_id = data.get('interactive_message_id')

        # Визначаємо новий текст та клавіатуру
        new_main_text = ""
        new_main_keyboard = None
        new_interactive_text = ""
        new_state: Optional[State] = None

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
        elif user_choice == MenuButton.BACK.value:
            user_first_name = message.from_user.first_name or "Користувач"
            new_main_text = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
            new_main_keyboard = get_main_menu()
            new_interactive_text = MAIN_MENU_DESCRIPTION
            new_state = MenuStates.MAIN_MENU
        else:
            new_main_text = UNKNOWN_COMMAND_TEXT
            new_main_keyboard = get_navigation_menu()
            new_interactive_text = "Невідома команда"
            new_state = MenuStates.NAVIGATION_MENU

        # Відправка нового повідомлення
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=new_main_keyboard
            )
            new_bot_message_id = main_message.message_id
        except Exception as e:
            logger.error(f"Не вдалося надіслати нове повідомлення: {e}")
            await handle_error(
                bot=bot,
                chat_id=message.chat.id,
                error_message=GENERIC_ERROR_MESSAGE_TEXT,
                logger=logger
            )
            return

        # Видалення старого звичайного повідомлення
        if bot_message_id:
            await safe_delete_message(bot, message.chat.id, bot_message_id)

        # Редагування інтерактивного повідомлення
        if interactive_message_id:
            await check_and_edit_message(
                bot=bot,
                chat_id=message.chat.id,
                message_id=interactive_message_id,
                new_text=new_interactive_text,
                new_keyboard=get_generic_inline_keyboard(),
                state=state
            )

        # Оновлення стану
        await state.update_data(bot_message_id=new_bot_message_id)
        if new_state:
            await state.set_state(new_state)

    except Exception as e:
        logger.error(f"Помилка в handle_navigation_menu_buttons: {e}")
        await handle_error(
            bot=bot,
            chat_id=message.chat.id,
            error_message=GENERIC_ERROR_MESSAGE_TEXT,
            logger=logger
        )

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка меню Персонажі
# --------------------------------------------------------------------------------
@router.message(MenuStates.HEROES_MENU)
async def handle_heroes_menu_buttons(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Обробчик кнопок у меню Персонажі.
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Персонажі")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        # Надсилаємо нове повідомлення з клавіатурою
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            await state.update_data(bot_message_id=main_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку головного меню: {e}")
            await handle_error(bot, chat_id=message.chat.id, error_message=MAIN_MENU_ERROR_TEXT, logger=logger)
        return

    new_main_text = ""
    new_main_keyboard = get_heroes_menu()
    new_interactive_text = ""
    new_state: Optional[State] = None

    hero_classes = list(MENU_BUTTON_TO_CLASS.keys())

    if user_choice in hero_classes:
        hero_class = MENU_BUTTON_TO_CLASS.get(user_choice, 'Танк')  # Default to 'Танк' if not found
        new_main_text = HERO_CLASS_MENU_TEXT.format(hero_class=hero_class)
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = HERO_CLASS_INTERACTIVE_TEXT.format(hero_class=hero_class)
        new_state = MenuStates.HERO_CLASS_MENU
        await state.update_data(hero_class=hero_class)
    elif user_choice == MenuButton.SEARCH_HERO.value:
        new_main_text = "🔍 Введіть ім'я героя для пошуку:"
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Пошук героя"
        new_state = MenuStates.SEARCH_HERO
    elif user_choice == MenuButton.COMPARISON.value:
        # Обробка функції порівняння персонажів
        await safe_delete_message(bot, message.chat.id, interactive_message_id)

        # Запитуємо імена двох героїв для порівняння
        try:
            comparison_prompt = "⚔️ Введіть імена двох героїв для порівняння, розділивши їх комою (наприклад, Hero A, Hero B):"
            confirmation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="✅ Так", callback_data="compare_confirm_yes")],
                [InlineKeyboardButton(text="❌ Скасувати", callback_data="compare_confirm_no")]
            ])
            comparison_message = await bot.send_message(
                chat_id=message.chat.id,
                text=comparison_prompt,
                reply_markup=confirmation_keyboard
            )
            await state.update_data(
                comparison_step=1,
                temp_data={'hero1_name': '', 'hero2_name': ''},
                interactive_message_id=comparison_message.message_id
            )
            await transition_state(state, MenuStates.COMPARISON_STEP_1)
        except Exception as e:
            logger.error(f"Не вдалося відправити запит на порівняння героїв: {e}")
            await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)
        return
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.HEROES_MENU

    # Відправка нового повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося надіслати нове повідомлення: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлюємо стан користувача
    if new_state:
        await transition_state(state, new_state)
    await state.update_data(bot_message_id=new_bot_message_id)

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка кроку 1 порівняння героїв
# --------------------------------------------------------------------------------
@router.message(MenuStates.COMPARISON_STEP_1)
async def handle_comparison_step_1(message: Message, state: FSMContext, db: AsyncSession, bot: Bot) -> None:
    """
    Обробчик для прийому імен героїв для порівняння.
    """
    heroes_input = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"Користувач {user_id} ввів героїв для порівняння: {heroes_input}")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    if ',' not in heroes_input:
        response_text = "❌ Будь ласка, введіть імена двох героїв, розділивши їх комою (наприклад, Hero A, Hero B)."
        try:
            await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку порівняння: {e}")
        return

    hero1_name, hero2_name = [name.strip() for name in heroes_input.split(',', 1)]

    # Зберігаємо імена героїв в тимчасові дані
    await state.update_data(
        comparison_step=2,
        temp_data={'hero1_name': hero1_name, 'hero2_name': hero2_name}
    )
    await transition_state(state, MenuStates.COMPARISON_STEP_2)

    # Запитуємо підтвердження або додаткову інформацію, якщо потрібно
    comparison_confirm_text = (
        f"Ви хочете порівняти **{hero1_name}** та **{hero2_name}**?\n\n"
        f"Натисніть '✅ Так' для підтвердження або '❌ Скасувати' для відміни."
    )
    confirmation_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Так", callback_data="compare_confirm_yes")],
        [InlineKeyboardButton(text="❌ Скасувати", callback_data="compare_confirm_no")]
    ])

    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=comparison_confirm_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=confirmation_keyboard
        )
    except Exception as e:
        logger.error(f"Не вдалося надіслати підтвердження порівняння: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка підтвердження порівняння героїв
# --------------------------------------------------------------------------------
@router.callback_query(F.data.startswith("compare_confirm_"))
async def handle_comparison_confirmation(callback: CallbackQuery, state: FSMContext, db: AsyncSession, bot: Bot) -> None:
    """
    Обробчик для підтвердження або скасування порівняння героїв.
    """
    data = callback.data
    state_data = await state.get_data()

    if data == "compare_confirm_yes":
        temp_data = state_data.get('temp_data', {})
        hero1_name = temp_data.get('hero1_name')
        hero2_name = temp_data.get('hero2_name')

        if not hero1_name or not hero2_name:
            response_text = "❌ Дані для порівняння відсутні. Спробуйте ще раз."
            try:
                await bot.send_message(chat_id=callback.message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
            except Exception as e:
                logger.error(f"Не вдалося надіслати повідомлення про помилку порівняння: {e}")
            await transition_state(state, MenuStates.HEROES_MENU)
            return

        # Отримання статистики героїв з бази даних
        try:
            hero1_stats = await get_hero_stats(db, hero1_name)
            hero2_stats = await get_hero_stats(db, hero2_name)
        except Exception as e:
            logger.error(f"Помилка при отриманні статистики героїв: {e}")
            await handle_error(bot, chat_id=callback.message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)
            await transition_state(state, MenuStates.HEROES_MENU)
            return

        if not hero1_stats or not hero2_stats:
            response_text = "❌ Один або обидва герої не знайдені. Перевірте правильність імен."
            try:
                await bot.send_message(chat_id=callback.message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
            except Exception as e:
                logger.error(f"Не вдалося надіслати повідомлення про помилку порівняння: {e}")
            await transition_state(state, MenuStates.HEROES_MENU)
            return

        # Генерація графіка порівняння
        try:
            comparison_graph_bytes = create_comparison_graph(hero1_stats, hero2_stats, hero1_name, hero2_name)
        except Exception as e:
            logger.error(f"Не вдалося згенерувати графік порівняння: {e}")
            await handle_error(bot, chat_id=callback.message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)
            await transition_state(state, MenuStates.HEROES_MENU)
            return

        # Надсилання графіка
        try:
            await bot.send_photo(
                chat_id=callback.message.chat.id,
                photo=io.BytesIO(comparison_graph_bytes),
                caption=f"⚔️ Порівняння: {hero1_name} vs {hero2_name}",
                reply_markup=get_generic_inline_keyboard()
            )
            logger.info(f"Порівняння між {hero1_name} та {hero2_name} надіслано користувачу {callback.from_user.id}")
        except Exception as e:
            logger.error(f"Не вдалося надіслати графік порівняння: {e}")
            await handle_error(bot, chat_id=callback.message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)

        # Очистка тимчасових даних та повернення до меню Персонажі
        await state.update_data(comparison_step=None, temp_data={})
        await transition_state(state, MenuStates.HEROES_MENU)

    elif data == "compare_confirm_no":
        response_text = "❌ Порівняння скасовано."
        try:
            await bot.send_message(chat_id=callback.message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про скасування порівняння: {e}")
        await transition_state(state, MenuStates.HEROES_MENU)
    else:
        logger.warning(f"Некоректні дані для порівняння: {data}")
        await bot.answer_callback_query(callback.id, text="Некоректна дія.", show_alert=True)

    await callback.answer()

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка меню класу героїв
# --------------------------------------------------------------------------------
@router.message(MenuStates.HERO_CLASS_MENU)
async def handle_hero_class_menu_buttons(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Обробчик кнопок у меню класу героїв.
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню класу героїв")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Логіка обробки вибору класу героїв
    if user_choice == MenuButton.BACK.value:
        await handle_menu(
            user_choice=MenuButton.BACK.value,
            message=message,
            state=state,
            db=None,  # Передайте потрібні параметри
            bot=bot,
            chat_id=message.chat.id,
            main_menu_error=UNKNOWN_COMMAND_TEXT,
            main_menu_keyboard_func=get_heroes_menu,
            main_menu_text=HEROES_MENU_TEXT,
            interactive_text=HEROES_INTERACTIVE_TEXT,
            new_state=MenuStates.HEROES_MENU
        )
    else:
        # Додайте вашу логіку для інших виборів
        await handle_menu(
            user_choice=user_choice,
            message=message,
            state=state,
            db=None,  # Передайте потрібні параметри
            bot=bot,
            chat_id=message.chat.id,
            main_menu_error=UNKNOWN_COMMAND_TEXT,
            main_menu_keyboard_func=lambda: get_hero_class_menu(user_choice),
            main_menu_text=HERO_CLASS_MENU_TEXT,
            interactive_text=HERO_CLASS_INTERACTIVE_TEXT.format(hero_class=user_choice),
            new_state=MenuStates.HERO_CLASS_MENU
        )

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка меню Білди
# --------------------------------------------------------------------------------
@router.message(MenuStates.BUILDS_MENU)
async def handle_builds_menu_buttons(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Обробчик кнопок у меню Білди.
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Білди")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Отримуємо дані стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        # Надсилаємо нове повідомлення з клавіатурою
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            # Зберігаємо ID повідомлення бота
            await state.update_data(bot_message_id=main_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку головного меню: {e}")
            await handle_error(bot, chat_id=message.chat.id, error_message=MAIN_MENU_ERROR_TEXT, logger=logger)
        return

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_builds_menu()
    new_interactive_text = ""
    new_state = MenuStates.BUILDS_MENU

    if user_choice == MenuButton.CREATE_BUILD.value:
        new_main_text = CREATE_BUILD_TEXT
        new_interactive_text = "Створення білду"
    elif user_choice == MenuButton.MY_BUILDS.value:
        new_main_text = MY_BUILDS_TEXT
        new_interactive_text = "Мої білди"
    elif user_choice == MenuButton.POPULAR_BUILDS.value:
        new_main_text = POPULAR_BUILDS_TEXT
        new_interactive_text = "Популярні білди"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.BUILDS_MENU

    # Відправка нового повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося надіслати нове повідомлення: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлюємо стан користувача
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка меню Голосування
# --------------------------------------------------------------------------------
@router.message(MenuStates.VOTING_MENU)
async def handle_voting_menu_buttons(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Обробчик кнопок у меню Голосування.
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Голосування")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Отримуємо дані стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        # Надсилаємо нове повідомлення з клавіатурою
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            # Зберігаємо ID повідомлення бота
            await state.update_data(bot_message_id=main_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку головного меню: {e}")
            await handle_error(bot, chat_id=message.chat.id, error_message=MAIN_MENU_ERROR_TEXT, logger=logger)
        return

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_voting_menu()
    new_interactive_text = ""
    new_state = MenuStates.VOTING_MENU

    if user_choice == MenuButton.CURRENT_VOTES.value:
        new_main_text = CURRENT_VOTES_TEXT
        new_interactive_text = "Поточні опитування"
    elif user_choice == MenuButton.MY_VOTES.value:
        new_main_text = MY_VOTES_TEXT
        new_interactive_text = "Мої голосування"
    elif user_choice == MenuButton.SUGGEST_TOPIC.value:
        new_main_text = SUGGEST_TOPIC_TEXT
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Пропозиція теми"
        new_state = MenuStates.SEARCH_TOPIC
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.VOTING_MENU

    # Відправка нового повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося надіслати нове повідомлення: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлюємо стан користувача
    if new_state:
        await transition_state(state, new_state)
    await state.update_data(bot_message_id=new_bot_message_id)

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка меню Профіль
# --------------------------------------------------------------------------------
@router.message(MenuStates.PROFILE_MENU)
async def handle_profile_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot) -> None:
    """
    Обробчик кнопок у меню Профіль.
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Профіль")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Отримуємо дані стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        # Надсилаємо нове повідомлення з клавіатурою
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            await state.update_data(bot_message_id=main_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку головного меню: {e}")
            await handle_error(bot, chat_id=message.chat.id, error_message=MAIN_MENU_ERROR_TEXT, logger=logger)
        return

    # Визначаємо новий текст та клавіатуру
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
        # Повернення до головного меню
        user_first_name = message.from_user.first_name or "Користувач"
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"
        new_main_keyboard = get_profile_menu()
        new_state = MenuStates.PROFILE_MENU

    # Відправляємо нове повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося надіслати нове повідомлення: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)
        return

    # Видаляємо старе повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагуємо інтерактивне повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлюємо стан користувача
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка невідомих повідомлень
# --------------------------------------------------------------------------------
@router.message()
async def unknown_command(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Обробчик для невідомих повідомлень.
    Відповідає залежно від поточного стану користувача.
    """
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо поточний стан
    current_state = await state.get_state()

    # Визначаємо новий текст та клавіатуру залежно від стану
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = current_state

    if current_state == MenuStates.MAIN_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Головне меню"
        new_state = MenuStates.MAIN_MENU
    elif current_state == MenuStates.NAVIGATION_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Навігаційний екран"
        new_state = MenuStates.NAVIGATION_MENU
    elif current_state == MenuStates.HEROES_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = "Меню Персонажі"
        new_state = MenuStates.HEROES_MENU
    elif current_state == MenuStates.HERO_CLASS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        hero_class = data.get('hero_class', 'Танк')
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = f"Меню класу {hero_class}"
        new_state = MenuStates.HERO_CLASS_MENU
    elif current_state == MenuStates.GUIDES_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_guides_menu()
        new_interactive_text = "Меню Гайди"
        new_state = MenuStates.GUIDES_MENU
    elif current_state == MenuStates.COUNTER_PICKS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_counter_picks_menu()
        new_interactive_text = "Меню Контр-піки"
        new_state = MenuStates.COUNTER_PICKS_MENU
    elif current_state == MenuStates.BUILDS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_builds_menu()
        new_interactive_text = "Меню Білди"
        new_state = MenuStates.BUILDS_MENU
    elif current_state == MenuStates.VOTING_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_voting_menu()
        new_interactive_text = "Меню Голосування"
        new_state = MenuStates.VOTING_MENU
    elif current_state == MenuStates.PROFILE_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "Меню Профіль"
        new_state = MenuStates.PROFILE_MENU
    elif current_state == MenuStates.STATISTICS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_statistics_menu()
        new_interactive_text = "Меню Статистика"
        new_state = MenuStates.STATISTICS_MENU
    elif current_state == MenuStates.ACHIEVEMENTS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_achievements_menu()
        new_interactive_text = "Меню Досягнення"
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif current_state == MenuStates.SETTINGS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_settings_menu()
        new_interactive_text = "Меню Налаштування"
        new_state = MenuStates.SETTINGS_MENU
    elif current_state in [
        MenuStates.SEARCH_HERO.state,
        MenuStates.SEARCH_TOPIC.state,
        MenuStates.CHANGE_USERNAME.state,
        MenuStates.RECEIVE_FEEDBACK.state,
        MenuStates.REPORT_BUG.state
    ]:
        # Якщо користувач перебуває в процесі введення, надсилаємо підказку
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=USE_BUTTON_NAVIGATION_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
        except Exception as e:
            logger.error(f"Не вдалося надіслати підказку: {e}")
        await transition_state(state, current_state)
        return
    else:
        user_first_name = message.from_user.first_name or "Користувач"
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU

    # Відправляємо нове повідомлення
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося надіслати нове повідомлення: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)
        return

    # Видаляємо старе повідомлення
    if bot_message_id:
        await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагуємо інтерактивне повідомлення
    if interactive_message_id:
        await check_and_edit_message(
            bot=bot,
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            new_text=new_interactive_text,
            new_keyboard=get_generic_inline_keyboard(),
            state=state
        )
    else:
        # Якщо інтерактивне повідомлення відсутнє, створюємо нове
        try:
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
        except Exception as e:
            logger.error(f"Не вдалося надіслати інтерактивне повідомлення: {e}")

    # Оновлюємо стан користувача
    await transition_state(state, new_state)
    await state.update_data(bot_message_id=new_bot_message_id)

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка меню Досягнення
# --------------------------------------------------------------------------------
@router.message(MenuStates.ACHIEVEMENTS_MENU)
async def handle_achievements_menu_buttons(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Обробчик кнопок у меню Досягнення.
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Досягнення")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Отримуємо дані стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        # Надсилаємо нове повідомлення з клавіатурою
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            # Зберігаємо ID повідомлення бота
            await state.update_data(bot_message_id=main_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку головного меню: {e}")
            await handle_error(bot, chat_id=message.chat.id, error_message=MAIN_MENU_ERROR_TEXT, logger=logger)
        return

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_achievements_menu()
    new_interactive_text = ""
    new_state = MenuStates.ACHIEVEMENTS_MENU

    if user_choice == MenuButton.BADGES.value:
        new_main_text = BADGES_TEXT
        new_interactive_text = "Мої бейджі"
    elif user_choice == MenuButton.PROGRESS.value:
        new_main_text = PROGRESS_TEXT
        new_interactive_text = "Прогрес"
    elif user_choice == MenuButton.TOURNAMENT_STATS.value:
        new_main_text = TOURNAMENT_STATS_TEXT
        new_interactive_text = "Турнірна статистика"
    elif user_choice == MenuButton.AWARDS.value:
        new_main_text = AWARDS_TEXT
        new_interactive_text = "Отримані нагороди"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.ACHIEVEMENTS_MENU

    # Відправка нового повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося надіслати нове повідомлення: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлюємо стан користувача
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка меню Статистика
# --------------------------------------------------------------------------------
@router.message(MenuStates.STATISTICS_MENU)
async def handle_statistics_menu_buttons(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Обробчик кнопок у меню Статистика.
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Статистика")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            await state.update_data(bot_message_id=main_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку головного меню: {e}")
            await handle_error(bot, chat_id=message.chat.id, error_message=MAIN_MENU_ERROR_TEXT, logger=logger)
        return

    new_main_text = ""
    new_main_keyboard = get_statistics_menu()
    new_interactive_text = ""
    new_state = MenuStates.STATISTICS_MENU

    if user_choice == MenuButton.ACTIVITY.value:
        new_main_text = ACTIVITY_TEXT
        new_interactive_text = "Графік активності"
    elif user_choice == MenuButton.RANKING.value:
        new_main_text = RANKING_TEXT
        new_interactive_text = "Рейтинг гравця"
    elif user_choice == MenuButton.GAME_STATS.value:
        new_main_text = GAME_STATS_TEXT
        new_interactive_text = "Ігрова статистика"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.STATISTICS_MENU

    # Відправка нового повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося надіслати нове повідомлення: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлюємо стан користувача
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка процесу відображення профілю
# --------------------------------------------------------------------------------
async def process_my_profile(message: Message, state: FSMContext, db: AsyncSession, bot: Bot) -> None:
    """
    Обробник для відображення профілю користувача.

    :param message: Повідомлення користувача.
    :param state: Контекст FSM.
    :param db: Асинхронна сесія бази даних.
    :param bot: Екземпляр бота.
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
            "last_update": profile_data.get('last_update').strftime('%d.%m.%Y %H:%M') if profile_data.get('last_update') else 'N/A'
        }
        try:
            formatted_profile_text = format_profile_text(PROFILE_INTERACTIVE_TEXT, profile_info)
        except ValueError as e:
            logger.error(f"Error formatting profile text: {e}")
            await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT)
            return

        # Генерація графіків для профілю
        try:
            overall_activity_bytes = create_overall_activity_graph()
            rating_bytes = create_rating_graph()
            game_stats_bytes = create_game_stats_graph()
        except Exception as e:
            logger.error(f"Помилка при генерації графіків профілю: {e}")
            overall_activity_bytes = rating_bytes = game_stats_bytes = None

        # Створення комбінованого зображення (опціонально)
        combined_image_bytes = None
        if overall_activity_bytes and rating_bytes and game_stats_bytes:
            try:
                # Відкриття зображень
                img1 = Image.open(io.BytesIO(overall_activity_bytes))
                img2 = Image.open(io.BytesIO(rating_bytes))
                img3 = Image.open(io.BytesIO(game_stats_bytes))

                # Встановлення розміру для графіків
                img1 = img1.resize((600, 400))
                img2 = img2.resize((600, 400))
                img3 = img3.resize((600, 400))

                # Створення нового зображення для об'єднання графіків
                combined_width = max(img1.width, img2.width, img3.width)
                combined_height = img1.height + img2.height + img3.height
                combined_image = Image.new('RGB', (combined_width, combined_height), (255, 255, 255))

                # Вставка графіків
                combined_image.paste(img1, (0, 0))
                combined_image.paste(img2, (0, img1.height))
                combined_image.paste(img3, (0, img1.height + img2.height))

                # Збереження комбінованого зображення в байтовий буфер
                buffer = io.BytesIO()
                combined_image.save(buffer, format="PNG")
                combined_image_bytes = buffer.getvalue()
            except Exception as e:
                logger.error(f"Помилка при об'єднанні графіків: {e}")

        # Форматування тексту профілю та надсилання графіків
        if combined_image_bytes:
            # Створення інтерактивного повідомлення з графіками
            try:
                await bot.edit_message_media(
                    media=types.InputMediaPhoto(media=combined_image_bytes, caption=formatted_profile_text),
                    chat_id=message.chat.id,
                    message_id=interactive_message_id,
                    reply_markup=get_generic_inline_keyboard()
                )
                logger.info(f"Інтерактивне повідомлення профілю оновлено для користувача {message.from_user.id}")
            except Exception as e:
                logger.error(f"Не вдалося відредагувати інтерактивне повідомлення профілю: {e}")
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
            # Якщо неможливо створити комбіноване зображення, відправляємо текстове повідомлення профілю
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
                logger.info(f"Текстове інтерактивне повідомлення профілю оновлено для користувача {message.from_user.id}")
            except Exception as e:
                logger.error(f"Не вдалося відредагувати текстове інтерактивне повідомлення профілю: {e}")
                interactive_message_id = await send_or_update_interactive_message(
                    bot=bot,
                    chat_id=message.chat.id,
                    text=formatted_profile_text,
                    keyboard=get_generic_inline_keyboard(),
                    message_id=None,
                    state=state,
                    parse_mode=ParseMode.HTML
                )

        # Надсилання нового звичайного повідомлення з текстом «🪪 Мій Профіль»
        try:
            my_profile_message = await bot.send_message(
                chat_id=message.chat.id,
                text="🪪 Мій Профіль\nОберіть опцію для перегляду:",
                reply_markup=get_profile_menu()
            )
            new_bot_message_id = my_profile_message.message_id
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення профілю: {e}")
            await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger)
            new_bot_message_id = None

        # Видалення старого звичайного повідомлення
        old_bot_message_id = data.get('bot_message_id')
        if old_bot_message_id:
            await safe_delete_message(bot, message.chat.id, old_bot_message_id)

        # Оновлення стану з новими ідентифікаторами повідомлень
        if new_bot_message_id:
            await state.update_data(bot_message_id=new_bot_message_id)

        # Встановлення стану до PROFILE_MENU
        await transition_state(state, MenuStates.PROFILE_MENU)
    else:
        # Обробка випадку, коли дані профілю не знайдено
        error_message = "❌ Дані профілю не знайдено. Зареєструйтесь, щоб переглянути статистику."
        try:
            await bot.send_message(chat_id=message.chat.id, text=error_message, reply_markup=get_generic_inline_keyboard())
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку: {e}")
        await transition_state(state, MenuStates.MAIN_MENU)

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка меню Меню Білди
# --------------------------------------------------------------------------------
@router.message(MenuStates.BUILDS_MENU)
async def handle_builds_menu_buttons(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Обробчик кнопок у меню Білди.
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Білди")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Отримуємо дані стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        # Надсилаємо нове повідомлення з клавіатурою
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_main_menu()
            )
            # Зберігаємо ID повідомлення бота
            await state.update_data(bot_message_id=main_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку головного меню: {e}")
            await handle_error(bot, chat_id=message.chat.id, error_message=MAIN_MENU_ERROR_TEXT, logger=logger)
        return

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_builds_menu()
    new_interactive_text = ""
    new_state = MenuStates.BUILDS_MENU

    if user_choice == MenuButton.CREATE_BUILD.value:
        new_main_text = CREATE_BUILD_TEXT
        new_interactive_text = "Створення білду"
    elif user_choice == MenuButton.MY_BUILDS.value:
        new_main_text = MY_BUILDS_TEXT
        new_interactive_text = "Мої білди"
    elif user_choice == MenuButton.POPULAR_BUILDS.value:
        new_main_text = POPULAR_BUILDS_TEXT
        new_interactive_text = "Популярні білди"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.BUILDS_MENU

    # Відправка нового повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося надіслати нове повідомлення: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлюємо стан користувача
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка меню Героїв
# --------------------------------------------------------------------------------
@router.message(MenuStates.GUIDES_MENU)
async def handle_guides_menu_buttons(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Обробчик кнопок у меню Гайди.
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Гайди")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Подальша реалізація залежить від конкретних опцій меню Гайди
    # Наприклад, перегляд гайдів, створення нових гайдів тощо

    # Приклад повернення до попереднього меню
    if user_choice == MenuButton.BACK.value:
        await handle_menu(
            user_choice=MenuButton.BACK.value,
            message=message,
            state=state,
            db=None,  # Передайте потрібні параметри
            bot=bot,
            chat_id=message.chat.id,
            main_menu_error=UNKNOWN_COMMAND_TEXT,
            main_menu_keyboard_func=get_guides_menu,
            main_menu_text=GUIDES_MENU_TEXT,
            interactive_text=GUIDES_INTERACTIVE_TEXT,
            new_state=MenuStates.GUIDES_MENU
        )
    else:
        # Додайте вашу логіку для інших виборів
        await handle_menu(
            user_choice=user_choice,
            message=message,
            state=state,
            db=None,  # Передайте потрібні параметри
            bot=bot,
            chat_id=message.chat.id,
            main_menu_error=UNKNOWN_COMMAND_TEXT,
            main_menu_keyboard_func=get_guides_menu,
            main_menu_text=GUIDES_MENU_TEXT,
            interactive_text=GUIDES_INTERACTIVE_TEXT,
            new_state=MenuStates.GUIDES_MENU
        )

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка меню Контр-піки
# --------------------------------------------------------------------------------
@router.message(MenuStates.COUNTER_PICKS_MENU)
async def handle_counter_picks_menu_buttons(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Обробчик кнопок у меню Контр-піки.
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Контр-піки")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Подальша реалізація залежить від конкретних опцій меню Контр-піки
    # Наприклад, пошук контр-піків, перегляд списку тощо

    # Приклад повернення до попереднього меню
    if user_choice == MenuButton.BACK.value:
        await handle_menu(
            user_choice=MenuButton.BACK.value,
            message=message,
            state=state,
            db=None,  # Передайте потрібні параметри
            bot=bot,
            chat_id=message.chat.id,
            main_menu_error=UNKNOWN_COMMAND_TEXT,
            main_menu_keyboard_func=get_counter_picks_menu,
            main_menu_text=COUNTER_PICKS_MENU_TEXT,
            interactive_text=COUNTER_PICKS_INTERACTIVE_TEXT,
            new_state=MenuStates.COUNTER_PICKS_MENU
        )
    else:
        # Додайте вашу логіку для інших виборів
        await handle_menu(
            user_choice=user_choice,
            message=message,
            state=state,
            db=None,  # Передайте потрібні параметри
            bot=bot,
            chat_id=message.chat.id,
            main_menu_error=UNKNOWN_COMMAND_TEXT,
            main_menu_keyboard_func=get_counter_picks_menu,
            main_menu_text=COUNTER_PICKS_MENU_TEXT,
            interactive_text=COUNTER_PICKS_INTERACTIVE_TEXT,
            new_state=MenuStates.COUNTER_PICKS_MENU
        )

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка інлайн-кнопок
# --------------------------------------------------------------------------------
@router.callback_query()
async def handle_inline_buttons(callback: CallbackQuery, state: FSMContext, bot: Bot) -> None:
    """
    Обробчик для інлайн-кнопок.
    """
    data = callback.data
    logger.info(f"Користувач {callback.from_user.id} натиснув інлайн-кнопку: {data}")

    # Отримуємо interactive_message_id з стану
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if interactive_message_id:
        # Обробляємо інлайн-кнопки
        if data == "mls_button":
            await bot.answer_callback_query(callback.id, text=MLS_BUTTON_RESPONSE_TEXT)
        elif data == "menu_back":
            # Повернення до головного меню
            await transition_state(state, MenuStates.MAIN_MENU)
            new_interactive_text = MAIN_MENU_DESCRIPTION
            new_interactive_keyboard = get_generic_inline_keyboard()

            # Редагуємо інтерактивне повідомлення
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
                await handle_error(bot, chat_id=callback.message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)

            # Відправляємо головне меню
            user_first_name = callback.from_user.first_name or "Користувач"
            main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
            try:
                main_message = await bot.send_message(
                    chat_id=callback.message.chat.id,
                    text=main_menu_text_formatted,
                    reply_markup=get_main_menu()
                )
                # Оновлюємо bot_message_id
                await state.update_data(bot_message_id=main_message.message_id)
            except Exception as e:
                logger.error(f"Не вдалося надіслати головне меню: {e}")
                await handle_error(bot, chat_id=callback.message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)

            # Видаляємо попереднє повідомлення з клавіатурою
            old_bot_message_id = state_data.get('bot_message_id')
            if old_bot_message_id:
                await safe_delete_message(bot, callback.message.chat.id, old_bot_message_id)
        else:
            # Додайте обробку інших інлайн-кнопок за потребою
            await bot.answer_callback_query(callback.id, text=UNHANDLED_INLINE_BUTTON_TEXT)
    else:
        logger.error("interactive_message_id не знайдено")
        await bot.answer_callback_query(callback.id, text=GENERIC_ERROR_MESSAGE_TEXT)

    await callback.answer()

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка пошуку героя
# --------------------------------------------------------------------------------
@router.message(MenuStates.SEARCH_HERO)
async def handle_search_hero(message: Message, state: FSMContext, bot: Bot, db: AsyncSession) -> None:
    """
    Обробчик для прийому імені героя для пошуку.
    """
    hero_name = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} шукає героя: {hero_name}")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    if hero_name:
        try:
            hero_data = await find_hero(db, hero_name)
            if hero_data:
                response_text = f"🔍 **{hero_name}** знайдений:\n\n{hero_data}"
            else:
                response_text = f"❌ Герой **{hero_name}** не знайдений."
        except Exception as e:
            logger.error(f"Помилка при пошуку героя {hero_name}: {e}")
            response_text = GENERIC_ERROR_MESSAGE_TEXT
    else:
        response_text = "Будь ласка, введіть ім'я героя для пошуку."

    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=response_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося надіслати повідомлення про пошук героя: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)

    # Повертаємо користувача до попереднього меню
    await transition_state(state, MenuStates.HEROES_MENU)

# --------------------------------------------------------------------------------
# XOMO-Handler: Обробка пропозиції теми
# --------------------------------------------------------------------------------
@router.message(MenuStates.SEARCH_TOPIC)
async def handle_search_topic(message: Message, state: FSMContext, bot: Bot, db: AsyncSession) -> None:
    """
    Обробчик для прийому теми пропозиції.
    """
    topic = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"Користувач {user_id} пропонує тему: {topic}")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    if topic:
        try:
            async with db.begin():
                new_suggestion = Feedback(user_id=user_id, feedback=topic, created_at=datetime.utcnow())
                db.add(new_suggestion)
                await db.commit()
            response_text = SUGGESTION_RESPONSE_TEXT.format(topic=topic)
            logger.info(f"Пропозиція теми збережена від користувача {user_id}")
        except Exception as e:
            logger.error(f"Помилка при збереженні пропозиції теми від користувача {user_id}: {e}")
            response_text = "❌ Виникла помилка при збереженні вашої пропозиції теми."
    else:
        response_text = "❌ Будь ласка, введіть тему для пропозиції."

    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=response_text,
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося надіслати повідомлення про пропозицію теми: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)

    # Повертаємо користувача до меню Зворотний Зв'язок
    await transition_state(state, MenuStates.FEEDBACK_MENU)

# --------------------------------------------------------------------------------
# XOMO-Handler: Функція для налаштування обробників
# --------------------------------------------------------------------------------
def setup_handlers(dp: Dispatcher) -> None:
    """
    Функція для налаштування обробників у Dispatcher.
    """
    dp.include_router(router)
    # Якщо у вас є інші роутери, включіть їх тут, наприклад:
    # dp.include_router(profile_router)