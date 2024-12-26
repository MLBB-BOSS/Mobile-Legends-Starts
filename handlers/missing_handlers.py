# handlers/missing_handlers.py

import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import Command

from states import MenuStates
from utils.state_utils import increment_step  # Новий шлях імпорту
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

# Допоміжна функція для переходу між станами без очищення даних
async def transition_state(state: FSMContext, new_state: MenuStates):
    await state.set_state(new_state)

# Уніфікована функція для відправки нового меню
async def send_new_menu(bot: Bot, chat_id: int, text: str, keyboard, state: FSMContext) -> int:
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
async def handle_error(bot: Bot, chat_id: int, error_message: str, state: FSMContext):
    try:
        await bot.send_message(chat_id=chat_id, text=error_message, reply_markup=get_generic_inline_keyboard())
    except Exception as e:
        logger.critical(f"Критична помилка при обробці помилки: {e}")
    await transition_state(state, MenuStates.MAIN_MENU)

# Уніфікована функція для обробки вибору назад
async def handle_back_action(bot: Bot, message: Message, state: FSMContext, new_state: MenuStates, new_text: str, new_keyboard):
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
@router.message(F.text == MenuButton.CHALLENGES.value, state=MenuStates.MAIN_MENU)
async def handle_challenges(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Challenges")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Отримуємо поточні дані стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Перевіряємо наявність необхідних повідомлень
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        await handle_error(bot, message.chat.id, MAIN_MENU_ERROR_TEXT, state)
        return

    # Відправка нового меню Challenges
    new_bot_message_id = await send_new_menu(bot, message.chat.id, CHALLENGES_TEXT, get_challenges_menu(), state)
    if not new_bot_message_id:
        return  # Якщо виникла помилка, обробка вже виконана у send_new_menu

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
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
        await handle_error(bot, message.chat.id, MAIN_MENU_ERROR_TEXT, state)
        return

    # Визначаємо новий текст та клавіатуру
    if user_choice == "➕ Додати Челендж":
        new_main_text = "Feature to add challenges is under development."
        new_main_keyboard = get_challenges_menu()
        new_state = MenuStates.CHALLENGES_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Main Navigation"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Оберіть розділ у навігації"
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_challenges_menu()
        new_state = MenuStates.CHALLENGES_MENU

    # Відправка нового меню
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Challenges menu: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text="Челенджі меню",
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обробник для кнопки "Guides"
@router.message(F.text == MenuButton.GUIDES.value, state=MenuStates.MAIN_MENU)
async def handle_guides(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Guides")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Отримуємо поточні дані стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Перевіряємо наявність необхідних повідомлень
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        await handle_error(bot, message.chat.id, MAIN_MENU_ERROR_TEXT, state)
        return

    # Відправка нового меню Guides
    new_bot_message_id = await send_new_menu(bot, message.chat.id, GUIDES_TEXT, get_guides_menu(), state)
    if not new_bot_message_id:
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
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
        await handle_error(bot, message.chat.id, MAIN_MENU_ERROR_TEXT, state)
        return

    # Визначаємо новий текст та клавіатуру
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
        new_main_keyboard = get_guides_menu()

    if user_choice != MenuButton.BACK.value:
        new_main_keyboard = get_guides_menu()
        new_state = MenuStates.GUIDES_MENU

    # Відправка нового меню
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Guides menu: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text=new_interactive_text if 'new_interactive_text' in locals() else "Меню Гайдів",
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обробник для кнопки "Bust"
@router.message(F.text == MenuButton.BUST.value, state=MenuStates.MAIN_MENU)
async def handle_bust(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Bust")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Отримуємо поточні дані стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Перевіряємо наявність необхідних повідомлень
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        await handle_error(bot, message.chat.id, MAIN_MENU_ERROR_TEXT, state)
        return

    # Відправка нового меню Bust
    new_bot_message_id = await send_new_menu(bot, message.chat.id, BUST_TEXT, get_bust_menu(), state)
    if not new_bot_message_id:
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
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
        await handle_error(bot, message.chat.id, MAIN_MENU_ERROR_TEXT, state)
        return

    # Визначаємо новий текст та клавіатуру
    if user_choice == "🔥 Підвищити Буст":
        new_main_text = "Feature to increase bust is under development."
        new_main_keyboard = get_bust_menu()
        new_state = MenuStates.BUST_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Main Navigation"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Оберіть розділ у навігації"
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_bust_menu()
        new_state = MenuStates.BUST_MENU

    # Відправка нового меню
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Bust menu: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text="Меню Bust",
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обробник для кнопки "Teams"
@router.message(F.text == MenuButton.TEAMS.value, state=MenuStates.MAIN_MENU)
async def handle_teams(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Teams")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Отримуємо поточні дані стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Перевіряємо наявність необхідних повідомлень
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        await handle_error(bot, message.chat.id, MAIN_MENU_ERROR_TEXT, state)
        return

    # Відправка нового меню Teams
    new_bot_message_id = await send_new_menu(bot, message.chat.id, TEAMS_TEXT, get_teams_menu(), state)
    if not new_bot_message_id:
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text="Меню Teams",
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану
    await increment_step(state)
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
        await handle_error(bot, message.chat.id, MAIN_MENU_ERROR_TEXT, state)
        return

    # Визначаємо новий текст та клавіатуру
    if user_choice == MenuButton.CREATE_TEAM.value:
        new_main_text = "Feature to create a team is under development."
        new_main_keyboard = get_teams_menu()
        new_state = MenuStates.TEAMS_MENU
    elif user_choice == MenuButton.VIEW_TEAMS.value:
        new_main_text = "Feature to view teams is under development."
        new_main_keyboard = get_teams_menu()
        new_state = MenuStates.TEAMS_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Main Navigation"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Оберіть розділ у навігації"
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_teams_menu()
        new_state = MenuStates.TEAMS_MENU

    # Відправка нового меню
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Teams menu: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text="Меню Teams",
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обробник для кнопки "Trading"
@router.message(F.text == MenuButton.TRADING.value, state=MenuStates.MAIN_MENU)
async def handle_trading(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Trading")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Отримуємо поточні дані стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Перевіряємо наявність необхідних повідомлень
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        await handle_error(bot, message.chat.id, MAIN_MENU_ERROR_TEXT, state)
        return

    # Відправка нового меню Trading
    new_bot_message_id = await send_new_menu(bot, message.chat.id, TRADING_TEXT, get_trading_menu(), state)
    if not new_bot_message_id:
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text="Меню Trading",
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану
    await increment_step(state)
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
        await handle_error(bot, message.chat.id, MAIN_MENU_ERROR_TEXT, state)
        return

    # Визначаємо новий текст та клавіатуру
    if user_choice == MenuButton.CREATE_TRADE.value:
        new_main_text = "Функція створення торгівлі ще в розробці!"
        new_main_keyboard = get_trading_menu()
        new_state = MenuStates.TRADING_MENU
    elif user_choice == MenuButton.VIEW_TRADES.value:
        new_main_text = "Ось всі доступні торгівлі:"
        new_main_keyboard = get_trading_menu()
        new_state = MenuStates.TRADING_MENU
    elif user_choice == MenuButton.MANAGE_TRADES.value:
        new_main_text = "Функція управління торгівлями ще в розробці!"
        new_main_keyboard = get_trading_menu()
        new_state = MenuStates.TRADING_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🏠 Main Navigation"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Оберіть розділ у навігації"
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_trading_menu()
        new_state = MenuStates.TRADING_MENU

    # Відправка нового меню
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Trading menu: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text="Меню Trading",
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обробник для кнопки "Settings"
@router.message(F.text == MenuButton.SETTINGS.value, state=MenuStates.MAIN_MENU)
async def handle_settings(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Settings")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Отримуємо поточні дані стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Перевіряємо наявність необхідних повідомлень
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        await handle_error(bot, message.chat.id, MAIN_MENU_ERROR_TEXT, state)
        return

    # Відправка нового меню Settings
    new_bot_message_id = await send_new_menu(bot, message.chat.id, "⚙️ Settings", get_settings_menu(), state)
    if not new_bot_message_id:
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text="⚙️ Settings Menu",
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану
    await increment_step(state)
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
        await handle_error(bot, message.chat.id, MAIN_MENU_ERROR_TEXT, state)
        return

    # Визначаємо новий текст та клавіатуру
    if user_choice == MenuButton.LANGUAGE.value:
        new_main_text = LANGUAGE_SELECTION_TEXT
        new_main_keyboard = get_language_menu()
        new_state = MenuStates.SELECT_LANGUAGE
    elif user_choice == MenuButton.CHANGE_USERNAME.value:
        new_main_text = "ℹ️ Enter new Username:"
        new_main_keyboard = ReplyKeyboardRemove()
        try:
            await bot.send_message(chat_id=message.chat.id, text=new_main_text, reply_markup=new_main_keyboard)
            await state.set_state(MenuStates.CHANGE_USERNAME)
            await increment_step(state)
        except Exception as e:
            logger.error(f"Failed to send Change Username prompt: {e}")
            await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)
        return
    elif user_choice == MenuButton.UPDATE_ID.value:
        new_main_text = UPDATE_ID_SUCCESS_TEXT
        new_main_keyboard = get_settings_menu()
        new_state = MenuStates.SETTINGS_SUBMENU
    elif user_choice == MenuButton.NOTIFICATIONS.value:
        new_main_text = NOTIFICATIONS_SETTINGS_TEXT
        new_main_keyboard = get_settings_menu()
        new_state = MenuStates.SETTINGS_SUBMENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🪪 My Profile"
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "🪪 My Profile Menu"
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_settings_menu()
        new_state = MenuStates.SETTINGS_SUBMENU

    # Визначення стану та тексту для редагування інтерактивного повідомлення
    if user_choice not in [MenuButton.LANGUAGE.value, MenuButton.CHANGE_USERNAME.value, 
                           MenuButton.UPDATE_ID.value, MenuButton.NOTIFICATIONS.value, MenuButton.BACK.value]:
        new_interactive_text = "⚙️ Settings Menu"

    # Відправка нового меню
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Settings menu: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення, якщо не відбувається зміна стану
    if user_choice not in [MenuButton.CHANGE_USERNAME.value]:
        await check_and_edit_message(
            bot=bot,
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            new_text=new_interactive_text if 'new_interactive_text' in locals() else "⚙️ Settings Menu",
            new_keyboard=get_generic_inline_keyboard(),
            state=state
        )

    # Оновлення стану та даних
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
    # Приклад:
    # user_id = message.from_user.id
    # async with db.begin():
    #     user = await db.execute(select(models.user.User).where(models.user.User.telegram_id == user_id))
    #     user = user.scalars().first()
    #     if user:
    #         user.language = selected_language
    #         await db.commit()
    #         response_text = f"Інтерфейс змінено на {selected_language}."
    #     else:
    #         response_text = "❌ Користувача не знайдено."

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
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)
        return

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
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)

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
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)
        return

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
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)

# Обробник для кнопки "Help"
@router.message(F.text == MenuButton.HELP.value, state=MenuStates.MAIN_MENU)
async def handle_help(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Help")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Отримуємо поточні дані стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Перевіряємо наявність необхідних повідомлень
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        await handle_error(bot, message.chat.id, MAIN_MENU_ERROR_TEXT, state)
        return

    # Відправка нового меню Help
    new_bot_message_id = await send_new_menu(bot, message.chat.id, "❓ Help", get_help_menu(), state)
    if not new_bot_message_id:
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text="❓ Help Menu",
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану
    await increment_step(state)
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
        await handle_error(bot, message.chat.id, MAIN_MENU_ERROR_TEXT, state)
        return

    # Визначаємо новий текст та клавіатуру
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
        new_state = MenuStates.HELP_SUBMENU

    if user_choice not in [MenuButton.BACK.value]:
        new_main_keyboard = get_help_menu()
        new_state = MenuStates.HELP_SUBMENU

    # Відправка нового меню
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Help menu: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення, якщо не відбувається зміна стану
    if user_choice not in [MenuButton.BACK.value]:
        await check_and_edit_message(
            bot=bot,
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            new_text="❓ Help Menu",
            new_keyboard=get_generic_inline_keyboard(),
            state=state
        )

    # Оновлення стану та даних
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обробник для кнопки "Help Support"
@router.message(F.text == MenuButton.HELP_SUPPORT.value, state=MenuStates.HELP_SUBMENU)
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
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)
        return

    # Повертаємося до меню Help Submenu
    try:
        help_submenu_message = await bot.send_message(
            chat_id=message.chat.id,
            text="❓ Help Menu",
            reply_markup=get_help_menu()
        )
        await state.update_data(bot_message_id=help_submenu_message.message_id)
        await increment_step(state)
        await transition_state(state, MenuStates.HELP_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Help Submenu after Help Support: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)

# Обробник для кнопки "Update ID"
@router.message(F.text == MenuButton.UPDATE_ID.value, state=MenuStates.SETTINGS_SUBMENU)
async def handle_update_id(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Update ID")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Тут реалізуйте логіку оновлення ID, наприклад, оновлення в базі даних
    # Приклад:
    # user_id = message.from_user.id
    # async with db.begin():
    #     user = await db.execute(select(models.user.User).where(models.user.User.telegram_id == user_id))
    #     user = user.scalars().first()
    #     if user:
    #         user.id = new_id  # Приклад оновлення
    #         await db.commit()
    #         response_text = UPDATE_ID_SUCCESS_TEXT
    #     else:
    #         response_text = "❌ Користувача не знайдено."

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
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)
        return

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
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)

# Обробник для кнопки "Notifications"
@router.message(F.text == MenuButton.NOTIFICATIONS.value, state=MenuStates.SETTINGS_SUBMENU)
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
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)
        return

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
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)

# Обробник для кнопки "Instructions"
@router.message(F.text == MenuButton.INSTRUCTIONS.value, state=MenuStates.MAIN_MENU)
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
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)

# Обробник для кнопки "FAQ"
@router.message(F.text == MenuButton.FAQ.value, state=MenuStates.MAIN_MENU)
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
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)

# Обробник для кнопки "Advanced Techniques"
@router.message(F.text == MenuButton.ADVANCED_TECHNIQUES.value, state=MenuStates.GUIDES_MENU)
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
    except Exception as e:
        logger.error(f"Failed to send Advanced Techniques info: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)

    # Можливо, потрібно встановити новий стан або залишити як є

# Обробник для кнопки "My Team"
@router.message(F.text == MenuButton.MY_TEAM.value, state=MenuStates.MAIN_MENU)
async def handle_my_team(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected My Team")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Отримуємо поточні дані стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Перевіряємо наявність необхідних повідомлень
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        await handle_error(bot, message.chat.id, MAIN_MENU_ERROR_TEXT, state)
        return

    # Відправка нового меню My Team
    new_bot_message_id = await send_new_menu(bot, message.chat.id, MY_TEAM_TEXT, get_my_team_menu(), state)
    if not new_bot_message_id:
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text="🪪 My Team Menu",
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану
    await increment_step(state)
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
        await handle_error(bot, message.chat.id, MAIN_MENU_ERROR_TEXT, state)
        return

    # Визначаємо новий текст та клавіатуру
    if user_choice == "➕ Створити Команду":
        new_main_text = "Feature to create a team is under development."
        new_main_keyboard = get_my_team_menu()
        new_state = MenuStates.MY_TEAM_MENU
    elif user_choice == "👀 Переглянути Команди":
        new_main_text = "Feature to view teams is under development."
        new_main_keyboard = get_my_team_menu()
        new_state = MenuStates.MY_TEAM_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🪪 My Profile"
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "🪪 My Profile Menu"
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_my_team_menu()
        new_state = MenuStates.MY_TEAM_MENU

    # Відправка нового меню
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new My Team menu: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text=new_interactive_text if 'new_interactive_text' in locals() else "🪪 My Team Menu",
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

# Обробник для кнопки "Language" у меню "Settings Submenu"
@router.message(F.text == MenuButton.LANGUAGE.value, state=MenuStates.SETTINGS_SUBMENU)
async def handle_language_selection(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Language")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Відправка меню вибору мови
    new_bot_message_id = await send_new_menu(bot, message.chat.id, LANGUAGE_SELECTION_TEXT, get_language_menu(), state)
    if not new_bot_message_id:
        return

    # Видалення старого повідомлення
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
            new_text="⚙️ Settings Menu",
            new_keyboard=get_generic_inline_keyboard(),
            state=state
        )

    # Оновлення стану
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, MenuStates.SELECT_LANGUAGE)

# Обробник для кнопки "Back" у різних меню
@router.message(F.text == MenuButton.BACK.value)
async def handle_back(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} selected Back")
    await safe_delete_message(bot, message.chat.id, message.message_id)

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
    await handle_back_action(bot, message, state, new_state, new_main_text, new_main_keyboard)

# Обробник для кнопки "Help Support" у різних меню
@router.message(F.text == MenuButton.HELP_SUPPORT.value, state=MenuStates.HELP_SUBMENU)
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
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)
        return

    # Повертаємося до меню Help Submenu
    try:
        help_submenu_message = await bot.send_message(
            chat_id=message.chat.id,
            text="❓ Help Menu",
            reply_markup=get_help_menu()
        )
        await state.update_data(bot_message_id=help_submenu_message.message_id)
        await increment_step(state)
        await transition_state(state, MenuStates.HELP_SUBMENU)
    except Exception as e:
        logger.error(f"Failed to send Help Submenu after Help Support: {e}")
        await handle_error(bot, message.chat.id, GENERIC_ERROR_MESSAGE_TEXT, state)

# Обробник для кнопки "My Profile" у меню "Back" дій
@router.message(F.text == "🪪 My Profile", state=MenuStates.BACK_FROM_PROFILE)
async def handle_my_profile_back(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"User {message.from_user.id} navigated back to My Profile")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Відправка меню профілю
    new_bot_message_id = await send_new_menu(bot, message.chat.id, "🪪 My Profile", get_profile_menu(), state)
    if not new_bot_message_id:
        return

    # Видалення старого повідомлення
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
            new_text="🪪 My Profile Menu",
            new_keyboard=get_generic_inline_keyboard(),
            state=state
        )

    # Оновлення стану
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, MenuStates.PROFILE_MENU)

# Функція для налаштування обробників
def setup_missing_handlers(dp: Router):
    dp.include_router(router)
    # Якщо у вас є інші роутери, включіть їх тут, наприклад:
    # dp.include_router(profile_router)