# handlers/base.py

import logging
import io
from typing import Optional

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.filters.text import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    ReplyKeyboardRemove
)
from aiogram.enums import ParseMode

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from states import MenuStates
from utils.db import get_user_profile
from utils.message_utils import safe_delete_message, check_and_edit_message
from utils.text_formatter import format_profile_text
from utils.error_handler import handle_error
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
    get_tournaments_menu, get_meta_menu, get_m6_menu, get_gpt_menu
)
from texts import (
    INTRO_PAGE_1_TEXT, INTRO_PAGE_2_TEXT, INTRO_PAGE_3_TEXT, MAIN_MENU_TEXT,
    MAIN_MENU_DESCRIPTION, MAIN_MENU_ERROR_TEXT, NAVIGATION_MENU_TEXT,
    NAVIGATION_INTERACTIVE_TEXT, PROFILE_MENU_TEXT, PROFILE_INTERACTIVE_TEXT,
    UNKNOWN_COMMAND_TEXT, GENERIC_ERROR_MESSAGE_TEXT, USE_BUTTON_NAVIGATION_TEXT,
    SEARCH_HERO_RESPONSE_TEXT, SUGGESTION_RESPONSE_TEXT, CHANGE_USERNAME_RESPONSE_TEXT,
    MLS_BUTTON_RESPONSE_TEXT, UNHANDLED_INLINE_BUTTON_TEXT, FEEDBACK_RECEIVED_TEXT,
    BUG_REPORT_RECEIVED_TEXT, TOURNAMENT_CREATE_TEXT, TOURNAMENT_VIEW_TEXT,
    META_HERO_LIST_TEXT, META_RECOMMENDATIONS_TEXT, META_UPDATES_TEXT,
    M6_INFO_TEXT, M6_STATS_TEXT, M6_NEWS_TEXT, GPT_MENU_TEXT
)

from PIL import Image
import plotly.graph_objects as go

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

# Допоміжні функції

async def transition_state(state: FSMContext, new_state: State):
    """
    Встановлення нового стану без очищення існуючих даних.

    :param state: Контекст FSM.
    :param new_state: Новий стан для встановлення.
    """
    await state.set_state(new_state)
    logger.debug(f"Стан встановлено на {new_state}")

def create_overall_activity_graph() -> bytes:
    """Генерація графіка загальної активності за місяць."""
    days = list(range(1, 31))
    activity = [i + (i % 5) * 10 for i in days]  # Приклад даних
    fig = go.Figure(data=go.Bar(x=days, y=activity))
    fig.update_layout(
        title="📊 Загальна Активність за Місяць",
        xaxis_title="Дні",
        yaxis_title="Активність",
        template="plotly_white"
    )
    with io.BytesIO() as buffer:
        fig.write_image(buffer, format="PNG")
        return buffer.getvalue()

def create_rating_graph() -> bytes:
    """Генерація графіка рейтингу за місяць."""
    months = ['Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень']
    ratings = [1500, 2000, 1800, 2200, 2100, 2300]  # Приклад даних
    fig = go.Figure(data=go.Scatter(x=months, y=ratings, mode='lines+markers'))
    fig.update_layout(
        title="🥇 Ваш Рейтинг за Місяць",
        xaxis_title="Місяці",
        yaxis_title="Рейтинг",
        template="plotly_white"
    )
    with io.BytesIO() as buffer:
        fig.write_image(buffer, format="PNG")
        return buffer.getvalue()

def create_game_stats_graph() -> bytes:
    """Генерація графіка ігрової статистики героїв."""
    heroes = ['Hero A', 'Hero B', 'Hero C', 'Hero D', 'Hero E']
    kills = [50, 70, 60, 80, 90]  # Приклад даних
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
    with io.BytesIO() as buffer:
        fig.write_image(buffer, format="PNG")
        return buffer.getvalue()

def create_comparison_graph(hero1_stats: dict, hero2_stats: dict, hero1_name: str, hero2_name: str) -> bytes:
    """
    Генерація графіка порівняння двох героїв.

    :param hero1_stats: Статистика першого героя.
    :param hero2_stats: Статистика другого героя.
    :param hero1_name: Ім'я першого героя.
    :param hero2_name: Ім'я другого героя.
    :return: Байти зображення графіка.
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
    with io.BytesIO() as buffer:
        fig.write_image(buffer, format="PNG")
        return buffer.getvalue()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    """
    Обробник команди /start, реєструє користувача та відправляє вступні сторінки.
    """
    user_id = message.from_user.id

    # Видаляємо повідомлення з командою /start
    await safe_delete_message(bot, message.chat.id, message.message_id)

    try:
        async with db.begin():
            user_result = await db.execute(
                select(models.user.User).where(models.user.User.telegram_id == user_id)
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

@router.callback_query(Text(equals="intro_next_1"))
async def handle_intro_next_1(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Обробник для переходу від INTRO_PAGE_1 до INTRO_PAGE_2.
    """
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
    await transition_state(state, new_state)
    await bot.answer_callback_query(callback.id)

@router.callback_query(Text(equals="intro_next_2"))
async def handle_intro_next_2(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Обробник для переходу від INTRO_PAGE_2 до INTRO_PAGE_3.
    """
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
    await transition_state(state, new_state)
    await bot.answer_callback_query(callback.id)

@router.callback_query(Text(equals="intro_start"))
async def handle_intro_start(callback: CallbackQuery, state: FSMContext, bot: Bot, db: AsyncSession):
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
        await bot.answer_callback_query(callback.id, text="Некоректна дія для цього стану.", show_alert=True)
        return

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
        await handle_error(bot, callback.message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger)

    # Надсилаємо нове звичайне повідомлення з головним меню
    try:
        main_menu_message = await bot.send_message(
            chat_id=callback.message.chat.id,
            text=main_menu_text_formatted,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_menu_message.message_id)
    except Exception as e:
        logger.error(f"Не вдалося надіслати головне меню: {e}")
        await handle_error(bot, callback.message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger)
        return

    # Видаляємо попереднє повідомлення з клавіатурою (якщо необхідно)
    old_bot_message_id = state_data.get('bot_message_id')
    if old_bot_message_id:
        await safe_delete_message(bot, callback.message.chat.id, old_bot_message_id)

    # Встановлення стану до MAIN_MENU
    await transition_state(state, MenuStates.MAIN_MENU)
    await bot.answer_callback_query(callback.id)

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
    Уніфікована функція для обробки різних меню.

    :param user_choice: Вибір користувача.
    :param message: Повідомлення користувача.
    :param state: Контекст FSM.
    :param db: Асинхронна сесія бази даних.
    :param bot: Екземпляр бота.
    :param chat_id: ID чату.
    :param main_menu_error: Текст повідомлення про помилку головного меню.
    :param main_menu_keyboard_func: Функція для отримання клавіатури головного меню.
    :param main_menu_text: Текст головного меню.
    :param interactive_text: Текст інтерактивного повідомлення.
    :param new_state: Новий стан після обробки.
    """
    logger.info(f"Користувач обрав '{user_choice}' в меню")

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Перевірка існування ID повідомлень
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        try:
            main_message = await bot.send_message(chat_id=chat_id, text=main_menu_error, reply_markup=main_menu_keyboard_func())
            await state.update_data(bot_message_id=main_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку головного меню: {e}")
            await handle_error(bot, chat_id, GENERIC_ERROR_MESSAGE_TEXT, logger)
        return

    # Логіка для вибору користувача
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    updated_state = new_state

    if user_choice == MenuButton.NAVIGATION.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        updated_state = MenuStates.NAVIGATION_MENU
    elif user_choice == MenuButton.PROFILE.value:
        # Виклик функції обробки профілю
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
        new_main_text = M6_INFO_TEXT  # Змінено відповідно до вашого тексту
        new_main_keyboard = get_m6_menu()
        new_interactive_text = M6_INFO_TEXT
        updated_state = MenuStates.M6_MENU
    elif user_choice == MenuButton.GPT.value:
        new_main_text = GPT_MENU_TEXT
        new_main_keyboard = get_gpt_menu()
        new_interactive_text = GPT_MENU_TEXT
        updated_state = MenuStates.GPT_MENU
    elif user_choice == MenuButton.BACK.value:
        # Повернення до головного меню
        user_first_name = message.from_user.first_name or "Користувач"
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        updated_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = main_menu_keyboard_func()
        new_interactive_text = "Невідома команда"
        updated_state = MenuStates.MAIN_MENU

    # Відправка нового звичайного повідомлення
    try:
        main_message = await bot.send_message(chat_id=chat_id, text=new_main_text, reply_markup=new_main_keyboard)
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося надіслати нове повідомлення: {e}")
        await handle_error(bot, chat_id, GENERIC_ERROR_MESSAGE_TEXT, logger)
        return

    # Видалення старого звичайного повідомлення
    await safe_delete_message(bot, chat_id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=chat_id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану користувача
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, updated_state)

async def process_my_profile(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    """
    Обробка відображення профілю користувача.

    :param message: Повідомлення користувача.
    :param state: Контекст FSM.
    :param db: Асинхронна сесія бази даних.
    :param bot: Екземпляр бота.
    """
    user_id = message.from_user.id
    profile_data = await get_user_profile(db, user_id)  # Отримання профілю з БД

    await safe_delete_message(bot, message.chat.id, message.message_id)

    if profile_data:
        # Підготовка даних для форматування
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

        # Форматування тексту профілю з використанням утиліти
        try:
            formatted_profile_text = format_profile_text(PROFILE_INTERACTIVE_TEXT, profile_info)
        except ValueError as e:
            logger.error(f"Помилка форматування профілю: {e}")
            formatted_profile_text = GENERIC_ERROR_MESSAGE_TEXT

        data = await state.get_data()
        old_bot_message_id = data.get('bot_message_id')  # ID попереднього звичайного повідомлення
        interactive_message_id = data.get('interactive_message_id')  # ID інлайн-повідомлення

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

@router.message(Text(equals="🪪 Мій Профіль", ignore_case=True))
async def handle_my_profile_handler(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    """
    Обробчик натискання кнопки "🪪 Мій Профіль".
    """
    await process_my_profile(message=message, state=state, db=db, bot=bot)

@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
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

@router.message(MenuStates.FEEDBACK_MENU)
async def handle_feedback_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
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
        new_main_text = "✉️ Введіть ваш зворотний зв'язок:"
        new_interactive_text = "Надсилання зворотного зв'язку"
        new_state = MenuStates.RECEIVE_FEEDBACK
        new_main_keyboard = ReplyKeyboardRemove()
    elif user_choice == MenuButton.REPORT_BUG.value:
        new_main_text = "🐞 Опишіть знайдену помилку:"
        new_interactive_text = "Повідомлення про помилку"
        new_state = MenuStates.REPORT_BUG
        new_main_keyboard = ReplyKeyboardRemove()
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

@router.message(MenuStates.CHANGE_USERNAME)
async def handle_change_username(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
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
                    select(models.user.User).where(models.user.User.telegram_id == user_id)
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

@router.message(MenuStates.RECEIVE_FEEDBACK)
async def handle_receive_feedback(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    """
    Обробчик для прийому зворотного зв'язку від користувача.
    """
    feedback = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"Користувач {user_id} надав зворотний зв'язок: {feedback}")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    if feedback:
        # Збереження зворотного зв'язку у базі даних або надсилання адміністратору
        # Приклад збереження у таблиці Feedback (необхідно реалізувати модель Feedback)
        # from models.feedback import Feedback
        # new_feedback = Feedback(user_id=user_id, feedback=feedback)
        # db.add(new_feedback)
        # await db.commit()

        response_text = FEEDBACK_RECEIVED_TEXT
        logger.info(f"Зворотний зв'язок отримано від користувача {user_id}")
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

@router.message(MenuStates.REPORT_BUG)
async def handle_report_bug(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    """
    Обробчик для прийому звіту про помилку від користувача.
    """
    bug_report = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"Користувач {user_id} повідомив про помилку: {bug_report}")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    if bug_report:
        # Збереження звіту про помилку у базі даних або надсилання адміністратору
        # Приклад збереження у таблиці BugReports (необхідно реалізувати модель BugReport)
        # from models.bug_report import BugReport
        # new_bug = BugReport(user_id=user_id, report=bug_report)
        # db.add(new_bug)
        # await db.commit()

        response_text = BUG_REPORT_RECEIVED_TEXT
        logger.info(f"Звіт про помилку отримано від користувача {user_id}")
    else:
        response_text = "❌ Будь ласка, опишіть помилку, яку ви зустріли."

    try:
        await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
    except Exception as e:
        logger.error(f"Не вдалося надіслати повідомлення про отримання звіту про помилку: {e}")

    await transition_state(state, MenuStates.FEEDBACK_MENU)

@router.message(MenuStates.TOURNAMENTS_MENU)
async def handle_tournaments_menu_buttons(message: Message, state: FSMContext, bot: Bot):
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
        new_main_text = "🛠️ Створення турніру ще в розробці."
        new_interactive_text = "Створення турніру"
    elif user_choice == MenuButton.VIEW_TOURNAMENTS.value:
        new_main_text = "👀 Перегляд турнірів:"
        new_interactive_text = "Перегляд турнірів"
        # Тут можна додати логіку для відображення списку турнірів
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

@router.message(MenuStates.META_MENU)
async def handle_meta_menu_buttons(message: Message, state: FSMContext, bot: Bot):
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
            await handle_error(bot, chat_id=message.chat.id, error_message=MAIN_MENU_ERROR_MESSAGE_TEXT, logger=logger)
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

@router.message(MenuStates.M6_MENU)
async def handle_m6_menu_buttons(message: Message, state: FSMContext, bot: Bot):
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

    # Редагуємо інтерактивне повідомлення
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

@router.message(MenuStates.GPT_MENU)
async def handle_gpt_menu_buttons(message: Message, state: FSMContext, bot: Bot):
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

    # Редагуємо інтерактивне повідомлення
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

@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    """
    Обробчик кнопок у меню Навігація.
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Навігація")

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
            # Зберігаємо ID повідомлення бота
            await state.update_data(bot_message_id=main_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку головного меню: {e}")
            await handle_error(bot, chat_id=message.chat.id, error_message=MAIN_MENU_ERROR_TEXT, logger=logger)
        return

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state: Optional[State] = None

    if user_choice == MenuButton.HEROES.value:
        new_main_text = "🔮 Оберіть клас героя:"
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = "Меню Персонажі"
        new_state = MenuStates.HEROES_MENU
    elif user_choice == MenuButton.GUIDES.value:
        new_main_text = "📚 Оберіть тип гайдів:"
        new_main_keyboard = get_guides_menu()
        new_interactive_text = "Меню Гайди"
        new_state = MenuStates.GUIDES_MENU
    elif user_choice == MenuButton.COUNTER_PICKS.value:
        new_main_text = "🔄 Оберіть контр-піки:"
        new_main_keyboard = get_counter_picks_menu()
        new_interactive_text = "Меню Контр-піки"
        new_state = MenuStates.COUNTER_PICKS_MENU
    elif user_choice == MenuButton.BUILDS.value:
        new_main_text = "🛠️ Оберіть білди:"
        new_main_keyboard = get_builds_menu()
        new_interactive_text = "Меню Білди"
        new_state = MenuStates.BUILDS_MENU
    elif user_choice == MenuButton.VOTING.value:
        new_main_text = "🗳️ Оберіть голосування:"
        new_main_keyboard = get_voting_menu()
        new_interactive_text = "Меню Голосування"
        new_state = MenuStates.VOTING_MENU
    elif user_choice == MenuButton.BACK.value:
        # Повернення до головного меню
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
    if new_state:
        await transition_state(state, new_state)
    await state.update_data(bot_message_id=new_bot_message_id)

@router.message(MenuStates.HEROES_MENU)
async def handle_heroes_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    """
    Обробчик кнопок у меню Персонажі.
    """
    user_choice = message.text
    state_data = await state.get_data()
    hero_class = state_data.get('hero_class', 'Танк')
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' у класі {hero_class}")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Тут додайте логіку для обробки вибору героя
    # Наприклад, відображення інформації про героя або вибір конкретного героя
    # Поки що відправимо повідомлення про отримання запиту

    response_text = f"🔍 Ви обрали героя з класу {hero_class}: {user_choice} (інформація ще не доступна)."

    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=response_text,
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося надіслати повідомлення про героя: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)

    # Повертаємо користувача до меню Персонажі
    await transition_state(state, MenuStates.HEROES_MENU)

@router.message(MenuStates.GUIDES_MENU)
async def handle_guides_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    """
    Обробчик кнопок у меню Гайди.
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Гайди")

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
    new_main_keyboard = get_guides_menu()
    new_interactive_text = ""
    new_state = MenuStates.GUIDES_MENU

    if user_choice == "Нові гайди":
        new_main_text = "🆕 Нові гайди ще в розробці."
        new_interactive_text = "Нові гайди"
    elif user_choice == "Популярні гайди":
        new_main_text = "🔥 Популярні гайди:"
        new_interactive_text = "Популярні гайди"
        # Тут можна додати логіку для відображення популярних гайдів
    elif user_choice == "Гайди для початківців":
        new_main_text = "📘 Гайди для початківців:"
        new_interactive_text = "Гайди для початківців"
        # Тут можна додати логіку для відображення гайдів для початківців
    elif user_choice == "Гайди для просунутих":
        new_main_text = "📗 Гайди для просунутих:"
        new_interactive_text = "Гайди для просунутих"
        # Тут можна додати логіку для відображення гайдів для просунутих
    elif user_choice == "Гайди для командної гри":
        new_main_text = "📕 Гайди для командної гри:"
        new_interactive_text = "Гайди для командної гри"
        # Тут можна додати логіку для відображення гайдів для командної гри
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.GUIDES_MENU

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

@router.message(MenuStates.COUNTER_PICKS_MENU)
async def handle_counter_picks_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    """
    Обробчик кнопок у меню Контр-піки.
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Контр-піки")

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
    new_main_keyboard = get_counter_picks_menu()
    new_interactive_text = ""
    new_state = MenuStates.COUNTER_PICKS_MENU

    if user_choice == "Пошук контр-піка":
        new_main_text = "🔍 Введіть ім'я героя для пошуку контр-піка:"
        new_interactive_text = "Пошук контр-піка"
        new_state = MenuStates.COUNTER_SEARCH
        new_main_keyboard = ReplyKeyboardRemove()
    elif user_choice == "Список контр-піків":
        new_main_text = "📜 Список контр-піків:"
        new_interactive_text = "Список контр-піків"
        # Тут можна додати логіку для відображення списку контр-піків
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.COUNTER_PICKS_MENU

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

@router.callback_query()
async def handle_inline_buttons(callback: CallbackQuery, state: FSMContext, bot: Bot):
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

@router.message(MenuStates.SEARCH_HERO)
async def handle_search_hero(message: Message, state: FSMContext, bot: Bot):
    """
    Обробчик для прийому імені героя для пошуку.
    """
    hero_name = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} шукає героя: {hero_name}")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Тут додайте логіку пошуку героя
    # Наприклад, перевірка чи існує герой, відправка інформації тощо
    # Поки що відправимо повідомлення про отримання запиту

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
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)

    # Повертаємо користувача до попереднього меню
    await transition_state(state, MenuStates.HEROES_MENU)

@router.message(MenuStates.SEARCH_TOPIC)
async def handle_search_topic(message: Message, state: FSMContext, bot: Bot):
    """
    Обробчик для прийому теми пропозиції.
    """
    topic = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"Користувач {user_id} пропонує тему: {topic}")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Тут додайте логіку обробки пропозиції теми
    # Наприклад, збереження в базі даних або надсилання адміністратору
    # Поки що відправимо повідомлення про отримання запиту

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
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)

    # Повертаємо користувача до меню Зворотний Зв'язок
    await transition_state(state, MenuStates.FEEDBACK_MENU)

@router.message(MenuStates.HERO_CLASS_MENU)
async def handle_hero_class_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    """
    Обробчик кнопок у меню класу героїв.
    """
    user_choice = message.text
    state_data = await state.get_data()
    hero_class = state_data.get('hero_class', 'Танк')
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' у класі {hero_class}")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Тут додайте логіку для обробки вибору героя
    # Наприклад, відображення інформації про героя або вибір конкретного героя
    # Поки що відправимо повідомлення про отримання запиту

    response_text = f"🔍 Ви обрали героя з класу {hero_class}: {user_choice} (інформація ще не доступна)."

    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=response_text,
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося надіслати повідомлення про героя: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)

    # Повертаємо користувача до меню Персонажі
    await transition_state(state, MenuStates.HEROES_MENU)

@router.message(MenuStates.GUIDES_MENU)
async def handle_guides_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    """
    Обробчик кнопок у меню Гайди.
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Гайди")

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
    new_main_keyboard = get_guides_menu()
    new_interactive_text = ""
    new_state = MenuStates.GUIDES_MENU

    if user_choice == "Нові гайди":
        new_main_text = "🆕 Нові гайди ще в розробці."
        new_interactive_text = "Нові гайди"
    elif user_choice == "Популярні гайди":
        new_main_text = "🔥 Популярні гайди:"
        new_interactive_text = "Популярні гайди"
        # Тут можна додати логіку для відображення популярних гайдів
    elif user_choice == "Гайди для початківців":
        new_main_text = "📘 Гайди для початківців:"
        new_interactive_text = "Гайди для початківців"
        # Тут можна додати логіку для відображення гайдів для початківців
    elif user_choice == "Гайди для просунутих":
        new_main_text = "📗 Гайди для просунутих:"
        new_interactive_text = "Гайди для просунутих"
        # Тут можна додати логіку для відображення гайдів для просунутих
    elif user_choice == "Гайди для командної гри":
        new_main_text = "📕 Гайди для командної гри:"
        new_interactive_text = "Гайди для командної гри"
        # Тут можна додати логіку для відображення гайдів для командної гри
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.GUIDES_MENU

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

@router.message(MenuStates.COUNTER_SEARCH)
async def handle_counter_search(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    """
    Обробчик для пошуку контр-піка.
    """
    hero_name = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"Користувач {user_id} шукає контр-пік для героя: {hero_name}")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    if hero_name:
        # Реалізуйте логіку пошуку контр-піка
        # Наприклад, пошук у базі даних або API
        # Поки що відправимо повідомлення про отримання запиту

        response_text = f"🔍 Результати пошуку контр-піка для героя **{hero_name}** ще не доступні."
    else:
        response_text = "❌ Будь ласка, введіть ім'я героя для пошуку контр-піка."

    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=response_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося надіслати повідомлення про пошук контр-піка: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)

    # Повертаємо користувача до меню Контр-піки
    await transition_state(state, MenuStates.COUNTER_PICKS_MENU)

@router.callback_query(Text(equals=["compare_confirm_yes", "compare_confirm_no"]))
async def handle_comparison_confirmation(callback: CallbackQuery, state: FSMContext, db: AsyncSession, bot: Bot):
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
        # Тут необхідно реалізувати функцію для отримання реальної статистики героїв
        # Для демонстрації використаємо фіктивні дані
        hero1_stats = {'kills': 50, 'deaths': 30, 'assists': 100}
        hero2_stats = {'kills': 70, 'deaths': 40, 'assists': 120}

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

@router.message(MenuStates.BUILDS_MENU)
async def handle_builds_menu_buttons(message: Message, state: FSMContext, bot: Bot):
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
        new_main_text = "🛠️ Створення білду ще в розробці."
        new_interactive_text = "Створення білду"
    elif user_choice == MenuButton.MY_BUILDS.value:
        new_main_text = "🗂️ Ваші білди:"
        new_interactive_text = "Мої білди"
        # Тут можна додати логіку для відображення списку білдів
    elif user_choice == MenuButton.POPULAR_BUILDS.value:
        new_main_text = "🔥 Популярні білди:"
        new_interactive_text = "Популярні білди"
        # Тут можна додати логіку для відображення популярних білдів
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

@router.message(MenuStates.VOTING_MENU)
async def handle_voting_menu_buttons(message: Message, state: FSMContext, bot: Bot):
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
        new_main_text = "🗳️ Поточні опитування:"
        new_interactive_text = "Поточні опитування"
        # Тут можна додати логіку для відображення поточних опитувань
    elif user_choice == MenuButton.MY_VOTES.value:
        new_main_text = "🗳️ Ваші голосування:"
        new_interactive_text = "Мої голосування"
        # Тут можна додати логіку для відображення голосувань користувача
    elif user_choice == MenuButton.SUGGEST_TOPIC.value:
        new_main_text = "📝 Введіть тему для пропозиції:"
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
    if new_state:
        await transition_state(state, new_state)
    await state.update_data(bot_message_id=new_bot_message_id)

@router.message(MenuStates.PROFILE_MENU)
async def handle_profile_menu_buttons(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
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
        new_main_text = "📈 Статистика профілю:"
        new_main_keyboard = get_statistics_menu()
        new_interactive_text = "Меню Статистика"
        new_state = MenuStates.STATISTICS_MENU
    elif user_choice == MenuButton.ACHIEVEMENTS.value:
        new_main_text = "🏆 Досягнення профілю:"
        new_main_keyboard = get_achievements_menu()
        new_interactive_text = "Меню Досягнення"
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif user_choice == MenuButton.SETTINGS.value:
        new_main_text = "⚙️ Налаштування профілю:"
        new_main_keyboard = get_settings_menu()
        new_interactive_text = "Меню Налаштування"
        new_state = MenuStates.SETTINGS_MENU
    elif user_choice == MenuButton.FEEDBACK.value:
        new_main_text = "✉️ Зворотний зв'язок:"
        new_main_keyboard = get_feedback_menu()
        new_interactive_text = "Меню Зворотний Зв'язок"
        new_state = MenuStates.FEEDBACK_MENU
    elif user_choice == MenuButton.HELP.value:
        new_main_text = "❓ Допомога:"
        new_main_keyboard = get_help_menu()
        new_interactive_text = "Меню Допомога"
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
    Відправка нового повідомлення або оновлення існуючого.

    :return: ID відправленого або оновленого повідомлення.
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
        return None

def setup_handlers(dp: Dispatcher):
    """
    Функція для налаштування обробників у Dispatcher.
    """
    dp.include_router(router)
    # Якщо у вас є інші роутери, включіть їх тут, наприклад:
    # dp.include_router(profile_router)