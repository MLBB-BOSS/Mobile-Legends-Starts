# handlers/missing_handlers.py

import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.enums import ParseMode

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
    get_language_menu
)
from texts import (
    MAIN_MENU_ERROR_TEXT, UNKNOWN_COMMAND_TEXT, GENERIC_ERROR_MESSAGE_TEXT,
    CHALLENGES_TEXT, GUIDES_TEXT, BUST_TEXT, TEAMS_TEXT, TRADING_TEXT,
    NEW_GUIDES_TEXT, M6_TEXT, POPULAR_GUIDES_TEXT, BEGINNER_GUIDES_TEXT,
    ADVANCED_TECHNIQUES_TEXT, TEAMPLAY_GUIDES_TEXT,
    LANGUAGE_SELECTION_TEXT, UPDATE_ID_SUCCESS_TEXT, NOTIFICATIONS_SETTINGS_TEXT,
    INSTRUCTIONS_TEXT, FAQ_TEXT, HELP_SUPPORT_TEXT,
    MY_TEAM_TEXT,
    TRADE_ITEM_TEXT, VIEW_TRADES_TEXT
)

# Ініціалізація логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

class MissingMenuStates(StatesGroup):
    CHALLENGES_MENU = State()
    GUIDES_MENU = State()
    BUST_MENU = State()
    TEAMS_MENU = State()
    TRADING_MENU = State()
    SETTINGS_SUBMENU = State()
    HELP_SUBMENU = State()
    MY_TEAM_MENU = State()
    SELECT_LANGUAGE = State()

async def safe_delete_message(bot: Bot, chat_id: int, message_id: int):
    if message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=message_id)
            logger.info(f"Deleted message {message_id} in chat {chat_id}.")
        except Exception as e:
            logger.error(f"Failed to delete message {message_id} in chat {chat_id}: {e}")

async def check_and_edit_message(
    bot: Bot,
    chat_id: int,
    message_id: int,
    new_text: str,
    new_keyboard,
    state: FSMContext,
    parse_mode: str = ParseMode.HTML
):
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
            logger.info(f"Edited message {message_id} in chat {chat_id}.")
        except Exception as e:
            logger.error(f"Failed to edit message {message_id} in chat {chat_id}: {e}")
            await bot.send_message(
                chat_id=chat_id,
                text=GENERIC_ERROR_MESSAGE_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )

# Навігаційне меню
@router.message(F.text == MenuButton.CHALLENGES.value)
async def handle_challenges(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Challenges")
    await message.delete()

    try:
        challenges_message = await bot.send_message(
            chat_id=message.chat.id,
            text=CHALLENGES_TEXT,
            reply_markup=get_challenges_menu()
        )
        await state.update_data(bot_message_id=challenges_message.message_id)
        await state.set_state(MissingMenuStates.CHALLENGES_MENU)
    except Exception as e:
        logger.error(f"Failed to send Challenges menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

@router.message(MissingMenuStates.CHALLENGES_MENU)
async def handle_challenges_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Challenges Menu")

    await message.delete()

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
            await state.set_state(MenuButton.MAIN_MENU.state)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = MissingMenuStates.CHALLENGES_MENU

    if user_choice == "➕ Додати Челендж":
        new_main_text = "Feature to add challenges is under development."
        new_interactive_text = "Adding a Challenge"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Main Navigation"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Main Navigation Menu"
        new_state = MenuButton.MAIN_MENU.state
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_challenges_menu()
        new_interactive_text = "Unknown Command"
        new_state = MissingMenuStates.CHALLENGES_MENU

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
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

@router.message(F.text == MenuButton.GUIDES.value)
async def handle_guides(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Guides")
    await message.delete()

    try:
        guides_message = await bot.send_message(
            chat_id=message.chat.id,
            text=GUIDES_TEXT,
            reply_markup=get_guides_menu()
        )
        await state.update_data(bot_message_id=guides_message.message_id)
        await state.set_state(MissingMenuStates.GUIDES_MENU)
    except Exception as e:
        logger.error(f"Failed to send Guides menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

@router.message(MissingMenuStates.GUIDES_MENU)
async def handle_guides_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Guides Menu")

    await message.delete()

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
            await state.set_state(MenuButton.MAIN_MENU.state)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = MissingMenuStates.GUIDES_MENU

    if user_choice == MenuButton.NEW_GUIDES.value:
        new_main_text = NEW_GUIDES_TEXT
        new_interactive_text = "New Guides"
    elif user_choice == MenuButton.POPULAR_GUIDES.value:
        new_main_text = POPULAR_GUIDES_TEXT
        new_interactive_text = "Popular Guides"
    elif user_choice == MenuButton.BEGINNER_GUIDES.value:
        new_main_text = BEGINNER_GUIDES_TEXT
        new_interactive_text = "Beginner Guides"
    elif user_choice == MenuButton.ADVANCED_TECHNIQUES.value:
        new_main_text = ADVANCED_TECHNIQUES_TEXT
        new_interactive_text = "Advanced Techniques"
    elif user_choice == MenuButton.TEAMPLAY_GUIDES.value:
        new_main_text = TEAMPLAY_GUIDES_TEXT
        new_interactive_text = "Teamplay Guides"
    elif user_choice == MenuButton.M6.value:
        new_main_text = M6_TEXT
        new_interactive_text = "M6 Information"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Main Navigation"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Main Navigation Menu"
        new_state = MenuButton.MAIN_MENU.state
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_guides_menu()
        new_interactive_text = "Unknown Command"
        new_state = MissingMenuStates.GUIDES_MENU

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
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

@router.message(F.text == MenuButton.BUST.value)
async def handle_bust(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Bust")
    await message.delete()

    try:
        bust_message = await bot.send_message(
            chat_id=message.chat.id,
            text=BUST_TEXT,
            reply_markup=get_bust_menu()
        )
        await state.update_data(bot_message_id=bust_message.message_id)
        await state.set_state(MissingMenuStates.BUST_MENU)
    except Exception as e:
        logger.error(f"Failed to send Bust menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

@router.message(MissingMenuStates.BUST_MENU)
async def handle_bust_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Bust Menu")

    await message.delete()

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
            await state.set_state(MenuButton.MAIN_MENU.state)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = MissingMenuStates.BUST_MENU

    if user_choice == "🔥 Підвищити Буст":
        new_main_text = "Feature to increase bust is under development."
        new_interactive_text = "Increasing Bust"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Main Navigation"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Main Navigation Menu"
        new_state = MenuButton.MAIN_MENU.state
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_bust_menu()
        new_interactive_text = "Unknown Command"
        new_state = MissingMenuStates.BUST_MENU

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
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

@router.message(F.text == MenuButton.TEAMS.value)
async def handle_teams(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Teams")
    await message.delete()

    try:
        teams_message = await bot.send_message(
            chat_id=message.chat.id,
            text=TEAMS_TEXT,
            reply_markup=get_teams_menu()
        )
        await state.update_data(bot_message_id=teams_message.message_id)
        await state.set_state(MissingMenuStates.TEAMS_MENU)
    except Exception as e:
        logger.error(f"Failed to send Teams menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

@router.message(MissingMenuStates.TEAMS_MENU)
async def handle_teams_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Teams Menu")

    await message.delete()

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
            await state.set_state(MenuButton.MAIN_MENU.state)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = MissingMenuStates.TEAMS_MENU

    if user_choice == MenuButton.CREATE_TEAM.value:
        new_main_text = "Feature to create a team is under development."
        new_interactive_text = "Creating a Team"
    elif user_choice == MenuButton.VIEW_TEAMS.value:
        new_main_text = VIEW_TEAMS_TEXT
        new_interactive_text = "Viewing Teams"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Main Navigation"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Main Navigation Menu"
        new_state = MenuButton.MAIN_MENU.state
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_teams_menu()
        new_interactive_text = "Unknown Command"
        new_state = MissingMenuStates.TEAMS_MENU

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
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

@router.message(F.text == MenuButton.TRADING.value)
async def handle_trading(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Trading")
    await message.delete()

    try:
        trading_message = await bot.send_message(
            chat_id=message.chat.id,
            text=TRADING_TEXT,
            reply_markup=get_trading_menu()
        )
        await state.update_data(bot_message_id=trading_message.message_id)
        await state.set_state(MissingMenuStates.TRADING_MENU)
    except Exception as e:
        logger.error(f"Failed to send Trading menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

@router.message(MissingMenuStates.TRADING_MENU)
async def handle_trading_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Trading Menu")

    await message.delete()

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
            await state.set_state(MenuButton.MAIN_MENU.state)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = MissingMenuStates.TRADING_MENU

    if user_choice == MenuButton.TRADE_ITEM.value:
        new_main_text = TRADE_ITEM_TEXT
        new_interactive_text = "Trading an Item"
    elif user_choice == MenuButton.VIEW_TRADES.value:
        new_main_text = VIEW_TRADES_TEXT
        new_interactive_text = "Viewing Trades"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Main Navigation"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Main Navigation Menu"
        new_state = MenuButton.MAIN_MENU.state
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_trading_menu()
        new_interactive_text = "Unknown Command"
        new_state = MissingMenuStates.TRADING_MENU

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
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

# Меню Налаштувань
@router.message(F.text == MenuButton.SETTINGS.value)
async def handle_settings(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Settings")
    await message.delete()

    try:
        settings_message = await bot.send_message(
            chat_id=message.chat.id,
            text="⚙️ Settings",
            reply_markup=get_settings_menu()
        )
        await state.update_data(bot_message_id=settings_message.message_id)
        await state.set_state(MissingMenuStates.SETTINGS_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Settings menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

@router.message(MissingMenuStates.SETTINGS_SUBMENU)
async def handle_settings_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Settings Menu")

    await message.delete()

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
            await state.set_state(MenuButton.MAIN_MENU.state)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = MissingMenuStates.SETTINGS_SUBMENU

    if user_choice == MenuButton.LANGUAGE.value:
        new_main_text = LANGUAGE_SELECTION_TEXT
        new_main_keyboard = get_language_menu()
        new_interactive_text = "Selecting Language"
        new_state = MissingMenuStates.SELECT_LANGUAGE
    elif user_choice == MenuButton.CHANGE_USERNAME.value:
        new_main_text = "ℹ️ Enter new Username:"
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Changing Username"
        await state.set_state(MenuButton.CHANGE_USERNAME.state)
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=new_main_keyboard
            )
        except Exception as e:
            logger.error(f"Failed to send Change Username prompt: {e}")
        return
    elif user_choice == MenuButton.UPDATE_ID.value:
        new_main_text = UPDATE_ID_SUCCESS_TEXT
        new_interactive_text = "Updating ID"
    elif user_choice == MenuButton.NOTIFICATIONS.value:
        new_main_text = NOTIFICATIONS_SETTINGS_TEXT
        new_interactive_text = "Notifications Settings"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🪪 My Profile"
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "My Profile Menu"
        new_state = MenuButton.PROFILE_MENU.state
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_settings_menu()
        new_interactive_text = "Unknown Command"
        new_state = MissingMenuStates.SETTINGS_SUBMENU

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
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

@router.message(MissingMenuStates.SELECT_LANGUAGE)
async def handle_select_language(message: Message, state: FSMContext, bot: Bot):
    selected_language = message.text
    logger.info(f"User {message.from_user.id} selected language: {selected_language}")
    await message.delete()

    # Implement language change logic here

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
        await state.set_state(MissingMenuStates.SETTINGS_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Settings menu after language change: {e}")

# Меню Допомоги
@router.message(F.text == MenuButton.HELP.value)
async def handle_help(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Help")
    await message.delete()

    try:
        help_message = await bot.send_message(
            chat_id=message.chat.id,
            text="❓ Help",
            reply_markup=get_help_menu()
        )
        await state.update_data(bot_message_id=help_message.message_id)
        await state.set_state(MissingMenuStates.HELP_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Help menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

@router.message(MissingMenuStates.HELP_SUBMENU)
async def handle_help_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Help Menu")

    await message.delete()

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
            await state.set_state(MenuButton.MAIN_MENU.state)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = MissingMenuStates.HELP_SUBMENU

    if user_choice == MenuButton.INSTRUCTIONS.value:
        new_main_text = INSTRUCTIONS_TEXT
        new_interactive_text = "Instructions"
    elif user_choice == MenuButton.FAQ.value:
        new_main_text = FAQ_TEXT
        new_interactive_text = "FAQ"
    elif user_choice == MenuButton.HELP_SUPPORT.value:
        new_main_text = HELP_SUPPORT_TEXT
        new_interactive_text = "Support"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🪪 My Profile"
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "My Profile Menu"
        new_state = MenuButton.PROFILE_MENU.state
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_help_menu()
        new_interactive_text = "Unknown Command"
        new_state = MissingMenuStates.HELP_SUBMENU

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
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

# Меню Профільної Команди
@router.message(F.text == MenuButton.MY_TEAM.value)
async def handle_my_team(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected My Team")
    await message.delete()

    try:
        my_team_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MY_TEAM_TEXT,
            reply_markup=get_my_team_menu()
        )
        await state.update_data(bot_message_id=my_team_message.message_id)
        await state.set_state(MissingMenuStates.MY_TEAM_MENU)
    except Exception as e:
        logger.error(f"Failed to send My Team menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

@router.message(MissingMenuStates.MY_TEAM_MENU)
async def handle_my_team_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in My Team Menu")

    await message.delete()

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
            await state.set_state(MenuButton.MAIN_MENU.state)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = MissingMenuStates.MY_TEAM_MENU

    if user_choice == "➕ Створити Команду":
        new_main_text = "Feature to create a team is under development."
        new_interactive_text = "Creating a Team"
    elif user_choice == "👀 Переглянути Команди":
        new_main_text = "Feature to view teams is under development."
        new_interactive_text = "Viewing Teams"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🪪 My Profile"
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "My Profile Menu"
        new_state = MenuButton.PROFILE_MENU.state
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_my_team_menu()
        new_interactive_text = "Unknown Command"
        new_state = MissingMenuStates.MY_TEAM_MENU

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
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

# Меню Стратегії Гри
@router.message(F.text == MenuButton.ADVANCED_TECHNIQUES.value)
async def handle_advanced_techniques(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Advanced Techniques")
    await message.delete()

    try:
        advanced_techniques_message = await bot.send_message(
            chat_id=message.chat.id,
            text=ADVANCED_TECHNIQUES_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(bot_message_id=advanced_techniques_message.message_id)
        # Optionally set a new state if further interaction is needed
    except Exception as e:
        logger.error(f"Failed to send Advanced Techniques info: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Меню Мови Інтерфейсу
@router.message(MissingMenuStates.SELECT_LANGUAGE)
async def handle_select_language(message: Message, state: FSMContext, bot: Bot):
    selected_language = message.text
    logger.info(f"User {message.from_user.id} selected language: {selected_language}")
    await message.delete()

    # Implement language change logic here

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
        await state.set_state(MissingMenuStates.SETTINGS_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Settings menu after language change: {e}")

# Меню Допомоги - Інструкції
@router.message(F.text == MenuButton.INSTRUCTIONS.value)
async def handle_instructions(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Instructions")
    await message.delete()

    try:
        instructions_message = await bot.send_message(
            chat_id=message.chat.id,
            text=INSTRUCTIONS_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(bot_message_id=instructions_message.message_id)
        # Optionally set a new state if further interaction is needed
    except Exception as e:
        logger.error(f"Failed to send Instructions: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Меню Допомоги - FAQ
@router.message(F.text == MenuButton.FAQ.value)
async def handle_faq(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected FAQ")
    await message.delete()

    try:
        faq_message = await bot.send_message(
            chat_id=message.chat.id,
            text=FAQ_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(bot_message_id=faq_message.message_id)
    except Exception as e:
        logger.error(f"Failed to send FAQ: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Меню Допомоги - Підтримка
@router.message(F.text == MenuButton.HELP_SUPPORT.value)
async def handle_help_support(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Help Support")
    await message.delete()

    try:
        help_support_message = await bot.send_message(
            chat_id=message.chat.id,
            text=HELP_SUPPORT_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(bot_message_id=help_support_message.message_id)
    except Exception as e:
        logger.error(f"Failed to send Help Support: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Меню Налаштувань - Оновити ID
@router.message(F.text == MenuButton.UPDATE_ID.value)
async def handle_update_id(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Update ID")
    await message.delete()

    # Implement ID update logic here

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
        await state.set_state(MissingMenuStates.SETTINGS_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Settings menu after updating ID: {e}")

# Меню Налаштувань - Сповіщення
@router.message(F.text == MenuButton.NOTIFICATIONS.value)
async def handle_notifications(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Notifications")
    await message.delete()

    # Implement notifications settings logic here

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
        await state.set_state(MissingMenuStates.SETTINGS_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Settings menu after notifications: {e}")

# Меню Профільної Команди - Моя команда
@router.message(F.text == MenuButton.MY_TEAM.value)
async def handle_my_team(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected My Team")
    await message.delete()

    try:
        my_team_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MY_TEAM_TEXT,
            reply_markup=get_my_team_menu()
        )
        await state.update_data(bot_message_id=my_team_message.message_id)
        await state.set_state(MissingMenuStates.MY_TEAM_MENU)
    except Exception as e:
        logger.error(f"Failed to send My Team menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

@router.message(MissingMenuStates.MY_TEAM_MENU)
async def handle_my_team_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in My Team Menu")

    await message.delete()

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
            await state.set_state(MenuButton.MAIN_MENU.state)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = MissingMenuStates.MY_TEAM_MENU

    if user_choice == "➕ Створити Команду":
        new_main_text = "Feature to create a team is under development."
        new_interactive_text = "Creating a Team"
    elif user_choice == "👀 Переглянути Команди":
        new_main_text = "Feature to view teams is under development."
        new_interactive_text = "Viewing Teams"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🪪 My Profile"
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "My Profile Menu"
        new_state = MenuButton.PROFILE_MENU.state
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_my_team_menu()
        new_interactive_text = "Unknown Command"
        new_state = MissingMenuStates.MY_TEAM_MENU

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
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

# Меню Допомоги - Інструкції
@router.message(F.text == MenuButton.INSTRUCTIONS.value)
async def handle_instructions(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Instructions")
    await message.delete()

    try:
        instructions_message = await bot.send_message(
            chat_id=message.chat.id,
            text=INSTRUCTIONS_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(bot_message_id=instructions_message.message_id)
    except Exception as e:
        logger.error(f"Failed to send Instructions: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Меню Допомоги - FAQ
@router.message(F.text == MenuButton.FAQ.value)
async def handle_faq(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected FAQ")
    await message.delete()

    try:
        faq_message = await bot.send_message(
            chat_id=message.chat.id,
            text=FAQ_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(bot_message_id=faq_message.message_id)
    except Exception as e:
        logger.error(f"Failed to send FAQ: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Меню Допомоги - Підтримка
@router.message(F.text == MenuButton.HELP_SUPPORT.value)
async def handle_help_support(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Help Support")
    await message.delete()

    try:
        help_support_message = await bot.send_message(
            chat_id=message.chat.id,
            text=HELP_SUPPORT_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(bot_message_id=help_support_message.message_id)
    except Exception as e:
        logger.error(f"Failed to send Help Support: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Меню Налаштувань - Зміна Username
@router.message(F.text)
async def handle_change_username(message: Message, state: FSMContext, bot: Bot):
    current_state = await state.get_state()
    if current_state != MenuButton.CHANGE_USERNAME.state:
        return

    new_username = message.text.strip()
    logger.info(f"User {message.from_user.id} is changing username to: {new_username}")
    await message.delete()

    # Implement username change logic here

    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Username changed to {new_username}.",
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
        await state.set_state(MissingMenuStates.SETTINGS_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Settings menu after changing username: {e}")

# Функція для налаштування обробників
def setup_missing_handlers(dp: Router):
    dp.include_router(router)
