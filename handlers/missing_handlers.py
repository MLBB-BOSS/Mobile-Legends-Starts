import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from aiogram.filters import Command

from states import MenuStates, increment_step
from keyboards.menus import (
    MenuButton,
    # Оскільки ми лишаємо get_generic_inline_keyboard для помилок і коротких інфо,
    # але основне меню беремо з ReplyKeyboardMarkup-функцій:
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

async def transition_state(state: FSMContext, new_state: MenuStates):
    """
    Допоміжна функція для очищення даних та встановлення нового стану.
    """
    await state.clear()
    await state.set_state(new_state)


# ------------------------------ CHALLENGES ------------------------------

@router.message(F.text == MenuButton.CHALLENGES.value)
async def handle_challenges(message: Message, state: FSMContext, bot: Bot):
    """
    Обробник для кнопки "Челенджі"
    """
    logger.info(f"User {message.from_user.id} selected Challenges")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Отримуємо з пам’яті bot_message_id (звичайне повідомлення) та interactive_message_id (інтерактивне/інлайн).
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Якщо немає потрібних повідомлень, показуємо помилку і повертаємося в MAIN_MENU
    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                # В даному випадку можна залишити інлайн клавіатуру-помилку
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(bot_message_id=main_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    # Відправляємо звичайне повідомлення з Reply-клавіатурою для "Челенджів"
    try:
        challenges_message = await bot.send_message(
            chat_id=message.chat.id,
            text=CHALLENGES_TEXT,
            reply_markup=get_challenges_menu()  # ReplyKeyboardMarkup
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

    # Прибираємо попереднє звичайне повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Оновлюємо інлайн-повідомлення (якщо воно було) якимось текстом, або робимо "заглушку"
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text="Челенджі меню",  # Просто показуємо, де зараз
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Переходимо до стану CHALLENGES_MENU
    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, MenuStates.CHALLENGES_MENU)


@router.message(MenuStates.CHALLENGES_MENU)
async def handle_challenges_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    """
    Обробник меню "Челенджі"
    """
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

    try:
        if new_main_keyboard:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=new_main_keyboard
            )
            new_bot_message_id = main_message.message_id
        else:
            # Якщо не вдалося визначити клавіатуру, надсилаємо Inline або None
            await bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=get_generic_inline_keyboard()
            )
            new_bot_message_id = bot_message_id
    except Exception as e:
        logger.error(f"Failed to send new Challenges menu: {e}")
        return

    # Видаляємо старе звичайне повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Оновлюємо інтерактивне повідомлення
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


# ------------------------------ GUIDES ------------------------------

@router.message(F.text == MenuButton.GUIDES.value)
async def handle_guides(message: Message, state: FSMContext, bot: Bot):
    """
    Обробник для кнопки "Гайди"
    """
    logger.info(f"User {message.from_user.id} selected Guides")
    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Аналогічна логіка, що й вище
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_ERROR_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(bot_message_id=main_message.message_id)
            await transition_state(state, MenuStates.MAIN_MENU)
        except Exception as e:
            logger.error(f"Failed to send main menu error message: {e}")
        return

    try:
        guides_message = await bot.send_message(
            chat_id=message.chat.id,
            text=GUIDES_TEXT,
            reply_markup=get_guides_menu()  # ReplyKeyboardMarkup
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

    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагуємо "інтерактивне" повідомлення (залишається як заглушка)
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text="Меню Гайдів",
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    await increment_step(state)
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, MenuStates.GUIDES_MENU)


@router.message(MenuStates.GUIDES_MENU)
async def handle_guides_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    """
    Обробник для меню "Guides Menu"
    """
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Guides Menu")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Та сама перевірка
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


# ------------------------------ BUST ------------------------------

@router.message(F.text == MenuButton.BUST.value)
async def handle_bust(message: Message, state: FSMContext, bot: Bot):
    ...
    # Аналогічно: відправляємо звичайне меню (Reply), редагуємо інтерактивне як заглушку.
    # Логіка така ж, як і для Guides / Challenges.
    # Залишивши код для прикладу – вище вже продемонстровано, як замінити.


@router.message(MenuStates.BUST_MENU)
async def handle_bust_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    ...
    # Аналогічно виправляємо під Reply-клавіатуру.


# ------------------------------ TEAMS ------------------------------

@router.message(F.text == MenuButton.TEAMS.value)
async def handle_teams(message: Message, state: FSMContext, bot: Bot):
    ...
    # Те саме для Команд


@router.message(MenuStates.TEAMS_MENU)
async def handle_teams_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    ...
    # Те саме для підменю команд


# ------------------------------ TRADING ------------------------------

@router.message(F.text == MenuButton.TRADING.value)
async def handle_trading(message: Message, state: FSMContext, bot: Bot):
    ...
    # Те саме


@router.message(MenuStates.TRADING_MENU)
async def handle_trading_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    ...
    # Те саме


# ------------------------------ SETTINGS ------------------------------

@router.message(F.text == MenuButton.SETTINGS.value)
async def handle_settings(message: Message, state: FSMContext, bot: Bot):
    ...
    # Аналогічно


@router.message(MenuStates.SETTINGS_SUBMENU)
async def handle_settings_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    ...
    # Аналогічно


# ------------------------------ SELECT LANGUAGE ------------------------------

@router.message(MenuStates.SELECT_LANGUAGE)
async def handle_select_language(message: Message, state: FSMContext, bot: Bot):
    ...
    # Аналогічно, залишається ReplyKeyboard.


# ------------------------------ CHANGE USERNAME ------------------------------

@router.message(MenuStates.CHANGE_USERNAME)
async def handle_change_username(message: Message, state: FSMContext, bot: Bot):
    ...
    # Аналогічно


# ------------------------------ HELP ------------------------------

@router.message(F.text == MenuButton.HELP.value)
async def handle_help(message: Message, state: FSMContext, bot: Bot):
    ...
    # Так само, приклад уже є вище


@router.message(MenuStates.HELP_SUBMENU)
async def handle_help_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    ...
    # Аналогічно


# ------------------------------ MY TEAM ------------------------------

@router.message(F.text == MenuButton.MY_TEAM.value)
async def handle_my_team(message: Message, state: FSMContext, bot: Bot):
    ...
    # Приклад аналогічний, все через ReplyKeyboard.


@router.message(MenuStates.MY_TEAM_MENU)
async def handle_my_team_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    ...
    # Аналогічно


# ------------------------------ ADVANCED TECHNIQUES ------------------------------

@router.message(F.text == MenuButton.ADVANCED_TECHNIQUES.value)
async def handle_advanced_techniques(message: Message, state: FSMContext, bot: Bot):
    ...
    # Відправити з ReplyKeyboard або get_generic_inline_keyboard, якщо це лише тимчасове інфо.


# ------------------------------ INSTRUCTIONS ------------------------------

@router.message(F.text == MenuButton.INSTRUCTIONS.value)
async def handle_instructions(message: Message, state: FSMContext, bot: Bot):
    ...
    # Теж саме


# ------------------------------ FAQ ------------------------------

@router.message(F.text == MenuButton.FAQ.value)
async def handle_faq(message: Message, state: FSMContext, bot: Bot):
    ...
    # Теж саме


# ------------------------------ HELP SUPPORT ------------------------------

@router.message(F.text == MenuButton.HELP_SUPPORT.value)
async def handle_help_support(message: Message, state: FSMContext, bot: Bot):
    ...
    # Теж саме


# ------------------------------ UPDATE ID ------------------------------

@router.message(F.text == MenuButton.UPDATE_ID.value)
async def handle_update_id(message: Message, state: FSMContext, bot: Bot):
    ...
    # Так само, все меню лишається ReplyKeyboard.


# ------------------------------ NOTIFICATIONS ------------------------------

@router.message(F.text == MenuButton.NOTIFICATIONS.value)
async def handle_notifications(message: Message, state: FSMContext, bot: Bot):
    ...
    # Аналогічно


# ------------------------------ SETUP MISSING HANDLERS ------------------------------

def setup_missing_handlers(dp: Router):
    """
    Функція для підключення цих хендлерів
    """
    dp.include_router(router)
    # Якщо треба, підключайте інші роутери