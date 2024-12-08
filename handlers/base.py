# handlers/base.py

import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command, Text
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler

# Імпортуємо клавіатури
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
    get_meta_menu,
    get_m6_menu,
    get_gpt_menu
)
from keyboards.inline_menus import (
    get_generic_inline_keyboard,
    get_intro_page_1_keyboard,
    get_intro_page_2_keyboard,
    get_intro_page_3_keyboard
)

# Імпортуємо тексти
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
    GENERIC_ERROR_MESSAGE_TEXT,
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
    GPT_MENU = State()
    META_MENU = State()
    M6_MENU = State()
    GPT_ASK_QUESTION = State()
    # Додайте додаткові стани, якщо це необхідно

# Допоміжні функції
async def send_new_main_message(
    chat_id: int,
    text: str,
    reply_markup,
    parse_mode: str,
    state: FSMContext,
    bot: Bot
) -> int:
    """
    Відправляє нове головне повідомлення та повертає його message_id.
    """
    main_message = await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=reply_markup,
        parse_mode=parse_mode
    )
    await state.update_data(bot_message_id=main_message.message_id)
    return main_message.message_id

async def edit_interactive_message(
    chat_id: int,
    message_id: int,
    text: str,
    reply_markup,
    parse_mode: str,
    state: FSMContext,
    bot: Bot
):
    """
    Редагує інтерактивне повідомлення. Якщо не вдалося, відправляє нове.
    """
    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

async def handle_unknown_command(
    chat_id: int,
    current_state: str,
    state: FSMContext,
    bot: Bot
):
    """
    Обробляє невідомі команди залежно від поточного стану.
    """
    new_main_text = UNKNOWN_COMMAND_TEXT
    new_main_keyboard = get_main_menu()
    new_interactive_text = MAIN_MENU_DESCRIPTION
    new_state = MenuStates.MAIN_MENU

    # Визначаємо відповідну клавіатуру та текст залежно від стану
    if current_state == MenuStates.MAIN_MENU.state:
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Головне меню"
        new_state = MenuStates.MAIN_MENU
    elif current_state == MenuStates.NAVIGATION_MENU.state:
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Навігаційний екран"
        new_state = MenuStates.NAVIGATION_MENU
    elif current_state == MenuStates.HEROES_MENU.state:
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = "Меню Персонажі"
        new_state = MenuStates.HEROES_MENU
    elif current_state == MenuStates.HERO_CLASS_MENU.state:
        hero_class = (await state.get_data()).get('hero_class', 'Танк')
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = f"Меню класу {hero_class}"
        new_state = MenuStates.HERO_CLASS_MENU
    elif current_state == MenuStates.GUIDES_MENU.state:
        new_main_keyboard = get_guides_menu()
        new_interactive_text = "Меню Гайди"
        new_state = MenuStates.GUIDES_MENU
    elif current_state == MenuStates.COUNTER_PICKS_MENU.state:
        new_main_keyboard = get_counter_picks_menu()
        new_interactive_text = "Меню Контр-піки"
        new_state = MenuStates.COUNTER_PICKS_MENU
    elif current_state == MenuStates.BUILDS_MENU.state:
        new_main_keyboard = get_builds_menu()
        new_interactive_text = "Меню Білди"
        new_state = MenuStates.BUILDS_MENU
    elif current_state == MenuStates.VOTING_MENU.state:
        new_main_keyboard = get_voting_menu()
        new_interactive_text = "Меню Голосування"
        new_state = MenuStates.VOTING_MENU
    elif current_state == MenuStates.PROFILE_MENU.state:
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "Меню Профіль"
        new_state = MenuStates.PROFILE_MENU
    elif current_state == MenuStates.STATISTICS_MENU.state:
        new_main_keyboard = get_statistics_menu()
        new_interactive_text = "Меню Статистика"
        new_state = MenuStates.STATISTICS_MENU
    elif current_state == MenuStates.ACHIEVEMENTS_MENU.state:
        new_main_keyboard = get_achievements_menu()
        new_interactive_text = "Меню Досягнення"
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif current_state == MenuStates.SETTINGS_MENU.state:
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
        new_main_text = USE_BUTTON_NAVIGATION_TEXT
        new_main_keyboard = get_generic_inline_keyboard()
        new_interactive_text = ""
        new_state = current_state
        # Не змінюємо стан
    else:
        new_main_text = MAIN_MENU_TEXT.format(user_first_name="Користувач")
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU

    # Відправляємо нове повідомлення
    main_message = await bot.send_message(
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML"
    )
    new_bot_message_id = main_message.message_id

    # Видаляємо старе повідомлення, якщо є
    bot_message_id = (await state.get_data()).get('bot_message_id')
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Редагуємо інтерактивне повідомлення
    interactive_message_id = (await state.get_data()).get('interactive_message_id')
    if interactive_message_id:
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=interactive_message_id,
                text=new_interactive_text,
                parse_mode="HTML",
                reply_markup=get_generic_inline_keyboard()
            )
        except Exception as e:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            interactive_message = await bot.send_message(
                chat_id=chat_id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard(),
                parse_mode="HTML"
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
    else:
        interactive_message = await bot.send_message(
            chat_id=chat_id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    # Оновлюємо стан
    await state.set_state(new_state)

# Middleware для перевірки наявності необхідних ID повідомлень
class CheckMessageMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: Message, data: dict):
        state: FSMContext = data.get('state')
        state_data = await state.get_data()
        bot_message_id = state_data.get('bot_message_id')
        interactive_message_id = state_data.get('interactive_message_id')

        if not bot_message_id or not interactive_message_id:
            logger.error("bot_message_id або interactive_message_id не знайдено")
            await message.reply(
                GENERIC_ERROR_MESSAGE_TEXT,
                reply_markup=get_generic_inline_keyboard(),
                parse_mode="HTML"
            )
            raise CancelHandler()

# Підключаємо Middleware
router.message.middleware(CheckMessageMiddleware())

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

# Обробник інлайн-кнопок для вступу
@router.callback_query(Text(startswith="intro_next"))
async def handle_intro_next(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = callback.data
    current_state = await state.get_state()
    logger.info(f"Користувач {callback.from_user.id} натиснув '{data}' в стані {current_state}")

    # Отримуємо ID інтерактивного повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if not interactive_message_id:
        logger.error("interactive_message_id не знайдено")
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        await callback.answer()
        return

    if data == "intro_next_1":
        new_text = INTRO_PAGE_2_TEXT
        new_keyboard = get_intro_page_2_keyboard()
        new_state = MenuStates.INTRO_PAGE_2
    elif data == "intro_next_2":
        new_text = INTRO_PAGE_3_TEXT
        new_keyboard = get_intro_page_3_keyboard()
        new_state = MenuStates.INTRO_PAGE_3
    elif data == "intro_start":
        user_first_name = callback.from_user.first_name
        new_text = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
        new_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
        # Збереження основного повідомлення
        main_message = await send_new_main_message(
            chat_id=callback.message.chat.id,
            text=new_text,
            reply_markup=new_keyboard,
            parse_mode="HTML",
            state=state,
            bot=bot
        )
        # Редагуємо інтерактивне повідомлення
        await edit_interactive_message(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML",
            state=state,
            bot=bot
        )
        await callback.answer()
        await state.set_state(new_state)
        return
    else:
        new_text = UNKNOWN_COMMAND_TEXT
        new_keyboard = get_generic_inline_keyboard()
        new_state = current_state

    # Редагуємо інтерактивне повідомлення
    await edit_interactive_message(
        chat_id=callback.message.chat.id,
        message_id=interactive_message_id,
        text=new_text,
        reply_markup=new_keyboard,
        parse_mode="HTML",
        state=state,
        bot=bot
    )

    # Оновлюємо стан
    await state.set_state(new_state)
    await callback.answer()

# Загальний обробник повідомлень на основі стану
@router.message()
async def handle_user_message(message: Message, state: FSMContext, bot: Bot):
    current_state = await state.get_state()
    user_input = message.text.strip()
    chat_id = message.chat.id
    user_id = message.from_user.id
    logger.info(f"Користувач {user_id} в стані {current_state} ввів: {user_input}")

    # Видаляємо повідомлення користувача
    await message.delete()

    if current_state == MenuStates.MAIN_MENU.state:
        await handle_main_menu(message, state, bot, user_input)
    elif current_state == MenuStates.NAVIGATION_MENU.state:
        await handle_navigation_menu(message, state, bot, user_input)
    elif current_state == MenuStates.HEROES_MENU.state:
        await handle_heroes_menu(message, state, bot, user_input)
    elif current_state == MenuStates.HERO_CLASS_MENU.state:
        await handle_hero_class_menu(message, state, bot, user_input)
    elif current_state == MenuStates.GUIDES_MENU.state:
        await handle_guides_menu(message, state, bot, user_input)
    elif current_state == MenuStates.COUNTER_PICKS_MENU.state:
        await handle_counter_picks_menu(message, state, bot, user_input)
    elif current_state == MenuStates.BUILDS_MENU.state:
        await handle_builds_menu(message, state, bot, user_input)
    elif current_state == MenuStates.VOTING_MENU.state:
        await handle_voting_menu(message, state, bot, user_input)
    elif current_state == MenuStates.PROFILE_MENU.state:
        await handle_profile_menu(message, state, bot, user_input)
    elif current_state == MenuStates.STATISTICS_MENU.state:
        await handle_statistics_menu(message, state, bot, user_input)
    elif current_state == MenuStates.ACHIEVEMENTS_MENU.state:
        await handle_achievements_menu(message, state, bot, user_input)
    elif current_state == MenuStates.SETTINGS_MENU.state:
        await handle_settings_menu(message, state, bot, user_input)
    elif current_state == MenuStates.SEARCH_HERO.state:
        await handle_search_hero(message, state, bot, user_input)
    elif current_state == MenuStates.SEARCH_TOPIC.state:
        await handle_search_topic(message, state, bot, user_input)
    elif current_state == MenuStates.CHANGE_USERNAME.state:
        await handle_change_username(message, state, bot, user_input)
    elif current_state == MenuStates.RECEIVE_FEEDBACK.state:
        await handle_receive_feedback(message, state, bot, user_input)
    elif current_state == MenuStates.REPORT_BUG.state:
        await handle_report_bug(message, state, bot, user_input)
    elif current_state == MenuStates.GPT_MENU.state:
        await handle_gpt_menu(message, state, bot, user_input)
    elif current_state == MenuStates.META_MENU.state:
        await handle_meta_menu(message, state, bot, user_input)
    elif current_state == MenuStates.M6_MENU.state:
        await handle_m6_menu(message, state, bot, user_input)
    elif current_state == MenuStates.GPT_ASK_QUESTION.state:
        await handle_gpt_question(message, state, bot, user_input)
    else:
        await handle_unknown_command(chat_id, current_state, state, bot)

# Функції обробки для кожного стану

async def handle_main_menu(message: Message, state: FSMContext, bot: Bot, user_choice: str):
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"Користувач {user_id} обрав '{user_choice}' у головному меню")

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо новий текст та клавіатуру для повідомлень
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
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
    elif user_choice == MenuButton.META.value:
        new_main_text = META_MENU_TEXT
        new_main_keyboard = get_meta_menu()
        new_interactive_text = "META: " + META_MENU_TEXT  # Можливо, потрібен окремий текст
        new_state = MenuStates.META_MENU
    elif user_choice == MenuButton.M6.value:
        new_main_text = M6_MENU_TEXT
        new_main_keyboard = get_m6_menu()
        new_interactive_text = "M6: " + M6_MENU_TEXT  # Можливо, потрібен окремий текст
        new_state = MenuStates.M6_MENU
    elif user_choice == MenuButton.GPT.value:
        new_main_text = "👾 GPT Menu"  # Потрібно замінити на відповідний текст
        new_main_keyboard = get_gpt_menu()
        new_interactive_text = "GPT: " + "AI підтримка та відповіді на ваші запитання щодо гри."
        new_state = MenuStates.GPT_MENU
    else:
        # Невідома команда
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.MAIN_MENU

    # Відправляємо нове повідомлення з клавіатурою (Повідомлення 1)
    main_message = await send_new_main_message(
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML",
        state=state,
        bot=bot
    )
    new_bot_message_id = main_message

    # Видаляємо попереднє повідомлення з клавіатурою
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Редагуємо інтерактивне повідомлення (Повідомлення 2)
    await edit_interactive_message(
        chat_id=chat_id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        reply_markup=get_generic_inline_keyboard(),
        parse_mode="HTML",
        state=state,
        bot=bot
    )

    # Оновлюємо стан користувача
    if new_state:
        await state.set_state(new_state)

async def handle_navigation_menu(message: Message, state: FSMContext, bot: Bot, user_choice: str):
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"Користувач {user_id} обрав '{user_choice}' в меню Навігація")

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
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
    elif user_choice == MenuButton.BACK.value:
        # Повертаємось до головного меню
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
    else:
        # Невідома команда
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.NAVIGATION_MENU

    # Відправляємо нове повідомлення з клавіатурою (Повідомлення 1)
    main_message = await send_new_main_message(
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML",
        state=state,
        bot=bot
    )
    new_bot_message_id = main_message

    # Видаляємо попереднє повідомлення з клавіатурою
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Редагуємо інтерактивне повідомлення (Повідомлення 2)
    await edit_interactive_message(
        chat_id=chat_id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        reply_markup=get_generic_inline_keyboard(),
        parse_mode="HTML",
        state=state,
        bot=bot
    )

    # Оновлюємо стан користувача
    if new_state:
        await state.set_state(new_state)

async def handle_heroes_menu(message: Message, state: FSMContext, bot: Bot, user_choice: str):
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"Користувач {user_id} обрав '{user_choice}' в меню Персонажі")

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    hero_classes = [
        MenuButton.TANK.value,
        MenuButton.MAGE.value,
        MenuButton.MARKSMAN.value,
        MenuButton.ASSASSIN.value,
        MenuButton.SUPPORT.value,
        MenuButton.FIGHTER.value
    ]

    if user_choice in hero_classes:
        hero_class = menu_button_to_class.get(user_choice)
        new_main_text = HERO_CLASS_MENU_TEXT.format(hero_class=hero_class)
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = HERO_CLASS_INTERACTIVE_TEXT.format(hero_class=hero_class)
        new_state = MenuStates.HERO_CLASS_MENU
        await state.update_data(hero_class=hero_class)
    elif user_choice == MenuButton.SEARCH_HERO.value:
        new_main_text = SEARCH_HERO_RESPONSE_TEXT.format(hero_name="")  # Placeholder, handled separately
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Пошук героя"
        new_state = MenuStates.SEARCH_HERO
    elif user_choice == MenuButton.COMPARISON.value:
        new_main_text = "Функція порівняння героїв ще в розробці."
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = "Порівняння героїв"
        new_state = MenuStates.HEROES_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_hero_class_menu(data.get('hero_class', 'Танк'))
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.HEROES_MENU

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await send_new_main_message(
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML",
        state=state,
        bot=bot
    )
    new_bot_message_id = main_message

    # Видаляємо старе повідомлення з клавіатурою
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Редагуємо інтерактивне повідомлення
    await edit_interactive_message(
        chat_id=chat_id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        reply_markup=get_generic_inline_keyboard(),
        parse_mode="HTML",
        state=state,
        bot=bot
    )

    # Оновлюємо стан користувача
    if new_state:
        await state.set_state(new_state)

async def handle_hero_class_menu(message: Message, state: FSMContext, bot: Bot, user_choice: str):
    user_id = message.from_user.id
    chat_id = message.chat.id
    data = await state.get_data()
    hero_class = data.get('hero_class', 'Танк')
    logger.info(f"Користувач {user_id} обрав '{user_choice}' в меню класу {hero_class}")

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice == MenuButton.BACK.value:
        # Повернення до меню вибору класу персонажа
        new_main_text = HEROES_MENU_TEXT
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = HEROES_INTERACTIVE_TEXT
        new_state = MenuStates.HEROES_MENU
    else:
        # Інші опції можна додати за потребою
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = f"Меню класу {hero_class}"
        new_state = MenuStates.HERO_CLASS_MENU

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await send_new_main_message(
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML",
        state=state,
        bot=bot
    )
    new_bot_message_id = main_message

    # Видаляємо старе повідомлення з клавіатурою
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Редагуємо інтерактивне повідомлення
    await edit_interactive_message(
        chat_id=chat_id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        reply_markup=get_generic_inline_keyboard(),
        parse_mode="HTML",
        state=state,
        bot=bot
    )

    # Оновлюємо стан користувача
    if new_state:
        await state.set_state(new_state)

async def handle_guides_menu(message: Message, state: FSMContext, bot: Bot, user_choice: str):
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"Користувач {user_id} обрав '{user_choice}' в меню Гайди")

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_guides_menu()
    new_interactive_text = ""
    new_state = MenuStates.GUIDES_MENU

    if user_choice == MenuButton.NEW_GUIDES.value:
        new_main_text = NEW_GUIDES_TEXT
        new_interactive_text = "Нові гайди"
    elif user_choice == MenuButton.POPULAR_GUIDES.value:
        new_main_text = POPULAR_GUIDES_TEXT
        new_interactive_text = "Популярні гайди"
    elif user_choice == MenuButton.BEGINNER_GUIDES.value:
        new_main_text = BEGINNER_GUIDES_TEXT
        new_interactive_text = "Гайди для початківців"
    elif user_choice == MenuButton.ADVANCED_TECHNIQUES.value:
        new_main_text = ADVANCED_TECHNIQUES_TEXT
        new_interactive_text = "Просунуті техніки"
    elif user_choice == MenuButton.TEAMPLAY_GUIDES.value:
        new_main_text = TEAMPLAY_GUIDES_TEXT
        new_interactive_text = "Командна гра"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"

    # Відправляємо нове повідомлення з клавіатурою (Повідомлення 1)
    main_message = await send_new_main_message(
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML",
        state=state,
        bot=bot
    )
    new_bot_message_id = main_message

    # Видаляємо старе повідомлення з клавіатурою
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Редагуємо інтерактивне повідомлення
    await edit_interactive_message(
        chat_id=chat_id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        reply_markup=get_generic_inline_keyboard(),
        parse_mode="HTML",
        state=state,
        bot=bot
    )

    # Оновлюємо стан користувача
    await state.set_state(new_state)

async def handle_counter_picks_menu(message: Message, state: FSMContext, bot: Bot, user_choice: str):
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"Користувач {user_id} обрав '{user_choice}' в меню Контр-піки")

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_counter_picks_menu()
    new_interactive_text = ""
    new_state = MenuStates.COUNTER_PICKS_MENU

    if user_choice == MenuButton.COUNTER_SEARCH.value:
        new_main_text = COUNTER_SEARCH_TEXT
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Пошук контр-піку"
        new_state = MenuStates.SEARCH_HERO
    elif user_choice == MenuButton.COUNTER_LIST.value:
        new_main_text = COUNTER_LIST_TEXT
        new_interactive_text = "Список контр-піків"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await send_new_main_message(
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML",
        state=state,
        bot=bot
    )
    new_bot_message_id = main_message

    # Видаляємо старе повідомлення з клавіатурою
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Редагуємо інтерактивне повідомлення
    await edit_interactive_message(
        chat_id=chat_id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        reply_markup=get_generic_inline_keyboard(),
        parse_mode="HTML",
        state=state,
        bot=bot
    )

    # Оновлюємо стан користувача
    await state.set_state(new_state)

async def handle_builds_menu(message: Message, state: FSMContext, bot: Bot, user_choice: str):
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"Користувач {user_id} обрав '{user_choice}' в меню Білди")

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_builds_menu()
    new_interactive_text = ""
    new_state = MenuStates.BUILDS_MENU

    if user_choice == MenuButton.CREATE_BUILD.value:
        new_main_text = CREATE_BUILD_TEXT
        new_interactive_text = "Створення білду"
    elif user_choice == MenuButton.MY_BUILDS.value:
        new_main_text = MY_BUILDS_TEXT
        new_interactive_text = "Мої білди"
    elif user_choice == MenuButton.POPULAR_BUILDS.value:
        new_main_text = POPULAR_BUILDS_TEXT
        new_interactive_text = "Популярні білди"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await send_new_main_message(
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML",
        state=state,
        bot=bot
    )
    new_bot_message_id = main_message

    # Видаляємо старе повідомлення з клавіатурою
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Редагуємо інтерактивне повідомлення
    await edit_interactive_message(
        chat_id=chat_id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        reply_markup=get_generic_inline_keyboard(),
        parse_mode="HTML",
        state=state,
        bot=bot
    )

    # Оновлюємо стан користувача
    await state.set_state(new_state)

async def handle_voting_menu(message: Message, state: FSMContext, bot: Bot, user_choice: str):
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"Користувач {user_id} обрав '{user_choice}' в меню Голосування")

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_voting_menu()
    new_interactive_text = ""
    new_state = MenuStates.VOTING_MENU

    if user_choice == MenuButton.CURRENT_VOTES.value:
        new_main_text = CURRENT_VOTES_TEXT
        new_interactive_text = "Поточні опитування"
    elif user_choice == MenuButton.MY_VOTES.value:
        new_main_text = MY_VOTES_TEXT
        new_interactive_text = "Мої голосування"
    elif user_choice == MenuButton.SUGGEST_TOPIC.value:
        new_main_text = SUGGEST_TOPIC_TEXT
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Пропозиція теми"
        new_state = MenuStates.SEARCH_TOPIC
    elif user_choice == MenuButton.BACK.value:
        new_main_text = NAVIGATION_MENU_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_INTERACTIVE_TEXT
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await send_new_main_message(
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML",
        state=state,
        bot=bot
    )
    new_bot_message_id = main_message

    # Видаляємо старе повідомлення з клавіатурою
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Редагуємо інтерактивне повідомлення
    await edit_interactive_message(
        chat_id=chat_id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        reply_markup=get_generic_inline_keyboard(),
        parse_mode="HTML",
        state=state,
        bot=bot
    )

    # Оновлюємо стан користувача
    await state.set_state(new_state)

async def handle_profile_menu(message: Message, state: FSMContext, bot: Bot, user_choice: str):
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"Користувач {user_id} обрав '{user_choice}' в меню Профіль")

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_profile_menu()
    new_interactive_text = ""
    new_state = MenuStates.PROFILE_MENU

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
    elif user_choice == MenuButton.BACK_TO_MAIN_MENU.value:
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await send_new_main_message(
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML",
        state=state,
        bot=bot
    )
    new_bot_message_id = main_message

    # Видаляємо старе повідомлення з клавіатурою
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Редагуємо інтерактивне повідомлення
    await edit_interactive_message(
        chat_id=chat_id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        reply_markup=get_generic_inline_keyboard(),
        parse_mode="HTML",
        state=state,
        bot=bot
    )

    # Оновлюємо стан користувача
    await state.set_state(new_state)

async def handle_statistics_menu(message: Message, state: FSMContext, bot: Bot, user_choice: str):
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"Користувач {user_id} обрав '{user_choice}' в меню Статистика")

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_statistics_menu()
    new_interactive_text = ""
    new_state = MenuStates.STATISTICS_MENU

    if user_choice == MenuButton.ACTIVITY.value:
        new_main_text = ACTIVITY_TEXT
        new_interactive_text = "Загальна активність"
    elif user_choice == MenuButton.RANKING.value:
        new_main_text = RANKING_TEXT
        new_interactive_text = "Рейтинг"
    elif user_choice == MenuButton.GAME_STATS.value:
        new_main_text = GAME_STATS_TEXT
        new_interactive_text = "Ігрова статистика"
    elif user_choice == MenuButton.BACK_TO_PROFILE.value:
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await send_new_main_message(
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML",
        state=state,
        bot=bot
    )
    new_bot_message_id = main_message

    # Видаляємо старе повідомлення з клавіатурою
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Редагуємо інтерактивне повідомлення
    await edit_interactive_message(
        chat_id=chat_id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        reply_markup=get_generic_inline_keyboard(),
        parse_mode="HTML",
        state=state,
        bot=bot
    )

    # Оновлюємо стан користувача
    await state.set_state(new_state)

async def handle_achievements_menu(message: Message, state: FSMContext, bot: Bot, user_choice: str):
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"Користувач {user_id} обрав '{user_choice}' в меню Досягнення")

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_achievements_menu()
    new_interactive_text = ""
    new_state = MenuStates.ACHIEVEMENTS_MENU

    if user_choice == MenuButton.BADGES.value:
        new_main_text = BADGES_TEXT
        new_interactive_text = "Мої бейджі"
    elif user_choice == MenuButton.PROGRESS.value:
        new_main_text = PROGRESS_TEXT
        new_interactive_text = "Прогрес"
    elif user_choice == MenuButton.TOURNAMENT_STATS.value:
        new_main_text = TOURNAMENT_STATS_TEXT
        new_interactive_text = "Турнірна статистика"
    elif user_choice == MenuButton.AWARDS.value:
        new_main_text = AWARDS_TEXT
        new_interactive_text = "Отримані нагороди"
    elif user_choice == MenuButton.BACK_TO_PROFILE.value:
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await send_new_main_message(
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML",
        state=state,
        bot=bot
    )
    new_bot_message_id = main_message

    # Видаляємо старе повідомлення з клавіатурою
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Редагуємо інтерактивне повідомлення
    await edit_interactive_message(
        chat_id=chat_id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        reply_markup=get_generic_inline_keyboard(),
        parse_mode="HTML",
        state=state,
        bot=bot
    )

    # Оновлюємо стан користувача
    await state.set_state(new_state)

async def handle_settings_menu(message: Message, state: FSMContext, bot: Bot, user_choice: str):
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"Користувач {user_id} обрав '{user_choice}' в меню Налаштування")

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_settings_menu()
    new_interactive_text = ""
    new_state = MenuStates.SETTINGS_MENU

    if user_choice == MenuButton.LANGUAGE.value:
        new_main_text = LANGUAGE_TEXT
        new_interactive_text = "Мова інтерфейсу"
    elif user_choice == MenuButton.CHANGE_USERNAME.value:
        new_main_text = CHANGE_USERNAME_TEXT
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Зміна Username"
        new_state = MenuStates.CHANGE_USERNAME
    elif user_choice == MenuButton.UPDATE_ID.value:
        new_main_text = UPDATE_ID_TEXT
        new_interactive_text = "Оновити ID гравця"
    elif user_choice == MenuButton.NOTIFICATIONS.value:
        new_main_text = NOTIFICATIONS_TEXT
        new_interactive_text = "Сповіщення"
    elif user_choice == MenuButton.BACK_TO_PROFILE.value:
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await send_new_main_message(
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML",
        state=state,
        bot=bot
    )
    new_bot_message_id = main_message

    # Видаляємо старе повідомлення з клавіатурою
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Редагуємо інтерактивне повідомлення
    await edit_interactive_message(
        chat_id=chat_id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        reply_markup=get_generic_inline_keyboard(),
        parse_mode="HTML",
        state=state,
        bot=bot
    )

    # Оновлюємо стан користувача
    await state.set_state(new_state)

async def handle_meta_menu(message: Message, state: FSMContext, bot: Bot, user_choice: str):
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"Користувач {user_id} обрав '{user_choice}' в меню META")

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_meta_menu()
    new_interactive_text = ""
    new_state = MenuStates.META_MENU

    if user_choice == "📈 Аналітика":
        new_main_text = "📈 Аналіз актуальних тенденцій гри ще в розробці."
        new_interactive_text = "Аналітика: Нова функція буде доступна скоро."
    elif user_choice == "📊 Статистика":
        new_main_text = "📊 Статистика META ще в розробці."
        new_interactive_text = "Статистика META: Нова функція буде доступна скоро."
    elif user_choice == "🔙 Меню":
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await send_new_main_message(
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML",
        state=state,
        bot=bot
    )
    new_bot_message_id = main_message

    # Видаляємо старе повідомлення з клавіатурою
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Редагуємо інтерактивне повідомлення
    await edit_interactive_message(
        chat_id=chat_id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        reply_markup=get_generic_inline_keyboard(),
        parse_mode="HTML",
        state=state,
        bot=bot
    )

    # Оновлюємо стан користувача
    await state.set_state(new_state)

async def handle_m6_menu(message: Message, state: FSMContext, bot: Bot, user_choice: str):
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"Користувач {user_id} обрав '{user_choice}' в меню M6")

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_m6_menu()
    new_interactive_text = ""
    new_state = MenuStates.M6_MENU

    if user_choice == "🏆 Результати":
        new_main_text = "🏆 Результати спеціальних подій ще в розробці."
        new_interactive_text = "Результати: Нова функція буде доступна скоро."
    elif user_choice == "🔍 Деталі":
        new_main_text = "🔍 Деталі спеціальних подій ще в розробці."
        new_interactive_text = "Деталі: Нова функція буде доступна скоро."
    elif user_choice == "🔙 Меню":
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"

    # Відправляємо нове повідомлення з клавіатурою (Повідомлення 1)
    main_message = await send_new_main_message(
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML",
        state=state,
        bot=bot
    )
    new_bot_message_id = main_message

    # Видаляємо старе повідомлення з клавіатурою
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Редагуємо інтерактивне повідомлення
    await edit_interactive_message(
        chat_id=chat_id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        reply_markup=get_generic_inline_keyboard(),
        parse_mode="HTML",
        state=state,
        bot=bot
    )

    # Оновлюємо стан користувача
    await state.set_state(new_state)

# Обробник для запитань GPT
async def handle_gpt_question(message: Message, state: FSMContext, bot: Bot, question: str):
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"Користувач {user_id} задав запитання GPT: {question}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Тут додайте інтеграцію з GPT (наприклад, через OpenAI API)
    # Наприклад:
    # response = await get_gpt_response(question)
    # Поки що ми використаємо загальну відповідь

    if question:
        # Приклад відповіді, замініть на реальну інтеграцію з GPT
        response = "Це приклад відповіді від GPT. Реалізуйте інтеграцію з API для отримання дійсних відповідей."
    else:
        response = "Будь ласка, введіть запитання."

    await bot.send_message(
        chat_id=chat_id,
        text=f"<b>Відповідь AI:</b>\n{response}",
        parse_mode="HTML",
        reply_markup=get_generic_inline_keyboard()
    )

    # Повертаємо користувача до меню GPT
    await state.set_state(MenuStates.GPT_MENU)

# Обробник для меню GPT
async def handle_gpt_menu(message: Message, state: FSMContext, bot: Bot, user_choice: str):
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"Користувач {user_id} обрав '{user_choice}' в меню GPT")

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_gpt_menu()
    new_interactive_text = ""
    new_state = MenuStates.GPT_MENU

    if user_choice == "📝 Задати питання":
        # Переведення користувача у стан запиту GPT
        new_main_text = "🤖 Введіть ваше запитання щодо гри, героїв або стратегій."
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Ви можете поставити будь-яке питання щодо гри."
        new_state = MenuStates.GPT_ASK_QUESTION
    elif user_choice == "❓ Допомога":
        new_main_text = "🆘 Для отримання допомоги використовуйте меню навігації."
        new_interactive_text = "Допомога доступна через меню навігації."
    elif user_choice == "🔙 Меню":
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await send_new_main_message(
        chat_id=chat_id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML",
        state=state,
        bot=bot
    )
    new_bot_message_id = main_message

    # Видаляємо старе повідомлення з клавіатурою
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Редагуємо інтерактивне повідомлення
    await edit_interactive_message(
        chat_id=chat_id,
        message_id=interactive_message_id,
        text=new_interactive_text,
        reply_markup=get_generic_inline_keyboard(),
        parse_mode="HTML",
        state=state,
        bot=bot
    )

    # Оновлюємо стан користувача
    await state.set_state(new_state)

# Обробник для меню META
async def handle_meta_menu(message: Message, state: FSMContext, bot: Bot, user_choice: str):
    # Функція вже визначена вище
    pass  # Виправлення дублювання, функція вже існує

# Обробник для меню M6
async def handle_m6_menu(message: Message, state: FSMContext, bot: Bot, user_choice: str):
    # Функція вже визначена вище
    pass  # Виправлення дублювання, функція вже існує

# Обробник інлайн-кнопок
@router.callback_query()
async def handle_inline_buttons(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = callback.data
    user_id = callback.from_user.id
    chat_id = callback.message.chat.id
    logger.info(f"Користувач {user_id} натиснув інлайн-кнопку: {data}")

    # Отримуємо interactive_message_id з стану
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if interactive_message_id:
        # Обробляємо інлайн-кнопки
        if data == "mls_button":
            await bot.answer_callback_query(callback.id, text=MLS_BUTTON_RESPONSE_TEXT)
        elif data == "menu_back":
            # Повернення до головного меню
            user_first_name = callback.from_user.first_name
            main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
            try:
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=interactive_message_id,
                    text=MAIN_MENU_DESCRIPTION,
                    parse_mode="HTML",
                    reply_markup=get_generic_inline_keyboard()
                )
                main_message = await send_new_main_message(
                    chat_id=chat_id,
                    text=main_menu_text_formatted,
                    reply_markup=get_main_menu(),
                    parse_mode="HTML",
                    state=state,
                    bot=bot
                )
                # Видаляємо попереднє повідомлення з клавіатурою
                old_bot_message_id = state_data.get('bot_message_id')
                if old_bot_message_id:
                    try:
                        await bot.delete_message(chat_id=chat_id, message_id=old_bot_message_id)
                    except Exception as e:
                        logger.error(f"Не вдалося видалити повідомлення бота: {e}")
            except Exception as e:
                logger.error(f"Помилка при поверненні до головного меню: {e}")
                await bot.send_message(
                    chat_id=chat_id,
                    text=GENERIC_ERROR_MESSAGE_TEXT,
                    reply_markup=get_generic_inline_keyboard(),
                    parse_mode="HTML"
                )
        else:
            # Додайте обробку інших інлайн-кнопок за потребою
            await bot.answer_callback_query(callback.id, text=UNHANDLED_INLINE_BUTTON_TEXT)
    else:
        logger.error("interactive_message_id не знайдено")
        await bot.answer_callback_query(callback.id, text=GENERIC_ERROR_MESSAGE_TEXT)

    await callback.answer()

# Обробник невідомих повідомлень
@router.message()
async def handle_unexpected_messages(message: Message, state: FSMContext, bot: Bot):
    current_state = await state.get_state()
    user_id = message.from_user.id
    logger.info(f"Користувач {user_id} має поточний стан: {current_state}")
    # Можна реалізувати логіку для завершення або обробки непередбачених станів

# Загальний обробник помилок
@router.errors()
async def handle_error(update: object, exception: Exception):
    logger.error(f"Сталася помилка: {exception}")
    # Можна реалізувати повідомлення користувачеві про помилку тут

# Функція для налаштування обробників
def setup_handlers(dp: Bot):
    dp.include_router(router)

# Додаткові обробники для різних станів

async def handle_search_hero(message: Message, state: FSMContext, bot: Bot, hero_name: str):
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"Користувач {user_id} шукає героя: {hero_name}")

    # Тут додайте логіку пошуку героя
    # Наприклад, перевірка чи існує герой, відправка інформації тощо
    # Поки що відправимо повідомлення про отримання запиту

    if hero_name:
        response_text = SEARCH_HERO_RESPONSE_TEXT.format(hero_name=hero_name)
    else:
        response_text = "Будь ласка, введіть ім'я героя для пошуку."

    await bot.send_message(
        chat_id=chat_id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard(),
        parse_mode="HTML"
    )

    # Повертаємо користувача до попереднього меню
    await state.set_state(MenuStates.HEROES_MENU)

async def handle_search_topic(message: Message, state: FSMContext, bot: Bot, topic: str):
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"Користувач {user_id} пропонує тему: {topic}")

    # Тут додайте логіку обробки пропозиції теми
    # Наприклад, збереження в базі даних або відправка адміністратору
    # Поки що відправимо повідомлення про отримання запиту

    if topic:
        response_text = SUGGESTION_RESPONSE_TEXT.format(topic=topic)
    else:
        response_text = "Будь ласка, введіть тему для пропозиції."

    await bot.send_message(
        chat_id=chat_id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard(),
        parse_mode="HTML"
    )

    # Повертаємо користувача до меню Голосування
    await state.set_state(MenuStates.VOTING_MENU)

async def handle_change_username(message: Message, state: FSMContext, bot: Bot, new_username: str):
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"Користувач {user_id} змінює Username на: {new_username}")

    # Тут додайте логіку зміни Username
    # Наприклад, перевірка унікальності, оновлення в базі даних тощо
    # Поки що відправимо повідомлення про отримання запиту

    if new_username:
        response_text = CHANGE_USERNAME_RESPONSE_TEXT.format(new_username=new_username)
    else:
        response_text = "Будь ласка, введіть новий Username."

    await bot.send_message(
        chat_id=chat_id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard(),
        parse_mode="HTML"
    )

    # Повертаємо користувача до меню Налаштування
    await state.set_state(MenuStates.SETTINGS_MENU)

async def handle_receive_feedback(message: Message, state: FSMContext, bot: Bot, feedback: str):
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"Користувач {user_id} надіслав відгук: {feedback}")

    # Тут додайте логіку зберігання відгуку
    # Наприклад, збереження в базі даних або відправка адміністратору
    # Поки що відправимо повідомлення про отримання відгуку

    if feedback:
        response_text = FEEDBACK_RECEIVED_TEXT
    else:
        response_text = "Будь ласка, залиште свій відгук."

    await bot.send_message(
        chat_id=chat_id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard(),
        parse_mode="HTML"
    )

    # Повертаємо користувача до меню Зворотний Зв'язок
    await state.set_state(MenuStates.FEEDBACK_MENU)

async def handle_report_bug(message: Message, state: FSMContext, bot: Bot, bug_report: str):
    user_id = message.from_user.id
    chat_id = message.chat.id
    logger.info(f"Користувач {user_id} повідомив про помилку: {bug_report}")

    # Тут додайте логіку обробки звіту про помилку
    # Наприклад, збереження в базі даних або відправка адміністратору
    # Поки що відправимо повідомлення про отримання звіту

    if bug_report:
        response_text = BUG_REPORT_RECEIVED_TEXT
    else:
        response_text = "Будь ласка, опишіть помилку, яку ви знайшли."

    await bot.send_message(
        chat_id=chat_id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard(),
        parse_mode="HTML"
    )

    # Повертаємо користувача до меню Зворотний Зв'язок
    await state.set_state(MenuStates.FEEDBACK_MENU)

async def handle_gpt_menu(message: Message, state: FSMContext, bot: Bot, user_choice: str):
    # Функція вже визначена вище
    pass  # Функція вже реалізована

# Додаткові обробники можна додати тут за потребою

# В кінці файлу, після визначення всіх функцій, підключаємо обробники

# Функція для налаштування обробників
def setup_handlers(dp: Bot):
    dp.include_router(router)