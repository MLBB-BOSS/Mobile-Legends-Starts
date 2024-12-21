import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Імпортуємо MenuStates та increment_step зі states.py
from states import MenuStates, increment_step

from utils.message_utils import safe_delete_message, check_and_edit_message
from utils.db import get_user_profile
from utils.text_formatter import format_profile_text
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

# Відповідність кнопок класам героїв
menu_button_to_class = {
    MenuButton.TANK.value: "Танк",
    MenuButton.MAGE.value: "Маг",
    MenuButton.MARKSMAN.value: "Стрілець",
    MenuButton.ASSASSIN.value: "Асасін",
    MenuButton.SUPPORT.value: "Підтримка",
    MenuButton.FIGHTER.value: "Боєць"
}

# -------------------- Допоміжні функції --------------------

async def increment_step(state: FSMContext):
    """
    Проста функція для лічильника кроків і очищення стану після 3-х змін
    """
    data = await state.get_data()
    step_count = data.get("step_count", 0) + 1
    if step_count >= 3:
        await state.clear()
        step_count = 0
    await state.update_data(step_count=step_count)

async def send_or_update_interactive_message(
    bot: Bot,
    chat_id: int,
    text: str,
    keyboard,
    message_id: int = None,
    state: FSMContext = None,
    parse_mode: str = ParseMode.HTML
) -> int:
    """
    Надсилає або оновлює інтерактивне повідомлення (інлайн).
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

    # Якщо message_id немає або редагування не вдалося, надсилаємо нове
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
        return message_id

async def safe_delete_message(bot: Bot, chat_id: int, message_id: int):
    """
    Безпечне видалення повідомлення з обробкою виключень.
    """
    if message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
            logger.info(f"Повідомлення {message_id} успішно видалено.")
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення {message_id}: {e}")

async def check_and_edit_message(
    bot: Bot,
    chat_id: int,
    message_id: int,
    new_text: str,
    new_keyboard,
    state: FSMContext,
    parse_mode: str = ParseMode.HTML
):
    """
    Перевірка зміни тексту чи клавіатури й подальше редагування інтерактивного повідомлення.
    """
    state_data = await state.get_data()
    last_text = state_data.get('last_text')
    last_keyboard = state_data.get('last_keyboard')

    # Редагуємо лише якщо справді є зміни
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
            await bot.send_message(
                chat_id=chat_id,
                text=GENERIC_ERROR_MESSAGE_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )

async def transition_state(state: FSMContext, new_state: State):
    """
    Очищує старі дані та встановлює новий стан.
    """
    await state.clear()
    await state.set_state(new_state)

# -------------------- Обробка профілю --------------------

async def process_my_profile(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    """
    Витягує дані профілю з БД та відображає їх у бота.
    """
    user_id = message.from_user.id
    profile_data = await get_user_profile(db, user_id)

    # Спершу видаляємо щойно надіслане повідомлення від користувача
    await safe_delete_message(bot, message.chat.id, message.message_id)

    if profile_data:
        # Готуємо словник із даними профілю
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
                if profile_data.get('last_update') else 'N/A'
            )
        }

        # Підставляємо їх у шаблон
        try:
            formatted_profile_text = format_profile_text(PROFILE_INTERACTIVE_TEXT, profile_info)
        except ValueError as e:
            logger.error(f"Помилка форматування профілю: {e}")
            formatted_profile_text = GENERIC_ERROR_MESSAGE_TEXT

        # Дістаємо message_id для поточної Reply-клавіатури та інтерактивного повідомлення
        data = await state.get_data()
        old_bot_message_id = data.get('bot_message_id')
        interactive_message_id = data.get('interactive_message_id')

        # Якщо інтерактивне повідомлення існує, редагуємо його
        if interactive_message_id:
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
            except Exception as e:
                logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
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
            # Інакше створюємо нове інтерактивне повідомлення
            interactive_message_id = await send_or_update_interactive_message(
                bot=bot,
                chat_id=message.chat.id,
                text=formatted_profile_text,
                keyboard=get_generic_inline_keyboard(),
                message_id=None,
                state=state,
                parse_mode=ParseMode.HTML
            )

        # Тепер надсилаємо нове звичайне повідомлення з профілем
        try:
            my_profile_message = await bot.send_message(
                chat_id=message.chat.id,
                text="🪪 Мій Профіль\nОберіть опцію для перегляду:",
                reply_markup=get_profile_menu()
            )
            new_bot_message_id = my_profile_message.message_id
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення профілю: {e}")
            new_bot_message_id = None

        # Видаляємо старе звичайне повідомлення (якщо було)
        if old_bot_message_id:
            await safe_delete_message(bot, message.chat.id, old_bot_message_id)

        # Зберігаємо нові дані в стан
        if new_bot_message_id:
            await state.update_data(bot_message_id=new_bot_message_id)

        # Встановлюємо стан MENU_PROFILE
        await state.set_state(MenuStates.PROFILE_MENU)
    else:
        # Якщо профіль відсутній
        error_message = "❌ Дані профілю не знайдено. Зареєструйтесь, щоб переглянути статистику."
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=error_message,
                reply_markup=get_generic_inline_keyboard()
            )
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку: {e}")
        await state.set_state(MenuStates.MAIN_MENU)

# -------------------- /start --------------------

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    """
    Команда /start: реєстрація користувача (якщо треба) + перехід до Intro Page 1
    """
    user_id = message.from_user.id

    async with db.begin():
        user_result = await db.execute(
            select(models.user.User).where(models.user.User.telegram_id == user_id)
        )
        user = user_result.scalars().first()

        if not user:
            # Якщо нового користувача немає, створюємо
            new_user = models.user.User(
                telegram_id=user_id,
                username=message.from_user.username
            )
            db.add(new_user)
            await db.flush()  
            # Додаємо базову статистику
            new_stats = models.user_stats.UserStats(user_id=new_user.id)
            db.add(new_stats)
            await db.commit()
            logger.info(f"Registered new user: {user_id}")
        else:
            logger.info(f"Existing user: {user_id}")

    # Скидаємо стан і встановлюємо INTROS
    await transition_state(state, MenuStates.INTRO_PAGE_1)

    try:
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=INTRO_PAGE_1_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=get_intro_page_1_keyboard()  # Інлайн-клавіатура
        )
        await state.update_data(
            interactive_message_id=interactive_message.message_id,
            last_text=INTRO_PAGE_1_TEXT,
            last_keyboard=get_intro_page_1_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося надіслати вступну сторінку 1: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# -------------------- Intro Page Handlers --------------------

@router.callback_query(F.data == "intro_next_1")
async def handle_intro_next_1(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Обробка натискання 'Далі' на першій сторінці інтро
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
    data = await state.get_data()
    interactive_message_id = data.get('interactive_message_id')

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

    await state.set_state(new_state)
    await callback.answer()

@router.callback_query(F.data == "intro_next_2")
async def handle_intro_next_2(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Обробка натискання 'Далі' на другій сторінці інтро
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
    data = await state.get_data()
    interactive_message_id = data.get('interactive_message_id')

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

    await state.set_state(new_state)
    await callback.answer()

@router.callback_query(F.data == "intro_start")
async def handle_intro_start(callback: CallbackQuery, state: FSMContext, bot: Bot, db: AsyncSession):
    """
    Обробка натискання 'Розпочати' на третій сторінці інтро
    """
    current_state = await state.get_state()
    if current_state not in [
        MenuStates.INTRO_PAGE_1.state, 
        MenuStates.INTRO_PAGE_2.state, 
        MenuStates.INTRO_PAGE_3.state
    ]:
        logger.warning(f"Некоректний стан для 'intro_start': {current_state}")
        await bot.answer_callback_query(callback.id, text="Некоректна дія для цього стану.", show_alert=True)
        return

    await increment_step(state)

    user_first_name = callback.from_user.first_name or "Користувач"
    main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=user_first_name)

    # Стартове головне меню (Reply-клавіатура)
    try:
        main_menu_message = await bot.send_message(
            chat_id=callback.message.chat.id,
            text=main_menu_text_formatted,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_menu_message.message_id)
    except Exception as e:
        logger.error(f"Не вдалося надіслати головне меню: {e}")

    # Оновлюємо/створюємо інтерактивне повідомлення (заглушку)
    data = await state.get_data()
    interactive_message_id = data.get('interactive_message_id')
    new_interactive_text = MAIN_MENU_DESCRIPTION
    new_interactive_keyboard = get_generic_inline_keyboard()

    interactive_message_id = await send_or_update_interactive_message(
        bot=bot,
        chat_id=callback.message.chat.id,
        text=new_interactive_text,
        keyboard=new_interactive_keyboard,
        message_id=interactive_message_id,
        state=state,
        parse_mode=ParseMode.HTML
    )

    await state.set_state(MenuStates.MAIN_MENU)
    await callback.answer()

# -------------------- Приклад обробника для кнопки "🪪 Мій Профіль" --------------------

@router.message(F.text == "🪪 Мій Профіль")
async def handle_my_profile_handler(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    """
    Коли користувач тисне «Мій Профіль»
    """
    await increment_step(state)
    await process_my_profile(message, state, db, bot)

# -------------------- Універсальна функція для обробки меню --------------------

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
):
    """
    Уніфікований метод обробки основних меню (наприклад MAIN_MENU)
    """
    logger.info(f"User selected '{user_choice}' in menu")

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
            await state.set_state(MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку головного меню: {e}")
        return

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    updated_state = new_state

    # Керуємо логікою залежно від того, який пункт меню обрано
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
        # Повертаємось до головного меню
        user_first_name = message.from_user.first_name or "Користувач"
        new_main_text = main_menu_text.format(user_first_name=user_first_name)
        new_main_keyboard = main_menu_keyboard_func()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        updated_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = main_menu_keyboard_func()
        new_interactive_text = "Невідома команда"
        updated_state = MenuStates.MAIN_MENU

    # Надсилаємо нове «звичайне» повідомлення (ReplyKeyboard)
    try:
        main_message = await bot.send_message(
            chat_id=chat_id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося надіслати нове повідомлення: {e}")
        return

    # Видаляємо попереднє звичайне повідомлення
    await safe_delete_message(bot, chat_id, bot_message_id)

    # Оновлюємо інтерактивне повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=chat_id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Зберігаємо новий bot_message_id та встановлюємо новий стан
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(updated_state)

# -------------------- Основний обробник для MENU_STATES.MAIN_MENU --------------------

@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    """
    Тут обробляємо кнопки головного меню: Навігація, Профіль тощо
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в головному меню")

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

# -------------------- Приклад решти хендлерів (Feedback, Tournaments і т.д.) --------------------
# (Вони вже наведені у вихідному коді, тому залишається та сама логіка з урахуванням ReplyKeyboard)

# … увесь решта коду (FEEDBACK_MENU, SETTINGS_MENU, HELP_MENU тощо) залишається,
#   як продемонстровано у вихідному прикладі, з заміною на ReplyKeyboardMarkup.

# -------------------- Обробник інлайн-кнопок --------------------

@router.callback_query()
async def handle_inline_buttons(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Єдиний обробник усіх callback-кнопок
    """
    data = callback.data
    logger.info(f"Користувач {callback.from_user.id} натиснув інлайн-кнопку: {data}")

    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if interactive_message_id:
        if data == "mls_button":
            await bot.answer_callback_query(callback.id, text=MLS_BUTTON_RESPONSE_TEXT)
        elif data == "menu_back":
            # Повертаємось до головного меню інлайн-кнопкою
            await state.set_state(MenuStates.MAIN_MENU)
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

            # Відправляємо головне меню (ReplyKeyboard)
            user_first_name = callback.from_user.first_name or "Користувач"
            main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
            try:
                main_message = await bot.send_message(
                    chat_id=callback.message.chat.id,
                    text=main_menu_text_formatted,
                    reply_markup=get_main_menu()
                )
                await state.update_data(bot_message_id=main_message.message_id)
            except Exception as e:
                logger.error(f"Не вдалося надіслати головне меню: {e}")

            # Видаляємо попереднє звичайне повідомлення
            old_bot_message_id = state_data.get('bot_message_id')
            if old_bot_message_id:
                await safe_delete_message(bot, callback.message.chat.id, old_bot_message_id)

        else:
            # Якщо є інші callback_data, яких ми не очікуємо
            await bot.answer_callback_query(callback.id, text=UNHANDLED_INLINE_BUTTON_TEXT)
    else:
        logger.error("interactive_message_id не знайдено")
        await bot.answer_callback_query(callback.id, text=GENERIC_ERROR_MESSAGE_TEXT)

    await callback.answer()

# -------------------- Пошук героя --------------------

@router.message(MenuStates.SEARCH_HERO)
async def handle_search_hero(message: Message, state: FSMContext, bot: Bot):
    """
    Стан пошуку героя: чекаємо на введення імені
    """
    hero_name = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} шукає героя: {hero_name}")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    if hero_name:
        response_text = SEARCH_HERO_RESPONSE_TEXT.format(hero_name=hero_name)
    else:
        response_text = "Будь ласка, введіть ім'я героя для пошуку."

    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=response_text,
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося надіслати повідомлення про пошук героя: {e}")

    # Повертаємо користувача до HEROES_MENU
    await state.set_state(MenuStates.HEROES_MENU)

# -------------------- Пошук теми для пропозиції --------------------

@router.message(MenuStates.SEARCH_TOPIC)
async def handle_search_topic(message: Message, state: FSMContext, bot: Bot):
    """
    Стан для введення теми пропозиції
    """
    topic = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} пропонує тему: {topic}")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    if topic:
        response_text = SUGGESTION_RESPONSE_TEXT.format(topic=topic)
    else:
        response_text = "Будь ласка, введіть тему для пропозиції."

    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=response_text,
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося надіслати повідомлення про пропозицію теми: {e}")

    # Повертаємо користувача до FEEDBACK_MENU
    await state.set_state(MenuStates.FEEDBACK_MENU)

# -------------------- Невідомі повідомлення --------------------

@router.message()
async def unknown_command(message: Message, state: FSMContext, bot: Bot):
    """
    Якщо повідомлення не підходить під жоден хендлер, виконується ця функція
    """
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    current_state = await state.get_state()

    # За замовчуванням залишаємося в поточному стані
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = current_state

    # Приклад логіки залежно від стану – якщо він відомий, показуємо UNKNOWN_COMMAND_TEXT + поточну ReplyKeyboard
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
        # Якщо користувач у стані введення інформації, радимо скористатися кнопками
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=USE_BUTTON_NAVIGATION_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
        except Exception as e:
            logger.error(f"Не вдалося надіслати підказку: {e}")
        await state.set_state(current_state)
        return
    else:
        # Якщо стан не визначено або нічого не підходить, повертаємося до MAIN_MENU
        new_main_text = MAIN_MENU_TEXT.format(user_first_name="Користувач")
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU

    # Відправляємо нове повідомлення з ReplyKeyboard
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося надіслати нове повідомлення: {e}")
        return

    # Видаляємо попереднє повідомлення
    if bot_message_id:
        await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Якщо існує інтерактивне повідомлення, оновлюємо його
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
        # Якщо немає інтерактивного повідомлення, створюємо (заглушку)
        try:
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
        except Exception as e:
            logger.error(f"Не вдалося надіслати інтерактивне повідомлення: {e}")

    # Оновлюємо стан
    await state.set_state(new_state)


# -------------------- Реєстрація хендлерів --------------------

def setup_handlers(dp: Router):
    """
    Функція для підключення (include) хендлерів з цього файлу
    """
    dp.include_router(router)
    # Якщо є інші роутери, підключайте їх, наприклад:
    # dp.include_router(profile_router)