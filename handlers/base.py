import logging
import io
import os
from typing import Optional

# Модулі для роботи з повідомленнями та графіками
import networkx as nx
import plotly.graph_objects as go
from PIL import Image

# Модулі Aiogram
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

# Модулі для роботи з базою даних (SQLAlchemy)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

# Імпорт власних модулів, станів та моделей
import models.user
import models.user_stats
from states import MenuStates
from utils.db import get_user_profile
from utils.message_utils import safe_delete_message, check_and_edit_message
from utils.text_formatter import format_profile_text

# Імпорт клавіатур та текстових констант
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
    M6_NEWS_TEXT, GPT_MENU_TEXT, TOURNAMENTS_MENU_TEXT, META_MENU_TEXT,
    LANGUAGE_CHANGED_TEXT, LANGUAGE_ERROR_TEXT, SETTINGS_TEXT,
    NOTIFICATIONS_TEXT, STATS_TEXT
)

# Додано імпорт для OpenAI
import openai

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Створюємо об'єкт роутера
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

# Ініціалізація OpenAI API
def initialize_openai():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.critical("OPENAI_API_KEY не встановлено в змінних оточення.")
        raise EnvironmentError("OPENAI_API_KEY не встановлено в змінних оточення.")
    openai.api_key = api_key
    logger.info("OpenAI API успішно ініціалізовано.")

# Викликаємо ініціалізацію одразу при імпорті модуля
initialize_openai()

# ------------------- Допоміжні функції -------------------

async def handle_error(
    bot: Bot,
    chat_id: int,
    error_message: str,
    logger: logging.Logger,
    exception: Exception = None
):
    """
    Централізована функція для обробки помилок: повідомлення логеру та відправка
    помилкового повідомлення користувачеві.
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

async def increment_step(state: FSMContext):
    """
    Інкрементує крок у FSM. Якщо крок досягає 3, не очищає стан.
    """
    data = await state.get_data()
    step_count = data.get("step_count", 0) + 1
    await state.update_data(step_count=step_count)
    logger.debug(f"Крок інкрементовано до {step_count}")

async def transition_state(state: FSMContext, new_state: State):
    """
    Встановлення нового стану без очищення існуючих даних.
    """
    await state.set_state(new_state)
    logger.debug(f"Стан встановлено на {new_state}")

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
    Перевіряє, чи змінився текст або клавіатура, і якщо так — редагує повідомлення.
    """
    state_data = await state.get_data()
    last_text = state_data.get('last_text')
    last_keyboard = state_data.get('last_keyboard')

    # Редагуємо повідомлення лише якщо є зміни
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

# ------------------- GPT-функція -------------------
async def get_gpt_response(prompt: str) -> str:
    """
    Отримання відповіді від ChatGPT (модель gpt-4) на заданий запит.
    """
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Ти допоміжний бот."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7,
        )
        answer = response.choices[0].message['content'].strip()
        logger.info(f"Отримано відповідь від GPT: {answer}")
        return answer
    except Exception as e:
        logger.error(f"Помилка при взаємодії з GPT: {e}")
        return "Виникла помилка при обробці вашого запиту. Спробуйте пізніше."

# ------------------- Графіки (Plotly) -------------------
def create_overall_activity_graph() -> bytes:
    """Генерація графіка загальної активності за місяць (псевдодані)."""
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
    """Генерація графіка рейтингу за місяць (псевдодані)."""
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
    """Генерація графіка ігрової статистики героїв (псевдодані)."""
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

# ------------------- Основні обробники -------------------

@router.message(Command("example"))
async def handle_example(message: Message, state: FSMContext):
    """
    Обробник для демонстрації переходу між станами.
    """
    await transition_state(state, MenuStates.MAIN_MENU)
    await message.answer("Перехід до головного меню.")

@router.message(Command("start"))
async def cmd_start(
    message: Message,
    state: FSMContext,
    db: AsyncSession,
    bot: Bot
):
    """
    Обробник команди /start, реєструє користувача і показує вступні сторінки.
    """
    user_id = message.from_user.id
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Реєстрація нового користувача (якщо його ще немає)
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
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger, e)
        return

    # Переходимо до стану INTRO_PAGE_1
    await transition_state(state, MenuStates.INTRO_PAGE_1)

    # Відправка першої "вступної" сторінки
    try:
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=INTRO_PAGE_1_TEXT,
            parse_mode=ParseMode.HTML,
            reply_markup=get_intro_page_1_keyboard()
        )
        # Зберігаємо в стан ID інтерактивного повідомлення
        await state.update_data(
            interactive_message_id=interactive_message.message_id,
            last_text=INTRO_PAGE_1_TEXT,
            last_keyboard=get_intro_page_1_keyboard(),
            bot_message_id=None
        )
    except Exception as e:
        logger.error(f"Не вдалося надіслати вступну сторінку 1: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger, e)

# ------------------- Функція для реєстрації обробників -------------------
def setup_handlers(dp: Dispatcher):
    """
    Функція для підключення всіх обробників з цього файлу до Dispatcher.
    """
    dp.include_router(router)
    logger.info("Base handlers have been set up.")