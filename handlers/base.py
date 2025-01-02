import logging
from aiogram import Router, F, Bot, Dispatcher
from aiogram.types import (
    Message, ReplyKeyboardRemove, InlineKeyboardMarkup,
    InlineKeyboardButton, CallbackQuery, ParseMode
)
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
    get_gpt_menu
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
    MLS_BUTTON_RESPONSE_TEXT, UNHANDLED_INLINE_BUTTON_TEXT
)
from handlers.graph_utils import create_comparison_graph  # Assuming this exists
# from models.feedback import Feedback  # Uncomment when models are implemented
# from models.bug_report import BugReport  # Uncomment when models are implemented

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

# Додаткові константи для навігаційного меню
NAVIGATION_MENU_TEXT = """
🧭 Навігаційне меню

Оберіть розділ для переходу:
- Challenges - випробування та досягнення
- Guides - корисні гайди та поради
- Bust - підвищення рівня
- Teams - управління командами
- Trading - торгівля предметами
"""

NAVIGATION_INTERACTIVE_TEXT = """
📱 Навігація по боту

Використовуйте кнопки нижче для переходу між розділами.
Поточний розділ: Навігація
"""

# Допоміжні функції
async def safe_delete_message(bot: Bot, chat_id: int, message_id: int):
    """Безпечне видалення повідомлення"""
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
    """Перевірка та редагування повідомлення, якщо зміни відбулися"""
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
    """Обробка помилок шляхом надсилання повідомлення користувачу"""
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
    """Безпечне оновлення інтерактивного екрану"""
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
    """Перевірка наявності необхідних даних у стані"""
    data = await state.get_data()
    required_fields = ['bot_message_id', 'interactive_message_id']
    
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        logger.error(f"Missing required state fields: {missing_fields}")
        return False, data
        
    return True, data

# Допоміжна функція для переходу між станами
async def transition_state(state: FSMContext, new_state: MenuStates):
    await state.set_state(new_state)

# Обробник команди /start
@router.message(commands=["start"])
async def handle_start(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    """Обробник команди /start"""
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name or "Користувач"
    logger.info(f"User {user_id} started the bot.")
    
    # Реєстрація користувача в базі даних, якщо необхідно
    # Перевірка, чи існує користувач
    # Якщо не існує, створити новий запис
    # Приклад:
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
            text=MAIN_MENU_DESCRIPTION,  # Define this in texts.py
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

# Обробник команди /example (як приклад)
@router.message(commands=["example"])
async def handle_example(message: Message, state: FSMContext, bot: Bot):
    """Приклад обробника команди"""
    logger.info(f"User {message.from_user.id} invoked /example command.")
    await safe_delete_message(bot, message.chat.id, message.message_id)
    
    try:
        example_message = await bot.send_message(
            chat_id=message.chat.id,
            text="Це приклад відповіді на команду /example.",
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(bot_message_id=example_message.message_id)
        await transition_state(state, MenuStates.EXAMPLE_STATE)  # Define EXAMPLE_STATE if needed
    except Exception as e:
        logger.error(f"Failed to send example message: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, logger)

# Обробник натискання звичайних кнопок у меню Навігація
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

# 1. Обробник кнопки "Back" для всіх меню
@router.message(F.text == MenuButton.BACK.value)
async def handle_back_button(message: Message, state: FSMContext, bot: Bot):
    """Універсальний обробник кнопки "Back" для повернення до попереднього меню"""
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
        MenuStates.HELP_MENU: MenuStates.PROFILE_MENU,
        MenuStates.GPT_MENU: MenuStates.PROFILE_MENU,
        MenuStates.HELP_SUBMENU: MenuStates.HELP_MENU,
        MenuStates.SEARCH_HERO: MenuStates.HEROES_MENU,
        MenuStates.SEARCH_TOPIC: MenuStates.FEEDBACK_MENU,
        MenuStates.CHANGE_USERNAME: MenuStates.SETTINGS_SUBMENU
    }
    
    next_state = BACK_TRANSITIONS.get(current_state, MenuStates.MAIN_MENU)
    
    try:
        # Видалення повідомлення користувача
        await safe_delete_message(bot, message.chat.id, message.message_id)
        
        # Отримання даних стану
        data = await state.get_data()
        old_message_id = data.get('bot_message_id')
        interactive_message_id = data.get('interactive_message_id')
        
        # Видалення старого повідомлення
        if old_message_id:
            await safe_delete_message(bot, message.chat.id, old_message_id)
        
        # Визначення тексту та клавіатури для наступного стану
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
            MenuStates.NAVIGATION_MENU: NAVIGATION_MENU_TEXT
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
            MenuStates.NAVIGATION_MENU: get_navigation_menu()
        }
        
        new_text = MENU_TEXTS.get(next_state, "🏠 Головне меню")
        new_keyboard = MENU_KEYBOARDS.get(next_state, get_main_menu())
        
        # Відправка нового повідомлення
        new_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_text,
            reply_markup=new_keyboard
        )
        
        # Оновлення інтерактивного екрану, якщо існує
        if interactive_message_id:
            await update_interactive_screen(
                bot=bot,
                chat_id=message.chat.id,
                message_id=interactive_message_id,
                text=f"Поточний розділ: {new_text}",
                keyboard=get_generic_inline_keyboard()
            )
        
        # Оновлення стану
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

# 2. Обробники для кнопок та їхніх підменю

# Обробник для кнопки "Challenges"
@router.message(F.text == MenuButton.CHALLENGES.value, MenuStates.MAIN_MENU)
async def handle_challenges(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    logger.info(f"User {message.from_user.id} selected Challenges")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Отримуємо поточні дані стану
    is_valid, data = await verify_state_data(state)
    if not is_valid:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await transition_state(state, MenuStates.MAIN_MENU)
        return

    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Відправляємо нове повідомлення з меню Challenges
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

    # Видаляємо попереднє повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Оновлюємо інтерактивний екран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text="🎯 Challenges Menu",
        keyboard=get_generic_inline_keyboard()
    )

    # Оновлення стану
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, MenuStates.CHALLENGES_MENU)

# Обробник для меню "Challenges Menu"
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

    # Видаляємо попереднє повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Оновлюємо інтерактивний екран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        keyboard=get_generic_inline_keyboard()
    )

    # Оновлення стану
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обробник для кнопки "Guides"
@router.message(F.text == MenuButton.GUIDES.value, MenuStates.MAIN_MENU)
async def handle_guides(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    logger.info(f"User {message.from_user.id} selected Guides")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Отримуємо поточні дані стану
    is_valid, data = await verify_state_data(state)
    if not is_valid:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await transition_state(state, MenuStates.MAIN_MENU)
        return

    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Відправляємо нове повідомлення з меню Guides
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

    # Видаляємо попереднє повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Оновлюємо інтерактивний екран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text="📚 Guides Menu",
        keyboard=get_generic_inline_keyboard()
    )

    # Оновлення стану
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, MenuStates.GUIDES_MENU)

# Обробник для меню "Guides Menu"
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

    # Видаляємо попереднє повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Оновлюємо інтерактивний екран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        keyboard=get_generic_inline_keyboard()
    )

    # Оновлення стану
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обробник для кнопки "Bust"
@router.message(F.text == MenuButton.BUST.value, MenuStates.MAIN_MENU)
async def handle_bust(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    logger.info(f"User {message.from_user.id} selected Bust")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Отримуємо поточні дані стану
    is_valid, data = await verify_state_data(state)
    if not is_valid:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await transition_state(state, MenuStates.MAIN_MENU)
        return

    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Відправляємо нове повідомлення з меню Bust
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

    # Видаляємо попереднє повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Оновлюємо інтерактивний екран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text="💪 Bust Menu",
        keyboard=get_generic_inline_keyboard()
    )

    # Оновлення стану
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, MenuStates.BUST_MENU)

# Обробник для меню "Bust Menu"
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

    # Видаляємо попереднє повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Оновлюємо інтерактивний екран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        keyboard=get_generic_inline_keyboard()
    )

    # Оновлення стану
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обробник для кнопки "Teams"
@router.message(F.text == MenuButton.TEAMS.value, MenuStates.MAIN_MENU)
async def handle_teams(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    logger.info(f"User {message.from_user.id} selected Teams")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Отримуємо поточні дані стану
    is_valid, data = await verify_state_data(state)
    if not is_valid:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await transition_state(state, MenuStates.MAIN_MENU)
        return

    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Відправляємо нове повідомлення з меню Teams
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

    # Видаляємо попереднє повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Оновлюємо інтерактивний екран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text="👥 Teams Menu",
        keyboard=get_generic_inline_keyboard()
    )

    # Оновлення стану
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, MenuStates.TEAMS_MENU)

# Обробник для меню "Teams Menu"
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

    # Видаляємо попереднє повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Оновлюємо інтерактивний екран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        keyboard=get_generic_inline_keyboard()
    )

    # Оновлення стану
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обробник натискання звичайних кнопок у меню Trading
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
        # Тут можна додати логіку відображення торгівель
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

    # Видаляємо попереднє повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Оновлюємо інтерактивний екран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        keyboard=get_generic_inline_keyboard()
    )

    # Оновлення стану
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обробник натискання звичайних кнопок у меню Settings Submenu
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

    # Видаляємо попереднє повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Оновлюємо інтерактивний екран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        keyboard=get_generic_inline_keyboard()
    )

    # Оновлення стану
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обробник для вибору мови
@router.message(MenuStates.SELECT_LANGUAGE)
async def handle_select_language(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    selected_language = message.text
    logger.info(f"User {message.from_user.id} selected language: {selected_language}")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Реалізуйте логіку зміни мови інтерфейсу, наприклад, оновлення в базі даних
    # Приклад:
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

    # Повертаємося до меню Settings Submenu
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

# Обробник для зміни імені користувача
@router.message(MenuStates.CHANGE_USERNAME)
async def handle_change_username(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    current_state = await state.get_state()
    if current_state != MenuStates.CHANGE_USERNAME.state:
        return

    new_username = message.text.strip()
    logger.info(f"User {message.from_user.id} is changing username to: {new_username}")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Реалізуйте логіку зміни імені користувача, наприклад, оновлення в базі даних
    # Приклад:
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

    # Повертаємося до меню Settings Submenu
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

# Обробник для кнопки "Help"
@router.message(F.text == MenuButton.HELP.value, MenuStates.MAIN_MENU)
async def handle_help(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    logger.info(f"User {message.from_user.id} selected Help")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Отримуємо поточні дані стану
    is_valid, data = await verify_state_data(state)
    if not is_valid:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await transition_state(state, MenuStates.MAIN_MENU)
        return

    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Відправляємо нове повідомлення з меню Help
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

    # Видаляємо попереднє повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Оновлюємо інтерактивний екран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text="❓ Help Menu",
        keyboard=get_generic_inline_keyboard()
    )

    # Оновлення стану
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, MenuStates.HELP_SUBMENU)

# Обробник для меню "Help Submenu"
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
        new_main_text = INSTRUCTIONS_TEXT  # Додайте відповідний текст у `texts.py`
    elif user_choice == MenuButton.FAQ.value:
        new_main_text = FAQ_TEXT  # Додайте відповідний текст у `texts.py`
    elif user_choice == MenuButton.HELP_SUPPORT.value:
        new_main_text = HELP_SUPPORT_TEXT  # Додайте відповідний текст у `texts.py`
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

    # Видаляємо попереднє повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Оновлюємо інтерактивний екран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        keyboard=get_generic_inline_keyboard()
    )

    # Оновлення стану
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обробник для кнопки "My Team"
@router.message(F.text == MenuButton.MY_TEAM.value, MenuStates.MAIN_MENU)
async def handle_my_team(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    logger.info(f"User {message.from_user.id} selected My Team")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Отримуємо поточні дані стану
    is_valid, data = await verify_state_data(state)
    if not is_valid:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await transition_state(state, MenuStates.MAIN_MENU)
        return

    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Відправляємо нове повідомлення з меню My Team
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

    # Видаляємо попереднє повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Оновлюємо інтерактивний екран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text="🪪 My Team Menu",
        keyboard=get_generic_inline_keyboard()
    )

    # Оновлення стану
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, MenuStates.MY_TEAM_MENU)

# Обробник для меню "My Team Menu"
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

    # Видаляємо попереднє повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Оновлюємо інтерактивний екран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        keyboard=get_generic_inline_keyboard()
    )

    # Оновлення стану
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обробник для кнопки "Advanced Techniques"
@router.message(F.text == MenuButton.ADVANCED_TECHNIQUES.value)
async def handle_advanced_techniques(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Advanced Techniques")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Тут можна додати логіку відображення Advanced Techniques
    # Наприклад, відправити інформацію або перейти до підменю
    try:
        advanced_techniques_message = await bot.send_message(
            chat_id=message.chat.id,
            text=ADVANCED_TECHNIQUES_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(bot_message_id=advanced_techniques_message.message_id)
        await increment_step(state)
        # Якщо потрібно, встановіть новий стан або залиште цей як кінцевий пункт
    except Exception as e:
        logger.error(f"Failed to send Advanced Techniques info: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Обробник для кнопки "Instructions"
@router.message(F.text == MenuButton.INSTRUCTIONS.value)
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

# Обробник для кнопки "FAQ"
@router.message(F.text == MenuButton.FAQ.value)
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

# Обробник для кнопки "Help Support"
@router.message(F.text == MenuButton.HELP_SUPPORT.value)
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

# Обробник для кнопки "Update ID"
@router.message(F.text == MenuButton.UPDATE_ID.value)
async def handle_update_id(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    logger.info(f"User {message.from_user.id} selected Update ID")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Реалізуйте логіку оновлення ID, наприклад, оновлення в базі даних
    # Приклад:
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
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

    # Повертаємося до меню Settings Submenu
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

# Обробник для кнопки "Notifications"
@router.message(F.text == MenuButton.NOTIFICATIONS.value)
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

    # Повертаємося до меню Settings Submenu
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

# Обробник для кнопки "Language" в меню "Settings Submenu"
@router.message(F.text == MenuButton.LANGUAGE.value, MenuStates.SETTINGS_SUBMENU)
async def handle_language_selection_menu(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    """Відкриття меню вибору мови"""
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

# Обробник для кнопки "Help" в різних контекстах (уникнення дублювання)
@router.message(F.text == MenuButton.HELP.value)
async def handle_help_general(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    """Обробник для кнопки Help у різних меню"""
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

# Обробник для кнопки "Profile"
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

# Обробник для меню "Profile Menu"
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
        new_main_text = VIEW_PROFILE_TEXT  # Додайте відповідний текст у `texts.py`
    elif user_choice == MenuButton.EDIT_PROFILE.value:
        new_main_text = EDIT_PROFILE_TEXT  # Додайте відповідний текст у `texts.py`
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

    # Видаляємо попереднє повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Оновлюємо інтерактивний екран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        keyboard=get_generic_inline_keyboard()
    )

    # Оновлення стану
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обробник для інлайн-кнопок
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
            new_interactive_text = MAIN_MENU_DESCRIPTION  # Define in texts.py
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

# Обробник невідомих повідомлень
@router.message()
async def unknown_command(message: Message, state: FSMContext, bot: Bot):
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
    elif current_state == MenuStates.CHALLENGES_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_challenges_menu()
        new_interactive_text = "Challenges Menu"
        new_state = MenuStates.CHALLENGES_MENU
    elif current_state == MenuStates.GUIDES_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_guides_menu()
        new_interactive_text = "Guides Menu"
        new_state = MenuStates.GUIDES_MENU
    elif current_state == MenuStates.BUST_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_bust_menu()
        new_interactive_text = "Bust Menu"
        new_state = MenuStates.BUST_MENU
    elif current_state == MenuStates.TEAMS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_teams_menu()
        new_interactive_text = "Teams Menu"
        new_state = MenuStates.TEAMS_MENU
    elif current_state == MenuStates.TRADING_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_trading_menu()
        new_interactive_text = "Trading Menu"
        new_state = MenuStates.TRADING_MENU
    elif current_state == MenuStates.SETTINGS_SUBMENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_settings_menu()
        new_interactive_text = "Settings Submenu"
        new_state = MenuStates.SETTINGS_SUBMENU
    elif current_state == MenuStates.SELECT_LANGUAGE.state:
        # Підказка користувачу використовувати кнопки навігації
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
    elif current_state == MenuStates.CHANGE_USERNAME.state:
        # Підказка користувачу використовувати кнопки навігації
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
    elif current_state == MenuStates.PROFILE_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "My Profile Menu"
        new_state = MenuStates.PROFILE_MENU
    elif current_state == MenuStates.HELP_SUBMENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_help_menu()
        new_interactive_text = "Help Menu"
        new_state = MenuStates.HELP_SUBMENU
    elif current_state == MenuStates.ACHIEVEMENTS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_achievements_menu()
        new_interactive_text = "Achievements Menu"
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif current_state == MenuStates.STATISTICS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_statistics_menu()
        new_interactive_text = "Statistics Menu"
        new_state = MenuStates.STATISTICS_MENU
    elif current_state == MenuStates.MY_TEAM_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_my_team_menu()
        new_interactive_text = "My Team Menu"
        new_state = MenuStates.MY_TEAM_MENU
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
    elif current_state == MenuStates.GPT_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_gpt_menu()
        new_interactive_text = "GPT Menu"
        new_state = MenuStates.GPT_MENU
    elif current_state == MenuStates.VOTING_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_voting_menu()
        new_interactive_text = "Voting Menu"
        new_state = MenuStates.VOTING_MENU
    else:
        user_first_name = message.from_user.first_name or "Користувач"
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION  # Define in texts.py
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
        logger.error(f"Failed to send new message: {e}")
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

# Обробник для порівняння персонажів (крок 1: введення імен героїв)
@router.message(MenuStates.COMPARISON_STEP_1)
async def handle_comparison_step_1(message: Message, state: FSMContext, db: AsyncSession, bot: Bot):
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

# Обробник підтвердження порівняння героїв
@router.callback_query(F.data.startswith("compare_confirm_"))
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
            await transition_state(state, MenuStates.CHALLENGES_MENU)
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
            await transition_state(state, MenuStates.CHALLENGES_MENU)
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

        # Очистка тимчасових даних та повернення до меню Challenges
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

# Обробник для прийому пошуку героя
@router.message(MenuStates.SEARCH_HERO)
async def handle_search_hero(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
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

    # Повертаємо користувача до меню Heroes
    await transition_state(state, MenuStates.HEROES_MENU)

# Обробник для прийому теми пропозиції
@router.message(MenuStates.SEARCH_TOPIC)
async def handle_search_topic(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    """
    Обробчик для прийому теми пропозиції.
    """
    topic = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"Користувач {user_id} пропонує тему: {topic}")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Тут додайте логіку обробки пропозиції теми
    # Наприклад, збереження в базі даних або відправка адміністратору
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

    # Повертаємо користувача до меню Feedback
    await transition_state(state, MenuStates.FEEDBACK_MENU)

# Обробник для прийому зворотного зв'язку
@router.message(MenuStates.FEEDBACK_MENU)
async def handle_feedback(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    """
    Обробчик для прийому зворотного зв'язку від користувача.
    """
    feedback = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"Користувач {user_id} залишив зворотний зв'язок: {feedback}")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    if feedback:
        # Збереження зворотного зв'язку у базі даних
        # Приклад:
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

    # Повертаємо користувача до головного меню або попереднього меню
    await transition_state(state, MenuStates.PROFILE_MENU)

# Обробник для прийому звіту про помилку
@router.message(MenuStates.REPORT_BUG)
async def handle_report_bug(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    """
    Обробчик для прийому звіту про помилку від користувача.
    """
    bug_report = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"Користувач {user_id} повідомив про помилку: {bug_report}")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    if bug_report:
        # Збереження звіту про помилку у базі даних або надсилання адміністратору
        # Приклад:
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

    # Повертаємо користувача до Feedback Menu
    await transition_state(state, MenuStates.FEEDBACK_MENU)

# Обробник для кнопки "GPT"
@router.message(F.text == MenuButton.GPT.value, MenuStates.MAIN_MENU)
async def handle_gpt(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    logger.info(f"User {message.from_user.id} selected GPT")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Отримуємо поточні дані стану
    is_valid, data = await verify_state_data(state)
    if not is_valid:
        await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await transition_state(state, MenuStates.MAIN_MENU)
        return

    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Відправляємо нове повідомлення з меню GPT
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

    # Видаляємо попереднє повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Оновлюємо інтерактивний екран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text="👾 GPT Menu",
        keyboard=get_generic_inline_keyboard()
    )

    # Оновлення стану
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, MenuStates.GPT_MENU)

# Обробник для меню "GPT Menu"
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
        # Можна встановити новий стан, наприклад, Chatting
    elif user_choice == MenuButton.ASSIST.value:
        new_main_text = "🤖 GPT Assist ще в розробці."
        # Можна встановити новий стан, наприклад, Assisting
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

    # Видаляємо попереднє повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Оновлюємо інтерактивний екран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        keyboard=get_generic_inline_keyboard()
    )

    # Оновлення стану
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обробник для натискання звичайних кнопок у підрозділі "Персонажі"
@router.message(MenuStates.HEROES_MENU)
async def handle_heroes_menu_buttons(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
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
            # Зберігаємо ID повідомлення бота
            await state.update_data(bot_message_id=main_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Не вдалося надіслати повідомлення про помилку головного меню: {e}")
            await handle_error(bot, chat_id=message.chat.id, error_message=MAIN_MENU_ERROR_TEXT, logger=logger)
        return

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state: Optional[MenuStates] = None

    hero_classes = list(MenuButton.__members__.values())  # Adjust as per actual mapping

    if user_choice in hero_classes:
        hero_class = MenuButton.__dict__.get(user_choice, 'Танк')  # Adjust logic as needed
        new_main_text = f"HERO_CLASS_MENU_TEXT.format(hero_class=hero_class)"  # Adjust accordingly
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = f"HERO_CLASS_INTERACTIVE_TEXT.format(hero_class=hero_class)"
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
            comparison_keyboard = ReplyKeyboardRemove()
            comparison_message = await bot.send_message(
                chat_id=message.chat.id,
                text=comparison_prompt,
                reply_markup=comparison_keyboard
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
        new_main_keyboard = get_heroes_menu()
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
        logger.error(f"Failed to send new Heroes menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        return

    # Видаляємо попереднє повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Оновлюємо інтерактивний екран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        keyboard=get_generic_inline_keyboard()
    )

    # Оновлюємо стан користувача
    if new_state:
        await transition_state(state, new_state)
    await state.update_data(bot_message_id=new_bot_message_id)

# Обробник для кнопки "GPT Assist" (додатковий приклад)
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
        # Можна встановити новий стан, наприклад, Chatting
    elif user_choice == MenuButton.ASSIST.value:
        new_main_text = "🤖 GPT Assist ще в розробці."
        # Можна встановити новий стан, наприклад, Assisting
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

    # Видаляємо попереднє повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Оновлюємо інтерактивний екран
    await update_interactive_screen(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        keyboard=get_generic_inline_keyboard()
    )

    # Оновлення стану
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обробчик для генерації графіку порівняння (приклад)
@router.message(MenuStates.GENERATE_COMPARISON_GRAPH)
async def generate_comparison_graph_handler(message: Message, state: FSMContext, bot: Bot, db: AsyncSession):
    # Припустимо, що це крок 3 у процесі порівняння
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

    # Реалізуйте отримання статистики героїв
    # hero1_stats = await get_hero_stats(db, hero1)
    # hero2_stats = await get_hero_stats(db, hero2)

    # Для демонстрації використаємо фіктивні дані
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

    # Очистка тимчасових даних та повернення до меню Персонажі
    await state.update_data(comparison_step=None, temp_data={})
    await transition_state(state, MenuStates.HEROES_MENU)

# Обробчик для невідомих повідомлень (доповнення)
@router.message()
async def handle_unknown(message: Message, state: FSMContext, bot: Bot):
    """Обробник невідомих команд або текстів"""
    await unknown_command(message, state, bot)

# Функція для налаштування обробників
def setup_handlers(dp: Dispatcher):
    """
    Функція для налаштування обробників у Dispatcher.
    """
    dp.include_router(router)
    # Якщо у вас є інші роутери, включіть їх тут, наприклад:
    # dp.include_router(profile_router)