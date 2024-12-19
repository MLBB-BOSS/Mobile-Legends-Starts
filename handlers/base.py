import logging
from aiogram import Router, F, Bot, Dispatcher
from aiogram.filters import Command
from aiogram.filters.text import Text  # Виправлений імпорт
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ParseMode  # Виправлений імпорт
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from utils.db import get_user_profile, search_hero, save_suggestion  # Імпорт необхідних функцій
import models.user
import models.user_stats
import models.hero  # Припустимо, є модель для героїв

from keyboards.menus import (
    MenuButton, get_main_menu, get_profile_menu, get_navigation_menu,
    get_heroes_menu, get_hero_class_menu, get_guides_menu,
    get_counter_picks_menu, get_builds_menu, get_voting_menu, get_statistics_menu,
    get_achievements_menu, get_settings_menu, get_feedback_menu, get_help_menu,
    get_tournaments_menu, get_meta_menu, get_m6_menu, get_gpt_menu
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

# Визначення станів меню
class MenuStates(StatesGroup):
    INTRO_PAGE_1 = State()
    INTRO_PAGE_2 = State()
    INTRO_PAGE_3 = State()
    MAIN_MENU = State()
    PROFILE_MENU = State()
    NAVIGATION_MENU = State()
    HEROES_MENU = State()
    HERO_CLASS_MENU = State()
    GUIDES_MENU = State()
    COUNTER_PICKS_MENU = State()
    BUILDS_MENU = State()
    VOTING_MENU = State()
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

# Визначення словника для класів героїв
menu_button_to_class = {
    "🛡️ Танк": "Танк",
    "🧙‍♂️ Маг": "Маг",
    "🏹 Стрілець": "Марксмен",
    "⚔️ Асасін": "Асасін",
    "❤️ Підтримка": "Підтримка",
    "🗡️ Боєць": "Файтер"
}

# Допоміжні функції

async def get_heroes_by_class(db: AsyncSession, hero_class: str) -> list:
    """
    Отримує список героїв для заданого класу.
    """
    result = await db.execute(select(models.hero.Hero).where(models.hero.Hero.class_ == hero_class))
    heroes = result.scalars().all()
    return [hero.name for hero in heroes]

async def search_hero(db: AsyncSession, hero_name: str) -> dict:
    """
    Шукає героя за ім'ям.
    """
    result = await db.execute(select(models.hero.Hero).where(models.hero.Hero.name.ilike(f"%{hero_name}%")))
    hero = result.scalars().first()
    if hero:
        return {
            'name': hero.name,
            'class': hero.class_,
            'rating': hero.rating,
            'description': hero.description
        }
    return None

async def save_suggestion(topic: str, user_id: int):
    """
    Зберігає пропозицію теми.
    """
    # Реалізуйте збереження пропозиції у базі даних або надсилання адміністратору
    pass

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
    Відправка нового повідомлення або оновлення існуючого.
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

    # Відправка нового повідомлення, якщо редагування не вдалося або message_id відсутній
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
    Перевірка зміни тексту або клавіатури перед редагуванням повідомлення.
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
            await bot.send_message(
                chat_id=chat_id,
                text=GENERIC_ERROR_MESSAGE_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )

async def transition_state(state: FSMContext, new_state: State):
    """
    Встановлення нового стану без очищення даних стану.
    """
    await state.set_state(new_state)

# Уніфікована функція для обробки меню
async def handle_menu(
    user_choice: str,
    state: FSMContext,
    db: AsyncSession,
    bot: Bot,
    chat_id: int,
    current_state: str,
    main_menu_error: str,
    main_menu_keyboard_func,
    main_menu_text: str,
    interactive_text: str,
    new_state: State
):
    logger.info(f"User selected '{user_choice}' in {current_state}")
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Перевірка існування ID повідомлень
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        try:
            main_message = await bot.send_message(chat_id=chat_id, text=main_menu_error, reply_markup=main_menu_keyboard_func())
            await state.update_data(bot_message_id=main_message.message_id)
            await state.set_state(MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку головного меню: {e}")
        return

    # Логіка для вибору користувача
    if user_choice == MenuButton.NAVIGATION.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    elif user_choice == MenuButton.PROFILE.value:
        # Завантаження профілю користувача
        profile_data = await get_user_profile(db, chat_id)
        if profile_data:
            # Детальна статистика у інтерактивному повідомленні
            detailed_profile_message = (
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
            # Коротке резюме у звичайному повідомленні
            short_summary = f"Ваш рівень: {profile_data['level']}\nРейтинг: {profile_data['rating']}"
            new_main_text = short_summary
            new_main_keyboard = get_profile_menu()
            new_interactive_text = detailed_profile_message
            new_state = MenuStates.PROFILE_MENU
        else:
            new_main_text = "❌ Дані профілю не знайдено. Зареєструйтесь, щоб переглянути статистику."
            new_main_keyboard = get_main_menu()
            new_interactive_text = "Меню Профіль"
            new_state = MenuStates.PROFILE_MENU
    elif user_choice == MenuButton.TOURNAMENTS.value:
        new_main_text = TOURNAMENT_CREATE_TEXT
        new_main_keyboard = get_tournaments_menu()
        new_interactive_text = "Меню Турніри"
        new_state = MenuStates.TOURNAMENTS_MENU
    elif user_choice == MenuButton.META.value:
        new_main_text = META_RECOMMENDATIONS_TEXT
        new_main_keyboard = get_meta_menu()
        new_interactive_text = "Меню META"
        new_state = MenuStates.META_MENU
    elif user_choice == MenuButton.M6.value:
        new_main_text = M6_INFO_TEXT
        new_main_keyboard = get_m6_menu()
        new_interactive_text = "Меню M6"
        new_state = MenuStates.M6_MENU
    elif user_choice == MenuButton.GPT.value:
        new_main_text = "🤖 Меню GPT"
        new_main_keyboard = get_gpt_menu()
        new_interactive_text = "Меню GPT"
        new_state = MenuStates.GPT_MENU
    else:
        # Невідома команда
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = main_menu_keyboard_func()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.MAIN_MENU

    # Відправка нового звичайного повідомлення
    try:
        main_message = await bot.send_message(chat_id=chat_id, text=new_main_text, reply_markup=new_main_keyboard)
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося надіслати нове повідомлення: {e}")
        return

    # Видалення старого звичайного повідомлення
    await safe_delete_message(bot, chat_id, bot_message_id)

    # Відправка або оновлення інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=chat_id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану з новими ідентифікаторами повідомлень
    await state.update_data(bot_message_id=new_bot_message_id)

    # Встановлення нового стану
    await state.set_state(new_state)

# Обробники

# Обробник команди /start з реєстрацією користувача
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_id = message.from_user.id
    async with db.begin():
        user_result = await db.execute(select(models.user.User).where(models.user.User.telegram_id == user_id))
        user = user_result.scalars().first()
        if not user:
            # Створення нового користувача
            new_user = models.user.User(telegram_id=user_id, username=message.from_user.username)
            db.add(new_user)
            await db.flush()  # Отримання ID перед commit
            # Створення статистики користувача
            new_stats = models.user_stats.UserStats(user_id=new_user.id)
            db.add(new_stats)
            await db.commit()
            logger.info(f"Registered new user: {user_id}")
        else:
            logger.info(f"Existing user: {user_id}")

    # Встановлення стану на INTRO_PAGE_1
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
            last_keyboard=get_intro_page_1_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося надіслати вступну сторінку 1: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Обробники вступних сторінок
@router.callback_query(Text(equals="intro_next_1"))
async def handle_intro_next_1(callback: CallbackQuery, state: FSMContext, bot: Bot):
    current_state = await state.get_state()
    if current_state != MenuStates.INTRO_PAGE_1.state:
        logger.warning(f"Некоректний стан для 'intro_next_1': {current_state}")
        await bot.answer_callback_query(callback.id, text="Некоректна дія для цього стану.", show_alert=True)
        return

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
    await state.set_state(new_state)
    await callback.answer()

@router.callback_query(Text(equals="intro_next_2"))
async def handle_intro_next_2(callback: CallbackQuery, state: FSMContext, bot: Bot):
    current_state = await state.get_state()
    if current_state != MenuStates.INTRO_PAGE_2.state:
        logger.warning(f"Некоректний стан для 'intro_next_2': {current_state}")
        await bot.answer_callback_query(callback.id, text="Некоректна дія для цього стану.", show_alert=True)
        return

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
    await state.set_state(new_state)
    await callback.answer()

@router.callback_query(Text(equals="intro_start"))
async def handle_intro_start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    current_state = await state.get_state()
    if current_state not in [MenuStates.INTRO_PAGE_1.state, MenuStates.INTRO_PAGE_2.state, MenuStates.INTRO_PAGE_3.state]:
        logger.warning(f"Некоректний стан для 'intro_start': {current_state}")
        await bot.answer_callback_query(callback.id, text="Некоректна дія для цього стану.", show_alert=True)
        return

    user_first_name = callback.from_user.first_name
    main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=user_first_name)

    # Відправка головного меню
    try:
        main_menu_message = await bot.send_message(
            chat_id=callback.message.chat.id,
            text=main_menu_text_formatted,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_menu_message.message_id)
    except Exception as e:
        logger.error(f"Не вдалося надіслати головне меню: {e}")

    # Оновлення або відправка інтерактивного повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')
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

    # Встановлення стану на MAIN_MENU
    await state.set_state(MenuStates.MAIN_MENU)
    await callback.answer()

# Уніфікований обробник для головного меню
@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    current_state = await state.get_state()
    await safe_delete_message(bot, message.chat.id, message.message_id)

    await handle_menu(
        user_choice=user_choice,
        state=state,
        db=db,
        bot=bot,
        chat_id=message.chat.id,
        current_state=current_state,
        main_menu_error=MAIN_MENU_ERROR_TEXT,
        main_menu_keyboard_func=get_main_menu,
        main_menu_text=MAIN_MENU_TEXT,
        interactive_text=MAIN_MENU_DESCRIPTION,
        new_state=MenuStates.MAIN_MENU
    )

# Обробчик кнопки "🪪 Мій Профіль"
@router.message(Text(equals="🪪 Мій Профіль"))
async def handle_my_profile(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_id = message.from_user.id
    profile_data = await get_user_profile(db, user_id)  # Отримання профілю з БД

    await safe_delete_message(bot, message.chat.id, message.message_id)

    if profile_data:
        # Детальна статистика у інтерактивному повідомленні
        detailed_profile_message = (
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
        # Коротке резюме у звичайному повідомленні
        short_summary = f"Ваш рівень: {profile_data['level']}\nРейтинг: {profile_data['rating']}"
        new_main_text = short_summary
        new_main_keyboard = get_profile_menu()
        new_interactive_text = detailed_profile_message
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = "❌ Дані профілю не знайдено. Зареєструйтесь, щоб переглянути статистику."
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Меню Профіль"
        new_state = MenuStates.PROFILE_MENU

    # Отримання IDs повідомлень з стану
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
            await state.set_state(MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку головного меню: {e}")
        return

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

    # Оновлення стану з новими ідентифікаторами повідомлень
    await state.update_data(bot_message_id=new_bot_message_id)

    # Встановлення нового стану
    await state.set_state(new_state)

# Обробчик меню "Feedback Menu"
@router.message(MenuStates.FEEDBACK_MENU)
async def handle_feedback_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    current_state = await state.get_state()
    await safe_delete_message(bot, message.chat.id, message.message_id)

    await handle_menu(
        user_choice=user_choice,
        state=state,
        db=db,
        bot=bot,
        chat_id=message.chat.id,
        current_state=current_state,
        main_menu_error=MAIN_MENU_ERROR_TEXT,
        main_menu_keyboard_func=get_main_menu,
        main_menu_text=MAIN_MENU_TEXT,
        interactive_text=MAIN_MENU_DESCRIPTION,
        new_state=MenuStates.FEEDBACK_MENU
    )

# Обробчик зміни імені користувача
@router.message(MenuStates.CHANGE_USERNAME)
async def handle_change_username(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    new_username = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"User {user_id} is changing username to: {new_username}")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    if new_username:
        try:
            async with db.begin():
                user_result = await db.execute(select(models.user.User).where(models.user.User.telegram_id == user_id))
                user = user_result.scalars().first()
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
        response_text = "❌ Будь ласка, введіть новий Username."

    try:
        await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
    except Exception as e:
        logger.error(f"Не вдалося надіслати повідомлення про зміну імені: {e}")

    await state.set_state(MenuStates.SETTINGS_MENU)

# Обробчик отримання зворотного зв'язку
@router.message(MenuStates.RECEIVE_FEEDBACK)
async def handle_receive_feedback(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    feedback = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"User {user_id} sent feedback: {feedback}")
    await safe_delete_message(bot, message.chat.id, message.message_id)

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
        response_text = "❌ Будь ласка, залиште свій відгук."

    try:
        await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
    except Exception as e:
        logger.error(f"Не вдалося надіслати повідомлення про отримання зворотного зв'язку: {e}")

    await state.set_state(MenuStates.FEEDBACK_MENU)

# Обробчик звіту про помилку
@router.message(MenuStates.REPORT_BUG)
async def handle_report_bug(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    bug_report = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"User {user_id} reported a bug: {bug_report}")
    await safe_delete_message(bot, message.chat.id, message.message_id)

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

    try:
        await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
    except Exception as e:
        logger.error(f"Не вдалося надіслати повідомлення про отримання звіту про помилку: {e}")

    await state.set_state(MenuStates.FEEDBACK_MENU)

# Обробчик меню "Navigation Menu"
@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Навігація")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        # Надсилаємо нове повідомлення з клавіатурою
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        # Зберігаємо ID повідомлення бота
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначаємо новий текст та клавіатуру
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
    elif user_choice == MenuButton.BACK.value:
        # Повертаємось до головного меню
        user_first_name = message.from_user.first_name
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
    else:
        # Невідома команда
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.NAVIGATION_MENU

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
        return

    # Видалення старого звичайного повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=new_interactive_keyboard,
        state=state
    )

    # Оновлення стану з новими ідентифікаторами повідомлень
    await state.update_data(bot_message_id=new_bot_message_id)

    # Встановлення нового стану
    await state.set_state(new_state)

# Обробчик меню "Heroes Menu"
@router.message(MenuStates.HEROES_MENU)
async def handle_heroes_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Персонажі")

    # Видаляємо повідомлення користувача
    await message.delete()

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
            # Зберігаємо ID повідомлення бота
            await state.update_data(bot_message_id=main_message.message_id)
            await state.set_state(MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку головного меню: {e}")
        return

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    hero_classes = list(menu_button_to_class.keys())

    if user_choice in hero_classes:
        hero_class = menu_button_to_class.get(user_choice, 'Танк')
        # Отримуємо список героїв для обраного класу
        heroes_list = await get_heroes_by_class(db, hero_class)
        new_main_text = HERO_CLASS_MENU_TEXT.format(hero_class=hero_class)
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = HERO_CLASS_INTERACTIVE_TEXT.format(hero_class=hero_class, heroes_list=", ".join(heroes_list))
        new_state = MenuStates.HERO_CLASS_MENU
        await state.update_data(hero_class=hero_class, heroes_list=heroes_list)
    elif user_choice == MenuButton.SEARCH_HERO.value:
        new_main_text = "🔍 Введіть ім'я героя для пошуку:"
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Пошук героя"
        new_state = MenuStates.SEARCH_HERO
    elif user_choice == MenuButton.COMPARISON.value:
        new_main_text = "Функція порівняння героїв ще в розробці."
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = "Порівняння героїв"
        new_state = MenuStates.HEROES_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_hero_class_menu(data.get('hero_class', 'Танк'))
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.HEROES_MENU

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

    # Оновлення стану з новими ідентифікаторами повідомлень
    await state.update_data(bot_message_id=new_bot_message_id)

    # Встановлення нового стану
    await state.set_state(new_state)

# Обробчик для інлайн-кнопок
@router.callback_query()
async def handle_inline_buttons(callback: CallbackQuery, state: FSMContext, bot: Bot):
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
            await state.set_state(MenuStates.MAIN_MENU)
            new_interactive_text = MAIN_MENU_DESCRIPTION
            new_interactive_keyboard = get_generic_inline_keyboard()

            # Редагуємо інтерактивне повідомлення
            try:
                await bot.edit_message_text(
                    chat_id=callback.message.chat.id,
                    message_id=interactive_message_id,
                    text=new_interactive_text,
                    reply_markup=new_interactive_keyboard
                )
            except Exception as e:
                logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")

            # Відправляємо головне меню
            user_first_name = callback.from_user.first_name
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

            # Видаляємо попереднє повідомлення з клавіатурою
            old_bot_message_id = state_data.get('bot_message_id')
            if old_bot_message_id:
                try:
                    await bot.delete_message(chat_id=callback.message.chat.id, message_id=old_bot_message_id)
                except Exception as e:
                    logger.error(f"Не вдалося видалити повідомлення бота: {e}")
        else:
            # Додайте обробку інших інлайн-кнопок за потребою
            await bot.answer_callback_query(callback.id, text=UNHANDLED_INLINE_BUTTON_TEXT)
    else:
        logger.error("interactive_message_id не знайдено")
        await bot.answer_callback_query(callback.id, text=GENERIC_ERROR_MESSAGE_TEXT)

    await callback.answer()

# Обробчик для прийому пошуку героя
@router.message(MenuStates.SEARCH_HERO)
async def handle_search_hero(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    hero_name = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} шукає героя: {hero_name}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Логіка пошуку героя
    if hero_name:
        hero_info = await search_hero(db, hero_name)
        if hero_info:
            response_text = (
                f"🔍 <b>Інформація про героя:</b>\n\n"
                f"• 🏅 Ім'я: {hero_info['name']}\n"
                f"• 🛡️ Клас: {hero_info['class']}\n"
                f"• 📈 Рейтинг: {hero_info['rating']}\n"
                f"• Опис: {hero_info['description']}\n"
            )
        else:
            response_text = f"❌ Герой з ім'ям '{hero_name}' не знайдено."
    else:
        response_text = "❌ Будь ласка, введіть ім'я героя для пошуку."

    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=response_text,
            parse_mode=ParseMode.HTML,
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося надіслати повідомлення про пошук героя: {e}")

    # Повертаємо користувача до меню Персонажі
    await state.set_state(MenuStates.HEROES_MENU)

# Обробчик для прийому теми пропозиції
@router.message(MenuStates.SEARCH_TOPIC)
async def handle_search_topic(message: Message, state: FSMContext, bot: Bot):
    topic = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} пропонує тему: {topic}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Логіка обробки пропозиції теми
    if topic:
        # Припустимо, ми маємо функцію для збереження пропозиції теми
        await save_suggestion(topic, message.from_user.id)
        response_text = SUGGESTION_RESPONSE_TEXT.format(topic=topic)
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

    # Повертаємо користувача до меню Зворотний Зв'язок
    await state.set_state(MenuStates.FEEDBACK_MENU)

# Обробчик невідомих повідомлень
@router.message()
async def unknown_command(message: Message, state: FSMContext, bot: Bot):
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо поточний стан
    current_state = await state.get_state()

    # Визначаємо новий текст та клавіатуру залежно від стану
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
        heroes_list = data.get('heroes_list', [])
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = f"Меню класу {hero_class}\nСписок героїв: {', '.join(heroes_list)}"
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
        await state.set_state(current_state)
        return
    else:
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)
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
        return

    # Видаляємо старе повідомлення
    if bot_message_id:
        await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагуємо інтерактивне повідомлення
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
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            interactive_message_id = await send_or_update_interactive_message(
                bot=bot,
                chat_id=message.chat.id,
                text=new_interactive_text,
                keyboard=get_generic_inline_keyboard(),
                message_id=None,
                state=state,
                parse_mode=ParseMode.HTML
            )
    else:
        interactive_message_id = await send_or_update_interactive_message(
            bot=bot,
            chat_id=message.chat.id,
            text=new_interactive_text,
            keyboard=get_generic_inline_keyboard(),
            message_id=None,
            state=state,
            parse_mode=ParseMode.HTML
        )

    # Оновлюємо стан користувача
    await state.update_data(bot_message_id=new_bot_message_id)

    # Встановлюємо новий стан
    await state.set_state(new_state)

# Функція для налаштування обробників
def setup_handlers(dp: Dispatcher):
    dp.include_router(router)
    # Якщо у вас є інші роутери, включіть їх тут, наприклад:
    # dp.include_router(profile_router)

# Основна функція запуску бота
async def main():
    bot = Bot(token='YOUR_BOT_TOKEN')  # Замініть на ваш токен
    dp = Dispatcher()
    setup_handlers(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())