# handlers/base.py

import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.menus import (
    MenuButton,
    menu_button_to_class,
    get_main_menu,
    get_navigation_menu,
    get_profile_menu,
    get_heroes_menu,
    get_hero_class_menu,
    get_guides_menu,
    get_counter_picks_menu,
    get_builds_menu,
    get_voting_menu,
    get_statistics_menu,
    get_achievements_menu,
    get_settings_menu,
    get_feedback_menu,
    get_help_menu,
    get_tournaments_menu,
    get_meta_menu,
    get_m6_menu,
    get_gpt_menu,  # Додано функцію для GPT меню
    heroes_by_class,
)
from keyboards.inline_menus import (
    get_generic_inline_keyboard,
    get_intro_page_1_keyboard,
    get_intro_page_2_keyboard,
    get_intro_page_3_keyboard
)

# Importing text constants
from texts import (
    INTRO_PAGE_1_TEXT,
    INTRO_PAGE_2_TEXT,
    INTRO_PAGE_3_TEXT,
    MAIN_MENU_TEXT,
    MAIN_MENU_DESCRIPTION,
    MAIN_MENU_ERROR_TEXT,
    NAVIGATION_MENU_TEXT,
    NAVIGATION_INTERACTIVE_TEXT,
    PROFILE_MENU_TEXT,
    PROFILE_INTERACTIVE_TEXT,
    UNKNOWN_COMMAND_TEXT,
    ERROR_MESSAGE_TEXT,
    HEROES_MENU_TEXT,
    HEROES_INTERACTIVE_TEXT,
    HERO_CLASS_MENU_TEXT,
    HERO_CLASS_INTERACTIVE_TEXT,
    GUIDES_MENU_TEXT,
    GUIDES_INTERACTIVE_TEXT,
    NEW_GUIDES_TEXT,
    POPULAR_GUIDES_TEXT,
    BEGINNER_GUIDES_TEXT,
    ADVANCED_TECHNIQUES_TEXT,
    TEAMPLAY_GUIDES_TEXT,
    COUNTER_PICKS_MENU_TEXT,
    COUNTER_PICKS_INTERACTIVE_TEXT,
    COUNTER_SEARCH_TEXT,
    COUNTER_LIST_TEXT,
    BUILDS_MENU_TEXT,
    BUILDS_INTERACTIVE_TEXT,
    CREATE_BUILD_TEXT,
    MY_BUILDS_TEXT,
    POPULAR_BUILDS_TEXT,
    VOTING_MENU_TEXT,
    VOTING_INTERACTIVE_TEXT,
    CURRENT_VOTES_TEXT,
    MY_VOTES_TEXT,
    SUGGEST_TOPIC_TEXT,
    SUGGESTION_RESPONSE_TEXT,
    STATISTICS_MENU_TEXT,
    STATISTICS_INTERACTIVE_TEXT,
    ACTIVITY_TEXT,
    RANKING_TEXT,
    GAME_STATS_TEXT,
    ACHIEVEMENTS_MENU_TEXT,
    ACHIEVEMENTS_INTERACTIVE_TEXT,
    BADGES_TEXT,
    PROGRESS_TEXT,
    TOURNAMENT_STATS_TEXT,
    AWARDS_TEXT,
    SETTINGS_MENU_TEXT,
    SETTINGS_INTERACTIVE_TEXT,
    LANGUAGE_TEXT,
    CHANGE_USERNAME_TEXT,
    UPDATE_ID_TEXT,
    NOTIFICATIONS_TEXT,
    FEEDBACK_MENU_TEXT,
    FEEDBACK_INTERACTIVE_TEXT,
    SEND_FEEDBACK_TEXT,
    REPORT_BUG_TEXT,
    FEEDBACK_RECEIVED_TEXT,
    BUG_REPORT_RECEIVED_TEXT,
    HELP_MENU_TEXT,
    HELP_INTERACTIVE_TEXT,
    INSTRUCTIONS_TEXT,
    FAQ_TEXT,
    HELP_SUPPORT_TEXT,
    GENERIC_ERROR_MESSAGE_TEXT,
    USE_BUTTON_NAVIGATION_TEXT,
    SEARCH_HERO_RESPONSE_TEXT,
    CHANGE_USERNAME_RESPONSE_TEXT,
    MLS_BUTTON_RESPONSE_TEXT,
    UNHANDLED_INLINE_BUTTON_TEXT,
    MAIN_MENU_BACK_TO_PROFILE_TEXT,
    TOURNAMENT_CREATE_TEXT,
    TOURNAMENT_VIEW_TEXT,
    META_HERO_LIST_TEXT,
    META_RECOMMENDATIONS_TEXT,
    META_UPDATES_TEXT,
    M6_INFO_TEXT,
    M6_STATS_TEXT,
    M6_NEWS_TEXT,
    MAIN_MENU_DESCRIPTION,
)

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Ініціалізація роутера
router = Router()

# Визначення станів для FSM
class MenuStates(StatesGroup):
    INTRO_PAGE_1 = State()
    INTRO_PAGE_2 = State()
    INTRO_PAGE_3 = State()
    MAIN_MENU = State()
    NAVIGATION_MENU = State()
    HEROES_MENU = State()
    HERO_CLASS_MENU = State()
    GUIDES_MENU = State()
    COUNTER_PICKS_MENU = State()
    BUILDS_MENU = State()
    VOTING_MENU = State()
    PROFILE_MENU = State()
    STATISTICS_MENU = State()
    ACHIEVEMENTS_MENU = State()
    SETTINGS_MENU = State()
    FEEDBACK_MENU = State()
    HELP_MENU = State()
    SEARCH_HERO = State()
    SUGGEST_TOPIC = State()
    CHANGE_USERNAME = State()
    RECEIVE_FEEDBACK = State()
    REPORT_BUG = State()
    TOURNAMENTS_MENU = State()
    META_MENU = State()
    M6_MENU = State()
    GPT_MENU = State()  # Додано цей рядок

# ======================
# Основні Хендлери
# ======================

# 1. Обробка команди /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    user_first_name = message.from_user.first_name
    logger.info(f"User {message.from_user.id} invoked /start")

    # Видалити повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Failed to delete /start message: {e}")

    # Встановити стан INTRO_PAGE_1
    await state.set_state(MenuStates.INTRO_PAGE_1)

    # Надіслати перше інструктивне повідомлення з кнопкою 'Next'
    try:
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=INTRO_PAGE_1_TEXT,
            parse_mode="HTML",
            reply_markup=get_intro_page_1_keyboard()
        )
        # Зберегти ID повідомлення для подальшого редагування
        await state.update_data(interactive_message_id=interactive_message.message_id)
    except Exception as e:
        logger.error(f"Failed to send intro page 1: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT
        )
        return

# 2. Обробка кнопки 'Next' на першій інструктивній сторінці
@router.callback_query(F.data == "intro_next_1")
async def handle_intro_next_1(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # Отримати ID інтерактивного повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if not interactive_message_id:
        logger.error("Interactive message ID not found for intro_next_1")
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT
        )
        await callback.answer()
        return

    # Редагувати повідомлення на другу інструктивну сторінку
    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=INTRO_PAGE_2_TEXT,
            parse_mode="HTML",
            reply_markup=get_intro_page_2_keyboard()
        )
    except Exception as e:
        logger.error(f"Failed to edit intro page 1 to page 2: {e}")
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT
        )
        await callback.answer()
        return

    # Оновити стан
    await state.set_state(MenuStates.INTRO_PAGE_2)
    await callback.answer()

# 3. Обробка кнопки 'Next' на другій інструктивній сторінці
@router.callback_query(F.data == "intro_next_2")
async def handle_intro_next_2(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # Отримати ID інтерактивного повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if not interactive_message_id:
        logger.error("Interactive message ID not found for intro_next_2")
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT
        )
        await callback.answer()
        return

    # Редагувати повідомлення на третю інструктивну сторінку
    try:
        # Перед відправкою INTRO_PAGE_3_TEXT, необхідно мати дані користувача: {username}, {level}, {rating}, {achievements_count}
        # Для прикладу, ми використовуємо заглушки. Ви повинні замінити їх на реальні дані з вашої бази даних або іншого джерела.
        user_data = {
            'username': "Гравець123",
            'level': "10",
            'rating': "1500",
            'achievements_count': "5"
        }

        formatted_intro_page_3 = INTRO_PAGE_3_TEXT.format(
            username=user_data['username'],
            level=user_data['level'],
            rating=user_data['rating'],
            achievements_count=user_data['achievements_count']
        )

        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=formatted_intro_page_3,
            parse_mode="HTML",
            reply_markup=get_intro_page_3_keyboard()
        )
    except Exception as e:
        logger.error(f"Failed to edit intro page 2 to page 3: {e}")
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT
        )
        await callback.answer()
        return

    # Оновити стан
    await state.set_state(MenuStates.INTRO_PAGE_3)
    await callback.answer()

# 4. Обробка кнопки 'Розпочати' на третій інструктивній сторінці
@router.callback_query(F.data == "intro_start")
async def handle_intro_start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_first_name = callback.from_user.first_name

    # Надіслати основне меню з клавіатурою
    try:
        main_menu_message = await bot.send_message(
            chat_id=callback.message.chat.id,
            text=MAIN_MENU_TEXT.format(user_first_name=user_first_name),
            reply_markup=get_main_menu()
        )
        # Зберегти ID повідомлення
        await state.update_data(bot_message_id=main_menu_message.message_id)
    except Exception as e:
        logger.error(f"Failed to send main menu: {e}")
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT
        )
        await callback.answer()
        return

    # Редагувати інтерактивне повідомлення з описом основного меню
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if interactive_message_id:
        try:
            await bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=interactive_message_id,
                text=MAIN_MENU_DESCRIPTION,
                parse_mode="HTML",
                reply_markup=get_generic_inline_keyboard()
            )
        except Exception as e:
            logger.error(f"Failed to edit interactive message to main menu description: {e}")
            # Надіслати нове інтерактивне повідомлення, якщо редагування не вдалося
            try:
                new_interactive_message = await bot.send_message(
                    chat_id=callback.message.chat.id,
                    text=MAIN_MENU_DESCRIPTION,
                    reply_markup=get_generic_inline_keyboard()
                )
                await state.update_data(interactive_message_id=new_interactive_message.message_id)
            except Exception as ex:
                logger.error(f"Failed to send new interactive message for main menu description: {ex}")
    else:
        # Якщо ID інтерактивного повідомлення не знайдено, надіслати нове
        try:
            new_interactive_message = await bot.send_message(
                chat_id=callback.message.chat.id,
                text=MAIN_MENU_DESCRIPTION,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_interactive_message.message_id)
        except Exception as e:
            logger.error(f"Failed to send interactive message for main menu description: {e}")

    # Встановити стан на MAIN_MENU
    await state.set_state(MenuStates.MAIN_MENU)
    await callback.answer()

# 5. Обробка вибору кнопок у головному меню
@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Main Menu")

    # Видалити повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Failed to delete user message in main menu: {e}")

    # Отримати ID повідомлення бота та інтерактивного повідомлення
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id or interactive_message_id not found in Main Menu handler")
        await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначити, яке меню обрати залежно від вибору користувача
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = None

    if user_choice == MenuButton.NAVIGATION.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    elif user_choice == MenuButton.PROFILE.value:
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    elif user_choice == MenuButton.GPT.value:
        new_main_text = "🤖 GPT Menu"  # Замінити на відповідний текст з texts.py
        new_main_keyboard = get_gpt_menu()
        new_interactive_text = "Welcome to the GPT Menu. Choose an option below:"
        new_state = MenuStates.GPT_MENU
    else:
        # Невідомий вибір у головному меню
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Невідома команда."
        new_state = MenuStates.MAIN_MENU

    # Надіслати нове повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new main menu message: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT
        )
        return

    # Видалити попереднє повідомлення бота
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Failed to delete previous bot message in Main Menu: {e}")

    # Оновити ID повідомлення бота в стані
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагувати інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    except Exception as e:
        logger.error(f"Failed to edit interactive message in Main Menu: {e}")
        # Надіслати нове інтерактивне повідомлення, якщо редагування не вдалося
        try:
            new_interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_interactive_message.message_id)
        except Exception as ex:
            logger.error(f"Failed to send new interactive message in Main Menu: {ex}")

    # Оновити стан користувача
    await state.set_state(new_state)

# 6. Обробка вибору кнопок у меню "Навігація"
@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Navigation Menu")

    # Видалити повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Failed to delete user message in Navigation Menu: {e}")

    # Отримати ID повідомлення бота та інтерактивного повідомлення
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id or interactive_message_id not found in Navigation Menu handler")
        await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначити, яке меню обрати залежно від вибору користувача
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = None

    if user_choice == MenuButton.HEROES.value:
        new_main_text = HEROES_MENU_TEXT
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = HEROES_INTERACTIVE_TEXT
        new_state = MenuStates.HEROES_MENU
    elif user_choice == MenuButton.GUIDES.value:
        new_main_text = GUIDES_MENU_TEXT
        new_main_keyboard = get_guides_menu()
        new_interactive_text = GUIDES_INTERACTIVE_TEXT
        new_state = MenuStates.GUIDES_MENU
    elif user_choice == MenuButton.COUNTER_PICKS.value:
        new_main_text = COUNTER_PICKS_MENU_TEXT
        new_main_keyboard = get_counter_picks_menu()
        new_interactive_text = COUNTER_PICKS_INTERACTIVE_TEXT
        new_state = MenuStates.COUNTER_PICKS_MENU
    elif user_choice == MenuButton.BUILDS.value:
        new_main_text = BUILDS_MENU_TEXT
        new_main_keyboard = get_builds_menu()
        new_interactive_text = BUILDS_INTERACTIVE_TEXT
        new_state = MenuStates.BUILDS_MENU
    elif user_choice == MenuButton.VOTING.value:
        new_main_text = VOTING_MENU_TEXT
        new_main_keyboard = get_voting_menu()
        new_interactive_text = VOTING_INTERACTIVE_TEXT
        new_state = MenuStates.VOTING_MENU
    elif user_choice == MenuButton.M6.value:
        new_main_text = M6_INFO_TEXT  # Або відповідний текст з texts.py
        new_main_keyboard = get_m6_menu()
        new_interactive_text = "🔥 Welcome to the M6 Menu!"
        new_state = MenuStates.M6_MENU
    elif user_choice == MenuButton.GPT.value:
        new_main_text = "🤖 GPT Menu"  # Замінити на відповідний текст з texts.py
        new_main_keyboard = get_gpt_menu()
        new_interactive_text = "Welcome to the GPT Menu. Choose an option below:"
        new_state = MenuStates.GPT_MENU
    elif user_choice == MenuButton.META.value:
        new_main_text = META_HERO_LIST_TEXT  # Або відповідний текст з texts.py
        new_main_keyboard = get_meta_menu()
        new_interactive_text = "📊 Welcome to the META Menu!"
        new_state = MenuStates.META_MENU
    elif user_choice == MenuButton.TOURNAMENTS.value:
        new_main_text = TOURNAMENTS_MENU_TEXT  # Або відповідний текст з texts.py
        new_main_keyboard = get_tournaments_menu()
        new_interactive_text = "🏆 Welcome to the Tournaments Menu!"
        new_state = MenuStates.TOURNAMENTS_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
    else:
        # Невідомий вибір у меню "Навігація"
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Невідома команда."
        new_state = MenuStates.NAVIGATION_MENU

    # Надіслати нове повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Navigation Menu message: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT
        )
        return

    # Видалити попереднє повідомлення бота
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Failed to delete previous bot message in Navigation Menu: {e}")

    # Оновити ID повідомлення бота в стані
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагувати інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    except Exception as e:
        logger.error(f"Failed to edit interactive message in Navigation Menu: {e}")
        # Надіслати нове інтерактивне повідомлення, якщо редагування не вдалося
        try:
            new_interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_interactive_message.message_id)
        except Exception as ex:
            logger.error(f"Failed to send new interactive message in Navigation Menu: {ex}")

    # Оновити стан користувача
    await state.set_state(new_state)

# 7. Обробка вибору кнопок у меню "Персонажі"
@router.message(MenuStates.HEROES_MENU)
async def handle_heroes_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Heroes Menu")

    # Видалити повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Failed to delete user message in Heroes Menu: {e}")

    # Отримати ID повідомлення бота та інтерактивного повідомлення
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id or interactive_message_id not found in Heroes Menu handler")
        await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначити, яке меню обрати залежно від вибору користувача
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = None

    if user_choice in menu_button_to_class:
        hero_class = menu_button_to_class[user_choice]
        new_main_text = HERO_CLASS_MENU_TEXT.format(hero_class=hero_class)
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = HERO_CLASS_INTERACTIVE_TEXT.format(hero_class=hero_class)
        new_state = MenuStates.HERO_CLASS_MENU
        await state.update_data(hero_class=hero_class)
    elif user_choice == MenuButton.SEARCH_HERO.value:
        new_main_text = SEARCH_HERO_RESPONSE_TEXT.format(hero_name="")
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "🔎 Введіть назву героя, якого ви хочете знайти."
        new_state = MenuStates.SEARCH_HERO
    elif user_choice == MenuButton.COMPARISON.value:
        new_main_text = "⚖️ Функція порівняння героїв ще розробляється."
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = "Функція порівняння героїв ще не доступна."
        new_state = MenuStates.HEROES_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        # Невідомий вибір у меню "Персонажі"
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = "Невідома команда."
        new_state = MenuStates.HEROES_MENU

    # Надіслати нове повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Heroes Menu message: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT
        )
        return

    # Видалити попереднє повідомлення бота
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Failed to delete previous bot message in Heroes Menu: {e}")

    # Оновити ID повідомлення бота в стані
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагувати інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    except Exception as e:
        logger.error(f"Failed to edit interactive message in Heroes Menu: {e}")
        # Надіслати нове інтерактивне повідомлення, якщо редагування не вдалося
        try:
            new_interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_interactive_message.message_id)
        except Exception as ex:
            logger.error(f"Failed to send new interactive message in Heroes Menu: {ex}")

    # Оновити стан користувача
    await state.set_state(new_state)

# 8. Обробка вибору кнопок у меню класу героїв
@router.message(MenuStates.HERO_CLASS_MENU)
async def handle_hero_class_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    # Отримати клас героя з даних стану
    data = await state.get_data()
    hero_class = data.get('hero_class', 'Unknown')
    logger.info(f"User {message.from_user.id} selected '{user_choice}' in Hero Class Menu for class {hero_class}")

    # Видалити повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Failed to delete user message in Hero Class Menu: {e}")

    # Отримати ID повідомлення бота та інтерактивного повідомлення
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id or interactive_message_id not found in Hero Class Menu handler")
        await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Перевірити, чи користувач обрав героя або повернувся
    if user_choice in heroes_by_class.get(hero_class, []):
        # Обробити вибір конкретного героя
        hero_name = user_choice
        # Припустимо, що функція get_hero_details_menu(hero_name) повертає текст з деталями героя
        # Вам потрібно реалізувати цю функцію відповідно до вашої логіки
        hero_details = f"**{hero_name}**\n\n📜 Біографія: ...\n⚔️ Навички: ...\n🛠️ Оптимальні білди: ...\n🎮 Ролі в команді: ...\n📊 Статистика: ..."

        # Надіслати детальну інформацію про героя
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=hero_details,
                parse_mode="HTML",
                reply_markup=get_hero_class_menu(hero_class)  # Можна замінити на відповідну клавіатуру
            )
        except Exception as e:
            logger.error(f"Failed to send hero details for {hero_name}: {e}")
            await bot.send_message(
                chat_id=message.chat.id,
                text=GENERIC_ERROR_MESSAGE_TEXT
            )

        # Залишити користувача в тому ж меню
        await state.set_state(MenuStates.HERO_CLASS_MENU)
        return
    elif user_choice == MenuButton.BACK.value:
        # Повернутися до меню "Персонажі"
        new_main_text = HEROES_MENU_TEXT
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = HEROES_INTERACTIVE_TEXT
        new_state = MenuStates.HEROES_MENU
    else:
        # Невідомий вибір у меню класу героїв
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = f"Hero Class Menu for {hero_class}"
        new_state = MenuStates.HERO_CLASS_MENU

    # Надіслати нове повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Hero Class Menu message: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT
        )
        return

    # Видалити попереднє повідомлення бота
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Failed to delete previous bot message in Hero Class Menu: {e}")

    # Оновити ID повідомлення бота в стані
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагувати інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    except Exception as e:
        logger.error(f"Failed to edit interactive message in Hero Class Menu: {e}")
        # Надіслати нове інтерактивне повідомлення, якщо редагування не вдалося
        try:
            new_interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_interactive_message.message_id)
        except Exception as ex:
            logger.error(f"Failed to send new interactive message in Hero Class Menu: {ex}")

    # Оновити стан користувача
    await state.set_state(new_state)

# 9. Обробка пошуку героя
@router.message(MenuStates.SEARCH_HERO)
async def handle_search_hero(message: Message, state: FSMContext, bot: Bot):
    hero_name = message.text.strip()
    logger.info(f"User {message.from_user.id} is searching for hero: {hero_name}")

    # Видалити повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Failed to delete user message in Search Hero: {e}")

    # Додати логіку пошуку героя тут
    # Наприклад, звернутися до бази даних або API для отримання інформації про героя

    if hero_name:
        # Приклад відповіді (замінити на реальну інформацію)
        hero_info = f"**{hero_name}**\n\n📜 Біографія: ...\n⚔️ Навички: ...\n🛠️ Оптимальні білди: ...\n🎮 Ролі в команді: ...\n📊 Статистика: ..."
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=hero_info,
                parse_mode="HTML",
                reply_markup=get_generic_inline_keyboard()
            )
        except Exception as e:
            logger.error(f"Failed to send hero info for {hero_name}: {e}")
            await bot.send_message(
                chat_id=message.chat.id,
                text=GENERIC_ERROR_MESSAGE_TEXT
            )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="🔎 Будь ласка, введіть назву героя, якого ви хочете знайти.",
            reply_markup=get_generic_inline_keyboard()
        )

    # Повернутися до меню "Персонажі"
    await state.set_state(MenuStates.HEROES_MENU)

# 10. Обробка голосування
@router.message(MenuStates.VOTING_MENU)
async def handle_voting_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Voting Menu")

    # Видалити повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Failed to delete user message in Voting Menu: {e}")

    # Отримати ID повідомлення бота та інтерактивного повідомлення
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id or interactive_message_id not found in Voting Menu handler")
        await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначити, яку дію обрати залежно від вибору користувача
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = None

    if user_choice == MenuButton.CURRENT_VOTES.value:
        new_main_text = CURRENT_VOTES_TEXT
        # Додати клавіатуру для поточних опитувань, якщо є
        new_main_keyboard = get_voting_menu()  # Можна замінити на відповідну клавіатуру
        new_interactive_text = "📍 Поточні Опитування відображаються нижче."
        new_state = MenuStates.VOTING_MENU
    elif user_choice == MenuButton.MY_VOTES.value:
        new_main_text = MY_VOTES_TEXT
        # Додати клавіатуру для моїх голосувань, якщо є
        new_main_keyboard = get_voting_menu()  # Можна замінити на відповідну клавіатуру
        new_interactive_text = "📋 Ваші Голосування відображаються нижче."
        new_state = MenuStates.VOTING_MENU
    elif user_choice == MenuButton.SUGGEST_TOPIC.value:
        new_main_text = SUGGEST_TOPIC_TEXT
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "➕ Будь ласка, введіть тему, яку ви хочете запропонувати."
        new_state = MenuStates.SUGGEST_TOPIC
    elif user_choice == MenuButton.BACK.value:
        # Повернутися до меню "Навігація"
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        # Невідомий вибір у меню "Голосування"
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_voting_menu()
        new_interactive_text = "Невідома команда."
        new_state = MenuStates.VOTING_MENU

    # Надіслати нове повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Voting Menu message: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT
        )
        return

    # Видалити попереднє повідомлення бота
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Failed to delete previous bot message in Voting Menu: {e}")

    # Оновити ID повідомлення бота в стані
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагувати інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    except Exception as e:
        logger.error(f"Failed to edit interactive message in Voting Menu: {e}")
        # Надіслати нове інтерактивне повідомлення, якщо редагування не вдалося
        try:
            new_interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_interactive_message.message_id)
        except Exception as ex:
            logger.error(f"Failed to send new interactive message in Voting Menu: {ex}")

    # Оновити стан користувача
    await state.set_state(new_state)

# 11. Обробка створення турніру
@router.message(MenuStates.TOURNAMENTS_MENU)
async def handle_tournaments_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected '{user_choice}' in Tournaments Menu")

    # Видалити повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Failed to delete user message in Tournaments Menu: {e}")

    # Отримати ID повідомлення бота та інтерактивного повідомлення
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id or interactive_message_id not found in Tournaments Menu handler")
        await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначити, яку дію обрати залежно від вибору користувача
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = None

    if user_choice == MenuButton.CREATE_TOURNAMENT.value:
        new_main_text = TOURNAMENT_CREATE_TEXT
        new_interactive_text = "🏗️ Створення нового турніру..."
        # Додати клавіатуру для створення турніру, якщо є
        new_main_keyboard = get_tournaments_menu()
        new_state = MenuStates.TOURNAMENTS_MENU  # Можливо, створити новий стан для вводу деталей
    elif user_choice == MenuButton.VIEW_TOURNAMENTS.value:
        new_main_text = TOURNAMENT_VIEW_TEXT
        new_interactive_text = "📄 Перегляд існуючих турнірів..."
        # Додати клавіатуру для перегляду турнірів, якщо є
        new_main_keyboard = get_tournaments_menu()
        new_state = MenuStates.TOURNAMENTS_MENU
    elif user_choice == MenuButton.BACK.value:
        # Повернутися до меню "Навігація"
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        # Невідомий вибір у меню "Турніри"
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_tournaments_menu()
        new_interactive_text = "Невідома команда."
        new_state = MenuStates.TOURNAMENTS_MENU

    # Надіслати нове повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Tournaments Menu message: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT
        )
        return

    # Видалити попереднє повідомлення бота
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Failed to delete previous bot message in Tournaments Menu: {e}")

    # Оновити ID повідомлення бота в стані
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагувати інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    except Exception as e:
        logger.error(f"Failed to edit interactive message in Tournaments Menu: {e}")
        # Надіслати нове інтерактивне повідомлення, якщо редагування не вдалося
        try:
            new_interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_interactive_message.message_id)
        except Exception as ex:
            logger.error(f"Failed to send new interactive message in Tournaments Menu: {ex}")

    # Оновити стан користувача
    await state.set_state(new_state)

# 12. Обробка META Menu buttons
@router.message(MenuStates.META_MENU)
async def handle_meta_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected '{user_choice}' in META Menu")

    # Видалити повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Failed to delete user message in META Menu: {e}")

    # Отримати ID повідомлення бота та інтерактивного повідомлення
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id or interactive_message_id not found in META Menu handler")
        await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначити, яку дію обрати залежно від вибору користувача
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = None

    if user_choice == MenuButton.META_HERO_LIST.value:
        new_main_text = META_HERO_LIST_TEXT
        # Додати клавіатуру для списку героїв у меті, якщо є
        new_main_keyboard = get_meta_menu()
        new_interactive_text = "🔍 Список героїв у поточній META."
        new_state = MenuStates.META_MENU
    elif user_choice == MenuButton.META_RECOMMENDATIONS.value:
        new_main_text = META_RECOMMENDATIONS_TEXT
        new_interactive_text = "🌟 Рекомендації для поточної META."
        new_main_keyboard = get_meta_menu()
        new_state = MenuStates.META_MENU
    elif user_choice == MenuButton.META_UPDATES.value:
        new_main_text = META_UPDATES_TEXT
        new_interactive_text = "📈 Оновлення поточної META."
        new_main_keyboard = get_meta_menu()
        new_state = MenuStates.META_MENU
    elif user_choice == MenuButton.BACK.value:
        # Повернутися до меню "Навігація"
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        # Невідомий вибір у меню "META"
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_meta_menu()
        new_interactive_text = "Невідома команда."
        new_state = MenuStates.META_MENU

    # Надіслати нове повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new META Menu message: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT
        )
        return

    # Видалити попереднє повідомлення бота
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Failed to delete previous bot message in META Menu: {e}")

    # Оновити ID повідомлення бота в стані
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагувати інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    except Exception as e:
        logger.error(f"Failed to edit interactive message in META Menu: {e}")
        # Надіслати нове інтерактивне повідомлення, якщо редагування не вдалося
        try:
            new_interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_interactive_message.message_id)
        except Exception as ex:
            logger.error(f"Failed to send new interactive message in META Menu: {ex}")

    # Оновити стан користувача
    await state.set_state(new_state)

# 13. Обробка GPT Menu buttons
@router.message(MenuStates.GPT_MENU)
async def handle_gpt_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected '{user_choice}' in GPT Menu")

    # Видалити повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Failed to delete user message in GPT Menu: {e}")

    # Отримати ID повідомлення бота та інтерактивного повідомлення
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id or interactive_message_id not found in GPT Menu handler")
        await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначити, яку дію обрати залежно від вибору користувача
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = None

    if user_choice == MenuButton.GPT_DATA_GENERATION.value:
        new_main_text = "📊 Генерація Даних..."
        new_interactive_text = "🤖 GPT генерує дані на основі вашого запиту."
        # Додати відповідну клавіатуру, якщо є
        new_main_keyboard = get_gpt_menu()
        new_state = MenuStates.GPT_MENU
    elif user_choice == MenuButton.GPT_HINTS.value:
        new_main_text = "💡 Поради..."
        new_interactive_text = "🤖 GPT надає поради для вашої гри."
        # Додати відповідну клавіатуру, якщо є
        new_main_keyboard = get_gpt_menu()
        new_state = MenuStates.GPT_MENU
    elif user_choice == MenuButton.GPT_HERO_STATS.value:
        new_main_text = "📈 Статистика Героїв..."
        new_interactive_text = "🤖 GPT збирає статистику героїв."
        # Додати відповідну клавіатуру, якщо є
        new_main_keyboard = get_gpt_menu()
        new_state = MenuStates.GPT_MENU
    elif user_choice == MenuButton.BACK.value:
        # Повернутися до головного меню
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_interactive_keyboard = get_generic_inline_keyboard()

        # Редагувати інтерактивне повідомлення
        try:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=interactive_message_id,
                text=new_interactive_text,
                reply_markup=new_interactive_keyboard
            )
        except Exception as e:
            logger.error(f"Failed to edit interactive message on menu_back: {e}")
            # Надіслати нове інтерактивне повідомлення, якщо редагування не вдалося
            try:
                new_interactive_message = await bot.send_message(
                    chat_id=message.chat.id,
                    text=new_interactive_text,
                    reply_markup=get_generic_inline_keyboard()
                )
                await state.update_data(interactive_message_id=new_interactive_message.message_id)
            except Exception as ex:
                logger.error(f"Failed to send new interactive message on menu_back: {ex}")

        # Надіслати основне меню з клавіатурою
        try:
            main_menu_message = await bot.send_message(
                chat_id=message.chat.id,
                text=MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name),
                reply_markup=get_main_menu()
            )
            # Зберегти ID повідомлення
            await state.update_data(bot_message_id=main_menu_message.message_id)
        except Exception as e:
            logger.error(f"Failed to send main menu: {e}")
            await bot.send_message(
                chat_id=message.chat.id,
                text=GENERIC_ERROR_MESSAGE_TEXT
            )
            return

        # Встановити стан на MAIN_MENU
        await state.set_state(MenuStates.MAIN_MENU)
        await bot.answer_callback_query(callback.id, "Повернуто до головного меню.")
        return
    else:
        # Невідомий вибір у GPT меню
        new_main_text = "Невідома команда."
        new_main_keyboard = get_gpt_menu()
        new_interactive_text = "Невідома команда."
        new_state = MenuStates.GPT_MENU

    # Надіслати нове повідомлення з клавіатурою
    if user_choice != MenuButton.BACK.value:
        try:
            main_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_main_text,
                reply_markup=new_main_keyboard
            )
            new_bot_message_id = main_message.message_id
        except Exception as e:
            logger.error(f"Failed to send new GPT Menu message: {e}")
            await bot.send_message(
                chat_id=message.chat.id,
                text=GENERIC_ERROR_MESSAGE_TEXT
            )
            return

        # Видалити попереднє повідомлення бота
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Failed to delete previous bot message in GPT Menu: {e}")

        # Оновити ID повідомлення бота в стані
        await state.update_data(bot_message_id=new_bot_message_id)

        # Редагувати інтерактивне повідомлення
        try:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=interactive_message_id,
                text=new_interactive_text,
                reply_markup=new_interactive_keyboard
            )
        except Exception as e:
            logger.error(f"Failed to edit interactive message in GPT Menu: {e}")
            # Надіслати нове інтерактивне повідомлення, якщо редагування не вдалося
            try:
                new_interactive_message = await bot.send_message(
                    chat_id=message.chat.id,
                    text=new_interactive_text,
                    reply_markup=get_generic_inline_keyboard()
                )
                await state.update_data(interactive_message_id=new_interactive_message.message_id)
            except Exception as ex:
                logger.error(f"Failed to send new interactive message in GPT Menu: {ex}")

    # Оновити стан користувача
    await state.set_state(new_state)
    await bot.answer_callback_query(callback.id)

# 14. Обробка кнопок "Профіль"
@router.message(MenuStates.PROFILE_MENU)
async def handle_profile_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Profile Menu")

    # Видалити повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Failed to delete user message in Profile Menu: {e}")

    # Отримати ID повідомлення бота та інтерактивного повідомлення
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id or interactive_message_id not found in Profile Menu handler")
        await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначити, яку дію обрати залежно від вибору користувача
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = None

    if user_choice == MenuButton.STATISTICS.value:
        new_main_text = STATISTICS_MENU_TEXT
        new_main_keyboard = get_statistics_menu()
        new_interactive_text = STATISTICS_INTERACTIVE_TEXT
        new_state = MenuStates.STATISTICS_MENU
    elif user_choice == MenuButton.ACHIEVEMENTS.value:
        new_main_text = ACHIEVEMENTS_MENU_TEXT
        new_main_keyboard = get_achievements_menu()
        new_interactive_text = ACHIEVEMENTS_INTERACTIVE_TEXT
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif user_choice == MenuButton.SETTINGS.value:
        new_main_text = SETTINGS_MENU_TEXT
        new_main_keyboard = get_settings_menu()
        new_interactive_text = SETTINGS_INTERACTIVE_TEXT
        new_state = MenuStates.SETTINGS_MENU
    elif user_choice == MenuButton.FEEDBACK.value:
        new_main_text = FEEDBACK_MENU_TEXT
        new_main_keyboard = get_feedback_menu()
        new_interactive_text = FEEDBACK_INTERACTIVE_TEXT
        new_state = MenuStates.FEEDBACK_MENU
    elif user_choice == MenuButton.HELP.value:
        new_main_text = HELP_MENU_TEXT
        new_main_keyboard = get_help_menu()
        new_interactive_text = HELP_INTERACTIVE_TEXT
        new_state = MenuStates.HELP_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
    else:
        # Невідомий вибір у меню "Профіль"
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "Невідома команда."
        new_state = MenuStates.PROFILE_MENU

    # Надіслати нове повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Profile Menu message: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT
        )
        return

    # Видалити попереднє повідомлення бота
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Failed to delete previous bot message in Profile Menu: {e}")

    # Оновити ID повідомлення бота в стані
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагувати інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    except Exception as e:
        logger.error(f"Failed to edit interactive message in Profile Menu: {e}")
        # Надіслати нове інтерактивне повідомлення, якщо редагування не вдалося
        try:
            new_interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_interactive_message.message_id)
        except Exception as ex:
            logger.error(f"Failed to send new interactive message in Profile Menu: {ex}")

    # Оновити стан користувача
    await state.set_state(new_state)

# 15. Обробка меню "Статистика"
@router.message(MenuStates.STATISTICS_MENU)
async def handle_statistics_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Statistics Menu")

    # Видалити повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Failed to delete user message in Statistics Menu: {e}")

    # Отримати ID повідомлення бота та інтерактивного повідомлення
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id or interactive_message_id not found in Statistics Menu handler")
        await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначити, яку дію обрати залежно від вибору користувача
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = None

    if user_choice == MenuButton.ACTIVITY.value:
        new_main_text = ACTIVITY_TEXT
        new_interactive_text = "📊 Відображення вашої загальної активності."
        new_main_keyboard = get_statistics_menu()
        new_state = MenuStates.STATISTICS_MENU
    elif user_choice == MenuButton.RANKING.value:
        new_main_text = RANKING_TEXT
        new_interactive_text = "🥇 Відображення вашого рейтингу."
        new_main_keyboard = get_statistics_menu()
        new_state = MenuStates.STATISTICS_MENU
    elif user_choice == MenuButton.GAME_STATS.value:
        new_main_text = GAME_STATS_TEXT
        new_interactive_text = "🎮 Відображення вашої ігрової статистики."
        new_main_keyboard = get_statistics_menu()
        new_state = MenuStates.STATISTICS_MENU
    elif user_choice == MenuButton.BACK.value:
        # Повернутися до меню "Профіль"
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        # Невідомий вибір у меню "Статистика"
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_statistics_menu()
        new_interactive_text = "Невідома команда."
        new_state = MenuStates.STATISTICS_MENU

    # Надіслати нове повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Statistics Menu message: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT
        )
        return

    # Видалити попереднє повідомлення бота
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Failed to delete previous bot message in Statistics Menu: {e}")

    # Оновити ID повідомлення бота в стані
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагувати інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    except Exception as e:
        logger.error(f"Failed to edit interactive message in Statistics Menu: {e}")
        # Надіслати нове інтерактивне повідомлення, якщо редагування не вдалося
        try:
            new_interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_interactive_message.message_id)
        except Exception as ex:
            logger.error(f"Failed to send new interactive message in Statistics Menu: {ex}")

    # Оновити стан користувача
    await state.set_state(new_state)

# 16. Обробка меню "Досягнення"
@router.message(MenuStates.ACHIEVEMENTS_MENU)
async def handle_achievements_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Achievements Menu")

    # Видалити повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Failed to delete user message in Achievements Menu: {e}")

    # Отримати ID повідомлення бота та інтерактивного повідомлення
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id or interactive_message_id not found in Achievements Menu handler")
        await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначити, яку дію обрати залежно від вибору користувача
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = None

    if user_choice == MenuButton.BADGES.value:
        new_main_text = BADGES_TEXT
        new_interactive_text = "🎖️ Відображення ваших бейджів."
        new_main_keyboard = get_achievements_menu()
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif user_choice == MenuButton.PROGRESS.value:
        new_main_text = PROGRESS_TEXT
        new_interactive_text = "🚀 Відображення вашого прогресу."
        new_main_keyboard = get_achievements_menu()
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif user_choice == MenuButton.TOURNAMENT_STATS.value:
        new_main_text = TOURNAMENT_STATS_TEXT
        new_interactive_text = "🏅 Відображення вашої турнірної статистики."
        new_main_keyboard = get_achievements_menu()
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif user_choice == MenuButton.AWARDS.value:
        new_main_text = AWARDS_TEXT
        new_interactive_text = "🎟️ Відображення отриманих нагород."
        new_main_keyboard = get_achievements_menu()
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif user_choice == MenuButton.BACK.value:
        # Повернутися до меню "Профіль"
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        # Невідомий вибір у меню "Досягнення"
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_achievements_menu()
        new_interactive_text = "Невідома команда."
        new_state = MenuStates.ACHIEVEMENTS_MENU

    # Надіслати нове повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Achievements Menu message: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT
        )
        return

    # Видалити попереднє повідомлення бота
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Failed to delete previous bot message in Achievements Menu: {e}")

    # Оновити ID повідомлення бота в стані
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагувати інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    except Exception as e:
        logger.error(f"Failed to edit interactive message in Achievements Menu: {e}")
        # Надіслати нове інтерактивне повідомлення, якщо редагування не вдалося
        try:
            new_interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_interactive_message.message_id)
        except Exception as ex:
            logger.error(f"Failed to send new interactive message in Achievements Menu: {ex}")

    # Оновити стан користувача
    await state.set_state(new_state)

# 17. Обробка меню "Налаштування"
@router.message(MenuStates.SETTINGS_MENU)
async def handle_settings_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Settings Menu")

    # Видалити повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Failed to delete user message in Settings Menu: {e}")

    # Отримати ID повідомлення бота та інтерактивного повідомлення
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id or interactive_message_id not found in Settings Menu handler")
        await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначити, яку дію обрати залежно від вибору користувача
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = None

    if user_choice == MenuButton.LANGUAGE.value:
        new_main_text = LANGUAGE_TEXT
        new_interactive_text = "🌐 Виберіть бажану мову інтерфейсу."
        # Додати клавіатуру для вибору мови, якщо є
        new_main_keyboard = get_settings_menu()
        new_state = MenuStates.SETTINGS_MENU
    elif user_choice == MenuButton.CHANGE_USERNAME.value:
        new_main_text = CHANGE_USERNAME_TEXT
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "ℹ️ Будь ласка, введіть ваш новий Username."
        new_state = MenuStates.CHANGE_USERNAME
    elif user_choice == MenuButton.UPDATE_ID.value:
        new_main_text = UPDATE_ID_TEXT
        new_interactive_text = "🆔 Будь ласка, введіть ваш новий Player ID."
        new_main_keyboard = get_settings_menu()
        new_state = MenuStates.SETTINGS_MENU
    elif user_choice == MenuButton.NOTIFICATIONS.value:
        new_main_text = NOTIFICATIONS_TEXT
        new_interactive_text = "🔔 Налаштуйте ваші сповіщення."
        # Додати клавіатуру для налаштування сповіщень, якщо є
        new_main_keyboard = get_settings_menu()
        new_state = MenuStates.SETTINGS_MENU
    elif user_choice == MenuButton.BACK.value:
        # Повернутися до меню "Профіль"
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        # Невідомий вибір у меню "Налаштування"
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_settings_menu()
        new_interactive_text = "Невідома команда."
        new_state = MenuStates.SETTINGS_MENU

    # Надіслати нове повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Settings Menu message: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT
        )
        return

    # Видалити попереднє повідомлення бота
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Failed to delete previous bot message in Settings Menu: {e}")

    # Оновити ID повідомлення бота в стані
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагувати інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    except Exception as e:
        logger.error(f"Failed to edit interactive message in Settings Menu: {e}")
        # Надіслати нове інтерактивне повідомлення, якщо редагування не вдалося
        try:
            new_interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_interactive_message.message_id)
        except Exception as ex:
            logger.error(f"Failed to send new interactive message in Settings Menu: {ex}")

    # Оновити стан користувача
    await state.set_state(new_state)

# 18. Обробка кнопок "Зворотний Зв'язок"
@router.message(MenuStates.FEEDBACK_MENU)
async def handle_feedback_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Feedback Menu")

    # Видалити повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Failed to delete user message in Feedback Menu: {e}")

    # Отримати ID повідомлення бота та інтерактивного повідомлення
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id or interactive_message_id not found in Feedback Menu handler")
        await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначити, яку дію обрати залежно від вибору користувача
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = None

    if user_choice == MenuButton.SEND_FEEDBACK.value:
        new_main_text = SEND_FEEDBACK_TEXT
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "✏️ Будь ласка, введіть ваш відгук нижче."
        new_state = MenuStates.RECEIVE_FEEDBACK
    elif user_choice == MenuButton.REPORT_BUG.value:
        new_main_text = REPORT_BUG_TEXT
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "🐛 Будь ласка, опишіть помилку, яку ви зустріли."
        new_state = MenuStates.REPORT_BUG
    elif user_choice == MenuButton.BACK.value:
        # Повернутися до меню "Профіль"
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        # Невідомий вибір у меню "Зворотний Зв'язок"
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_feedback_menu()
        new_interactive_text = "Невідома команда."
        new_state = MenuStates.FEEDBACK_MENU

    # Надіслати нове повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Feedback Menu message: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT
        )
        return

    # Видалити попереднє повідомлення бота
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Failed to delete previous bot message in Feedback Menu: {e}")

    # Оновити ID повідомлення бота в стані
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагувати інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    except Exception as e:
        logger.error(f"Failed to edit interactive message in Feedback Menu: {e}")
        # Надіслати нове інтерактивне повідомлення, якщо редагування не вдалося
        try:
            new_interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_interactive_message.message_id)
        except Exception as ex:
            logger.error(f"Failed to send new interactive message in Feedback Menu: {ex}")

    # Оновити стан користувача
    await state.set_state(new_state)

# 19. Обробка меню "Допомога"
@router.message(MenuStates.HELP_MENU)
async def handle_help_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"User {message.from_user.id} selected {user_choice} in Help Menu")

    # Видалити повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Failed to delete user message in Help Menu: {e}")

    # Отримати ID повідомлення бота та інтерактивного повідомлення
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id or interactive_message_id not found in Help Menu handler")
        await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначити, яку дію обрати залежно від вибору користувача
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = None

    if user_choice == MenuButton.INSTRUCTIONS.value:
        new_main_text = INSTRUCTIONS_TEXT
        new_interactive_text = "📄 Ось інструкції для використання бота."
        new_main_keyboard = get_help_menu()
        new_state = MenuStates.HELP_MENU
    elif user_choice == MenuButton.FAQ.value:
        new_main_text = FAQ_TEXT
        new_interactive_text = "❔ Ось часті запитання."
        new_main_keyboard = get_help_menu()
        new_state = MenuStates.HELP_MENU
    elif user_choice == MenuButton.HELP_SUPPORT.value:
        new_main_text = HELP_SUPPORT_TEXT
        new_interactive_text = "📞 Зв'яжіться з підтримкою для подальшої допомоги."
        new_main_keyboard = get_help_menu()
        new_state = MenuStates.HELP_MENU
    elif user_choice == MenuButton.BACK.value:
        # Повернутися до меню "Профіль"
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        # Невідомий вибір у меню "Допомога"
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_help_menu()
        new_interactive_text = "Невідома команда."
        new_state = MenuStates.HELP_MENU

    # Надіслати нове повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Failed to send new Help Menu message: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT
        )
        return

    # Видалити попереднє повідомлення бота
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Failed to delete previous bot message in Help Menu: {e}")

    # Оновити ID повідомлення бота в стані
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагувати інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
    except Exception as e:
        logger.error(f"Failed to edit interactive message in Help Menu: {e}")
        # Надіслати нове інтерактивне повідомлення, якщо редагування не вдалося
        try:
            new_interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=new_interactive_message.message_id)
        except Exception as ex:
            logger.error(f"Failed to send new interactive message in Help Menu: {ex}")

    # Оновити стан користувача
    await state.set_state(new_state)

# ======================
# Обробка Inline Кнопок
# ======================

@router.callback_query()
async def handle_inline_buttons(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = callback.data
    logger.info(f"User {callback.from_user.id} pressed inline button: {data}")

    # Отримати ID інтерактивного повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if not interactive_message_id:
        logger.error("Interactive message ID not found in Inline Button handler")
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT
        )
        await callback.answer()
        return

    # Обробка inline кнопок
    if data == "mls_button":
        await bot.answer_callback_query(callback.id, text=MLS_BUTTON_RESPONSE_TEXT)
    elif data == "menu_back":
        # Повернутися до головного меню
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_interactive_keyboard = get_generic_inline_keyboard()

        # Редагувати інтерактивне повідомлення
        try:
            await bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=interactive_message_id,
                text=new_interactive_text,
                reply_markup=new_interactive_keyboard
            )
        except Exception as e:
            logger.error(f"Failed to edit interactive message on menu_back: {e}")
            # Надіслати нове інтерактивне повідомлення, якщо редагування не вдалося
            try:
                new_interactive_message = await bot.send_message(
                    chat_id=callback.message.chat.id,
                    text=new_interactive_text,
                    reply_markup=get_generic_inline_keyboard()
                )
                await state.update_data(interactive_message_id=new_interactive_message.message_id)
            except Exception as ex:
                logger.error(f"Failed to send new interactive message on menu_back: {ex}")

        # Повернутися до стану MAIN_MENU
        await state.set_state(MenuStates.MAIN_MENU)
        await callback.answer("Повернуто до головного меню.")
    else:
        # Обробка невідомих inline кнопок
        await bot.answer_callback_query(callback.id, text=UNHANDLED_INLINE_BUTTON_TEXT)

    await callback.answer()

# ======================
# Обробка інших станів
# ======================

# 10. Обробка створення білду (як приклад)
@router.message(MenuStates.CREATE_BUILD)
async def handle_create_build(message: Message, state: FSMContext, bot: Bot):
    build_name = message.text.strip()
    logger.info(f"User {message.from_user.id} is creating a build: {build_name}")

    # Видалити повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Failed to delete user message in Create Build: {e}")

    # Додати логіку створення білду тут
    if build_name:
        # Приклад відповіді (замінити на реальну логіку)
        response_text = f"✅ Білд <b>{build_name}</b> успішно створено!"
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=response_text,
                parse_mode="HTML",
                reply_markup=get_generic_inline_keyboard()
            )
        except Exception as e:
            logger.error(f"Failed to send build creation response: {e}")
            await bot.send_message(
                chat_id=message.chat.id,
                text=GENERIC_ERROR_MESSAGE_TEXT
            )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="🔍 Будь ласка, введіть назву білду.",
            reply_markup=get_generic_inline_keyboard()
        )

    # Повернутися до меню "Білди"
    await state.set_state(MenuStates.BUILDS_MENU)

# ======================
# Обробка невідомих команд
# ======================

@router.message()
async def unknown_command(message: Message, state: FSMContext, bot: Bot):
    logger.warning(f"Unknown message from {message.from_user.id}: {message.text}")

    # Видалити повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Failed to delete unknown user message: {e}")

    # Отримати поточний стан користувача
    current_state = await state.get_state()
    state_data = await state.get_data()

    # Визначити відповідний текст та клавіатуру залежно від стану
    new_main_text = ""
    new_main_keyboard = None

    if current_state == MenuStates.MAIN_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_main_menu()
    elif current_state == MenuStates.NAVIGATION_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_navigation_menu()
    elif current_state == MenuStates.HEROES_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_heroes_menu()
    elif current_state == MenuStates.HERO_CLASS_MENU.state:
        hero_class = state_data.get('hero_class', 'Tank')
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_hero_class_menu(hero_class)
    elif current_state == MenuStates.GUIDES_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_guides_menu()
    elif current_state == MenuStates.COUNTER_PICKS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_counter_picks_menu()
    elif current_state == MenuStates.BUILDS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_builds_menu()
    elif current_state == MenuStates.VOTING_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_voting_menu()
    elif current_state == MenuStates.PROFILE_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_profile_menu()
    elif current_state == MenuStates.STATISTICS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_statistics_menu()
    elif current_state == MenuStates.ACHIEVEMENTS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_achievements_menu()
    elif current_state == MenuStates.SETTINGS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_settings_menu()
    elif current_state == MenuStates.FEEDBACK_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_feedback_menu()
    elif current_state == MenuStates.HELP_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_help_menu()
    elif current_state == MenuStates.TOURNAMENTS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_tournaments_menu()
    elif current_state == MenuStates.META_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_meta_menu()
    elif current_state == MenuStates.M6_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_m6_menu()
    elif current_state in [
        MenuStates.SEARCH_HERO.state,
        MenuStates.SUGGEST_TOPIC.state,
        MenuStates.CHANGE_USERNAME.state,
        MenuStates.RECEIVE_FEEDBACK.state,
        MenuStates.REPORT_BUG.state
    ]:
        # Якщо користувач в процесі введення, надіслати підказку
        await bot.send_message(
            chat_id=message.chat.id,
            text=USE_BUTTON_NAVIGATION_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        # Залишити стан без змін
        return
    else:
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)
        new_main_keyboard = get_main_menu()

    # Надіслати відповідь
    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
    except Exception as e:
        logger.error(f"Failed to send unknown command response: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT
        )
        return

    # Оновити стан користувача, якщо необхідно
    if new_main_text != MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name):
        await state.set_state(current_state)
    else:
        await state.set_state(MenuStates.MAIN_MENU)

# ======================
# Функція для реєстрації хендлерів
# ======================

def setup_handlers(dp: Router):
    dp.include_router(router)