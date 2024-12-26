# handlers/missing_handlers.py

import logging
from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

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
from handlers.base import safe_delete_message, check_and_edit_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()

# Допоміжна функція для переходу між станами
async def transition_state(state: FSMContext, new_state: MenuStates):
    await state.set_state(new_state)

# Уніфікована функція для відправки нового меню
async def send_new_menu(bot, chat_id: int, text: str, keyboard, state: FSMContext) -> int:
    try:
        new_message = await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=keyboard
        )
        return new_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося надіслати меню: {e}")
        await handle_error(bot, chat_id, GENERIC_ERROR_MESSAGE_TEXT, state)
        return None

# Уніфікована функція для обробки помилок
async def handle_error(bot, chat_id: int, error_message: str, state: FSMContext):
    try:
        await bot.send_message(chat_id=chat_id, text=error_message, reply_markup=get_generic_inline_keyboard())
    except Exception as e:
        logger.critical(f"Критична помилка при обробці помилки: {e}")
    await transition_state(state, MenuStates.MAIN_MENU)

# Уніфікована функція для обробки вибору назад
async def handle_back_action(bot, message: Message, state: FSMContext, new_state: MenuStates, new_text: str, new_keyboard):
    try:
        new_bot_message_id = await send_new_menu(bot, message.chat.id, new_text, new_keyboard, state)
        if not new_bot_message_id:
            return

        data = await state.get_data()
        old_bot_message_id = data.get('bot_message_id')
        interactive_message_id = data.get('interactive_message_id')

        if old_bot_message_id:
            await safe_delete_message(bot, message.chat.id, old_bot_message_id)

        if interactive_message_id:
            await check_and_edit_message(
                bot=bot,
                chat_id=message.chat.id,
                message_id=interactive_message_id,
                new_text=new_text,
                new_keyboard=get_generic_inline_keyboard(),
                state=state
            )

        await increment_step(state)
        await state.update_data(bot_message_id=new_bot_message_id)
        await transition_state(state, new_state)
    except Exception as e:
        logger.error(f"Failed to handle back action: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)

# Обробник для кнопки "Challenges"
@router.message(F.text == MenuButton.CHALLENGES.value)
async def handle_challenges(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} selected Challenges")
    await safe_delete_message(message.bot, message.chat.id, message.message_id)

    # Отримуємо поточні дані стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Перевіряємо наявність необхідних повідомлень
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        await handle_error(message.bot, message.chat.id, MAIN_MENU_ERROR_TEXT, state)
        return

    # Відправка нового меню Challenges
    new_bot_message_id = await send_new_menu(message.bot, message.chat.id, CHALLENGES_TEXT, get_challenges_menu(), state)
    if not new_bot_message_id:
        return  # Якщо виникла помилка, обробка вже виконана у send_new_menu

    # Видалення старого повідомлення
    await safe_delete_message(message.bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=message.bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text="Челенджі меню",
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, MenuStates.CHALLENGES_MENU)

# Обробник для меню "Challenges Menu"
@router.message(StateFilter(MenuStates.CHALLENGES_MENU))
async def handle_challenges_menu_buttons(message: Message, state: FSMContext):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Challenges Menu")

    await safe_delete_message(message.bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        await handle_error(message.bot, message.chat.id, MAIN_MENU_ERROR_TEXT, state)
        return

    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = "Челенджі меню"
    new_state = MenuStates.CHALLENGES_MENU

    if user_choice == "➕ Додати Челендж":
        new_main_text = "Feature to add challenges is under development."
        new_main_keyboard = get_challenges_menu()
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Main Navigation"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Оберіть розділ у навігації"
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_challenges_menu()

    # Відправка нового меню
    try:
        if new_main_keyboard:
            main_message = await message.bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=new_main_keyboard
            )
            new_bot_message_id = main_message.message_id
        else:
            await message.bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=get_generic_inline_keyboard()
            )
            new_bot_message_id = bot_message_id
    except Exception as e:
        logger.error(f"Failed to send new Challenges menu: {e}")
        await handle_error(message.bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)
        return

    # Видалення старого повідомлення
    await safe_delete_message(message.bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=message.bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Аналогічні обробники для інших меню (Guides, Bust, Teams, Trading, Settings, Help, My Team)

# Обробник для кнопки "Guides"
@router.message(F.text == MenuButton.GUIDES.value)
async def handle_guides(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} selected Guides")
    await safe_delete_message(message.bot, message.chat.id, message.message_id)

    # Отримуємо поточні дані стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Перевіряємо наявність необхідних повідомлень
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        await handle_error(message.bot, message.chat.id, MAIN_MENU_ERROR_TEXT, state)
        return

    # Відправка нового меню Guides
    new_bot_message_id = await send_new_menu(message.bot, message.chat.id, GUIDES_TEXT, get_guides_menu(), state)
    if not new_bot_message_id:
        return

    # Видалення старого повідомлення
    await safe_delete_message(message.bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=message.bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text="Меню Гайдів",
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, MenuStates.GUIDES_MENU)

# Обробник для меню "Guides Menu"
@router.message(StateFilter(MenuStates.GUIDES_MENU))
async def handle_guides_menu_buttons(message: Message, state: FSMContext):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Guides Menu")

    await safe_delete_message(message.bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        await handle_error(message.bot, message.chat.id, MAIN_MENU_ERROR_TEXT, state)
        return

    new_main_text = ""
    new_main_keyboard = get_guides_menu()
    new_interactive_text = "Меню Гайдів"
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
        new_interactive_text = "Оберіть розділ у навігації"
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT

    # Відправка нового меню
    try:
        main_message = await message.bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Guides menu: {e}")
        await handle_error(message.bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)
        return

    # Видалення старого повідомлення
    await safe_delete_message(message.bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=message.bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Аналогічні обробники для Bust, Teams, Trading, Settings, Help, My Team

# Приклад обробника для кнопки "Bust"
@router.message(F.text == MenuButton.BUST.value)
async def handle_bust(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} selected Bust")
    await safe_delete_message(message.bot, message.chat.id, message.message_id)

    # Отримуємо поточні дані стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Перевіряємо наявність необхідних повідомлень
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        await handle_error(message.bot, message.chat.id, MAIN_MENU_ERROR_TEXT, state)
        return

    # Відправка нового меню Bust
    new_bot_message_id = await send_new_menu(message.bot, message.chat.id, BUST_TEXT, get_bust_menu(), state)
    if not new_bot_message_id:
        return

    # Видалення старого повідомлення
    await safe_delete_message(message.bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=message.bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text="Меню Bust",
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, MenuStates.BUST_MENU)

# Обробник для меню "Bust Menu"
@router.message(StateFilter(MenuStates.BUST_MENU))
async def handle_bust_menu_buttons(message: Message, state: FSMContext):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Bust Menu")

    await safe_delete_message(message.bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        await handle_error(message.bot, message.chat.id, MAIN_MENU_ERROR_TEXT, state)
        return

    new_main_text = ""
    new_main_keyboard = get_bust_menu()
    new_interactive_text = "Меню Bust"
    new_state = MenuStates.BUST_MENU

    if user_choice == "🔥 Підвищити Буст":
        new_main_text = "Feature to increase bust is under development."
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Main Navigation"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Оберіть розділ у навігації"
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT

    # Відправка нового меню
    try:
        if new_main_keyboard:
            main_message = await message.bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=new_main_keyboard
            )
            new_bot_message_id = main_message.message_id
        else:
            await message.bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=get_generic_inline_keyboard()
            )
            new_bot_message_id = bot_message_id
    except Exception as e:
        logger.error(f"Failed to send new Bust menu: {e}")
        await handle_error(message.bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)
        return

    # Видалення старого повідомлення
    await safe_delete_message(message.bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=message.bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Повторіть аналогічну структуру для обробників "Teams", "Trading", "Settings", "Help", "My Team"

# Обробник для кнопки "Back" у різних меню
@router.message(F.text == MenuButton.BACK.value)
async def handle_back(message: Message, state: FSMContext):
    logger.info(f"User {message.from_user.id} selected Back")
    await safe_delete_message(message.bot, message.chat.id, message.message_id)

    # Отримуємо попередній стан з даних (можливо, потрібно зберігати його раніше)
    data = await state.get_data()
    previous_state = data.get('previous_state', MenuStates.MAIN_MENU)

    if previous_state == MenuStates.NAVIGATION_MENU:
        new_main_text = "🏠 Main Navigation"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Оберіть розділ у навігації"
        new_state = MenuStates.NAVIGATION_MENU
    elif previous_state == MenuStates.CHALLENGES_MENU:
        new_main_text = CHALLENGES_TEXT
        new_main_keyboard = get_challenges_menu()
        new_interactive_text = "Челенджі меню"
        new_state = MenuStates.CHALLENGES_MENU
    elif previous_state == MenuStates.GUIDES_MENU:
        new_main_text = GUIDES_TEXT
        new_main_keyboard = get_guides_menu()
        new_interactive_text = "Меню Гайдів"
        new_state = MenuStates.GUIDES_MENU
    elif previous_state == MenuStates.BUST_MENU:
        new_main_text = BUST_TEXT
        new_main_keyboard = get_bust_menu()
        new_interactive_text = "Меню Bust"
        new_state = MenuStates.BUST_MENU
    elif previous_state == MenuStates.TEAMS_MENU:
        new_main_text = TEAMS_TEXT
        new_main_keyboard = get_teams_menu()
        new_interactive_text = "Меню Teams"
        new_state = MenuStates.TEAMS_MENU
    elif previous_state == MenuStates.TRADING_MENU:
        new_main_text = TRADING_TEXT
        new_main_keyboard = get_trading_menu()
        new_interactive_text = "Меню Trading"
        new_state = MenuStates.TRADING_MENU
    elif previous_state == MenuStates.SETTINGS_SUBMENU:
        new_main_text = "⚙️ Settings"
        new_main_keyboard = get_settings_menu()
        new_interactive_text = "⚙️ Settings Menu"
        new_state = MenuStates.SETTINGS_SUBMENU
    elif previous_state == MenuStates.HELP_SUBMENU:
        new_main_text = "❓ Help"
        new_main_keyboard = get_help_menu()
        new_interactive_text = "❓ Help Menu"
        new_state = MenuStates.HELP_SUBMENU
    elif previous_state == MenuStates.MY_TEAM_MENU:
        new_main_text = "🪪 My Team"
        new_main_keyboard = get_my_team_menu()
        new_interactive_text = "🪪 My Team Menu"
        new_state = MenuStates.MY_TEAM_MENU
    else:
        # Повернення до головного меню
        new_main_text = "🏠 Main Navigation"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Оберіть розділ у навігації"
        new_state = MenuStates.NAVIGATION_MENU

    # Використовуємо допоміжну функцію для обробки повернення
    await handle_back_action(message.bot, message, state, new_state, new_main_text, new_main_keyboard)

# Функція для налаштування обробників
def setup_missing_handlers(dp: Router):
    dp.include_router(router)
    # Якщо у вас є інші роутери, включіть їх тут, наприклад:
    # dp.include_router(profile_router)