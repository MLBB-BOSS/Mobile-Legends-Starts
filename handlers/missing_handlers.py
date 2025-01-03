import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from typing import Optional
from datetime import datetime

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
    STATISTICS_TEXT, ACHIEVEMENTS_TEXT, FEEDBACK_TEXT, GPT_TEXT
)
from handlers.base import safe_delete_message, check_and_edit_message

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
            reply_markup=keyboard or get_generic_inline_keyboard()
        )
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
        MenuStates.HELP_SUBMENU: MenuStates.HELP_MENU
    }
    
    next_state = BACK_TRANSITIONS.get(current_state, MenuStates.MAIN_MENU)
    
    try:
        # Видалення повідомлення користувача
        await safe_delete_message(bot, message.chat.id, message.message_id)
        
        # Отримання даних стану
        is_valid, data = await verify_state_data(state)
        if not is_valid:
            await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await transition_state(state, MenuStates.MAIN_MENU)
            return

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
            MenuStates.SETTINGS_SUBMENU: "⚙️ Settings Submenu"
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
            MenuStates.SETTINGS_SUBMENU: get_settings_menu()
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
async def handle_challenges(message: Message, state: FSMContext, bot: Bot):
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
async def handle_challenges_menu_buttons(message: Message, state: FSMContext, bot: Bot):
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
async def handle_guides(message: Message, state: FSMContext, bot: Bot):
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
async def handle_guides_menu_buttons(message: Message, state: FSMContext, bot: Bot):
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

    # Видаляємо попереднє повідом