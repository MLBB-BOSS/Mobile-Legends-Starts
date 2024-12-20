# handlers/missing_handlers.py

import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

# Імпортуємо MenuStates та increment_step зі states.py
from states import MenuStates, increment_step

from handlers.base import safe_delete_message, check_and_edit_message
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
    get_profile_menu
)
from texts import (
    MAIN_MENU_ERROR_TEXT, UNKNOWN_COMMAND_TEXT, GENERIC_ERROR_MESSAGE_TEXT,
    CHALLENGES_TEXT, GUIDES_TEXT, BUST_TEXT, TEAMS_TEXT, TRADING_TEXT,
    NEW_GUIDES_TEXT, M6_TEXT, POPULAR_GUIDES_TEXT, BEGINNER_GUIDES_TEXT,
    ADVANCED_TECHNIQUES_TEXT, TEAMPLAY_GUIDES_TEXT,
    LANGUAGE_SELECTION_TEXT, UPDATE_ID_SUCCESS_TEXT, NOTIFICATIONS_SETTINGS_TEXT,
    INSTRUCTIONS_TEXT, FAQ_TEXT, HELP_SUPPORT_TEXT,
    MY_TEAM_TEXT
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

# ... увесь інший код missing_handlers.py без визначення MenuStates та increment_step ...


# Обробник для кнопки "Челенджі"
@router.message(F.text == MenuButton.CHALLENGES.value)
async def handle_challenges(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Challenges")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    try:
        challenges_message = await bot.send_message(
            chat_id=message.chat.id,
            text=CHALLENGES_TEXT,
            reply_markup=get_challenges_menu()
        )
        await state.update_data(bot_message_id=challenges_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.CHALLENGES_MENU)
    except Exception as e:
        logger.error(f"Failed to send Challenges menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Обробник для меню "Челенджі"
@router.message(MenuStates.CHALLENGES_MENU)
async def handle_challenges_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Challenges Menu")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    if not bot_message_id:
        logger.error("bot_message_id not found")
        try:
            error_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(bot_message_id=error_message.message_id)
            await state.set_state(MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = None
    new_state = MenuStates.CHALLENGES_MENU

    if user_choice == "➕ Додати Челендж":
        new_main_text = "Feature to add challenges is under development."
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Main Navigation"
        new_main_keyboard = get_navigation_menu()
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_challenges_menu()

    try:
        if new_main_keyboard:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=new_main_keyboard
            )
            new_bot_message_id = main_message.message_id
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=get_generic_inline_keyboard()
            )
            new_bot_message_id = bot_message_id
    except Exception as e:
        logger.error(f"Failed to send new Challenges menu: {e}")
        return

    await safe_delete_message(bot, message.chat.id, bot_message_id)
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

# Обробник для кнопки "Гайди"
@router.message(F.text == MenuButton.GUIDES.value)
async def handle_guides(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Guides")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    try:
        guides_message = await bot.send_message(
            chat_id=message.chat.id,
            text=GUIDES_TEXT,
            reply_markup=get_guides_menu()
        )
        await state.update_data(bot_message_id=guides_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.GUIDES_MENU)
    except Exception as e:
        logger.error(f"Failed to send Guides menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Обробник для меню "Гайди"
@router.message(MenuStates.GUIDES_MENU)
async def handle_guides_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Guides Menu")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    if not bot_message_id:
        logger.error("bot_message_id not found")
        try:
            error_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(bot_message_id=error_message.message_id)
            await state.set_state(MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = None
    new_state = MenuStates.GUIDES_MENU

    if user_choice == MenuButton.NEW_GUIDES.value:
        new_main_text = NEW_GUIDES_TEXT
    elif user_choice == MenuButton.POPULAR_GUIDES.value:
        new_main_text = POPULAR_GUIDES_TEXT
    elif user_choice == MenuButton.BEGINNER_GUIDES.value:
        new_main_text = BEGINNER_GUIDES_TEXT
    elif user_choice == MenuButton.ADVANCED_TECHNIQUES.value:
        new_main_text = ADVANCED_TECHNIQUES_TEXT
    elif user_choice == MenuButton.TEAMPLAY_GUIDES.value:
        new_main_text = TEAMPLAY_GUIDES_TEXT
    elif user_choice == MenuButton.M6.value:
        new_main_text = M6_TEXT
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Main Navigation"
        new_main_keyboard = get_navigation_menu()
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_guides_menu()

    try:
        if new_main_keyboard:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=new_main_keyboard
            )
            new_bot_message_id = main_message.message_id
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=get_generic_inline_keyboard()
            )
            new_bot_message_id = bot_message_id
    except Exception as e:
        logger.error(f"Failed to send new Guides menu: {e}")
        return

    await safe_delete_message(bot, message.chat.id, bot_message_id)
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

# Обробник для кнопки "Bust"
@router.message(F.text == MenuButton.BUST.value)
async def handle_bust(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Bust")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    try:
        bust_message = await bot.send_message(
            chat_id=message.chat.id,
            text=BUST_TEXT,
            reply_markup=get_bust_menu()
        )
        await state.update_data(bot_message_id=bust_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.BUST_MENU)
    except Exception as e:
        logger.error(f"Failed to send Bust menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Обробник для меню "Bust"
@router.message(MenuStates.BUST_MENU)
async def handle_bust_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Bust Menu")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    if not bot_message_id:
        logger.error("bot_message_id not found")
        try:
            error_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(bot_message_id=error_message.message_id)
            await state.set_state(MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = None
    new_state = MenuStates.BUST_MENU

    if user_choice == "🔥 Підвищити Буст":
        new_main_text = "Feature to increase bust is under development."
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Main Navigation"
        new_main_keyboard = get_navigation_menu()
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_bust_menu()

    try:
        if new_main_keyboard:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=new_main_keyboard
            )
            new_bot_message_id = main_message.message_id
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=get_generic_inline_keyboard()
            )
            new_bot_message_id = bot_message_id
    except Exception as e:
        logger.error(f"Failed to send new Bust menu: {e}")
        return

    await safe_delete_message(bot, message.chat.id, bot_message_id)
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

# Обробник для кнопки "Teams"
@router.message(F.text == MenuButton.TEAMS.value)
async def handle_teams(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Teams")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    try:
        teams_message = await bot.send_message(
            chat_id=message.chat.id,
            text=TEAMS_TEXT,
            reply_markup=get_teams_menu()
        )
        await state.update_data(bot_message_id=teams_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.TEAMS_MENU)
    except Exception as e:
        logger.error(f"Failed to send Teams menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Обробник для меню "Teams"
@router.message(MenuStates.TEAMS_MENU)
async def handle_teams_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Teams Menu")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    if not bot_message_id:
        logger.error("bot_message_id not found")
        try:
            error_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(bot_message_id=error_message.message_id)
            await state.set_state(MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = None
    new_state = MenuStates.TEAMS_MENU

    if user_choice == MenuButton.CREATE_TEAM.value:
        new_main_text = "Feature to create a team is under development."
    elif user_choice == MenuButton.VIEW_TEAMS.value:
        new_main_text = VIEW_TRADES_TEXT  # Або VIEW_TEAMS_TEXT, якщо потрібен інший текст
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Main Navigation"
        new_main_keyboard = get_navigation_menu()
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_teams_menu()

    try:
        if new_main_keyboard:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=new_main_keyboard
            )
            new_bot_message_id = main_message.message_id
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=get_generic_inline_keyboard()
            )
            new_bot_message_id = bot_message_id
    except Exception as e:
        logger.error(f"Failed to send new Teams menu: {e}")
        return

    await safe_delete_message(bot, message.chat.id, bot_message_id)
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

# Обробник для кнопки "Trading"
@router.message(F.text == MenuButton.TRADING.value)
async def handle_trading(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Trading")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    try:
        trading_message = await bot.send_message(
            chat_id=message.chat.id,
            text=TRADING_TEXT,
            reply_markup=get_trading_menu()
        )
        await state.update_data(bot_message_id=trading_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.TRADING_MENU)
    except Exception as e:
        logger.error(f"Failed to send Trading menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Обробник для меню "Trading"
@router.message(MenuStates.TRADING_MENU)
async def handle_trading_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Trading Menu")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    if not bot_message_id:
        logger.error("bot_message_id not found")
        try:
            error_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(bot_message_id=error_message.message_id)
            await state.set_state(MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = None
    new_state = MenuStates.TRADING_MENU

    if user_choice == MenuButton.CREATE_TRADE.value:
        new_main_text = "Функція створення торгівлі ще в розробці!"
    elif user_choice == MenuButton.VIEW_TRADES.value:
        new_main_text = "Ось всі доступні торгівлі:"
    elif user_choice == MenuButton.MANAGE_TRADES.value:
        new_main_text = "Функція управління торгівлями ще в розробці!"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Main Navigation"
        new_main_keyboard = get_navigation_menu()
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_trading_menu()

    try:
        if new_main_keyboard:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=new_main_keyboard
            )
            new_bot_message_id = main_message.message_id
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=get_generic_inline_keyboard()
            )
            new_bot_message_id = bot_message_id
    except Exception as e:
        logger.error(f"Failed to send new Trading menu: {e}")
        return

    await safe_delete_message(bot, message.chat.id, bot_message_id)
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

# Обробник для кнопки "Settings"
@router.message(F.text == MenuButton.SETTINGS.value)
async def handle_settings(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Settings")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    try:
        settings_message = await bot.send_message(
            chat_id=message.chat.id,
            text="⚙️ Settings",
            reply_markup=get_settings_menu()
        )
        await state.update_data(bot_message_id=settings_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.SETTINGS_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Settings menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Обробник для меню "Settings"
@router.message(MenuStates.SETTINGS_SUBMENU)
async def handle_settings_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Settings Menu")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    if not bot_message_id:
        logger.error("bot_message_id not found")
        try:
            error_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(bot_message_id=error_message.message_id)
            await state.set_state(MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = None
    new_state = MenuStates.SETTINGS_SUBMENU

    if user_choice == MenuButton.LANGUAGE.value:
        new_main_text = LANGUAGE_SELECTION_TEXT
        new_main_keyboard = get_language_menu()
        new_state = MenuStates.SELECT_LANGUAGE
    elif user_choice == MenuButton.CHANGE_USERNAME.value:
        new_main_text = "ℹ️ Enter new Username:"
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
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_settings_menu()

    try:
        if new_main_keyboard:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=new_main_keyboard
            )
            new_bot_message_id = main_message.message_id
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=get_generic_inline_keyboard()
            )
            new_bot_message_id = bot_message_id
    except Exception as e:
        logger.error(f"Failed to send new Settings menu: {e}")
        return

    await safe_delete_message(bot, message.chat.id, bot_message_id)
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

# Обробник для вибору мови
@router.message(MenuStates.SELECT_LANGUAGE)
async def handle_select_language(message: Message, state: FSMContext, bot: Bot):
    selected_language = message.text
    logger.info(f"User {message.from_user.id} selected language: {selected_language}")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Interface language changed to {selected_language}.",
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Failed to send language change confirmation: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

    try:
        settings_message = await bot.send_message(
            chat_id=message.chat.id,
            text="⚙️ Settings",
            reply_markup=get_settings_menu()
        )
        await state.update_data(bot_message_id=settings_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.SETTINGS_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Settings menu after language change: {e}")

# Обробник для кнопки "Help"
@router.message(F.text == MenuButton.HELP.value)
async def handle_help(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Help")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    try:
        help_message = await bot.send_message(
            chat_id=message.chat.id,
            text="❓ Help",
            reply_markup=get_help_menu()
        )
        await state.update_data(bot_message_id=help_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.HELP_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Help menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Обробник для меню "Help"
@router.message(MenuStates.HELP_SUBMENU)
async def handle_help_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Help Menu")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    if not bot_message_id:
        logger.error("bot_message_id not found")
        try:
            error_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(bot_message_id=error_message.message_id)
            await state.set_state(MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = None
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
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_help_menu()

    try:
        if new_main_keyboard:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=new_main_keyboard
            )
            new_bot_message_id = main_message.message_id
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=get_generic_inline_keyboard()
            )
            new_bot_message_id = bot_message_id
    except Exception as e:
        logger.error(f"Failed to send new Help menu: {e}")
        return

    await safe_delete_message(bot, message.chat.id, bot_message_id)
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

# Обробник для кнопки "My Team"
@router.message(F.text == MenuButton.MY_TEAM.value)
async def handle_my_team(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected My Team")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    try:
        my_team_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MY_TEAM_TEXT,
            reply_markup=get_my_team_menu()
        )
        await state.update_data(bot_message_id=my_team_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.MY_TEAM_MENU)
    except Exception as e:
        logger.error(f"Failed to send My Team menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Обробник для меню "My Team"
@router.message(MenuStates.MY_TEAM_MENU)
async def handle_my_team_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in My Team Menu")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    if not bot_message_id:
        logger.error("bot_message_id not found")
        try:
            error_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(bot_message_id=error_message.message_id)
            await state.set_state(MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = None
    new_state = MenuStates.MY_TEAM_MENU

    if user_choice == "➕ Створити Команду":
        new_main_text = "Feature to create a team is under development."
    elif user_choice == "👀 Переглянути Команди":
        new_main_text = "Feature to view teams is under development."
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🪪 My Profile"
        new_main_keyboard = get_profile_menu()
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_my_team_menu()

    try:
        if new_main_keyboard:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=new_main_keyboard
            )
            new_bot_message_id = main_message.message_id
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=get_generic_inline_keyboard()
            )
            new_bot_message_id = bot_message_id
    except Exception as e:
        logger.error(f"Failed to send new My Team menu: {e}")
        return

    await safe_delete_message(bot, message.chat.id, bot_message_id)
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

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

    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=UPDATE_ID_SUCCESS_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Failed to send Update ID confirmation: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

    try:
        settings_message = await bot.send_message(
            chat_id=message.chat.id,
            text="⚙️ Settings",
            reply_markup=get_settings_menu()
        )
        await state.update_data(bot_message_id=settings_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.SETTINGS_SUBMENU)
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

    try:
        settings_message = await bot.send_message(
            chat_id=message.chat.id,
            text="⚙️ Settings",
            reply_markup=get_settings_menu()
        )
        await state.update_data(bot_message_id=settings_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.SETTINGS_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Settings menu after notifications: {e}")

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
    # Приклад:
    # user_id = message.from_user.id
    # async with db.begin():
    #     user = await db.execute(select(models.user.User).where(models.user.User.telegram_id == user_id))
    #     user = user.scalars().first()
    #     if user:
    #         user.username = new_username
    #         await db.commit()
    #         response_text = CHANGE_USERNAME_RESPONSE_TEXT.format(new_username=new_username)
    #     else:
    #         response_text = "❌ Користувача не знайдено."

    # Для демонстрації відправимо підтвердження:
    try:
        response_text = f"Username changed to {new_username}."
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

    try:
        settings_message = await bot.send_message(
            chat_id=message.chat.id,
            text="⚙️ Settings",
            reply_markup=get_settings_menu()
        )
        await state.update_data(bot_message_id=settings_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.SETTINGS_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Settings menu after changing username: {e}")

# Функція для налаштування обробників
def setup_missing_handlers(dp: Router):
    dp.include_router(router)
