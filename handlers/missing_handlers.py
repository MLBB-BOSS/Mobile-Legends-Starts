# handlers/missing_handlers.py

import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import Command

from states import MenuStates, increment_step
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
from handlers.base import safe_delete_message, check_and_edit_message, send_or_update_interactive_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

# Допоміжна функція для переходу між станами
async def transition_state(state: FSMContext, new_state: MenuStates):
    await state.clear()
    await state.set_state(new_state)

# Спільна функція для обробки переходів між меню
async def handle_menu_transition(
    user_choice: str,
    message: Message,
    state: FSMContext,
    bot: Bot,
    chat_id: int,
    current_state: MenuStates,
    new_state: MenuStates,
    new_text: str,
    new_keyboard_func
):
    logger.info(f"User {message.from_user.id} selected '{user_choice}' in {current_state.name}")

    await safe_delete_message(bot, chat_id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        try:
            error_message = await bot.send_message(
                chat_id=chat_id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(bot_message_id=error_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    try:
        main_message = await bot.send_message(
            chat_id=chat_id,
            text=new_text,
            reply_markup=new_keyboard_func()
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send {current_state.name} menu: {e}")
        await bot.send_message(
            chat_id=chat_id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        return

    await safe_delete_message(bot, chat_id, bot_message_id)

    await check_and_edit_message(
        bot=bot,
        chat_id=chat_id,
        message_id=interactive_message_id,
        new_text=new_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обробник для кнопки "Challenges"
@router.message(F.text == MenuButton.CHALLENGES.value)
async def handle_challenges(message: Message, state: FSMContext, bot: Bot):
    await handle_menu_transition(
        user_choice=message.text,
        message=message,
        state=state,
        bot=bot,
        chat_id=message.chat.id,
        current_state=MenuStates.MAIN_MENU,
        new_state=MenuStates.CHALLENGES_MENU,
        new_text=CHALLENGES_TEXT,
        new_keyboard_func=get_challenges_menu
    )

# Обробник для меню "Challenges Menu"
@router.message(MenuStates.CHALLENGES_MENU)
async def handle_challenges_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    await handle_menu_transition(
        user_choice=user_choice,
        message=message,
        state=state,
        bot=bot,
        chat_id=message.chat.id,
        current_state=MenuStates.CHALLENGES_MENU,
        new_state=MenuStates.CHALLENGES_MENU,
        new_text=CHALLENGES_TEXT,  # Можливо, тут слід оновити текст відповідно до вибору
        new_keyboard_func=get_challenges_menu
    )

# Обробник для кнопки "Guides"
@router.message(F.text == MenuButton.GUIDES.value)
async def handle_guides(message: Message, state: FSMContext, bot: Bot):
    await handle_menu_transition(
        user_choice=message.text,
        message=message,
        state=state,
        bot=bot,
        chat_id=message.chat.id,
        current_state=MenuStates.MAIN_MENU,
        new_state=MenuStates.GUIDES_MENU,
        new_text=GUIDES_TEXT,
        new_keyboard_func=get_guides_menu
    )

# Обробник для меню "Guides Menu"
@router.message(MenuStates.GUIDES_MENU)
async def handle_guides_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    await handle_menu_transition(
        user_choice=user_choice,
        message=message,
        state=state,
        bot=bot,
        chat_id=message.chat.id,
        current_state=MenuStates.GUIDES_MENU,
        new_state=MenuStates.GUIDES_MENU,
        new_text=GUIDES_TEXT,  # Можливо, оновити відповідно до вибору
        new_keyboard_func=get_guides_menu
    )

# Обробник для кнопки "Bust"
@router.message(F.text == MenuButton.BUST.value)
async def handle_bust(message: Message, state: FSMContext, bot: Bot):
    await handle_menu_transition(
        user_choice=message.text,
        message=message,
        state=state,
        bot=bot,
        chat_id=message.chat.id,
        current_state=MenuStates.MAIN_MENU,
        new_state=MenuStates.BUST_MENU,
        new_text=BUST_TEXT,
        new_keyboard_func=get_bust_menu
    )

# Обробник для меню "Bust Menu"
@router.message(MenuStates.BUST_MENU)
async def handle_bust_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    await handle_menu_transition(
        user_choice=user_choice,
        message=message,
        state=state,
        bot=bot,
        chat_id=message.chat.id,
        current_state=MenuStates.BUST_MENU,
        new_state=MenuStates.BUST_MENU,
        new_text=BUST_TEXT,  # Оновити відповідно до вибору
        new_keyboard_func=get_bust_menu
    )

# Обробник для кнопки "Teams"
@router.message(F.text == MenuButton.TEAMS.value)
async def handle_teams(message: Message, state: FSMContext, bot: Bot):
    await handle_menu_transition(
        user_choice=message.text,
        message=message,
        state=state,
        bot=bot,
        chat_id=message.chat.id,
        current_state=MenuStates.MAIN_MENU,
        new_state=MenuStates.TEAMS_MENU,
        new_text=TEAMS_TEXT,
        new_keyboard_func=get_teams_menu
    )

# Обробник для меню "Teams Menu"
@router.message(MenuStates.TEAMS_MENU)
async def handle_teams_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    await handle_menu_transition(
        user_choice=user_choice,
        message=message,
        state=state,
        bot=bot,
        chat_id=message.chat.id,
        current_state=MenuStates.TEAMS_MENU,
        new_state=MenuStates.TEAMS_MENU,
        new_text=TEAMS_TEXT,  # Оновити відповідно до вибору
        new_keyboard_func=get_teams_menu
    )

# Обробник для кнопки "Trading"
@router.message(F.text == MenuButton.TRADING.value)
async def handle_trading(message: Message, state: FSMContext, bot: Bot):
    await handle_menu_transition(
        user_choice=message.text,
        message=message,
        state=state,
        bot=bot,
        chat_id=message.chat.id,
        current_state=MenuStates.MAIN_MENU,
        new_state=MenuStates.TRADING_MENU,
        new_text=TRADING_TEXT,
        new_keyboard_func=get_trading_menu
    )

# Обробник для меню "Trading Menu"
@router.message(MenuStates.TRADING_MENU)
async def handle_trading_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    await handle_menu_transition(
        user_choice=user_choice,
        message=message,
        state=state,
        bot=bot,
        chat_id=message.chat.id,
        current_state=MenuStates.TRADING_MENU,
        new_state=MenuStates.TRADING_MENU,
        new_text=TRADING_TEXT,  # Оновити відповідно до вибору
        new_keyboard_func=get_trading_menu
    )

# Обробник для кнопки "Settings"
@router.message(F.text == MenuButton.SETTINGS.value)
async def handle_settings(message: Message, state: FSMContext, bot: Bot):
    await handle_menu_transition(
        user_choice=message.text,
        message=message,
        state=state,
        bot=bot,
        chat_id=message.chat.id,
        current_state=MenuStates.MAIN_MENU,
        new_state=MenuStates.SETTINGS_SUBMENU,
        new_text="⚙️ Settings",
        new_keyboard_func=get_settings_menu
    )

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
        new_interactive_text = "🪪 My Profile Menu"
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

    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    await increment_step(state)
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
@router.message(F.text == MenuButton.HELP.value)
async def handle_help(message: Message, state: FSMContext, bot: Bot):
    await handle_menu_transition(
        user_choice=message.text,
        message=message,
        state=state,
        bot=bot,
        chat_id=message.chat.id,
        current_state=MenuStates.MAIN_MENU,
        new_state=MenuStates.HELP_SUBMENU,
        new_text="❓ Help",
        new_keyboard_func=get_help_menu
    )

# Обробник для меню "Help Submenu"
@router.message(MenuStates.HELP_SUBMENU)
async def handle_help_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    await handle_menu_transition(
        user_choice=user_choice,
        message=message,
        state=state,
        bot=bot,
        chat_id=message.chat.id,
        current_state=MenuStates.HELP_SUBMENU,
        new_state=MenuStates.HELP_SUBMENU,
        new_text="❓ Help",
        new_keyboard_func=get_help_menu
    )

# Обробник для кнопки "My Team"
@router.message(F.text == MenuButton.MY_TEAM.value)
async def handle_my_team(message: Message, state: FSMContext, bot: Bot):
    await handle_menu_transition(
        user_choice=message.text,
        message=message,
        state=state,
        bot=bot,
        chat_id=message.chat.id,
        current_state=MenuStates.MAIN_MENU,
        new_state=MenuStates.MY_TEAM_MENU,
        new_text=MY_TEAM_TEXT,
        new_keyboard_func=get_my_team_menu
    )

# Обробник для меню "My Team Menu"
@router.message(MenuStates.MY_TEAM_MENU)
async def handle_my_team_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    await handle_menu_transition(
        user_choice=user_choice,
        message=message,
        state=state,
        bot=bot,
        chat_id=message.chat.id,
        current_state=MenuStates.MY_TEAM_MENU,
        new_state=MenuStates.MY_TEAM_MENU,
        new_text=MY_TEAM_TEXT,  # Оновити відповідно до вибору
        new_keyboard_func=get_my_team_menu
    )

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

# Функція для налаштування обробників
def setup_missing_handlers(dp: Router):
    dp.include_router(router)
    # Якщо у вас є інші роутери, включіть їх тут, наприклад:
    # dp.include_router(profile_router)