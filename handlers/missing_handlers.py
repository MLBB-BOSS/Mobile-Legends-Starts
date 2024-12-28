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
async def handle_bust(message: Message, state: FSMContext, bot: Bot):
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
async def handle_bust_menu_buttons(message: Message, state: FSMContext, bot: Bot):
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
async def handle_teams(message: Message, state: FSMContext, bot: Bot):
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
async def handle_teams_menu_buttons(message: Message, state: FSMContext, bot: Bot):
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

# Обробник для кнопки "Trading"
@router.message(F.text == MenuButton.TRADING.value, MenuStates.MAIN_MENU)
async def handle_trading(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Trading")
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

    # Відправляємо нове повідомлення з меню Trading
    try:
        trading_message = await bot.send_message(
            chat_id=message.chat.id,
            text=TRADING_TEXT,
            reply_markup=get_trading_menu()
        )
        new_bot_message_id = trading_message.message_id
    except Exception as e:
        logger.error(f"Failed to send Trading menu: {e}")
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
        text="💼 Trading Menu",
        keyboard=get_generic_inline_keyboard()
    )

    # Оновлення стану
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, MenuStates.TRADING_MENU)

# Обробник для меню "Trading Menu"
@router.message(MenuStates.TRADING_MENU)
async def handle_trading_menu_buttons(message: Message, state: FSMContext, bot: Bot):
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

# Обробник для кнопки "Settings"
@router.message(F.text == MenuButton.SETTINGS.value, MenuStates.MAIN_MENU)
async def handle_settings(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Settings")
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

    # Відправляємо нове повідомлення з меню Settings
    try:
        settings_message = await bot.send_message(
            chat_id=message.chat.id,
            text="⚙️ Settings",
            reply_markup=get_settings_menu()
        )
        new_bot_message_id = settings_message.message_id
    except Exception as e:
        logger.error(f"Failed to send Settings menu: {e}")
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
        text="⚙️ Settings Menu",
        keyboard=get_generic_inline_keyboard()
    )

    # Оновлення стану
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, MenuStates.SETTINGS_SUBMENU)

# Обробник для меню "Settings Submenu"
@router.message(MenuStates.SETTINGS_SUBMENU)
async def handle_settings_menu_buttons(message: Message, state: FSMContext, bot: Bot):
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
async def handle_select_language(message: Message, state: FSMContext, bot: Bot):
    selected_language = message.text
    logger.info(f"User {message.from_user.id} selected language: {selected_language}")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Тут реалізуйте логіку зміни мови інтерфейсу, наприклад, оновлення в базі даних
    # Для демонстрації відправимо підтвердження:
    try:
        response_text = f"Інтерфейс змінено на {selected_language}."
        await bot.send_message(
            chat_id=message.chat.id,
            text=response_text,
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Failed to send language change confirmation: {e}")
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
        logger.error(f"Failed to send Settings menu after language change: {e}")

# Обробник для зміни імені користувача
@router.message(MenuStates.CHANGE_USERNAME)
async def handle_change_username(message: Message, state: FSMContext, bot: Bot):
    current_state = await state.get_state()
    if current_state != MenuStates.CHANGE_USERNAME.state:
        return

    new_username = message.text.strip()
    logger.info(f"User {message.from_user.id} is changing username to: {new_username}")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Тут реалізуйте логіку зміни імені користувача, наприклад, оновлення в базі даних
    # Для демонстрації відправимо підтвердження:
    try:
        response_text = f"Username змінено на {new_username}."
        await bot.send_message(
            chat_id=message.chat.id,
            text=response_text,
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Failed to send username change confirmation: {e}")
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
        logger.error(f"Failed to send Settings menu after changing username: {e}")

# Обробник для кнопки "Help"
@router.message(F.text == MenuButton.HELP.value, MenuStates.MAIN_MENU)
async def handle_help(message: Message, state: FSMContext, bot: Bot):
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
async def handle_help_menu_buttons(message: Message, state: FSMContext, bot: Bot):
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
        new_main_text = INSTRUCTIONS_TEXT
    elif user_choice == MenuButton.FAQ.value:
        new_main_text = FAQ_TEXT
    elif user_choice == MenuButton.HELP_SUPPORT.value:
        new_main_text = HELP_SUPPORT_TEXT
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
async def handle_my_team(message: Message, state: FSMContext, bot: Bot):
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
async def handle_my_team_menu_buttons(message: Message, state: FSMContext, bot: Bot):
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
async def handle_update_id(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Update ID")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Тут реалізуйте логіку оновлення ID, наприклад, оновлення в базі даних
    # Для демонстрації відправимо підтвердження:
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
async def handle_notifications(message: Message, state: FSMContext, bot: Bot):
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
async def handle_language_selection_menu(message: Message, state: FSMContext, bot: Bot):
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

# Обробник для кнопки "Help" в різних контекстах
@router.message(F.text == MenuButton.HELP.value)
async def handle_help_general(message: Message, state: FSMContext, bot: Bot):
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
async def handle_profile(message: Message, state: FSMContext, bot: Bot):
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
async def handle_profile_menu_buttons(message: Message, state: FSMContext, bot: Bot):
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

# Інші обробники можуть бути додані аналогічно нижче

# Не забудьте зареєструвати всі нові обробники в основному файлі запуску бота, якщо це ще не зроблено.