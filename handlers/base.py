# handlers/base.py

import logging
from aiogram import Router, F, Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import types  # Для використання ReplyKeyboardRemove
from aiogram.exceptions import BadRequest

from keyboards.menus import (
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
    menu_button_to_class,
    heroes_by_class
)

from keyboards.inline_menus import (
    get_generic_inline_keyboard,
    get_intro_page_1_keyboard,
    get_intro_page_2_keyboard,
    get_intro_page_3_keyboard
)

# Імпортуйте всі необхідні константи тексту з texts.py
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
)

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
router = Router()

# Визначаємо стани меню
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
    SEARCH_TOPIC = State()
    CHANGE_USERNAME = State()
    RECEIVE_FEEDBACK = State()
    REPORT_BUG = State()
    # Додайте додаткові стани, якщо це необхідно

# Команда /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    user_name = message.from_user.first_name
    logger.info(f"Користувач {message.from_user.id} викликав /start")

    # Видаляємо повідомлення користувача /start
    await message.delete()

    # Встановлюємо стан користувача на INTRO_PAGE_1
    await state.set_state(MenuStates.INTRO_PAGE_1)

    # Відправляємо перше інтерктивне повідомлення з кнопкою 'Далі'
    interactive_message = await bot.send_message(
        chat_id=message.chat.id,
        text=INTRO_PAGE_1_TEXT,
        parse_mode="HTML",
        reply_markup=get_intro_page_1_keyboard()
    )

    # Зберігаємо ID інтерактивного повідомлення
    await state.update_data(interactive_message_id=interactive_message.message_id)

# Обробник натискання інлайн-кнопки 'Далі' на першій сторінці
@router.callback_query(F.data == "intro_next_1")
async def handle_intro_next_1(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # Отримуємо ID інтерактивного повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=INTRO_PAGE_2_TEXT,
            parse_mode="HTML",
            reply_markup=get_intro_page_2_keyboard()
        )
    except BadRequest as e:
        if "message is not modified" in str(e):
            logger.info("Повідомлення не змінено, пропускаємо редагування.")
        else:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text=GENERIC_ERROR_MESSAGE_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await callback.answer()
        return

    await state.set_state(MenuStates.INTRO_PAGE_2)
    await callback.answer()

# Обробник натискання інлайн-кнопки 'Далі' на другій сторінці
@router.callback_query(F.data == "intro_next_2")
async def handle_intro_next_2(callback: CallbackQuery, state: FSMContext, bot: Bot):
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=INTRO_PAGE_3_TEXT,
            parse_mode="HTML",
            reply_markup=get_intro_page_3_keyboard()
        )
    except BadRequest as e:
        if "message is not modified" in str(e):
            logger.info("Повідомлення не змінено, пропускаємо редагування.")
        else:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text=GENERIC_ERROR_MESSAGE_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await callback.answer()
        return

    await state.set_state(MenuStates.INTRO_PAGE_3)
    await callback.answer()

# Обробник натискання інлайн-кнопки 'Розпочати' на третій сторінці
@router.callback_query(F.data == "intro_start")
async def handle_intro_start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_first_name = callback.from_user.first_name

    main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
    main_menu_message = await bot.send_message(
        chat_id=callback.message.chat.id,
        text=main_menu_text_formatted,
        reply_markup=get_main_menu()
    )

    await state.update_data(bot_message_id=main_menu_message.message_id)

    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=MAIN_MENU_DESCRIPTION,
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )
    except BadRequest as e:
        if "message is not modified" in str(e):
            logger.info("Повідомлення не змінено, пропускаємо редагування.")
        else:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            interactive_message = await bot.send_message(
                chat_id=callback.message.chat.id,
                text=MAIN_MENU_DESCRIPTION,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=callback.message.chat.id,
            text=MAIN_MENU_DESCRIPTION,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(MenuStates.MAIN_MENU)
    await callback.answer()

# Обробник натискання звичайних кнопок у головному меню
@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' у головному меню")

    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Логіка переходу
    if user_choice == "🧭 Розділи":
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    elif user_choice == "🪪 Профіль":
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    elif user_choice in ["🔥 META", "🏆 M6", "👾 GPT"]:
        # Обробка нових кнопок в головному меню
        new_main_text = f"Ви обрали {user_choice}"
        new_main_keyboard = get_main_menu()  # Повертаємося до головного меню
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
    else:
        # Невідома команда
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.MAIN_MENU

    # Якщо новий текст та клавіатура ідентичні поточним, уникнути редагування
    current_main_text = MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)
    if new_main_text == current_main_text and new_main_keyboard == get_main_menu():
        logger.info("Текст та клавіатура не змінилися. Пропускаємо редагування.")
    else:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id

        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

        await state.update_data(bot_message_id=new_bot_message_id)

    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )
    except BadRequest as e:
        if "message is not modified" in str(e):
            logger.info("Повідомлення не змінено, пропускаємо редагування.")
        else:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Обробники для меню Навігація
@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Навігація")

    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Логіка переходу
    if user_choice == "🥷 Герої":
        new_main_text = HEROES_MENU_TEXT
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = HEROES_INTERACTIVE_TEXT
        new_state = MenuStates.HEROES_MENU
    elif user_choice == "📚 Гайди":
        new_main_text = GUIDES_MENU_TEXT
        new_main_keyboard = get_guides_menu()
        new_interactive_text = GUIDES_INTERACTIVE_TEXT
        new_state = MenuStates.GUIDES_MENU
    elif user_choice == "⚖️ Протидії":
        new_main_text = COUNTER_PICKS_MENU_TEXT
        new_main_keyboard = get_counter_picks_menu()
        new_interactive_text = COUNTER_PICKS_INTERACTIVE_TEXT
        new_state = MenuStates.COUNTER_PICKS_MENU
    elif user_choice == "🛡️ Снаряга":
        new_main_text = BUILDS_MENU_TEXT
        new_main_keyboard = get_builds_menu()
        new_interactive_text = BUILDS_INTERACTIVE_TEXT
        new_state = MenuStates.BUILDS_MENU
    elif user_choice == "📊 Опитування":
        new_main_text = VOTING_MENU_TEXT
        new_main_keyboard = get_voting_menu()
        new_interactive_text = VOTING_INTERACTIVE_TEXT
        new_state = MenuStates.VOTING_MENU
    elif user_choice == "🔙 Назад":
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
    elif user_choice in ["🔥 META", "🏆 M6", "👾 GPT"]:
        # Обробка нових кнопок у навігації
        new_main_text = f"Ви обрали {user_choice} у навігації"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        # Невідома команда
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.NAVIGATION_MENU

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    await state.update_data(bot_message_id=new_bot_message_id)

    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )
    except BadRequest as e:
        if "message is not modified" in str(e):
            logger.info("Повідомлення не змінено, пропускаємо редагування.")
        else:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Обробники для меню Персонажі
@router.message(MenuStates.HEROES_MENU)
async def handle_heroes_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Персонажі")

    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Логіка переходу
    if user_choice in ["🛡️ Танки", "🧙‍♂️ Маги", "🏹 Стрільці", "⚔️ Асасіни", "❤️ Сапорти", "🗡️ Бійці"]:
        hero_class = menu_button_to_class.get(user_choice, "Танк")
        new_main_text = f"Меню класу {hero_class}"
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = f"Меню класу {hero_class}"
        new_state = MenuStates.HERO_CLASS_MENU
    elif user_choice == "⚖️ Порівняти":
        new_main_text = "Функція порівняння героїв ще не реалізована."
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = "Меню Персонажі"
        new_state = MenuStates.HEROES_MENU
    elif user_choice == "🔎 Шукати":
        new_main_text = "Будь ласка, введіть ім'я героя для пошуку."
        new_main_keyboard = types.ReplyKeyboardRemove()
        new_interactive_text = "Меню Персонажі"
        new_state = MenuStates.SEARCH_HERO
    elif user_choice == "🔙":
        # Повертаємось до меню Персонажі
        new_main_text = HEROES_MENU_TEXT
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = HEROES_INTERACTIVE_TEXT
        new_state = MenuStates.HEROES_MENU
    else:
        # Невідома команда
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.HEROES_MENU

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагуємо інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )
    except BadRequest as e:
        if "message is not modified" in str(e):
            logger.info("Повідомлення не змінено, пропускаємо редагування.")
        else:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Обробники для меню Класу Героя
@router.message(MenuStates.HERO_CLASS_MENU)
async def handle_hero_class_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню класу героя")

    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Логіка переходу
    if user_choice == "🔙":
        new_main_text = HEROES_MENU_TEXT
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = HEROES_INTERACTIVE_TEXT
        new_state = MenuStates.HEROES_MENU
    else:
        # Тут можна додати логіку для відображення конкретного героя
        # Наприклад, відправити детальну інформацію про героя
        new_main_text = f"Інформація про героя '{user_choice}' ще не реалізована."
        new_main_keyboard = get_hero_class_menu(menu_button_to_class.get(user_choice, "Танк"))
        new_interactive_text = f"Меню класу {menu_button_to_class.get(user_choice, 'Танк')}"
        new_state = MenuStates.HERO_CLASS_MENU

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагуємо інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )
    except BadRequest as e:
        if "message is not modified" in str(e):
            logger.info("Повідомлення не змінено, пропускаємо редагування.")
        else:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Обробники для меню Гайди
@router.message(MenuStates.GUIDES_MENU)
async def handle_guides_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Гайди")

    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Логіка переходу
    if user_choice == "🆕 Нові":
        new_main_text = NEW_GUIDES_TEXT
        new_main_keyboard = get_guides_menu()
        new_interactive_text = "Нові гайди"
        new_state = MenuStates.GUIDES_MENU
    elif user_choice == "🌟 Топ":
        new_main_text = POPULAR_GUIDES_TEXT
        new_main_keyboard = get_guides_menu()
        new_interactive_text = "Топ гайди"
        new_state = MenuStates.GUIDES_MENU
    elif user_choice == "📘 Новачкам":
        new_main_text = BEGINNER_GUIDES_TEXT
        new_main_keyboard = get_guides_menu()
        new_interactive_text = "Гайди для новачків"
        new_state = MenuStates.GUIDES_MENU
    elif user_choice == "🧙 Стратегії":
        new_main_text = ADVANCED_TECHNIQUES_TEXT
        new_main_keyboard = get_guides_menu()
        new_interactive_text = "Стратегії"
        new_state = MenuStates.GUIDES_MENU
    elif user_choice == "🤝 Команда":
        new_main_text = TEAMPLAY_GUIDES_TEXT
        new_main_keyboard = get_guides_menu()
        new_interactive_text = "Командні гайди"
        new_state = MenuStates.GUIDES_MENU
    elif user_choice == "🔙 Назад":
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        # Невідома команда
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_guides_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.GUIDES_MENU

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагуємо інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )
    except BadRequest as e:
        if "message is not modified" in str(e):
            logger.info("Повідомлення не змінено, пропускаємо редагування.")
        else:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Обробники для меню Контр-піки
@router.message(MenuStates.COUNTER_PICKS_MENU)
async def handle_counter_picks_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Контр-піки")

    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Логіка переходу
    if user_choice == "🔎 Шукати":
        new_main_text = COUNTER_SEARCH_TEXT
        new_main_keyboard = get_counter_picks_menu()
        new_interactive_text = "Шукати контр-піки"
        new_state = MenuStates.SEARCH_TOPIC
    elif user_choice == "📄 Список":
        new_main_text = COUNTER_LIST_TEXT
        new_main_keyboard = get_counter_picks_menu()
        new_interactive_text = "Список контр-піків"
        new_state = MenuStates.COUNTER_PICKS_MENU
    elif user_choice == "🔙 Назад":
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        # Невідома команда
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_counter_picks_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.COUNTER_PICKS_MENU

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагуємо інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )
    except BadRequest as e:
        if "message is not modified" in str(e):
            logger.info("Повідомлення не змінено, пропускаємо редагування.")
        else:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Обробники для меню Білди
@router.message(MenuStates.BUILDS_MENU)
async def handle_builds_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Білди")

    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Логіка переходу
    if user_choice == "🏗️ Новий":
        new_main_text = CREATE_BUILD_TEXT
        new_main_keyboard = get_builds_menu()
        new_interactive_text = "Створення нового білду"
        new_state = MenuStates.CREATE_BUILD
    elif user_choice == "📄 Збережені":
        new_main_text = MY_BUILDS_TEXT
        new_main_keyboard = get_builds_menu()
        new_interactive_text = "Ваші збережені білди"
        new_state = MenuStates.MY_BUILDS
    elif user_choice == "🔥 Популярні":
        new_main_text = POPULAR_BUILDS_TEXT
        new_main_keyboard = get_builds_menu()
        new_interactive_text = "Популярні білди"
        new_state = MenuStates.POPULAR_BUILDS
    elif user_choice == "🔙 Назад":
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        # Невідома команда
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_builds_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.BUILDS_MENU

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагуємо інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )
    except BadRequest as e:
        if "message is not modified" in str(e):
            logger.info("Повідомлення не змінено, пропускаємо редагування.")
        else:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Обробники для меню Голосування
@router.message(MenuStates.VOTING_MENU)
async def handle_voting_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Голосування")

    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Логіка переходу
    if user_choice == "📍 Активні":
        new_main_text = CURRENT_VOTES_TEXT
        new_main_keyboard = get_voting_menu()
        new_interactive_text = "Активні голосування"
        new_state = MenuStates.VOTING_MENU
    elif user_choice == "📋 Ваші":
        new_main_text = MY_VOTES_TEXT
        new_main_keyboard = get_voting_menu()
        new_interactive_text = "Ваші голосування"
        new_state = MenuStates.VOTING_MENU
    elif user_choice == "➕ Ідея":
        new_main_text = SUGGEST_TOPIC_TEXT
        new_main_keyboard = get_voting_menu()
        new_interactive_text = "Додати ідею для голосування"
        new_state = MenuStates.SUGGEST_TOPIC
    elif user_choice == "🔙 Назад":
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        # Невідома команда
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_voting_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.VOTING_MENU

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагуємо інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )
    except BadRequest as e:
        if "message is not modified" in str(e):
            logger.info("Повідомлення не змінено, пропускаємо редагування.")
        else:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Обробники для меню Профіль
@router.message(MenuStates.PROFILE_MENU)
async def handle_profile_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Профіль")

    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_profile_menu()
    new_interactive_text = ""
    new_state = MenuStates.PROFILE_MENU

    if user_choice == "📈 Дані":
        new_main_text = STATISTICS_MENU_TEXT
        new_main_keyboard = get_statistics_menu()
        new_interactive_text = STATISTICS_INTERACTIVE_TEXT
        new_state = MenuStates.STATISTICS_MENU
    elif user_choice == "🏆 Успіхи":
        new_main_text = ACHIEVEMENTS_MENU_TEXT
        new_main_keyboard = get_achievements_menu()
        new_interactive_text = ACHIEVEMENTS_INTERACTIVE_TEXT
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif user_choice == "⚙️ Опції":
        new_main_text = SETTINGS_MENU_TEXT
        new_main_keyboard = get_settings_menu()
        new_interactive_text = SETTINGS_INTERACTIVE_TEXT
        new_state = MenuStates.SETTINGS_MENU
    elif user_choice == "💌 Відгук":
        new_main_text = FEEDBACK_MENU_TEXT
        new_main_keyboard = get_feedback_menu()
        new_interactive_text = FEEDBACK_INTERACTIVE_TEXT
        new_state = MenuStates.FEEDBACK_MENU
    elif user_choice == "❓ Питання":
        new_main_text = HELP_MENU_TEXT
        new_main_keyboard = get_help_menu()
        new_interactive_text = HELP_INTERACTIVE_TEXT
        new_state = MenuStates.HELP_MENU
    elif user_choice == "🔙 Меню":
        # Повертаємось до головного меню
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
    else:
        # Невідома команда
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.PROFILE_MENU

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагуємо інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )
    except BadRequest as e:
        if "message is not modified" in str(e):
            logger.info("Повідомлення не змінено, пропускаємо редагування.")
        else:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Обробники для підрозділу Статистика
@router.message(MenuStates.STATISTICS_MENU)
async def handle_statistics_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Статистика")

    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Логіка переходу
    if user_choice == "📊 Активність":
        new_main_text = ACTIVITY_TEXT
        new_main_keyboard = get_statistics_menu()
        new_interactive_text = "Активність"
        new_state = MenuStates.STATISTICS_MENU
    elif user_choice == "🥇 Рейтинг":
        new_main_text = RANKING_TEXT
        new_main_keyboard = get_statistics_menu()
        new_interactive_text = "Рейтинг"
        new_state = MenuStates.STATISTICS_MENU
    elif user_choice == "🎮 Ігри":
        new_main_text = GAME_STATS_TEXT
        new_main_keyboard = get_statistics_menu()
        new_interactive_text = "Ігри"
        new_state = MenuStates.STATISTICS_MENU
    elif user_choice == "🔙 Назад":
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        # Невідома команда
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_statistics_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.STATISTICS_MENU

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагуємо інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )
    except BadRequest as e:
        if "message is not modified" in str(e):
            logger.info("Повідомлення не змінено, пропускаємо редагування.")
        else:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Обробники для підрозділу Досягнення
@router.message(MenuStates.ACHIEVEMENTS_MENU)
async def handle_achievements_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Досягнення")

    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Логіка переходу
    if user_choice == "🎖️ Бейджі":
        new_main_text = BADGES_TEXT
        new_main_keyboard = get_achievements_menu()
        new_interactive_text = "Бейджі"
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif user_choice == "🚀 Прогрес":
        new_main_text = PROGRESS_TEXT
        new_main_keyboard = get_achievements_menu()
        new_interactive_text = "Прогрес"
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif user_choice == "🏅 Турніри":
        new_main_text = TOURNAMENT_STATS_TEXT
        new_main_keyboard = get_achievements_menu()
        new_interactive_text = "Турніри"
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif user_choice == "🎟️ Нагороди":
        new_main_text = AWARDS_TEXT
        new_main_keyboard = get_achievements_menu()
        new_interactive_text = "Нагороди"
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif user_choice == "🔙 Назад":
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        # Невідома команда
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_achievements_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.ACHIEVEMENTS_MENU

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагуємо інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )
    except BadRequest as e:
        if "message is not modified" in str(e):
            logger.info("Повідомлення не змінено, пропускаємо редагування.")
        else:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Обробники для підрозділу Налаштування
@router.message(MenuStates.SETTINGS_MENU)
async def handle_settings_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Налаштування")

    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Логіка переходу
    if user_choice == "🌐 Мова":
        new_main_text = LANGUAGE_TEXT
        new_main_keyboard = get_settings_menu()
        new_interactive_text = "Вибір мови"
        new_state = MenuStates.SETTINGS_MENU
    elif user_choice == "ℹ️ Нік":
        new_main_text = CHANGE_USERNAME_TEXT
        new_main_keyboard = get_settings_menu()
        new_interactive_text = "Зміна імені користувача"
        new_state = MenuStates.CHANGE_USERNAME
    elif user_choice == "🆔 ID":
        new_main_text = UPDATE_ID_TEXT
        new_main_keyboard = get_settings_menu()
        new_interactive_text = "Ваш ID"
        new_state = MenuStates.UPDATE_ID
    elif user_choice == "🔔 Алєрти":
        new_main_text = NOTIFICATIONS_TEXT
        new_main_keyboard = get_settings_menu()
        new_interactive_text = "Налаштування алєртів"
        new_state = MenuStates.NOTIFICATIONS
    elif user_choice == "🔙 Назад":
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        # Невідома команда
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_settings_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.SETTINGS_MENU

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагуємо інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )
    except BadRequest as e:
        if "message is not modified" in str(e):
            logger.info("Повідомлення не змінено, пропускаємо редагування.")
        else:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Обробники для підрозділу Зворотний Зв'язок
@router.message(MenuStates.FEEDBACK_MENU)
async def handle_feedback_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Зворотний Зв'язок")

    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Логіка переходу
    if user_choice == "✏️ Пропозиція":
        new_main_text = SEND_FEEDBACK_TEXT
        new_main_keyboard = get_feedback_menu()
        new_interactive_text = "Введіть вашу пропозицію."
        new_state = MenuStates.RECEIVE_FEEDBACK
    elif user_choice == "🐛 Помилка":
        new_main_text = REPORT_BUG_TEXT
        new_main_keyboard = get_feedback_menu()
        new_interactive_text = "Опишіть знайдену помилку."
        new_state = MenuStates.REPORT_BUG
    elif user_choice == "🔙 Назад":
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        # Невідома команда
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_feedback_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.FEEDBACK_MENU

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагуємо інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )
    except BadRequest as e:
        if "message is not modified" in str(e):
            logger.info("Повідомлення не змінено, пропускаємо редагування.")
        else:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Обробники для підрозділу Допомога
@router.message(MenuStates.HELP_MENU)
async def handle_help_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Допомога")

    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Логіка переходу
    if user_choice == "📄 Гайд":
        new_main_text = INSTRUCTIONS_TEXT
        new_main_keyboard = get_help_menu()
        new_interactive_text = "Гайд"
        new_state = MenuStates.HELP_MENU
    elif user_choice == "❔ FAQ":
        new_main_text = FAQ_TEXT
        new_main_keyboard = get_help_menu()
        new_interactive_text = "FAQ"
        new_state = MenuStates.HELP_MENU
    elif user_choice == "📞 Контакти":
        new_main_text = HELP_SUPPORT_TEXT
        new_main_keyboard = get_help_menu()
        new_interactive_text = "Контакти"
        new_state = MenuStates.HELP_MENU
    elif user_choice == "🔙 Назад":
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        # Невідома команда
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_help_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.HELP_MENU

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагуємо інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )
    except BadRequest as e:
        if "message is not modified" in str(e):
            logger.info("Повідомлення не змінено, пропускаємо редагування.")
        else:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Обробники для підрозділу Статистика
@router.message(MenuStates.STATISTICS_MENU)
async def handle_statistics_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Статистика")

    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Логіка переходу
    if user_choice == "📊 Активність":
        new_main_text = ACTIVITY_TEXT
        new_main_keyboard = get_statistics_menu()
        new_interactive_text = "Активність"
        new_state = MenuStates.STATISTICS_MENU
    elif user_choice == "🥇 Рейтинг":
        new_main_text = RANKING_TEXT
        new_main_keyboard = get_statistics_menu()
        new_interactive_text = "Рейтинг"
        new_state = MenuStates.STATISTICS_MENU
    elif user_choice == "🎮 Ігри":
        new_main_text = GAME_STATS_TEXT
        new_main_keyboard = get_statistics_menu()
        new_interactive_text = "Ігри"
        new_state = MenuStates.STATISTICS_MENU
    elif user_choice == "🔙 Назад":
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        # Невідома команда
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_statistics_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.STATISTICS_MENU

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагуємо інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )
    except BadRequest as e:
        if "message is not modified" in str(e):
            logger.info("Повідомлення не змінено, пропускаємо редагування.")
        else:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Обробники для підрозділу Мова, Нік, ID, Алєрти (налаштування)
@router.message(MenuStates.SETTINGS_MENU)
async def handle_settings_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Налаштування")

    await message.delete()
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Логіка переходу
    if user_choice == "🌐 Мова":
        new_main_text = LANGUAGE_TEXT
        new_main_keyboard = get_settings_menu()
        new_interactive_text = "Вибір мови"
        new_state = MenuStates.LANGUAGE
    elif user_choice == "ℹ️ Нік":
        new_main_text = CHANGE_USERNAME_TEXT
        new_main_keyboard = get_settings_menu()
        new_interactive_text = "Зміна імені користувача"
        new_state = MenuStates.CHANGE_USERNAME
    elif user_choice == "🆔 ID":
        new_main_text = UPDATE_ID_TEXT
        new_main_keyboard = get_settings_menu()
        new_interactive_text = "Ваш ID"
        new_state = MenuStates.UPDATE_ID
    elif user_choice == "🔔 Алєрти":
        new_main_text = NOTIFICATIONS_TEXT
        new_main_keyboard = get_settings_menu()
        new_interactive_text = "Налаштування алєртів"
        new_state = MenuStates.NOTIFICATIONS
    elif user_choice == "🔙 Назад":
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        # Невідома команда
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_settings_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.SETTINGS_MENU

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагуємо інтерактивне повідомлення
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )
    except BadRequest as e:
        if "message is not modified" in str(e):
            logger.info("Повідомлення не змінено, пропускаємо редагування.")
        else:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Обробники для підрозділу Введення нової пропозиції (Feedback)
@router.message(MenuStates.RECEIVE_FEEDBACK)
async def handle_receive_feedback(message: Message, state: FSMContext, bot: Bot):
    feedback = message.text
    user_id = message.from_user.id
    logger.info(f"Користувач {user_id} надіслав пропозицію: {feedback}")

    # Зберігаємо або обробляємо відгук за потреби
    # Наприклад, надсилаємо адміністратору
    # await bot.send_message(admin_chat_id, f"Відгук від {user_id}: {feedback}")

    # Надсилаємо підтвердження користувачу
    await bot.send_message(
        chat_id=message.chat.id,
        text=FEEDBACK_RECEIVED_TEXT,
        reply_markup=get_generic_inline_keyboard()
    )

    # Переводимо користувача назад до меню Профіль
    await state.set_state(MenuStates.PROFILE_MENU)

# Обробники для підрозділу Репорт помилки (Bug Report)
@router.message(MenuStates.REPORT_BUG)
async def handle_report_bug(message: Message, state: FSMContext, bot: Bot):
    bug_report = message.text
    user_id = message.from_user.id
    logger.info(f"Користувач {user_id} надіслав репорт помилки: {bug_report}")

    # Зберігаємо або обробляємо репорт за потреби
    # Наприклад, надсилаємо адміністратору
    # await bot.send_message(admin_chat_id, f"Репорт помилки від {user_id}: {bug_report}")

    # Надсилаємо підтвердження користувачу
    await bot.send_message(
        chat_id=message.chat.id,
        text=BUG_REPORT_RECEIVED_TEXT,
        reply_markup=get_generic_inline_keyboard()
    )

    # Переводимо користувача назад до меню Профіль
    await state.set_state(MenuStates.PROFILE_MENU)

# Обробники для підрозділу Зміна Імені (Change Username)
@router.message(MenuStates.CHANGE_USERNAME)
async def handle_change_username(message: Message, state: FSMContext, bot: Bot):
    new_username = message.text
    user_id = message.from_user.id
    logger.info(f"Користувач {user_id} змінив ім'я на: {new_username}")

    # Зберігаємо нове ім'я користувача
    # Наприклад, оновлюємо базу даних
    # await update_username_in_db(user_id, new_username)

    # Надсилаємо підтвердження користувачу
    await bot.send_message(
        chat_id=message.chat.id,
        text=CHANGE_USERNAME_RESPONSE_TEXT.format(username=new_username),
        reply_markup=get_generic_inline_keyboard()
    )

    # Переводимо користувача назад до меню Налаштування
    await state.set_state(MenuStates.SETTINGS_MENU)

# Обробники для підрозділу Пошуку Героя (Search Hero)
@router.message(MenuStates.SEARCH_HERO)
async def handle_search_hero(message: Message, state: FSMContext, bot: Bot):
    hero_name = message.text
    user_id = message.from_user.id
    logger.info(f"Користувач {user_id} шукає героя: {hero_name}")

    # Здійснюємо пошук героя
    # Наприклад, звертаємося до бази даних або API
    # hero_info = search_hero_in_db(hero_name)
    # if hero_info:
    #     await bot.send_message(chat_id=message.chat.id, text=hero_info)
    # else:
    #     await bot.send_message(chat_id=message.chat.id, text="Герой не знайдено.")

    # Для прикладу, надсилаємо загальне повідомлення
    await bot.send_message(
        chat_id=message.chat.id,
        text=SEARCH_HERO_RESPONSE_TEXT.format(hero_name=hero_name),
        reply_markup=get_generic_inline_keyboard()
    )

    # Переводимо користувача назад до меню Персонажі
    await state.set_state(MenuStates.HEROES_MENU)

# Обробники для підрозділу Пошуку Теми (Search Topic) в Голосуваннях
@router.message(MenuStates.SUGGEST_TOPIC)
async def handle_suggest_topic(message: Message, state: FSMContext, bot: Bot):
    topic = message.text
    user_id = message.from_user.id
    logger.info(f"Користувач {user_id} пропонує тему: {topic}")

    # Зберігаємо або обробляємо пропозицію
    # Наприклад, надсилаємо адміністратору
    # await bot.send_message(admin_chat_id, f"Пропозиція теми від {user_id}: {topic}")

    # Надсилаємо підтвердження користувачу
    await bot.send_message(
        chat_id=message.chat.id,
        text=SUGGESTION_RESPONSE_TEXT,
        reply_markup=get_generic_inline_keyboard()
    )

    # Переводимо користувача назад до меню Голосування
    await state.set_state(MenuStates.VOTING_MENU)

# Обробник для невідомих повідомлень у всіх інших станах
@router.message()
async def unknown_command(message: Message, state: FSMContext, bot: Bot):
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо поточний стан
    current_state = await state.get_state()

    # Визначаємо новий текст та клавіатуру залежно від стану
    if current_state == MenuStates.MAIN_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Головне меню"
        new_state = MenuStates.MAIN_MENU
    elif current_state == MenuStates.NAVIGATION_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Навігаційний екран"
        new_state = MenuStates.NAVIGATION_MENU
    elif current_state == MenuStates.HEROES_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = "Меню Персонажі"
        new_state = MenuStates.HEROES_MENU
    elif current_state == MenuStates.HERO_CLASS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        hero_class = data.get('hero_class', 'Танк')
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = f"Меню класу {hero_class}"
        new_state = MenuStates.HERO_CLASS_MENU
    elif current_state == MenuStates.GUIDES_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_guides_menu()
        new_interactive_text = "Меню Гайди"
        new_state = MenuStates.GUIDES_MENU
    elif current_state == MenuStates.COUNTER_PICKS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_counter_picks_menu()
        new_interactive_text = "Меню Контр-піки"
        new_state = MenuStates.COUNTER_PICKS_MENU
    elif current_state == MenuStates.BUILDS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_builds_menu()
        new_interactive_text = "Меню Білди"
        new_state = MenuStates.BUILDS_MENU
    elif current_state == MenuStates.VOTING_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_voting_menu()
        new_interactive_text = "Меню Голосування"
        new_state = MenuStates.VOTING_MENU
    elif current_state == MenuStates.PROFILE_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "Меню Профіль"
        new_state = MenuStates.PROFILE_MENU
    elif current_state == MenuStates.STATISTICS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_statistics_menu()
        new_interactive_text = "Меню Статистика"
        new_state = MenuStates.STATISTICS_MENU
    elif current_state == MenuStates.ACHIEVEMENTS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_achievements_menu()
        new_interactive_text = "Меню Досягнення"
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif current_state == MenuStates.SETTINGS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_settings_menu()
        new_interactive_text = "Меню Налаштування"
        new_state = MenuStates.SETTINGS_MENU
    elif current_state in [
        MenuStates.SEARCH_HERO.state,
        MenuStates.SEARCH_TOPIC.state,
        MenuStates.CHANGE_USERNAME.state,
        MenuStates.RECEIVE_FEEDBACK.state,
        MenuStates.REPORT_BUG.state
    ]:
        # Якщо користувач перебуває в процесі введення, надсилаємо підказку
        await bot.send_message(
            chat_id=message.chat.id,
            text=USE_BUTTON_NAVIGATION_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.set_state(current_state)
        return
    else:
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU

    # Відправляємо нове повідомлення
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    # Видаляємо старе повідомлення
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Редагуємо інтерактивне повідомлення
    if interactive_message_id:
        try:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=interactive_message_id,
                text=new_interactive_text,
                parse_mode="HTML",
                reply_markup=get_generic_inline_keyboard()
            )
        except BadRequest as e:
            if "message is not modified" in str(e):
                logger.info("Повідомлення не змінено, пропускаємо редагування.")
            else:
                logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
                interactive_message = await bot.send_message(
                    chat_id=message.chat.id,
                    text=new_interactive_text,
                    reply_markup=get_generic_inline_keyboard()
                )
                await state.update_data(interactive_message_id=interactive_message.message_id)
    else:
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    # Оновлюємо стан користувача
    await state.set_state(new_state)

# Функція для налаштування роутерів
def setup_handlers(dp: Dispatcher):
    dp.include_router(router)
    # dp.include_router(ai_router)  # Підключення AI-роутера виконується в bot.py
