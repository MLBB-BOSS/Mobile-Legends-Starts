import logging
from aiogram import Router, F, Bot, Dispatcher
from aiogram.types import (
    Message, ReplyKeyboardRemove, InlineKeyboardMarkup,
    InlineKeyboardButton, CallbackQuery
)
from aiogram.enums import ParseMode  # Updated import for ParseMode in v3.x
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text
from typing import Optional
from datetime import datetime
import io

from states import MenuStates
from utils.state_utils import increment_step
from keyboards.menus import (
    MenuButton,
    get_generic_inline_keyboard,
    get_navigation_menu,
    get_challenges_menu,
    get_guides_menu,
    get_bust_menu,
    get_teams_menu,
    get_trading_menu,
    get_settings_menu,
    get_help_menu,
    get_my_team_menu,
    get_language_menu,
    get_profile_menu,
    get_main_menu,
    get_statistics_menu,
    get_achievements_menu,
    get_feedback_menu,
    get_gpt_menu,
    get_voting_menu  # Ensure this function exists in keyboards.menus
)
from texts import (
    MAIN_MENU_ERROR_TEXT, UNKNOWN_COMMAND_TEXT, GENERIC_ERROR_MESSAGE_TEXT,
    CHALLENGES_TEXT, GUIDES_TEXT, BUST_TEXT, TEAMS_TEXT, TRADING_TEXT,
    NEW_GUIDES_TEXT, M6_TEXT, POPULAR_GUIDES_TEXT, BEGINNER_GUIDES_TEXT,
    ADVANCED_TECHNIQUES_TEXT, TEAMPLAY_GUIDES_TEXT,
    LANGUAGE_SELECTION_TEXT, UPDATE_ID_SUCCESS_TEXT, NOTIFICATIONS_SETTINGS_TEXT,
    INSTRUCTIONS_TEXT, FAQ_TEXT, HELP_SUPPORT_TEXT,
    MY_TEAM_TEXT, VIEW_PROFILE_TEXT, EDIT_PROFILE_TEXT,
    STATISTICS_TEXT, ACHIEVEMENTS_TEXT, FEEDBACK_TEXT, GPT_TEXT,
    USE_BUTTON_NAVIGATION_TEXT, FEEDBACK_RECEIVED_TEXT, BUG_REPORT_RECEIVED_TEXT,
    SEARCH_HERO_RESPONSE_TEXT, SUGGESTION_RESPONSE_TEXT,
    MLS_BUTTON_RESPONSE_TEXT, UNHANDLED_INLINE_BUTTON_TEXT,
    MAIN_MENU_DESCRIPTION, MAIN_MENU_TEXT  # Ensure these texts are defined in texts.py
)
from handlers.graph_utils import create_comparison_graph  # Ensure this exists
# from models.feedback import Feedback  # Uncomment when models are implemented
# from models.bug_report import BugReport  # Uncomment when models are implemented

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

# Дополнительные константы для навигационного меню
NAVIGATION_MENU_TEXT = """
🧭 Навигаційне меню

Оберіть розділ для переходу:
- Challenges - випробування та досягнення
- Guides - корисні гайди та поради
- Bust - підвищення рівня
- Teams - управління командами
- Trading - торгівля предметами
- Settings - налаштування
- Help - допомога
- Profile - профіль
- GPT - GPT інтеграція
"""

NAVIGATION_INTERACTIVE_TEXT = """
📱 Навігація по боту

Використовуйте кнопки нижче для переходу між розділами.
Поточний розділ: Навігація
"""

# Дополнительные функции
async def safe_delete_message(bot: Bot, chat_id: int, message_id: int):
    """Безпечное удаление сообщения"""
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        logger.debug(f"Deleted message {message_id} in chat {chat_id}")
    except Exception as e:
        logger.warning(f"Could not delete message {message_id} in chat {chat_id}: {e}")

async def check_and_edit_message(
    bot: Bot,
    chat_id: int,
    message_id: int,
    new_text: str,
    new_keyboard: Optional[InlineKeyboardMarkup],
    state: FSMContext,
    parse_mode: Optional[str] = None
):
    """Проверка и редактирование сообщения, если изменения произошли"""
    try:
        current_message = await bot.get_message(chat_id=chat_id, message_id=message_id)
        if current_message.text != new_text or current_message.reply_markup != new_keyboard:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=new_text,
                reply_markup=new_keyboard,
                parse_mode=parse_mode
            )
            logger.debug(f"Edited message {message_id} in chat {chat_id}")
    except Exception as e:
        logger.error(f"Failed to edit message {message_id} in chat {chat_id}: {e}")
        await handle_error(bot, chat_id, GENERIC_ERROR_MESSAGE_TEXT, logger)

async def handle_error(bot: Bot, chat_id: int, error_message: str, logger_instance: logging.Logger):
    """Обработка ошибок путем отправки сообщения пользователю"""
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=error_message,
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger_instance.critical(f"Failed to send error message to chat {chat_id}: {e}")

async def update_interactive_screen(
    bot: Bot,
    chat_id: int,
    message_id: int,
    text: str,
    keyboard: Optional[InlineKeyboardMarkup] = None
) -> bool:
    """Безопасное обновление интерактивного экрана"""
    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            reply_markup=keyboard or get_generic_inline_keyboard(),
            parse_mode=ParseMode.HTML
        )
        logger.debug(f"Updated interactive screen {message_id} in chat {chat_id}")
        return True
    except Exception as e:
        logger.error(f"Failed to update interactive screen: {e}")
        return False

async def verify_state_data(state: FSMContext) -> tuple[bool, dict]:
    """Проверка наличия необходимых данных в состоянии"""
    data = await state.get_data()
    required_fields = ['bot_message_id', 'interactive_message_id']
    
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        logger.error(f"Missing required state fields: {missing_fields}")
        return False, data
        
    return True, data

# Вспомогательная функция для перехода между состояниями
async def transition_state(state: FSMContext, new_state: MenuStates):
    await state.set_state(new_state)

# Обработчик команды /start
@router.message(commands=["start"])
async def handle_start(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    """Обработчик команды /start"""
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name or "Користувач"
    logger.info(f"User {user_id} started the bot.")
    
    # Регистрация пользователя в базе данных, если необходимо
    # Пример:
    # user = await db.get(User, user_id)
    # if not user:
    #     user = User(id=user_id, first_name=user_first_name)
    #     db.add(user)
    #     await db.commit()
    
    main_menu_text = f"🏠 Привіт, {user_first_name}! Ласкаво просимо до нашого бота."
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=main_menu_text,
            reply_markup=get_main_menu()
        )
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_DESCRIPTION,  # Определите этот текст в texts.py
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(
            bot_message_id=main_message.message_id,
            interactive_message_id=interactive_message.message_id
        )
        await transition_state(state, MenuStates.MAIN_MENU)
    except Exception as e:
        logger.error(f"Failed to send start messages: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger)

# Обработчик команды /example (пример)
@router.message(commands=["example"])
async def handle_example(message: Message, state: FSMContext, bot: Bot):
    """Пример обработчика команды"""
    logger.info(f"User {message.from_user.id} invoked /example command.")
    await safe_delete_message(bot, message.chat.id, message.message_id)
    
    try:
        example_message = await bot.send_message(
            chat_id=message.chat.id,
            text="Це приклад відповіді на команду /example.",
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(bot_message_id=example_message.message_id)
        await transition_state(state, MenuStates.EXAMPLE_STATE)  # Определите EXAMPLE_STATE в MenuStates
    except Exception as e:
        logger.error(f"Failed to send example message: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger)

# Обработчик нажатия обычных кнопок в меню Навигация
@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    """
    Обработчик кнопок в меню Навигация.
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Навигація")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Получаем IDs сообщений из состояния
    is_valid, data = await verify_state_data(state)
    if not is_valid:
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку головного меню: {e}")
        return

    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Определяем новый текст и клавиатуру
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state: Optional[MenuStates] = None

    if user_choice == MenuButton.CHALLENGES.value:
        new_main_text = CHALLENGES_TEXT
        new_main_keyboard = get_challenges_menu()
        new_interactive_text = "🎯 Challenges Menu"
        new_state = MenuStates.CHALLENGES_MENU
    elif user_choice == MenuButton.GUIDES.value:
        new_main_text = GUIDES_TEXT
        new_main_keyboard = get_guides_menu()
        new_interactive_text = "📚 Guides Menu"
        new_state = MenuStates.GUIDES_MENU
    elif user_choice == MenuButton.BUST.value:
        new_main_text = BUST_TEXT
        new_main_keyboard = get_bust_menu()
        new_interactive_text = "💪 Bust Menu"
        new_state = MenuStates.BUST_MENU
    elif user_choice == MenuButton.TEAMS.value:
        new_main_text = TEAMS_TEXT
        new_main_keyboard = get_teams_menu()
        new_interactive_text = "👥 Teams Menu"
        new_state = MenuStates.TEAMS_MENU
    elif user_choice == MenuButton.TRADING.value:
        new_main_text = TRADING_TEXT
        new_main_keyboard = get_trading_menu()
        new_interactive_text = "💼 Trading Menu"
        new_state = MenuStates.TRADING_MENU
    elif user_choice == MenuButton.SETTINGS.value:
        new_main_text = "⚙️ Settings"
        new_main_keyboard = get_settings_menu()
        new_interactive_text = "⚙️ Settings Menu"
        new_state = MenuStates.SETTINGS_SUBMENU
    elif user_choice == MenuButton.HELP.value:
        new_main_text = "❓ Help"
        new_main_keyboard = get_help_menu()
        new_interactive_text = "❓ Help Menu"
        new_state = MenuStates.HELP_SUBMENU
    elif user_choice == MenuButton.MY_TEAM.value:
        new_main_text = MY_TEAM_TEXT
        new_main_keyboard = get_my_team_menu()
        new_interactive_text = "🪪 My Team Menu"
        new_state = MenuStates.MY_TEAM_MENU
    elif user_choice == MenuButton.PROFILE.value:
        new_main_text = "🪪 My Profile"
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "🪪 My Profile Menu"
        new_state = MenuStates.PROFILE_MENU
    elif user_choice == MenuButton.VOTING.value:
        new_main_text = "📊 Voting Menu"  # Define appropriate text in texts.py
        new_main_keyboard = get_voting_menu()  # Ensure get_voting_menu() is defined
        new_interactive_text = "📊 Voting Menu"
        new_state = MenuStates.VOTING_MENU
    elif user_choice == MenuButton.GPT.value:
        new_main_text = GPT_TEXT
        new_main_keyboard = get_gpt_menu()
        new_interactive_text = "👾 GPT Menu"
        new_state = MenuStates.GPT_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.NAVIGATION_MENU

    # Отправляем новое сообщение с клавиатурой
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

    # Удаляем старое обычное сообщение
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редактируем интерактивное сообщение
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Обновляем состояние пользователя
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# 1. Обработчик кнопки "Back" для всех меню
@router.message(F.text == MenuButton.BACK.value)
async def handle_back_button(message: Message, state: FSMContext, bot: Bot):
    """Универсальный обработчик кнопки "Back" для возврата в предыдущее меню"""
    logger.info(f"User {message.from_user.id} pressed Back button")
    
    current_state = await state.get_state()
    BACK_TRANSITIONS = {
        MenuStates.CHALLENGES_MENU: MenuStates.MAIN_MENU,
        MenuStates.GUIDES_MENU: MenuStates.MAIN_MENU,
        MenuStates.BUST_MENU: MenuStates.MAIN_MENU,
        MenuStates.TEAMS_MENU: MenuStates.MAIN_MENU,
        MenuStates.TRADING_MENU: MenuStates.MAIN_MENU,
        MenuStates.SETTINGS_SUBMENU: MenuStates.SETTINGS_MENU,
        MenuStates.SELECT_LANGUAGE: MenuStates.SETTINGS_SUBMENU,
        MenuStates.PROFILE_MENU: MenuStates.MAIN_MENU,
        MenuStates.STATISTICS_MENU: MenuStates.PROFILE_MENU,
        MenuStates.MY_TEAM_MENU: MenuStates.PROFILE_MENU,
        MenuStates.ACHIEVEMENTS_MENU: MenuStates.PROFILE_MENU,
        MenuStates.FEEDBACK_MENU: MenuStates.PROFILE_MENU,
        MenuStates.HELP_SUBMENU: MenuStates.HELP_MENU,
        MenuStates.SEARCH_HERO: MenuStates.HEROES_MENU,
        MenuStates.SEARCH_TOPIC: MenuStates.FEEDBACK_MENU,
        MenuStates.CHANGE_USERNAME: MenuStates.SETTINGS_SUBMENU,
        MenuStates.HELP_MENU: MenuStates.PROFILE_MENU,
        MenuStates.GPT_MENU: MenuStates.PROFILE_MENU,
        MenuStates.VOTING_MENU: MenuStates.MAIN_MENU
    }
    
    next_state = BACK_TRANSITIONS.get(current_state, MenuStates.MAIN_MENU)
    
    try:
        # Удаление сообщения пользователя
        await safe_delete_message(bot, message.chat.id, message.message_id)
        
        # Получение данных состояния
        data = await state.get_data()
        old_bot_message_id = data.get('bot_message_id')
        interactive_message_id = data.get('interactive_message_id')
        
        # Удаление старого сообщения бота
        if old_bot_message_id:
            await safe_delete_message(bot, message.chat.id, old_bot_message_id)
        
        # Определение текста и клавиатуры для следующего состояния
        MENU_TEXTS = {
            MenuStates.MAIN_MENU: "🏠 Головне меню",
            MenuStates.SETTINGS_MENU: "⚙️ Settings",
            MenuStates.PROFILE_MENU: "🪪 My Profile",
            MenuStates.HELP_MENU: "❓ Help Menu",
            MenuStates.HELP_SUBMENU: "❓ Help Menu",
            MenuStates.STATISTICS_MENU: "📊 Статистика",
            MenuStates.MY_TEAM_MENU: "🪪 My Team Menu",
            MenuStates.ACHIEVEMENTS_MENU: "🏆 Досягнення",
            MenuStates.FEEDBACK_MENU: "💌 Зворотний зв'язок",
            MenuStates.GPT_MENU: "👾 GPT",
            MenuStates.CHALLENGES_MENU: "🎯 Challenges Menu",
            MenuStates.GUIDES_MENU: "📚 Guides Menu",
            MenuStates.BUST_MENU: "💪 Bust Menu",
            MenuStates.TEAMS_MENU: "👥 Teams Menu",
            MenuStates.TRADING_MENU: "💼 Trading Menu",
            MenuStates.SETTINGS_SUBMENU: "⚙️ Settings Submenu",
            MenuStates.NAVIGATION_MENU: NAVIGATION_MENU_TEXT,
            MenuStates.VOTING_MENU: "📊 Voting Menu"
        }
        
        MENU_KEYBOARDS = {
            MenuStates.MAIN_MENU: get_main_menu(),
            MenuStates.SETTINGS_MENU: get_settings_menu(),
            MenuStates.PROFILE_MENU: get_profile_menu(),
            MenuStates.HELP_MENU: get_help_menu(),
            MenuStates.HELP_SUBMENU: get_help_menu(),
            MenuStates.STATISTICS_MENU: get_statistics_menu(),
            MenuStates.MY_TEAM_MENU: get_my_team_menu(),
            MenuStates.ACHIEVEMENTS_MENU: get_achievements_menu(),
            MenuStates.FEEDBACK_MENU: get_feedback_menu(),
            MenuStates.GPT_MENU: get_gpt_menu(),
            MenuStates.CHALLENGES_MENU: get_challenges_menu(),
            MenuStates.GUIDES_MENU: get_guides_menu(),
            MenuStates.BUST_MENU: get_bust_menu(),
            MenuStates.TEAMS_MENU: get_teams_menu(),
            MenuStates.TRADING_MENU: get_trading_menu(),
            MenuStates.SETTINGS_SUBMENU: get_settings_menu(),
            MenuStates.NAVIGATION_MENU: get_navigation_menu(),
            MenuStates.VOTING_MENU: get_voting_menu()
        }
        
        new_text = MENU_TEXTS.get(next_state, "🏠 Головне меню")
        new_keyboard = MENU_KEYBOARDS.get(next_state, get_main_menu())
        
        # Отправка нового сообщения
        new_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_text,
            reply_markup=new_keyboard
        )
        
        # Обновление интерактивного экрана, если существует
        new_interactive_text = ""
        if next_state in MENU_TEXTS:
            if next_state == MenuStates.NAVIGATION_MENU:
                new_interactive_text = "📱 Навігаційний екран"
            else:
                new_interactive_text = f"{new_text} Menu"
        
        if interactive_message_id and new_interactive_text:
            await update_interactive_screen(
                bot=bot,
                chat_id=message.chat.id,
                message_id=interactive_message_id,
                text=new_interactive_text,
                keyboard=get_generic_inline_keyboard()
            )
        
        # Обновление состояния
        await state.update_data(
            bot_message_id=new_message.message_id,
            last_state=next_state.state,
            last_text=new_text,
            last_keyboard=new_keyboard,
            last_update=datetime.now().isoformat()
        )
        await transition_state(state, next_state)
        
    except Exception as e:
        logger.error(f"Error in back button handler: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# 2. Обработчики для кнопок и их подменю

# Обработчик кнопки "Challenges"
@router.message(F.text == MenuButton.CHALLENGES.value, MenuStates.MAIN_MENU)
async def handle_challenges(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    logger.info(f"User {message.from_user.id} selected Challenges")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Получаем текущие данные состояния
    is_valid, data = await verify_state_data(state)
    if not is_valid:
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Отправляем новое сообщение с меню Challenges
    try:
        challenges_message = await bot.send_message(
            chat_id=message.chat.id,
            text=CHALLENGES_TEXT,
            reply_markup=get_challenges_menu()
        )
        new_bot_message_id = challenges_message.message_id
    except Exception as e:
        logger.error(f"Failed to send Challenges menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        return

    # Удаляем предыдущее сообщение
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Обновляем интерактивный экран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text="🎯 Challenges Menu",
        keyboard=get_generic_inline_keyboard()
    )

    # Обновление состояния
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, MenuStates.CHALLENGES_MENU)

# Обработчик меню "Challenges Menu"
@router.message(MenuStates.CHALLENGES_MENU)
async def handle_challenges_menu_buttons(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Challenges Menu")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        try:
            error_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(bot_message_id=error_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = get_challenges_menu()
    new_interactive_text = "🎯 Challenges Menu"
    new_state = MenuStates.CHALLENGES_MENU

    if user_choice == MenuButton.ADD_CHALLENGE.value:
        new_main_text = "Функція додавання челенджів знаходиться в розробці."
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Головне меню"
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Оберіть розділ у головному меню"
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_challenges_menu()

    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Challenges menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        return

    # Удаляем предыдущее сообщение
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Обновляем интерактивный экран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        keyboard=get_generic_inline_keyboard()
    )

    # Обновление состояния
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обработчик кнопки "Guides"
@router.message(F.text == MenuButton.GUIDES.value, MenuStates.MAIN_MENU)
async def handle_guides(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    logger.info(f"User {message.from_user.id} selected Guides")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Получаем текущие данные состояния
    is_valid, data = await verify_state_data(state)
    if not is_valid:
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Отправляем новое сообщение с меню Guides
    try:
        guides_message = await bot.send_message(
            chat_id=message.chat.id,
            text=GUIDES_TEXT,
            reply_markup=get_guides_menu()
        )
        new_bot_message_id = guides_message.message_id
    except Exception as e:
        logger.error(f"Failed to send Guides menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        return

    # Удаляем предыдущее сообщение
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Обновляем интерактивный экран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text="📚 Guides Menu",
        keyboard=get_generic_inline_keyboard()
    )

    # Обновление состояния
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, MenuStates.GUIDES_MENU)

# Обработчик меню "Guides Menu"
@router.message(MenuStates.GUIDES_MENU)
async def handle_guides_menu_buttons(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Guides Menu")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        try:
            error_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(bot_message_id=error_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = get_guides_menu()
    new_interactive_text = "📚 Guides Menu"
    new_state = MenuStates.GUIDES_MENU

    if user_choice == "📄 Нові гайди":
        new_main_text = NEW_GUIDES_TEXT
    elif user_choice == "⭐ Популярні гайди":
        new_main_text = POPULAR_GUIDES_TEXT
    elif user_choice == "👶 Гайди для початківців":
        new_main_text = BEGINNER_GUIDES_TEXT
    elif user_choice == MenuButton.ADVANCED_TECHNIQUES.value:
        new_main_text = ADVANCED_TECHNIQUES_TEXT
    elif user_choice == "👥 Teamplay Guides":
        new_main_text = TEAMPLAY_GUIDES_TEXT
    elif user_choice == MenuButton.M6.value:
        new_main_text = M6_TEXT
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Головне меню"
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Оберіть розділ у головному меню"
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_guides_menu()

    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Guides menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        return

    # Удаляем предыдущее сообщение
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Обновляем интерактивный экран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        keyboard=get_generic_inline_keyboard()
    )

    # Обновление состояния
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обработчик кнопки "Bust"
@router.message(F.text == MenuButton.BUST.value, MenuStates.MAIN_MENU)
async def handle_bust(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    logger.info(f"User {message.from_user.id} selected Bust")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Получаем текущие данные состояния
    is_valid, data = await verify_state_data(state)
    if not is_valid:
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Отправляем новое сообщение с меню Bust
    try:
        bust_message = await bot.send_message(
            chat_id=message.chat.id,
            text=BUST_TEXT,
            reply_markup=get_bust_menu()
        )
        new_bot_message_id = bust_message.message_id
    except Exception as e:
        logger.error(f"Failed to send Bust menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        return

    # Удаляем предыдущее сообщение
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Обновляем интерактивный экран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text="💪 Bust Menu",
        keyboard=get_generic_inline_keyboard()
    )

    # Обновление состояния
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, MenuStates.BUST_MENU)

# Обработчик меню "Bust Menu"
@router.message(MenuStates.BUST_MENU)
async def handle_bust_menu_buttons(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Bust Menu")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        try:
            error_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(bot_message_id=error_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = get_bust_menu()
    new_interactive_text = "💪 Bust Menu"
    new_state = MenuStates.BUST_MENU

    if user_choice == "🔥 Підвищити Буст":
        new_main_text = "Функція підвищення буста знаходиться в розробці."
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Головне меню"
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Оберіть розділ у головному меню"
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_bust_menu()

    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Bust menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        return

    # Удаляем предыдущее сообщение
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Обновляем интерактивный экран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        keyboard=get_generic_inline_keyboard()
    )

    # Обновление состояния
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обработчик кнопки "Teams"
@router.message(F.text == MenuButton.TEAMS.value, MenuStates.MAIN_MENU)
async def handle_teams(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    logger.info(f"User {message.from_user.id} selected Teams")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Получаем текущие данные состояния
    is_valid, data = await verify_state_data(state)
    if not is_valid:
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Отправляем новое сообщение с меню Teams
    try:
        teams_message = await bot.send_message(
            chat_id=message.chat.id,
            text=TEAMS_TEXT,
            reply_markup=get_teams_menu()
        )
        new_bot_message_id = teams_message.message_id
    except Exception as e:
        logger.error(f"Failed to send Teams menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        return

    # Удаляем предыдущее сообщение
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Обновляем интерактивный экран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text="👥 Teams Menu",
        keyboard=get_generic_inline_keyboard()
    )

    # Обновление состояния
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, MenuStates.TEAMS_MENU)

# Обработчик меню "Teams Menu"
@router.message(MenuStates.TEAMS_MENU)
async def handle_teams_menu_buttons(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Teams Menu")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        try:
            error_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(bot_message_id=error_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = get_teams_menu()
    new_interactive_text = "👥 Teams Menu"
    new_state = MenuStates.TEAMS_MENU

    if user_choice == MenuButton.CREATE_TEAM.value:
        new_main_text = "Функція створення команди знаходиться в розробці."
    elif user_choice == MenuButton.VIEW_TEAMS.value:
        new_main_text = "Функція перегляду команд знаходиться в розробці."
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Головне меню"
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Оберіть розділ у головному меню"
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_teams_menu()

    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Teams menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        return

    # Удаляем предыдущее сообщение
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Обновляем интерактивный экран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        keyboard=get_generic_inline_keyboard()
    )

    # Обновление состояния
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обработчик нажатия обычных кнопок в меню Trading
@router.message(MenuStates.TRADING_MENU)
async def handle_trading_menu_buttons(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Trading Menu")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        try:
            error_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(bot_message_id=error_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = get_trading_menu()
    new_interactive_text = "💼 Trading Menu"
    new_state = MenuStates.TRADING_MENU

    if user_choice == MenuButton.CREATE_TRADE.value:
        new_main_text = "Функція створення торгівлі знаходиться в розробці!"
    elif user_choice == MenuButton.VIEW_TRADES.value:
        new_main_text = "Ось всі доступні торгівлі:"
        # Здесь можно добавить логику отображения торгов
    elif user_choice == MenuButton.MANAGE_TRADES.value:
        new_main_text = "Функція управління торгівлями знаходиться в розробці!"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Головне меню"
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Оберіть розділ у головному меню"
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_trading_menu()

    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Trading menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        return

    # Удаляем предыдущее сообщение
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Обновляем интерактивный экран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        keyboard=get_generic_inline_keyboard()
    )

    # Обновление состояния
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обработчик нажатия обычных кнопок в меню Settings Submenu
@router.message(MenuStates.SETTINGS_SUBMENU)
async def handle_settings_menu_buttons(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Settings Menu")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        try:
            error_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(bot_message_id=error_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = get_settings_menu()
    new_interactive_text = "⚙️ Settings Menu"
    new_state = MenuStates.SETTINGS_SUBMENU

    if user_choice == MenuButton.LANGUAGE.value:
        new_main_text = LANGUAGE_SELECTION_TEXT
        new_main_keyboard = get_language_menu()
        new_state = MenuStates.SELECT_LANGUAGE
    elif user_choice == MenuButton.CHANGE_USERNAME.value:
        new_main_text = "ℹ️ Введіть новий Username:"
        new_main_keyboard = ReplyKeyboardRemove()
        await increment_step(state)
        await state.set_state(MenuStates.CHANGE_USERNAME)
        try:
            await bot.send_message(chat_id=message.chat.id, text=new_main_text, reply_markup=new_main_keyboard)
        except Exception as e:
            logger.error(f"Failed to send Change Username prompt: {e}")
        return
    elif user_choice == MenuButton.UPDATE_ID.value:
        new_main_text = UPDATE_ID_SUCCESS_TEXT
    elif user_choice == MenuButton.NOTIFICATIONS.value:
        new_main_text = NOTIFICATIONS_SETTINGS_TEXT
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🪪 My Profile"
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "🪪 My Profile Menu"
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_settings_menu()

    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Settings menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        return

    # Удаляем предыдущее сообщение
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Обновляем интерактивный экран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        keyboard=get_generic_inline_keyboard()
    )

    # Обновление состояния
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обработчик выбора языка
@router.message(MenuStates.SELECT_LANGUAGE)
async def handle_select_language(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    selected_language = message.text
    logger.info(f"User {message.from_user.id} selected language: {selected_language}")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Реализуйте логику смены языка интерфейса, например, обновление в базе данных
    # Пример:
    # user_id = message.from_user.id
    # await update_user_language(db, user_id, selected_language)

    try:
        response_text = f"Інтерфейс змінено на {selected_language}."
        await bot.send_message(
            chat_id=message.chat.id,
            text=response_text,
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Failed to send language change confirmation: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)

    # Возвращаемся в меню Settings Submenu
    try:
        settings_message = await bot.send_message(
            chat_id=message.chat.id,
            text="⚙️ Settings",
            reply_markup=get_settings_menu()
        )
        await state.update_data(bot_message_id=settings_message.message_id)
        await increment_step(state)
        await transition_state(state, MenuStates.SETTINGS_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Settings menu after language change: {e}")

# Обработчик смены имени пользователя
@router.message(MenuStates.CHANGE_USERNAME)
async def handle_change_username(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    current_state = await state.get_state()
    if current_state != MenuStates.CHANGE_USERNAME.state:
        return

    new_username = message.text.strip()
    logger.info(f"User {message.from_user.id} is changing username to: {new_username}")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Реализуйте логику смены имени пользователя, например, обновление в базе данных
    # Пример:
    # user_id = message.from_user.id
    # await update_user_username(db, user_id, new_username)

    try:
        response_text = f"Username змінено на {new_username}."
        await bot.send_message(
            chat_id=message.chat.id,
            text=response_text,
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Failed to send username change confirmation: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)

    # Возвращаемся в меню Settings Submenu
    try:
        settings_message = await bot.send_message(
            chat_id=message.chat.id,
            text="⚙️ Settings",
            reply_markup=get_settings_menu()
        )
        await state.update_data(bot_message_id=settings_message.message_id)
        await increment_step(state)
        await transition_state(state, MenuStates.SETTINGS_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Settings menu after changing username: {e}")

# Обработчик кнопки "Help"
@router.message(F.text == MenuButton.HELP.value, MenuStates.MAIN_MENU)
async def handle_help(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    logger.info(f"User {message.from_user.id} selected Help")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Получаем текущие данные состояния
    is_valid, data = await verify_state_data(state)
    if not is_valid:
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Отправляем новое сообщение с меню Help
    try:
        help_message = await bot.send_message(
            chat_id=message.chat.id,
            text="❓ Help",
            reply_markup=get_help_menu()
        )
        new_bot_message_id = help_message.message_id
    except Exception as e:
        logger.error(f"Failed to send Help menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        return

    # Удаляем предыдущее сообщение
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Обновляем интерактивный экран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text="❓ Help Menu",
        keyboard=get_generic_inline_keyboard()
    )

    # Обновление состояния
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, MenuStates.HELP_SUBMENU)

# Обработчик меню "Help Submenu"
@router.message(MenuStates.HELP_SUBMENU)
async def handle_help_menu_buttons(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Help Menu")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        try:
            error_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(bot_message_id=error_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = get_help_menu()
    new_interactive_text = "❓ Help Menu"
    new_state = MenuStates.HELP_SUBMENU

    if user_choice == MenuButton.INSTRUCTIONS.value:
        new_main_text = INSTRUCTIONS_TEXT  # Добавьте соответствующий текст в `texts.py`
    elif user_choice == MenuButton.FAQ.value:
        new_main_text = FAQ_TEXT  # Добавьте соответствующий текст в `texts.py`
    elif user_choice == MenuButton.HELP_SUPPORT.value:
        new_main_text = HELP_SUPPORT_TEXT  # Добавьте соответствующий текст в `texts.py`
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🪪 My Profile"
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "🪪 My Profile Menu"
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_help_menu()

    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Help menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        return

    # Удаляем предыдущее сообщение
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Обновляем интерактивный экран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        keyboard=get_generic_inline_keyboard()
    )

    # Обновление состояния
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обработчик кнопки "My Team"
@router.message(F.text == MenuButton.MY_TEAM.value, MenuStates.MAIN_MENU)
async def handle_my_team(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    logger.info(f"User {message.from_user.id} selected My Team")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Получаем текущие данные состояния
    is_valid, data = await verify_state_data(state)
    if not is_valid:
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Отправляем новое сообщение с меню My Team
    try:
        my_team_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MY_TEAM_TEXT,
            reply_markup=get_my_team_menu()
        )
        new_bot_message_id = my_team_message.message_id
    except Exception as e:
        logger.error(f"Failed to send My Team menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        return

    # Удаляем предыдущее сообщение
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Обновляем интерактивный экран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text="🪪 My Team Menu",
        keyboard=get_generic_inline_keyboard()
    )

    # Обновление состояния
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, MenuStates.MY_TEAM_MENU)

# Обработчик меню "My Team Menu"
@router.message(MenuStates.MY_TEAM_MENU)
async def handle_my_team_menu_buttons(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in My Team Menu")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        try:
            error_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(bot_message_id=error_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = get_my_team_menu()
    new_interactive_text = "🪪 My Team Menu"
    new_state = MenuStates.MY_TEAM_MENU

    if user_choice == "➕ Створити Команду":
        new_main_text = "Функція створення команди знаходиться в розробці."
    elif user_choice == "👀 Переглянути Команди":
        new_main_text = "Функція перегляду команд знаходиться в розробці."
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Головне меню"
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Оберіть розділ у головному меню"
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_my_team_menu()

    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new My Team menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        return

    # Удаляем предыдущее сообщение
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Обновляем интерактивный экран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        keyboard=get_generic_inline_keyboard()
    )

    # Обновление состояния
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обработчик кнопки "Advanced Techniques"
@router.message(F.text == MenuButton.ADVANCED_TECHNIQUES.value)
async def handle_advanced_techniques(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Advanced Techniques")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Здесь можно добавить логику отображения Advanced Techniques
    # Например, отправить информацию или перейти к подменю
    try:
        advanced_techniques_message = await bot.send_message(
            chat_id=message.chat.id,
            text=ADVANCED_TECHNIQUES_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(bot_message_id=advanced_techniques_message.message_id)
        await increment_step(state)
        # Если нужно, установите новый статус или оставьте этот как конечный пункт
    except Exception as e:
        logger.error(f"Failed to send Advanced Techniques info: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Обработчик кнопки "Instructions"
@router.message(F.text == MenuButton.INSTRUCTIONS.value, MenuStates.HELP_SUBMENU)
async def handle_instructions(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Instructions")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    try:
        instructions_message = await bot.send_message(
            chat_id=message.chat.id,
            text=INSTRUCTIONS_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(bot_message_id=instructions_message.message_id)
        await increment_step(state)
    except Exception as e:
        logger.error(f"Failed to send Instructions: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Обработчик кнопки "FAQ"
@router.message(F.text == MenuButton.FAQ.value, MenuStates.HELP_SUBMENU)
async def handle_faq(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected FAQ")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    try:
        faq_message = await bot.send_message(
            chat_id=message.chat.id,
            text=FAQ_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(bot_message_id=faq_message.message_id)
        await increment_step(state)
    except Exception as e:
        logger.error(f"Failed to send FAQ: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Обработчик кнопки "Help Support"
@router.message(F.text == MenuButton.HELP_SUPPORT.value, MenuStates.HELP_SUBMENU)
async def handle_help_support(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Help Support")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    try:
        help_support_message = await bot.send_message(
            chat_id=message.chat.id,
            text=HELP_SUPPORT_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(bot_message_id=help_support_message.message_id)
        await increment_step(state)
    except Exception as e:
        logger.error(f"Failed to send Help Support: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Обработчик кнопки "Update ID"
@router.message(F.text == MenuButton.UPDATE_ID.value, MenuStates.SETTINGS_SUBMENU)
async def handle_update_id(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    logger.info(f"User {message.from_user.id} selected Update ID")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Реализуйте логику обновления ID, например, обновление в базе данных
    # Пример:
    # user_id = message.from_user.id
    # await update_user_id(db, user_id)

    try:
        response_text = UPDATE_ID_SUCCESS_TEXT
        await bot.send_message(
            chat_id=message.chat.id,
            text=response_text,
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Failed to send Update ID confirmation: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)

    # Возвращаемся в меню Settings Submenu
    try:
        settings_message = await bot.send_message(
            chat_id=message.chat.id,
            text="⚙️ Settings",
            reply_markup=get_settings_menu()
        )
        await state.update_data(bot_message_id=settings_message.message_id)
        await increment_step(state)
        await transition_state(state, MenuStates.SETTINGS_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Settings menu after updating ID: {e}")

# Обработчик кнопки "Notifications"
@router.message(F.text == MenuButton.NOTIFICATIONS.value, MenuStates.SETTINGS_SUBMENU)
async def handle_notifications(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    logger.info(f"User {message.from_user.id} selected Notifications")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=NOTIFICATIONS_SETTINGS_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Failed to send Notifications settings: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

    # Возвращаемся в меню Settings Submenu
    try:
        settings_message = await bot.send_message(
            chat_id=message.chat.id,
            text="⚙️ Settings",
            reply_markup=get_settings_menu()
        )
        await state.update_data(bot_message_id=settings_message.message_id)
        await increment_step(state)
        await transition_state(state, MenuStates.SETTINGS_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Settings menu after notifications: {e}")

# Обработчик кнопки "Language" в меню "Settings Submenu"
@router.message(F.text == MenuButton.LANGUAGE.value, MenuStates.SETTINGS_SUBMENU)
async def handle_language_selection_menu(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    """Открытие меню выбора языка"""
    logger.info(f"User {message.from_user.id} is selecting language")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=LANGUAGE_SELECTION_TEXT,
            reply_markup=get_language_menu()
        )
        await transition_state(state, MenuStates.SELECT_LANGUAGE)
    except Exception as e:
        logger.error(f"Failed to send Language selection menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Обработчик кнопки "Help" в различных контекстах (избежание дублирования)
@router.message(F.text == MenuButton.HELP.value)
async def handle_help_general(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    """Обработчик для кнопки Help в различных меню"""
    logger.info(f"User {message.from_user.id} selected Help")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    try:
        help_message = await bot.send_message(
            chat_id=message.chat.id,
            text=HELP_SUPPORT_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(bot_message_id=help_message.message_id)
        await increment_step(state)
    except Exception as e:
        logger.error(f"Failed to send Help message: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Обработчик кнопки "Profile"
@router.message(F.text == MenuButton.PROFILE.value, MenuStates.MAIN_MENU)
async def handle_profile(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    logger.info(f"User {message.from_user.id} selected Profile")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    try:
        profile_message = await bot.send_message(
            chat_id=message.chat.id,
            text="🪪 My Profile",
            reply_markup=get_profile_menu()
        )
        await state.update_data(bot_message_id=profile_message.message_id)
        await transition_state(state, MenuStates.PROFILE_MENU)
    except Exception as e:
        logger.error(f"Failed to send Profile menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Обработчик меню "Profile Menu"
@router.message(MenuStates.PROFILE_MENU)
async def handle_profile_menu_buttons(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Profile Menu")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        try:
            error_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(bot_message_id=error_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = get_profile_menu()
    new_interactive_text = "🪪 My Profile Menu"
    new_state = MenuStates.PROFILE_MENU

    if user_choice == MenuButton.VIEW_PROFILE.value:
        new_main_text = VIEW_PROFILE_TEXT  # Добавьте соответствующий текст в `texts.py`
    elif user_choice == MenuButton.EDIT_PROFILE.value:
        new_main_text = EDIT_PROFILE_TEXT  # Добавьте соответствующий текст в `texts.py`
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Головне меню"
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Оберіть розділ у головному меню"
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_profile_menu()

    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Profile menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        return

    # Удаляем предыдущее сообщение
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Обновляем интерактивный экран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        keyboard=get_generic_inline_keyboard()
    )

    # Обновление состояния
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обработчик для инлайн-кнопок
@router.callback_query()
async def handle_inline_buttons(callback: CallbackQuery, state: FSMContext, bot: Bot):
    """
    Обработчик для инлайн-кнопок.
    """
    data = callback.data
    logger.info(f"Користувач {callback.from_user.id} натиснув інлайн-кнопку: {data}")

    # Получаем interactive_message_id из состояния
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if interactive_message_id:
        # Обрабатываем инлайн-кнопки
        if data == "mls_button":
            await bot.answer_callback_query(callback.id, text=MLS_BUTTON_RESPONSE_TEXT)
        elif data == "compare_confirm_yes":
            # Обработка подтверждения сравнения героев
            comparison_data = state_data.get('temp_data', {})
            hero1_name = comparison_data.get('hero1_name')
            hero2_name = comparison_data.get('hero2_name')

            if not hero1_name or not hero2_name:
                response_text = "❌ Дані для порівняння відсутні. Спробуйте ще раз."
                try:
                    await bot.send_message(chat_id=callback.message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
                except Exception as e:
                    logger.error(f"Failed to send missing data message: {e}")
                await transition_state(state, MenuStates.CHALLENGES_MENU)
                return

            # Получение статистики героев из базы данных
            # Здесь необходимо реализовать функцию для получения реальной статистики героев
            # Для демонстрации используем фиктивные данные
            hero1_stats = {'kills': 50, 'deaths': 30, 'assists': 100}
            hero2_stats = {'kills': 70, 'deaths': 40, 'assists': 120}

            # Генерация графика сравнения
            try:
                comparison_graph_bytes = create_comparison_graph(hero1_stats, hero2_stats, hero1_name, hero2_name)
            except Exception as e:
                logger.error(f"Не вдалося згенерувати графік порівняння: {e}")
                await handle_error(bot, chat_id=callback.message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)
                await transition_state(state, MenuStates.CHALLENGES_MENU)
                return

            # Отправка графика
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

            # Очистка временных данных и возвращение в меню Challenges
            await state.update_data(comparison_step=None, temp_data={})
            await transition_state(state, MenuStates.CHALLENGES_MENU)
        elif data == "compare_confirm_no":
            response_text = "❌ Порівняння скасовано."
            try:
                await bot.send_message(chat_id=callback.message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
            except Exception as e:
                logger.error(f"Не вдалося надіслати повідомлення про скасування порівняння: {e}")
            await transition_state(state, MenuStates.CHALLENGES_MENU)
        elif data == "menu_back":
            # Возвращение в главное меню
            await transition_state(state, MenuStates.MAIN_MENU)
            new_interactive_text = MAIN_MENU_DESCRIPTION  # Определите в texts.py
            new_interactive_keyboard = get_generic_inline_keyboard()

            # Редактируем интерактивное сообщение
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

            # Отправляем главное меню
            user_first_name = callback.from_user.first_name or "Користувач"
            main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
            try:
                main_message = await bot.send_message(
                    chat_id=callback.message.chat.id,
                    text=main_menu_text_formatted,
                    reply_markup=get_main_menu()
                )
                # Обновляем bot_message_id
                await state.update_data(bot_message_id=main_message.message_id)
            except Exception as e:
                logger.error(f"Не вдалося надіслати головне меню: {e}")
                await handle_error(bot, chat_id=callback.message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)

            # Удаляем предыдущее сообщение с клавиатурой
            old_bot_message_id = state_data.get('bot_message_id')
            if old_bot_message_id:
                await safe_delete_message(bot, callback.message.chat.id, old_bot_message_id)
        else:
            # Добавьте обработку других инлайн-кнопок по мере необходимости
            await bot.answer_callback_query(callback.id, text=UNHANDLED_INLINE_BUTTON_TEXT)
    
    else:
        logger.error("interactive_message_id не знайдено")
        await bot.answer_callback_query(callback.id, text=GENERIC_ERROR_MESSAGE_TEXT)

    await callback.answer()

# Обработчик неизвестных сообщений
@router.message()
async def unknown_command(message: Message, state: FSMContext, bot: Bot):
    """
    Обработчик для неизвестных сообщений.
    Отвечает в зависимости от текущего состояния пользователя.
    """
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Получаем данные состояния
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Определяем текущее состояние
    current_state = await state.get_state()

    # Определяем новый текст и клавиатуру в зависимости от состояния
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = current_state

    MENU_TEXTS = {
        MenuStates.MAIN_MENU: UNKNOWN_COMMAND_TEXT,
        MenuStates.NAVIGATION_MENU: UNKNOWN_COMMAND_TEXT,
        MenuStates.CHALLENGES_MENU: UNKNOWN_COMMAND_TEXT,
        MenuStates.GUIDES_MENU: UNKNOWN_COMMAND_TEXT,
        MenuStates.BUST_MENU: UNKNOWN_COMMAND_TEXT,
        MenuStates.TEAMS_MENU: UNKNOWN_COMMAND_TEXT,
        MenuStates.TRADING_MENU: UNKNOWN_COMMAND_TEXT,
        MenuStates.SETTINGS_SUBMENU: UNKNOWN_COMMAND_TEXT,
        MenuStates.SELECT_LANGUAGE: USE_BUTTON_NAVIGATION_TEXT,
        MenuStates.CHANGE_USERNAME: USE_BUTTON_NAVIGATION_TEXT,
        MenuStates.PROFILE_MENU: UNKNOWN_COMMAND_TEXT,
        MenuStates.HELP_SUBMENU: UNKNOWN_COMMAND_TEXT,
        MenuStates.ACHIEVEMENTS_MENU: UNKNOWN_COMMAND_TEXT,
        MenuStates.STATISTICS_MENU: UNKNOWN_COMMAND_TEXT,
        MenuStates.MY_TEAM_MENU: UNKNOWN_COMMAND_TEXT,
        MenuStates.FEEDBACK_MENU: UNKNOWN_COMMAND_TEXT,
        MenuStates.GPT_MENU: UNKNOWN_COMMAND_TEXT,
        MenuStates.VOTING_MENU: UNKNOWN_COMMAND_TEXT
    }

    MENU_KEYBOARDS = {
        MenuStates.MAIN_MENU: get_main_menu(),
        MenuStates.NAVIGATION_MENU: get_navigation_menu(),
        MenuStates.CHALLENGES_MENU: get_challenges_menu(),
        MenuStates.GUIDES_MENU: get_guides_menu(),
        MenuStates.BUST_MENU: get_bust_menu(),
        MenuStates.TEAMS_MENU: get_teams_menu(),
        MenuStates.TRADING_MENU: get_trading_menu(),
        MenuStates.SETTINGS_SUBMENU: get_settings_menu(),
        MenuStates.PROFILE_MENU: get_profile_menu(),
        MenuStates.HELP_SUBMENU: get_help_menu(),
        MenuStates.ACHIEVEMENTS_MENU: get_achievements_menu(),
        MenuStates.STATISTICS_MENU: get_statistics_menu(),
        MenuStates.MY_TEAM_MENU: get_my_team_menu(),
        MenuStates.FEEDBACK_MENU: get_feedback_menu(),
        MenuStates.GPT_MENU: get_gpt_menu(),
        MenuStates.VOTING_MENU: get_voting_menu()
    }

    new_main_text = MENU_TEXTS.get(current_state, MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name or "Користувач"))
    new_main_keyboard = MENU_KEYBOARDS.get(current_state, get_main_menu())

    if current_state == MenuStates.SELECT_LANGUAGE.state or current_state == MenuStates.CHANGE_USERNAME.state:
        # Подсказка пользователю использовать кнопки навигации
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

    if current_state == MenuStates.GPT_MENU.state:
        new_interactive_text = "👾 GPT Menu"
    elif current_state == MenuStates.FEEDBACK_MENU.state:
        new_interactive_text = "💌 Feedback Menu"
    else:
        new_interactive_text = "🏠 Головне меню"

    # Отправляем новое сообщение
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new message: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)
        return

    # Удаляем старое сообщение
    if bot_message_id:
        await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редактируем интерактивное сообщение
    if interactive_message_id:
        await check_and_edit_message(
            bot=bot,
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            new_text=new_interactive_text,
            new_keyboard=get_generic_inline_keyboard(),
            state=state,
            parse_mode=ParseMode.HTML
        )
    else:
        # Если интерактивное сообщение отсутствует, создаем новое
        try:
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
        except Exception as e:
            logger.error(f"Не вдалося надіслати інтерактивне повідомлення: {e}")

    # Обновляем состояние пользователя
    await transition_state(state, new_state)
    await state.update_data(bot_message_id=new_bot_message_id)

# Обработчик для сравнения персонажей (шаг 1: ввод имен героев)
@router.message(MenuStates.COMPARISON_STEP_1)
async def handle_comparison_step_1(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
    """
    Обработчик для приема имен героев для сравнения.
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

    # Сохраняем имена героев во временные данные
    await state.update_data(
        comparison_step=2,
        temp_data={'hero1_name': hero1_name, 'hero2_name': hero2_name}
    )
    await transition_state(state, MenuStates.COMPARISON_STEP_2)

    # Запрашиваем подтверждение или дополнительную информацию, если нужно
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

# Обработчик подтверждения сравнения героев
@router.callback_query(F.data == "compare_confirm_yes" | F.data == "compare_confirm_no")
async def handle_comparison_confirmation(callback: CallbackQuery, state: FSMContext, db: AsyncSession, bot: Bot):
    """
    Обработчик для подтверждения или отмены сравнения героев.
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
            await transition_state(state, MenuStates.CHALLENGES_MENU)
            return

        # Получение статистики героев из базы данных
        # Здесь необходимо реализовать функцию для получения реальной статистики героев
        # Для демонстрации используем фиктивные данные
        hero1_stats = {'kills': 50, 'deaths': 30, 'assists': 100}
        hero2_stats = {'kills': 70, 'deaths': 40, 'assists': 120}

        # Генерация графика сравнения
        try:
            comparison_graph_bytes = create_comparison_graph(hero1_stats, hero2_stats, hero1_name, hero2_name)
        except Exception as e:
            logger.error(f"Не вдалося згенерувати графік порівняння: {e}")
            await handle_error(bot, chat_id=callback.message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)
            await transition_state(state, MenuStates.CHALLENGES_MENU)
            return

        # Отправка графика
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

        # Очистка временных данных и возвращение в меню Challenges
        await state.update_data(comparison_step=None, temp_data={})
        await transition_state(state, MenuStates.CHALLENGES_MENU)
    elif data == "compare_confirm_no":
        response_text = "❌ Порівняння скасовано."
        try:
            await bot.send_message(chat_id=callback.message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про скасування порівняння: {e}")
        await transition_state(state, MenuStates.CHALLENGES_MENU)
    else:
        logger.warning(f"Некоректні дані для порівняння: {data}")
        await bot.answer_callback_query(callback.id, text="Некоректна дія.", show_alert=True)

    await callback.answer()

# Обработчик для приема поиска героя
@router.message(MenuStates.SEARCH_HERO)
async def handle_search_hero(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    """
    Обработчик для приема имени героя для поиска.
    """
    hero_name = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} шукає героя: {hero_name}")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Добавьте логику поиска героя
    # Например, проверка существования героя, отправка информации и т.д.
    # Пока что отправим сообщение о получении запроса

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

    # Возвращаемся в меню Heroes
    await transition_state(state, MenuStates.HEROES_MENU)

# Обработчик для приема темы предложения
@router.message(MenuStates.SEARCH_TOPIC)
async def handle_search_topic(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    """
    Обработчик для приема темы предложения.
    """
    topic = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"Користувач {user_id} пропонує тему: {topic}")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Добавьте логику обработки предложения темы
    # Например, сохранение в базу данных или отправка администратору
    # Пока что отправим сообщение о получении запроса

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

    # Возвращаемся в меню Feedback
    await transition_state(state, MenuStates.FEEDBACK_MENU)

# Обработчик для приема обратной связи
@router.message(MenuStates.FEEDBACK_MENU)
async def handle_feedback(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    """
    Обработчик для приема обратной связи от пользователя.
    """
    feedback = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"Користувач {user_id} залишив зворотний зв'язок: {feedback}")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    if feedback:
        # Сохранение обратной связи в базу данных
        # Пример:
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
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)

    # Возвращаемся в меню Profile
    await transition_state(state, MenuStates.PROFILE_MENU)

# Обработчик для приема отчета об ошибке
@router.message(MenuStates.REPORT_BUG)
async def handle_report_bug(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    """
    Обработчик для приема отчета об ошибке от пользователя.
    """
    bug_report = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"Користувач {user_id} повідомив про помилку: {bug_report}")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    if bug_report:
        # Сохранение отчета об ошибке в базу данных или отправка администратору
        # Пример:
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
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)

    # Возвращаемся в меню Feedback
    await transition_state(state, MenuStates.FEEDBACK_MENU)

# Обработчик кнопки "GPT"
@router.message(F.text == MenuButton.GPT.value, MenuStates.MAIN_MENU)
async def handle_gpt(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    logger.info(f"User {message.from_user.id} selected GPT")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Получаем текущие данные состояния
    is_valid, data = await verify_state_data(state)
    if not is_valid:
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Отправляем новое сообщение с меню GPT
    try:
        gpt_message = await bot.send_message(
            chat_id=message.chat.id,
            text=GPT_TEXT,
            reply_markup=get_gpt_menu()
        )
        new_bot_message_id = gpt_message.message_id
    except Exception as e:
        logger.error(f"Failed to send GPT menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        return

    # Удаляем предыдущее сообщение
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Обновляем интерактивный экран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text="👾 GPT Menu",
        keyboard=get_generic_inline_keyboard()
    )

    # Обновление состояния
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, MenuStates.GPT_MENU)

# Обработчик меню "GPT Menu"
@router.message(MenuStates.GPT_MENU)
async def handle_gpt_menu_buttons(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in GPT Menu")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        try:
            error_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(bot_message_id=error_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = get_gpt_menu()
    new_interactive_text = "👾 GPT Menu"
    new_state = MenuStates.GPT_MENU

    if user_choice == MenuButton.CHAT.value:
        new_main_text = "🤖 GPT Chat ще в розробці."
        # Можно установить новый статус, например, Chatting
    elif user_choice == MenuButton.ASSIST.value:
        new_main_text = "🤖 GPT Assist ще в розробці."
        # Можно установить новый статус, например, Assisting
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Головне меню"
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Оберіть розділ у головному меню"
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_gpt_menu()

    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new GPT menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        return

    # Удаляем предыдущее сообщение
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Обновляем интерактивный экран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        keyboard=get_generic_inline_keyboard()
    )

    # Обновление состояния
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обработчик для генерации графика сравнения (пример)
@router.message(MenuStates.GENERATE_COMPARISON_GRAPH)
async def generate_comparison_graph_handler(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    # Предположим, что это шаг 3 в процессе сравнения
    comparison_data = await state.get_data()
    hero1 = comparison_data.get('hero1_name')
    hero2 = comparison_data.get('hero2_name')

    if not hero1 or not hero2:
        response_text = "❌ Дані для порівняння відсутні. Спробуйте ще раз."
        try:
            await bot.send_message(chat_id=message.chat.id, text=response_text, reply_markup=get_generic_inline_keyboard())
        except Exception as e:
            logger.error(f"Failed to send missing data message: {e}")
        await transition_state(state, MenuStates.HEROES_MENU)
        return

    # Реализуйте получение статистики героев
    # hero1_stats = await get_hero_stats(db, hero1)
    # hero2_stats = await get_hero_stats(db, hero2)

    # Для демонстрации используем фиктивные данные
    hero1_stats = {'kills': 50, 'deaths': 30, 'assists': 100}
    hero2_stats = {'kills': 70, 'deaths': 40, 'assists': 120}

    try:
        comparison_graph_bytes = create_comparison_graph(hero1_stats, hero2_stats, hero1, hero2)
    except Exception as e:
        logger.error(f"Failed to create comparison graph: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)
        await transition_state(state, MenuStates.HEROES_MENU)
        return

    try:
        await bot.send_photo(
            chat_id=message.chat.id,
            photo=io.BytesIO(comparison_graph_bytes),
            caption=f"⚔️ Порівняння: {hero1} vs {hero2}",
            reply_markup=get_generic_inline_keyboard()
        )
        logger.info(f"Sent comparison graph for {hero1} vs {hero2} to user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Failed to send comparison graph: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)

    # Очистка временных данных и возвращение в меню Heroes
    await state.update_data(comparison_step=None, temp_data={})
    await transition_state(state, MenuStates.HEROES_MENU)

# Обработчик неизвестных сообщений (дополнение)
@router.message()
async def handle_unknown(message: Message, state: FSMContext, bot: Bot):
    """Обработчик неизвестных команд или текстов"""
    await unknown_command(message, state, bot)

# Функция для настройки обработчиков
def setup_handlers(dp: Dispatcher):
    """
    Функция для настройки обработчиков в Dispatcher.
    """
    dp.include_router(router)
    # Если у вас есть другие роутеры, включите их здесь, например:
    # dp.include_router(profile_router)