# handlers/missing_handlers.py

import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode

from handlers.base import MenuStates, increment_step  # Імпортуємо стани і функцію increment_step з base.py
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
    MY_TEAM_TEXT,
    TRADE_ITEM_TEXT, VIEW_TRADES_TEXT
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

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
        await increment_step(state)
        await state.set_state(MenuStates.CHALLENGES_MENU)
    except Exception as e:
        logger.error(f"Failed to send Challenges menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

@router.message(MenuStates.CHALLENGES_MENU)
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
        await increment_step(state)
        await state.set_state(MenuStates.GUIDES_MENU)
    except Exception as e:
        logger.error(f"Failed to send Guides menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

@router.message(MenuStates.GUIDES_MENU)
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
        await increment_step(state)
        await state.set_state(MenuStates.BUST_MENU)
    except Exception as e:
        logger.error(f"Failed to send Bust menu: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

@router.message(MenuStates.BUST_MENU)
async def handle_bust_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Bust Menu")

    await message.delete()

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    if not bot_message_id:
        logger.error("bot_message_id not found")
        try:
            error_message = await bot.send_message(chat_id=message.chat.id, text=MAIN_MENU_ERROR_TEXT, reply_markup=get_generic_inline_keyboard())
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
            main_message = await bot.send_message(chat_id=message.chat.id, text=new_main_text, reply_markup=new_main_keyboard)
            new_bot_message_id = main_message.message_id
        else:
            await bot.send_message(chat_id=message.chat.id, text=new_main_text, reply_markup=get_generic_inline_keyboard())
            new_bot_message_id = bot_message_id
    except Exception as e:
        logger.error(f"Failed to send new Bust menu: {e}")
        return

    await safe_delete_message(bot, message.chat.id, bot_message_id)
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

@router.message(F.text == MenuButton.TEAMS.value)
async def handle_teams(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Teams")
    await message.delete()

    try:
        teams_message = await bot.send_message(chat_id=message.chat.id, text=TEAMS_TEXT, reply_markup=get_teams_menu())
        await state.update_data(bot_message_id=teams_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.TEAMS_MENU)
    except Exception as e:
        logger.error(f"Failed to send Teams menu: {e}")
        await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=get_generic_inline_keyboard())

@router.message(MenuStates.TEAMS_MENU)
async def handle_teams_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Teams Menu")

    await message.delete()

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    if not bot_message_id:
        logger.error("bot_message_id not found")
        try:
            error_message = await bot.send_message(chat_id=message.chat.id, text=MAIN_MENU_ERROR_TEXT, reply_markup=get_generic_inline_keyboard())
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
        new_main_text = VIEW_TRADES_TEXT  # або VIEW_TEAMS_TEXT, якщо ви хочете інший текст (у вихідному коді його не було)
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Main Navigation"
        new_main_keyboard = get_navigation_menu()
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_teams_menu()

    try:
        if new_main_keyboard:
            main_message = await bot.send_message(chat_id=message.chat.id, text=new_main_text, reply_markup=new_main_keyboard)
            new_bot_message_id = main_message.message_id
        else:
            await bot.send_message(chat_id=message.chat.id, text=new_main_text, reply_markup=get_generic_inline_keyboard())
            new_bot_message_id = bot_message_id
    except Exception as e:
        logger.error(f"Failed to send new Teams menu: {e}")
        return

    await safe_delete_message(bot, message.chat.id, bot_message_id)
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

@router.message(F.text == MenuButton.TRADING.value)
async def handle_trading(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Trading")
    await message.delete()

    try:
        trading_message = await bot.send_message(chat_id=message.chat.id, text=TRADING_TEXT, reply_markup=get_trading_menu())
        await state.update_data(bot_message_id=trading_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.TRADING_MENU)
    except Exception as e:
        logger.error(f"Failed to send Trading menu: {e}")
        await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=get_generic_inline_keyboard())

@router.message(MenuStates.TRADING_MENU)
async def handle_trading_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Trading Menu")

    await message.delete()

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    if not bot_message_id:
        logger.error("bot_message_id not found")
        try:
            error_message = await bot.send_message(chat_id=message.chat.id, text=MAIN_MENU_ERROR_TEXT, reply_markup=get_generic_inline_keyboard())
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
            main_message = await bot.send_message(chat_id=message.chat.id, text=new_main_text, reply_markup=new_main_keyboard)
            new_bot_message_id = main_message.message_id
        else:
            await bot.send_message(chat_id=message.chat.id, text=new_main_text, reply_markup=get_generic_inline_keyboard())
            new_bot_message_id = bot_message_id
    except Exception as e:
        logger.error(f"Failed to send new Trading menu: {e}")
        return

    await safe_delete_message(bot, message.chat.id, bot_message_id)
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

@router.message(F.text == MenuButton.SETTINGS.value)
async def handle_settings(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Settings")
    await message.delete()

    try:
        settings_message = await bot.send_message(chat_id=message.chat.id, text="⚙️ Settings", reply_markup=get_settings_menu())
        await state.update_data(bot_message_id=settings_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.SETTINGS_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Settings menu: {e}")
        await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=get_generic_inline_keyboard())

@router.message(MenuStates.SETTINGS_SUBMENU)
async def handle_settings_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Settings Menu")

    await message.delete()

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    if not bot_message_id:
        logger.error("bot_message_id not found")
        try:
            error_message = await bot.send_message(chat_id=message.chat.id, text=MAIN_MENU_ERROR_TEXT, reply_markup=get_generic_inline_keyboard())
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
        # Змінимо стан на MenuStates.CHANGE_USERNAME
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
            main_message = await bot.send_message(chat_id=message.chat.id, text=new_main_text, reply_markup=new_main_keyboard)
            new_bot_message_id = main_message.message_id
        else:
            await bot.send_message(chat_id=message.chat.id, text=new_main_text, reply_markup=get_generic_inline_keyboard())
            new_bot_message_id = bot_message_id
    except Exception as e:
        logger.error(f"Failed to send new Settings menu: {e}")
        return

    await safe_delete_message(bot, message.chat.id, bot_message_id)
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

@router.message(MenuStates.SELECT_LANGUAGE)
async def handle_select_language(message: Message, state: FSMContext, bot: Bot):
    selected_language = message.text
    logger.info(f"User {message.from_user.id} selected language: {selected_language}")
    await message.delete()

    try:
        await bot.send_message(chat_id=message.chat.id, text=f"Interface language changed to {selected_language}.", reply_markup=get_generic_inline_keyboard())
    except Exception as e:
        logger.error(f"Failed to send language change confirmation: {e}")
        await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=get_generic_inline_keyboard())

    try:
        settings_message = await bot.send_message(chat_id=message.chat.id, text="⚙️ Settings", reply_markup=get_settings_menu())
        await state.update_data(bot_message_id=settings_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.SETTINGS_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Settings menu after language change: {e}")

@router.message(F.text == MenuButton.HELP.value)
async def handle_help(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Help")
    await message.delete()

    try:
        help_message = await bot.send_message(chat_id=message.chat.id, text="❓ Help", reply_markup=get_help_menu())
        await state.update_data(bot_message_id=help_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.HELP_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Help menu: {e}")
        await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=get_generic_inline_keyboard())

@router.message(MenuStates.HELP_SUBMENU)
async def handle_help_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Help Menu")

    await message.delete()

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    if not bot_message_id:
        logger.error("bot_message_id not found")
        try:
            error_message = await bot.send_message(chat_id=message.chat.id, text=MAIN_MENU_ERROR_TEXT, reply_markup=get_generic_inline_keyboard())
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
            main_message = await bot.send_message(chat_id=message.chat.id, text=new_main_text, reply_markup=new_main_keyboard)
            new_bot_message_id = main_message.message_id
        else:
            await bot.send_message(chat_id=message.chat.id, text=new_main_text, reply_markup=get_generic_inline_keyboard())
            new_bot_message_id = bot_message_id
    except Exception as e:
        logger.error(f"Failed to send new Help menu: {e}")
        return

    await safe_delete_message(bot, message.chat.id, bot_message_id)
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

@router.message(F.text == MenuButton.MY_TEAM.value)
async def handle_my_team(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected My Team")
    await message.delete()

    try:
        my_team_message = await bot.send_message(chat_id=message.chat.id, text=MY_TEAM_TEXT, reply_markup=get_my_team_menu())
        await state.update_data(bot_message_id=my_team_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.MY_TEAM_MENU)
    except Exception as e:
        logger.error(f"Failed to send My Team menu: {e}")
        await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=get_generic_inline_keyboard())

@router.message(MenuStates.MY_TEAM_MENU)
async def handle_my_team_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in My Team Menu")

    await message.delete()

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    if not bot_message_id:
        logger.error("bot_message_id not found")
        try:
            error_message = await bot.send_message(chat_id=message.chat.id, text=MAIN_MENU_ERROR_TEXT, reply_markup=get_generic_inline_keyboard())
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
            main_message = await bot.send_message(chat_id=message.chat.id, text=new_main_text, reply_markup=new_main_keyboard)
            new_bot_message_id = main_message.message_id
        else:
            await bot.send_message(chat_id=message.chat.id, text=new_main_text, reply_markup=get_generic_inline_keyboard())
            new_bot_message_id = bot_message_id
    except Exception as e:
        logger.error(f"Failed to send new My Team menu: {e}")
        return

    await safe_delete_message(bot, message.chat.id, bot_message_id)
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

@router.message(F.text == MenuButton.ADVANCED_TECHNIQUES.value)
async def handle_advanced_techniques(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Advanced Techniques")
    await message.delete()

    try:
        advanced_techniques_message = await bot.send_message(chat_id=message.chat.id, text=ADVANCED_TECHNIQUES_TEXT, reply_markup=get_generic_inline_keyboard())
        await state.update_data(bot_message_id=advanced_techniques_message.message_id)
        await increment_step(state)
        # Якщо потрібно, встановлюємо новий стан або залишаємо цей як кінцевий пункт
    except Exception as e:
        logger.error(f"Failed to send Advanced Techniques info: {e}")
        await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=get_generic_inline_keyboard())

@router.message(F.text == MenuButton.INSTRUCTIONS.value)
async def handle_instructions(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Instructions")
    await message.delete()
    try:
        instructions_message = await bot.send_message(chat_id=message.chat.id, text=INSTRUCTIONS_TEXT, reply_markup=get_generic_inline_keyboard())
        await state.update_data(bot_message_id=instructions_message.message_id)
        await increment_step(state)
    except Exception as e:
        logger.error(f"Failed to send Instructions: {e}")
        await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=get_generic_inline_keyboard())

@router.message(F.text == MenuButton.FAQ.value)
async def handle_faq(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected FAQ")
    await message.delete()
    try:
        faq_message = await bot.send_message(chat_id=message.chat.id, text=FAQ_TEXT, reply_markup=get_generic_inline_keyboard())
        await state.update_data(bot_message_id=faq_message.message_id)
        await increment_step(state)
    except Exception as e:
        logger.error(f"Failed to send FAQ: {e}")
        await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=get_generic_inline_keyboard())

@router.message(F.text == MenuButton.HELP_SUPPORT.value)
async def handle_help_support(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Help Support")
    await message.delete()
    try:
        help_support_message = await bot.send_message(chat_id=message.chat.id, text=HELP_SUPPORT_TEXT, reply_markup=get_generic_inline_keyboard())
        await state.update_data(bot_message_id=help_support_message.message_id)
        await increment_step(state)
    except Exception as e:
        logger.error(f"Failed to send Help Support: {e}")
        await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=get_generic_inline_keyboard())

@router.message(F.text == MenuButton.UPDATE_ID.value)
async def handle_update_id(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Update ID")
    await message.delete()

    try:
        await bot.send_message(chat_id=message.chat.id, text=UPDATE_ID_SUCCESS_TEXT, reply_markup=get_generic_inline_keyboard())
    except Exception as e:
        logger.error(f"Failed to send Update ID confirmation: {e}")
        await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=get_generic_inline_keyboard())

    try:
        settings_message = await bot.send_message(chat_id=message.chat.id, text="⚙️ Settings", reply_markup=get_settings_menu())
        await state.update_data(bot_message_id=settings_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.SETTINGS_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Settings menu after updating ID: {e}")

@router.message(F.text == MenuButton.NOTIFICATIONS.value)
async def handle_notifications(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Notifications")
    await message.delete()
    try:
        await bot.send_message(chat_id=message.chat.id, text=NOTIFICATIONS_SETTINGS_TEXT, reply_markup=get_generic_inline_keyboard())
    except Exception as e:
        logger.error(f"Failed to send Notifications settings: {e}")
        await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=get_generic_inline_keyboard())

    try:
        settings_message = await bot.send_message(chat_id=message.chat.id, text="⚙️ Settings", reply_markup=get_settings_menu())
        await state.update_data(bot_message_id=settings_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.SETTINGS_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Settings menu after notifications: {e}")

@router.message(F.text == MenuButton.MY_TEAM.value)
async def handle_my_team_again(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected My Team")
    await message.delete()
    try:
        my_team_message = await bot.send_message(chat_id=message.chat.id, text=MY_TEAM_TEXT, reply_markup=get_my_team_menu())
        await state.update_data(bot_message_id=my_team_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.MY_TEAM_MENU)
    except Exception as e:
        logger.error(f"Failed to send My Team menu: {e}")
        await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=get_generic_inline_keyboard())

@router.message(MenuStates.MY_TEAM_MENU)
async def handle_my_team_menu_buttons_again(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in My Team Menu")

    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    if not bot_message_id:
        logger.error("bot_message_id not found")
        try:
            error_message = await bot.send_message(chat_id=message.chat.id, text=MAIN_MENU_ERROR_TEXT, reply_markup=get_generic_inline_keyboard())
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
            main_message = await bot.send_message(chat_id=message.chat.id, text=new_main_text, reply_markup=new_main_keyboard)
            new_bot_message_id = main_message.message_id
        else:
            await bot.send_message(chat_id=message.chat.id, text=new_main_text, reply_markup=get_generic_inline_keyboard())
            new_bot_message_id = bot_message_id
    except Exception as e:
        logger.error(f"Failed to send new My Team menu: {e}")
        return
    await safe_delete_message(bot, message.chat.id, bot_message_id)
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

@router.message(F.text == MenuButton.ADVANCED_TECHNIQUES.value)
async def handle_advanced_techniques_again(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Advanced Techniques")
    await message.delete()
    try:
        advanced_techniques_message = await bot.send_message(chat_id=message.chat.id, text=ADVANCED_TECHNIQUES_TEXT, reply_markup=get_generic_inline_keyboard())
        await state.update_data(bot_message_id=advanced_techniques_message.message_id)
        await increment_step(state)
    except Exception as e:
        logger.error(f"Failed to send Advanced Techniques info: {e}")
        await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=get_generic_inline_keyboard())

@router.message(F.text == MenuButton.INSTRUCTIONS.value)
async def handle_instructions_again(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Instructions")
    await message.delete()
    try:
        instructions_message = await bot.send_message(chat_id=message.chat.id, text=INSTRUCTIONS_TEXT, reply_markup=get_generic_inline_keyboard())
        await state.update_data(bot_message_id=instructions_message.message_id)
        await increment_step(state)
    except Exception as e:
        logger.error(f"Failed to send Instructions: {e}")
        await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=get_generic_inline_keyboard())

@router.message(F.text == MenuButton.FAQ.value)
async def handle_faq_again(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected FAQ")
    await message.delete()
    try:
        faq_message = await bot.send_message(chat_id=message.chat.id, text=FAQ_TEXT, reply_markup=get_generic_inline_keyboard())
        await state.update_data(bot_message_id=faq_message.message_id)
        await increment_step(state)
    except Exception as e:
        logger.error(f"Failed to send FAQ: {e}")
        await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=get_generic_inline_keyboard())

@router.message(F.text == MenuButton.HELP_SUPPORT.value)
async def handle_help_support_again(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Help Support")
    await message.delete()
    try:
        help_support_message = await bot.send_message(chat_id=message.chat.id, text=HELP_SUPPORT_TEXT, reply_markup=get_generic_inline_keyboard())
        await state.update_data(bot_message_id=help_support_message.message_id)
        await increment_step(state)
    except Exception as e:
        logger.error(f"Failed to send Help Support: {e}")
        await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=get_generic_inline_keyboard())

@router.message(F.text == MenuButton.UPDATE_ID.value)
async def handle_update_id_again(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Update ID")
    await message.delete()
    try:
        await bot.send_message(chat_id=message.chat.id, text=UPDATE_ID_SUCCESS_TEXT, reply_markup=get_generic_inline_keyboard())
    except Exception as e:
        logger.error(f"Failed to send Update ID confirmation: {e}")
        await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=get_generic_inline_keyboard())
    try:
        settings_message = await bot.send_message(chat_id=message.chat.id, text="⚙️ Settings", reply_markup=get_settings_menu())
        await state.update_data(bot_message_id=settings_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.SETTINGS_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Settings menu after updating ID: {e}")

@router.message(F.text == MenuButton.NOTIFICATIONS.value)
async def handle_notifications_again(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Notifications")
    await message.delete()
    try:
        await bot.send_message(chat_id=message.chat.id, text=NOTIFICATIONS_SETTINGS_TEXT, reply_markup=get_generic_inline_keyboard())
    except Exception as e:
        logger.error(f"Failed to send Notifications settings: {e}")
        await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=get_generic_inline_keyboard())
    try:
        settings_message = await bot.send_message(chat_id=message.chat.id, text="⚙️ Settings", reply_markup=get_settings_menu())
        await state.update_data(bot_message_id=settings_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.SETTINGS_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Settings menu after notifications: {e}")

@router.message(F.text == MenuButton.MY_TEAM.value)
async def handle_my_team_again2(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected My Team")
    await message.delete()
    try:
        my_team_message = await bot.send_message(chat_id=message.chat.id, text=MY_TEAM_TEXT, reply_markup=get_my_team_menu())
        await state.update_data(bot_message_id=my_team_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.MY_TEAM_MENU)
    except Exception as e:
        logger.error(f"Failed to send My Team menu: {e}")
        await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=get_generic_inline_keyboard())

@router.message(MenuStates.MY_TEAM_MENU)
async def handle_my_team_menu_buttons_again2(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in My Team Menu")

    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    if not bot_message_id:
        logger.error("bot_message_id not found")
        try:
            error_message = await bot.send_message(chat_id=message.chat.id, text=MAIN_MENU_ERROR_TEXT, reply_markup=get_generic_inline_keyboard())
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
            main_message = await bot.send_message(chat_id=message.chat.id, text=new_main_text, reply_markup=new_main_keyboard)
            new_bot_message_id = main_message.message_id
        else:
            await bot.send_message(chat_id=message.chat.id, text=new_main_text, reply_markup=get_generic_inline_keyboard())
            new_bot_message_id = bot_message_id
    except Exception as e:
        logger.error(f"Failed to send new My Team menu: {e}")
        return
    await safe_delete_message(bot, message.chat.id, bot_message_id)
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await state.set_state(new_state)

@router.message(F.text == MenuButton.ADVANCED_TECHNIQUES.value)
async def handle_advanced_techniques_again3(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Advanced Techniques")
    await message.delete()
    try:
        advanced_techniques_message = await bot.send_message(chat_id=message.chat.id, text=ADVANCED_TECHNIQUES_TEXT, reply_markup=get_generic_inline_keyboard())
        await state.update_data(bot_message_id=advanced_techniques_message.message_id)
        await increment_step(state)
    except Exception as e:
        logger.error(f"Failed to send Advanced Techniques info: {e}")
        await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=get_generic_inline_keyboard())

@router.message(F.text)
async def handle_change_username(message: Message, state: FSMContext, bot: Bot):
    current_state = await state.get_state()
    if current_state != MenuStates.CHANGE_USERNAME.state:
        return
    new_username = message.text.strip()
    logger.info(f"User {message.from_user.id} is changing username to: {new_username}")
    await message.delete()
    # Тут логіка зміни імені
    try:
        await bot.send_message(chat_id=message.chat.id, text=f"Username changed to {new_username}.", reply_markup=get_generic_inline_keyboard())
    except Exception as e:
        logger.error(f"Failed to send username change confirmation: {e}")
        await bot.send_message(chat_id=message.chat.id, text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=get_generic_inline_keyboard())
    try:
        settings_message = await bot.send_message(chat_id=message.chat.id, text="⚙️ Settings", reply_markup=get_settings_menu())
        await state.update_data(bot_message_id=settings_message.message_id)
        await increment_step(state)
        await state.set_state(MenuStates.SETTINGS_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Settings menu after changing username: {e}")

@router.message(F.text == MenuButton.BACK.value)
async def back_handler(message: Message):
    logger.info(f"Користувач повернувся назад: {message.from_user.id}")
    # Якщо потрібно повертатися до головного меню - можна використати get_main_menu()
    # або якщо Navigation menu є головним екраном - get_navigation_menu()
    await message.answer("Ви повернулися до головного меню.", reply_markup=get_main_menu())

def setup_missing_handlers(dp: Router):
    dp.include_router(router)