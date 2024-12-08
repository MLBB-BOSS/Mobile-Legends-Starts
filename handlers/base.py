# handlers/base.py

import logging
from aiogram import Router, Bot, F
from aiogram.filters import Command, Text
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardRemove,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

# Імпортуємо клавіатури
from keyboards.menus import (
    MenuButton,
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
    AI_INTRO_TEXT,
    AI_RESPONSE_TEXT
)

# Допоміжні функції та інтеграція з базою даних або іншими сервісами
from utils.helpers import (
    get_gpt_response,
    save_feedback,
    send_bug_report_to_admin,
    send_topic_to_admin,
    update_username,
    update_id,
    save_build,
    get_saved_builds,
    get_popular_builds,
    get_current_polls,
    get_user_polls,
    get_popular_picks,
    get_popular_builds
)

# Налаштування логування
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Створюємо Router
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
    SUGGEST_TOPIC = State()
    CHANGE_USERNAME = State()
    SEND_FEEDBACK = State()
    REPORT_BUG = State()
    GPT_MENU = State()
    GPT_ASK_QUESTION = State()
    # Додайте додаткові стани, якщо це необхідно

# Команда /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    user_name = message.from_user.first_name
    logger.info(f"Користувач {message.from_user.id} викликав /start")

    # Видаляємо повідомлення користувача /start
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення /start: {e}")

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

# Обробники інлайн кнопок для вступу
@router.callback_query(Text("intro_next_1"))
async def handle_intro_next_1(callback: CallbackQuery, state: FSMContext, bot: Bot):
    logger.info(f"Користувач {callback.from_user.id} натиснув 'Далі ➡️' на сторінці 1")

    # Отримуємо ID інтерактивного повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if not interactive_message_id:
        logger.error("interactive_message_id не знайдено")
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await callback.answer()
        return

    # Редагуємо інтерактивне повідомлення на другу сторінку
    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=INTRO_PAGE_2_TEXT,
            parse_mode="HTML",
            reply_markup=get_intro_page_2_keyboard()
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

    # Оновлюємо стан
    await state.set_state(MenuStates.INTRO_PAGE_2)
    await callback.answer()

@router.callback_query(Text("intro_next_2"))
async def handle_intro_next_2(callback: CallbackQuery, state: FSMContext, bot: Bot):
    logger.info(f"Користувач {callback.from_user.id} натиснув 'Далі ➡️' на сторінці 2")

    # Отримуємо ID інтерактивного повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if not interactive_message_id:
        logger.error("interactive_message_id не знайдено")
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await callback.answer()
        return

    # Редагуємо інтерактивне повідомлення на третю сторінку
    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=INTRO_PAGE_3_TEXT,
            parse_mode="HTML",
            reply_markup=get_intro_page_3_keyboard()
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

    # Оновлюємо стан
    await state.set_state(MenuStates.INTRO_PAGE_3)
    await callback.answer()

@router.callback_query(Text("intro_start"))
async def handle_intro_start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_first_name = callback.from_user.first_name
    logger.info(f"Користувач {callback.from_user.id} натиснув 'Розпочати 🚀'")

    # Відправляємо основне меню з клавіатурою
    main_menu_text_formatted = f"{MAIN_MENU_TEXT.format(user_first_name=user_first_name)}"
    main_menu_message = await bot.send_message(
        chat_id=callback.message.chat.id,
        text=main_menu_text_formatted,
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )

    # Оновлюємо bot_message_id
    await state.update_data(bot_message_id=main_menu_message.message_id)

    # Отримуємо ID інтерактивного повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if interactive_message_id:
        # Оновлюємо інтерактивне повідомлення з описом основного меню
        try:
            await bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=interactive_message_id,
                text=MAIN_MENU_DESCRIPTION,
                parse_mode="HTML",
                reply_markup=get_generic_inline_keyboard()
            )
        except Exception as e:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            # Якщо не вдалося редагувати, відправляємо нове інтерактивне повідомлення
            interactive_message = await bot.send_message(
                chat_id=callback.message.chat.id,
                text=MAIN_MENU_DESCRIPTION,
                reply_markup=get_generic_inline_keyboard(),
                parse_mode="HTML"
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
    else:
        # Якщо interactive_message_id не знайдено, відправляємо нове інтерактивне повідомлення
        interactive_message = await bot.send_message(
            chat_id=callback.message.chat.id,
            text=MAIN_MENU_DESCRIPTION,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    # Встановлюємо стан користувача на MAIN_MENU
    await state.set_state(MenuStates.MAIN_MENU)
    await callback.answer()

# Обробники натискання звичайних кнопок у головному меню
@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' у головному меню")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        # Надсилаємо нове повідомлення з клавіатурою
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu(),
            parse_mode="HTML"
        )
        # Зберігаємо ID повідомлення бота
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначаємо новий текст та клавіатуру для повідомлень
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = "Головне меню"
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = None

    # Використовуємо f-string для фільтрів та текстів
    if user_choice == MenuButton.NAVIGATION.value:
        new_main_text = f"{NAVIGATION_MENU_TEXT}"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = f"{NAVIGATION_INTERACTIVE_TEXT}"
        new_state = MenuStates.NAVIGATION_MENU
    elif user_choice == MenuButton.PROFILE.value:
        new_main_text = f"{PROFILE_MENU_TEXT}"
        new_main_keyboard = get_profile_menu()
        new_interactive_text = f"{PROFILE_INTERACTIVE_TEXT}"
        new_state = MenuStates.PROFILE_MENU
    elif user_choice == MenuButton.META.value:
        new_main_text = f"{META_MENU_TEXT}"
        new_main_keyboard = get_meta_menu()
        new_interactive_text = f"{META_INTERACTIVE_TEXT}"
        new_state = MenuStates.META_MENU
    elif user_choice == MenuButton.M6.value:
        new_main_text = f"{M6_MENU_TEXT}"
        new_main_keyboard = get_m6_menu()
        new_interactive_text = f"{M6_INTERACTIVE_TEXT}"
        new_state = MenuStates.M6_MENU
    elif user_choice == MenuButton.GPT.value:
        new_main_text = f"{GPT_MENU_TEXT}"
        new_main_keyboard = get_gpt_menu()
        new_interactive_text = f"{GPT_INTERACTIVE_TEXT}"
        new_state = MenuStates.GPT_MENU
    else:
        # Невідома команда
        new_main_text = f"{UNKNOWN_COMMAND_TEXT}"
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.MAIN_MENU

    # Відправляємо нове повідомлення з клавіатурою (Повідомлення 1)
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard,
            parse_mode="HTML"
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося відправити нове повідомлення: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        return

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Оновлюємо bot_message_id в стані
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагуємо інтерактивне повідомлення (Повідомлення 2)
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=new_interactive_keyboard
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        # Якщо не вдалося редагувати, відправляємо нове повідомлення
        try:
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard(),
                parse_mode="HTML"
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
        except Exception as ex:
            logger.error(f"Не вдалося відправити нове інтерактивне повідомлення: {ex}")

    # Оновлюємо стан користувача
    await state.set_state(new_state)

# Приклад обробника для меню Навігація
@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Навігація")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        # Надсилаємо нове повідомлення з клавіатурою
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu(),
            parse_mode="HTML"
        )
        # Зберігаємо ID повідомлення бота
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_navigation_menu()
    new_interactive_text = "Навігаційний екран"
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = MenuStates.NAVIGATION_MENU

    # Використовуємо f-string для фільтрів та текстів
    if user_choice == MenuButton.HEROES.value:
        new_main_text = f"{HEROES_MENU_TEXT}"
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = f"{HEROES_INTERACTIVE_TEXT}"
        new_state = MenuStates.HEROES_MENU
    elif user_choice == MenuButton.GUIDES.value:
        new_main_text = f"{GUIDES_MENU_TEXT}"
        new_main_keyboard = get_guides_menu()
        new_interactive_text = f"{GUIDES_INTERACTIVE_TEXT}"
        new_state = MenuStates.GUIDES_MENU
    elif user_choice == MenuButton.COUNTER_PICKS.value:
        new_main_text = f"{COUNTER_PICKS_MENU_TEXT}"
        new_main_keyboard = get_counter_picks_menu()
        new_interactive_text = f"{COUNTER_PICKS_INTERACTIVE_TEXT}"
        new_state = MenuStates.COUNTER_PICKS_MENU
    elif user_choice == MenuButton.BUILDS.value:
        new_main_text = f"{BUILDS_MENU_TEXT}"
        new_main_keyboard = get_builds_menu()
        new_interactive_text = f"{BUILDS_INTERACTIVE_TEXT}"
        new_state = MenuStates.BUILDS_MENU
    elif user_choice == MenuButton.VOTING.value:
        new_main_text = f"{VOTING_MENU_TEXT}"
        new_main_keyboard = get_voting_menu()
        new_interactive_text = f"{VOTING_INTERACTIVE_TEXT}"
        new_state = MenuStates.VOTING_MENU
    elif user_choice == MenuButton.BACK.value:
        # Повертаємось до головного меню
        new_main_text = f"{MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)}"
        new_main_keyboard = get_main_menu()
        new_interactive_text = f"{MAIN_MENU_DESCRIPTION}"
        new_state = MenuStates.MAIN_MENU
    else:
        # Невідома команда
        new_main_text = f"{UNKNOWN_COMMAND_TEXT}"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.NAVIGATION_MENU

    # Відправляємо нове повідомлення з клавіатурою (Повідомлення 1)
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard,
            parse_mode="HTML"
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося відправити нове повідомлення: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        return

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Оновлюємо bot_message_id в стані
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагуємо інтерактивне повідомлення (Повідомлення 2)
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=new_interactive_keyboard
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        # Якщо не вдалося редагувати, відправляємо нове повідомлення
        try:
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard(),
                parse_mode="HTML"
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
        except Exception as ex:
            logger.error(f"Не вдалося відправити нове інтерактивне повідомлення: {ex}")

    # Оновлюємо стан користувача
    await state.set_state(new_state)

# Подібні обробники для інших меню (Персонажі, Гайди, Контр-піки, Білди, Голосування, Профіль, Статистика, Досягнення, Налаштування, Зворотній зв'язок, Допомога, GPT)

# Приклад обробника для меню Персонажі
@router.message(MenuStates.HEROES_MENU)
async def handle_heroes_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Персонажі")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        # Надсилаємо нове повідомлення з клавіатурою
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu(),
            parse_mode="HTML"
        )
        # Зберігаємо ID повідомлення бота
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_heroes_menu()
    new_interactive_text = "Меню Персонажі"
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = MenuStates.HEROES_MENU

    hero_classes = [
        MenuButton.TANK.value,
        MenuButton.MAGE.value,
        MenuButton.MARKSMAN.value,
        MenuButton.ASSASSIN.value,
        MenuButton.SUPPORT.value,
        MenuButton.FIGHTER.value
    ]

    if user_choice in hero_classes:
        hero_class = menu_button_to_class.get(user_choice, "Танк")
        new_main_text = f"{HERO_CLASS_MENU_TEXT.format(hero_class=hero_class)}"
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = f"{HERO_CLASS_INTERACTIVE_TEXT.format(hero_class=hero_class)}"
        new_state = MenuStates.HERO_CLASS_MENU
        await state.update_data(hero_class=hero_class)
    elif user_choice == MenuButton.SEARCH_HERO.value:
        new_main_text = f"{SEARCH_HERO_RESPONSE_TEXT.format(hero_name='')}"  # Placeholder
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Пошук героя"
        new_state = MenuStates.SEARCH_HERO
    elif user_choice == MenuButton.COMPARISON.value:
        new_main_text = "Функція порівняння героїв ще в розробці."
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = "Порівняння героїв"
        new_state = MenuStates.HEROES_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = f"{NAVIGATION_MENU_TEXT}"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = f"{NAVIGATION_INTERACTIVE_TEXT}"
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = f"{UNKNOWN_COMMAND_TEXT}"
        new_main_keyboard = get_hero_class_menu(data.get('hero_class', 'Танк'))
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.HEROES_MENU

    # Відправляємо нове повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard,
            parse_mode="HTML"
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося відправити нове повідомлення: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        return

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Оновлюємо bot_message_id в стані
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагуємо інтерактивне повідомлення (Повідомлення 2)
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=new_interactive_keyboard
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        # Якщо не вдалося редагувати, відправляємо нове повідомлення
        try:
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard(),
                parse_mode="HTML"
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
        except Exception as ex:
            logger.error(f"Не вдалося відправити нове інтерактивне повідомлення: {ex}")

    # Оновлюємо стан користувача
    await state.set_state(new_state)

# Обробники для меню GPT
@router.message(MenuStates.GPT_MENU)
async def handle_gpt_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню GPT")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        # Надсилаємо нове повідомлення з клавіатурою
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu(),
            parse_mode="HTML"
        )
        # Зберігаємо ID повідомлення бота
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_gpt_menu()
    new_interactive_text = "Меню GPT"
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = MenuStates.GPT_MENU

    if user_choice == MenuButton.ASK_GPT.value:
        new_main_text = f"{AI_INTRO_TEXT}"
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Надсилання питання GPT"
        new_state = MenuStates.GPT_ASK_QUESTION
    elif user_choice == MenuButton.BACK.value:
        new_main_text = f"{NAVIGATION_MENU_TEXT}"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = f"{NAVIGATION_INTERACTIVE_TEXT}"
        new_state = MenuStates.NAVIGATION_MENU
    else:
        # Невідома команда
        new_main_text = f"{UNKNOWN_COMMAND_TEXT}"
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.GPT_MENU

    # Відправляємо нове повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard,
            parse_mode="HTML"
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося відправити нове повідомлення: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        return

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Оновлюємо bot_message_id в стані
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагуємо інтерактивне повідомлення (Повідомлення 2)
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=new_interactive_keyboard
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        # Якщо не вдалося редагувати, відправляємо нове повідомлення
        try:
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard(),
                parse_mode="HTML"
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
        except Exception as ex:
            logger.error(f"Не вдалося відправити нове інтерактивне повідомлення: {ex}")

    # Оновлюємо стан користувача
    await state.set_state(new_state)

# Обробники для прийому питання GPT
@router.message(MenuStates.GPT_ASK_QUESTION)
async def handle_gpt_ask_question(message: Message, state: FSMContext, bot: Bot):
    user_question = message.text.strip()
    user_id = message.from_user.id
    logger.info(f"Користувач {user_id} задає питання GPT: {user_question}")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Отримуємо відповідь від GPT
    try:
        gpt_answer = await get_gpt_response(user_question)
    except Exception as e:
        logger.error(f"Не вдалося отримати відповідь від GPT: {e}")
        gpt_answer = "Виникла помилка при отриманні відповіді від GPT. Спробуйте пізніше."

    response_text = f"{AI_RESPONSE_TEXT.format(response=gpt_answer)}"

    # Відправляємо відповідь від GPT
    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=response_text,
            reply_markup=get_gpt_menu(),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Не вдалося відправити відповідь GPT: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )

    # Повертаємо користувача до меню GPT
    await state.set_state(MenuStates.GPT_MENU)

# Обробник інлайн кнопок
@router.callback_query()
async def handle_inline_buttons(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = callback.data
    logger.info(f"Користувач {callback.from_user.id} натиснув інлайн-кнопку: {data}")

    # Отримуємо interactive_message_id з стану
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if interactive_message_id:
        # Обробляємо інлайн-кнопки
        if data == "mls_button":
            await bot.answer_callback_query(callback.id, text=MLS_BUTTON_RESPONSE_TEXT)
        elif data == "menu_back":
            # Повернення до головного меню
            await state.set_state(MenuStates.MAIN_MENU)
            new_interactive_text = MAIN_MENU_DESCRIPTION
            new_interactive_keyboard = get_generic_inline_keyboard()

            # Редагуємо інтерактивне повідомлення
            try:
                await bot.edit_message_text(
                    chat_id=callback.message.chat.id,
                    message_id=interactive_message_id,
                    text=new_interactive_text,
                    parse_mode="HTML",
                    reply_markup=new_interactive_keyboard
                )
            except Exception as e:
                logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")

            # Відправляємо головне меню
            main_menu_text_formatted = f"{MAIN_MENU_TEXT.format(user_first_name=callback.from_user.first_name)}"
            try:
                main_message = await bot.send_message(
                    chat_id=callback.message.chat.id,
                    text=main_menu_text_formatted,
                    reply_markup=get_main_menu(),
                    parse_mode="HTML"
                )
                # Оновлюємо bot_message_id
                await state.update_data(bot_message_id=main_message.message_id)
            except Exception as e:
                logger.error(f"Не вдалося відправити головне меню: {e}")

            # Видаляємо попереднє повідомлення з клавіатурою
            old_bot_message_id = state_data.get('bot_message_id')
            if old_bot_message_id:
                try:
                    await bot.delete_message(chat_id=callback.message.chat.id, message_id=old_bot_message_id)
                except Exception as e:
                    logger.error(f"Не вдалося видалити повідомлення бота: {e}")
        else:
            # Додайте обробку інших інлайн-кнопок за потребою
            await bot.answer_callback_query(callback.id, text=UNHANDLED_INLINE_BUTTON_TEXT)
    else:
        logger.error("interactive_message_id не знайдено")
        await bot.answer_callback_query(callback.id, text=GENERIC_ERROR_MESSAGE_TEXT)

    await callback.answer()

# Обробник невідомих повідомлень
@router.message()
async def unknown_command(message: Message, state: FSMContext, bot: Bot):
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо поточний стан
    current_state = await state.get_state()

    # Визначаємо новий текст та клавіатуру залежно від стану
    if current_state == MenuStates.MAIN_MENU:
        new_main_text = f"{UNKNOWN_COMMAND_TEXT}"
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Головне меню"
        new_state = MenuStates.MAIN_MENU
    elif current_state == MenuStates.NAVIGATION_MENU:
        new_main_text = f"{UNKNOWN_COMMAND_TEXT}"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Навігаційний екран"
        new_state = MenuStates.NAVIGATION_MENU
    elif current_state == MenuStates.HEROES_MENU:
        new_main_text = f"{UNKNOWN_COMMAND_TEXT}"
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = "Меню Персонажі"
        new_state = MenuStates.HEROES_MENU
    elif current_state == MenuStates.HERO_CLASS_MENU:
        hero_class = data.get('hero_class', 'Танк')
        new_main_text = f"{UNKNOWN_COMMAND_TEXT}"
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = f"Меню класу {hero_class}"
        new_state = MenuStates.HERO_CLASS_MENU
    elif current_state == MenuStates.GUIDES_MENU:
        new_main_text = f"{UNKNOWN_COMMAND_TEXT}"
        new_main_keyboard = get_guides_menu()
        new_interactive_text = "Меню Гайди"
        new_state = MenuStates.GUIDES_MENU
    elif current_state == MenuStates.COUNTER_PICKS_MENU:
        new_main_text = f"{UNKNOWN_COMMAND_TEXT}"
        new_main_keyboard = get_counter_picks_menu()
        new_interactive_text = "Меню Контр-піки"
        new_state = MenuStates.COUNTER_PICKS_MENU
    elif current_state == MenuStates.BUILDS_MENU:
        new_main_text = f"{UNKNOWN_COMMAND_TEXT}"
        new_main_keyboard = get_builds_menu()
        new_interactive_text = "Меню Білди"
        new_state = MenuStates.BUILDS_MENU
    elif current_state == MenuStates.VOTING_MENU:
        new_main_text = f"{UNKNOWN_COMMAND_TEXT}"
        new_main_keyboard = get_voting_menu()
        new_interactive_text = "Меню Голосування"
        new_state = MenuStates.VOTING_MENU
    elif current_state == MenuStates.PROFILE_MENU:
        new_main_text = f"{UNKNOWN_COMMAND_TEXT}"
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "Меню Профіль"
        new_state = MenuStates.PROFILE_MENU
    elif current_state == MenuStates.STATISTICS_MENU:
        new_main_text = f"{UNKNOWN_COMMAND_TEXT}"
        new_main_keyboard = get_statistics_menu()
        new_interactive_text = "Меню Статистика"
        new_state = MenuStates.STATISTICS_MENU
    elif current_state == MenuStates.ACHIEVEMENTS_MENU:
        new_main_text = f"{UNKNOWN_COMMAND_TEXT}"
        new_main_keyboard = get_achievements_menu()
        new_interactive_text = "Меню Досягнення"
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif current_state == MenuStates.SETTINGS_MENU:
        new_main_text = f"{UNKNOWN_COMMAND_TEXT}"
        new_main_keyboard = get_settings_menu()
        new_interactive_text = "Меню Налаштування"
        new_state = MenuStates.SETTINGS_MENU
    elif current_state in [
        MenuStates.SEARCH_HERO,
        MenuStates.SUGGEST_TOPIC,
        MenuStates.CHANGE_USERNAME,
        MenuStates.SEND_FEEDBACK,
        MenuStates.REPORT_BUG
    ]:
        # Якщо користувач перебуває в процесі введення, надсилаємо підказку
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=USE_BUTTON_NAVIGATION_TEXT,
                reply_markup=get_generic_inline_keyboard(),
                parse_mode="HTML"
            )
        except Exception as e:
            logger.error(f"Не вдалося відправити підказку: {e}")
        await state.set_state(current_state)
        return
    else:
        new_main_text = f"{MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)}"
        new_main_keyboard = get_main_menu()
        new_interactive_text = f"{MAIN_MENU_DESCRIPTION}"
        new_state = MenuStates.MAIN_MENU

    # Відправляємо нове повідомлення
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard,
            parse_mode="HTML"
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося відправити нове повідомлення: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        return

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
        except Exception as e:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            # Якщо не вдалося редагувати, відправляємо нове інтерактивне повідомлення
            try:
                interactive_message = await bot.send_message(
                    chat_id=message.chat.id,
                    text=new_interactive_text,
                    reply_markup=get_generic_inline_keyboard(),
                    parse_mode="HTML"
                )
                await state.update_data(interactive_message_id=interactive_message.message_id)
            except Exception as ex:
                logger.error(f"Не вдалося відправити нове інтерактивне повідомлення: {ex}")
    else:
        # Якщо interactive_message_id не знайдено, відправляємо нове інтерактивне повідомлення
        try:
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard(),
                parse_mode="HTML"
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
        except Exception as e:
            logger.error(f"Не вдалося відправити інтерактивне повідомлення: {e}")

    # Оновлюємо стан користувача
    await state.set_state(new_state)

# Обробники для меню Зворотній Зв'язок
@router.message(MenuStates.FEEDBACK_MENU)
async def handle_feedback_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Зворотній Зв'язок")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        # Надсилаємо нове повідомлення з клавіатурою
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu(),
            parse_mode="HTML"
        )
        # Зберігаємо ID повідомлення бота
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_feedback_menu()
    new_interactive_text = "Меню Зворотній Зв'язок"
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = MenuStates.FEEDBACK_MENU

    if user_choice == MenuButton.SEND_FEEDBACK.value:
        new_main_text = f"{SEND_FEEDBACK_TEXT}"
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Надсилання відгуку"
        new_state = MenuStates.SEND_FEEDBACK
    elif user_choice == MenuButton.REPORT_BUG.value:
        new_main_text = f"{REPORT_BUG_TEXT}"
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Повідомлення про помилку"
        new_state = MenuStates.REPORT_BUG
    elif user_choice == MenuButton.BACK.value:
        new_main_text = f"{NAVIGATION_MENU_TEXT}"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = f"{NAVIGATION_INTERACTIVE_TEXT}"
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = f"{UNKNOWN_COMMAND_TEXT}"
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.FEEDBACK_MENU

    # Відправляємо нове повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard,
            parse_mode="HTML"
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося відправити нове повідомлення: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        return

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Оновлюємо bot_message_id в стані
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагуємо інтерактивне повідомлення (Повідомлення 2)
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=new_interactive_keyboard
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        # Якщо не вдалося редагувати, відправляємо нове інтерактивне повідомлення
        try:
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard(),
                parse_mode="HTML"
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
        except Exception as ex:
            logger.error(f"Не вдалося відправити нове інтерактивне повідомлення: {ex}")

    # Оновлюємо стан користувача
    await state.set_state(new_state)

# Обробники для прийому відгуку
@router.message(MenuStates.SEND_FEEDBACK)
async def handle_send_feedback(message: Message, state: FSMContext, bot: Bot):
    feedback = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} надіслав відгук: {feedback}")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Тут додайте логіку зберігання відгуку
    # Наприклад, збереження в базі даних або відправка адміністратору
    try:
        await save_feedback(user_id=message.from_user.id, feedback=feedback)
    except Exception as e:
        logger.error(f"Не вдалося зберегти відгук: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        return

    # Відправляємо підтвердження
    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=FEEDBACK_RECEIVED_TEXT,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Не вдалося відправити підтвердження відгуку: {e}")

    # Повертаємо користувача до меню Зворотній Зв'язок
    await state.set_state(MenuStates.FEEDBACK_MENU)

# Обробники для звіту про помилку
@router.message(MenuStates.REPORT_BUG)
async def handle_report_bug(message: Message, state: FSMContext, bot: Bot):
    bug_report = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} повідомив про помилку: {bug_report}")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Тут додайте логіку обробки звіту про помилку
    # Наприклад, збереження в базі даних або відправка адміністратору
    try:
        await send_bug_report_to_admin(user_id=message.from_user.id, bug_report=bug_report)
    except Exception as e:
        logger.error(f"Не вдалося відправити звіт про помилку адміністратору: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        return

    # Відправляємо підтвердження
    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=BUG_REPORT_RECEIVED_TEXT,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Не вдалося відправити підтвердження звіту про помилку: {e}")

    # Повертаємо користувача до меню Зворотній Зв'язок
    await state.set_state(MenuStates.FEEDBACK_MENU)

# Обробники для прийому пропозиції теми
@router.message(MenuStates.SUGGEST_TOPIC)
async def handle_suggest_topic(message: Message, state: FSMContext, bot: Bot):
    topic = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} пропонує тему: {topic}")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Тут додайте логіку обробки пропозиції теми
    # Наприклад, збереження в базі даних або відправка адміністратору
    try:
        await send_topic_to_admin(user_id=message.from_user.id, topic=topic)
    except Exception as e:
        logger.error(f"Не вдалося відправити пропозицію теми адміністратору: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        return

    # Відправляємо підтвердження
    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=SUGGESTION_RESPONSE_TEXT.format(topic=topic),
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Не вдалося відправити підтвердження пропозиції теми: {e}")

    # Повертаємо користувача до меню Зворотній Зв'язок
    await state.set_state(MenuStates.FEEDBACK_MENU)

# Обробники для зміни Username
@router.message(MenuStates.CHANGE_USERNAME)
async def handle_change_username(message: Message, state: FSMContext, bot: Bot):
    new_username = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} змінює Username на: {new_username}")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Тут додайте логіку зміни Username
    # Наприклад, перевірка унікальності, оновлення в базі даних тощо
    try:
        await update_username(user_id=message.from_user.id, new_username=new_username)
    except Exception as e:
        logger.error(f"Не вдалося оновити Username: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        return

    # Відправляємо підтвердження
    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=CHANGE_USERNAME_RESPONSE_TEXT.format(new_username=new_username),
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Не вдалося відправити підтвердження зміни Username: {e}")

    # Повертаємо користувача до меню Налаштування
    await state.set_state(MenuStates.SETTINGS_MENU)

# Обробники для прийому відгуку
@router.message(MenuStates.SEND_FEEDBACK)
async def handle_send_feedback(message: Message, state: FSMContext, bot: Bot):
    feedback = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} надіслав відгук: {feedback}")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Тут додайте логіку зберігання відгуку
    # Наприклад, збереження в базі даних або відправка адміністратору
    try:
        await save_feedback(user_id=message.from_user.id, feedback=feedback)
    except Exception as e:
        logger.error(f"Не вдалося зберегти відгук: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        return

    # Відправляємо підтвердження
    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=FEEDBACK_RECEIVED_TEXT,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Не вдалося відправити підтвердження відгуку: {e}")

    # Повертаємо користувача до меню Зворотній Зв'язок
    await state.set_state(MenuStates.FEEDBACK_MENU)

# Обробники для звіту про помилку
@router.message(MenuStates.REPORT_BUG)
async def handle_report_bug(message: Message, state: FSMContext, bot: Bot):
    bug_report = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} повідомив про помилку: {bug_report}")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Тут додайте логіку обробки звіту про помилку
    # Наприклад, збереження в базі даних або відправка адміністратору
    try:
        await send_bug_report_to_admin(user_id=message.from_user.id, bug_report=bug_report)
    except Exception as e:
        logger.error(f"Не вдалося відправити звіт про помилку адміністратору: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        return

    # Відправляємо підтвердження
    try:
        await bot.send_message(
            chat_id=message.chat.id,
            text=BUG_REPORT_RECEIVED_TEXT,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
    except Exception as e:
        logger.error(f"Не вдалося відправити підтвердження звіту про помилку: {e}")

    # Повертаємо користувача до меню Зворотній Зв'язок
    await state.set_state(MenuStates.FEEDBACK_MENU)

# Обробники для меню Допомога
@router.message(MenuStates.HELP_MENU)
async def handle_help_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Допомога")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        # Надсилаємо нове повідомлення з клавіатурою
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_ERROR_TEXT,
            reply_markup=get_main_menu(),
            parse_mode="HTML"
        )
        # Зберігаємо ID повідомлення бота
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_help_menu()
    new_interactive_text = "Меню Допомога"
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = MenuStates.HELP_MENU

    if user_choice == MenuButton.INSTRUCTIONS.value:
        new_main_text = f"{INSTRUCTIONS_TEXT}"
        new_interactive_text = "Інструкції"
    elif user_choice == MenuButton.FAQ.value:
        new_main_text = f"{FAQ_TEXT}"
        new_interactive_text = "FAQ"
    elif user_choice == MenuButton.HELP_SUPPORT.value:
        new_main_text = f"{HELP_SUPPORT_TEXT}"
        new_interactive_text = "Підтримка"
    elif user_choice == MenuButton.BACK_TO_PROFILE.value:
        new_main_text = f"{PROFILE_MENU_TEXT}"
        new_main_keyboard = get_profile_menu()
        new_interactive_text = f"{PROFILE_INTERACTIVE_TEXT}"
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = f"{UNKNOWN_COMMAND_TEXT}"
        new_interactive_text = "Невідома команда"

    # Відправляємо нове повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard,
            parse_mode="HTML"
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося відправити нове повідомлення: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        return

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Оновлюємо bot_message_id в стані
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагуємо інтерактивне повідомлення (Повідомлення 2)
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            parse_mode="HTML",
            reply_markup=new_interactive_keyboard
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        # Якщо не вдалося редагувати, відправляємо нове інтерактивне повідомлення
        try:
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard(),
                parse_mode="HTML"
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
        except Exception as ex:
            logger.error(f"Не вдалося відправити нове інтерактивне повідомлення: {ex}")

    # Оновлюємо стан користувача
    await state.set_state(new_state)

# Обробник для невідомих інлайн-кнопок
@router.callback_query(Text("unknown_inline_button"))
async def handle_unknown_inline_button(callback: CallbackQuery, state: FSMContext, bot: Bot):
    logger.info(f"Користувач {callback.from_user.id} натиснув невідому інлайн-кнопку")
    await bot.answer_callback_query(callback.id, text=UNHANDLED_INLINE_BUTTON_TEXT)
    await callback.answer()

# Обробник помилок
@router.errors()
async def handle_error(update: object, exception: Exception):
    logger.error(f"Сталася помилка: {exception}")
    # Визначаємо тип оновлення
    if isinstance(update, Message):
        try:
            await update.answer(text=GENERIC_ERROR_MESSAGE_TEXT, reply_markup=ReplyKeyboardRemove(), parse_mode="HTML")
        except Exception as e:
            logger.error(f"Не вдалося відправити повідомлення про помилку: {e}")
    elif isinstance(update, CallbackQuery):
        try:
            await update.answer(text=GENERIC_ERROR_MESSAGE_TEXT, show_alert=True)
        except Exception as e:
            logger.error(f"Не вдалося відправити повідомлення про помилку: {e}")

# Функція для налаштування обробників
def setup_handlers(router: Router):
    router.message.register(cmd_start, Command("start"))
    router.callback_query.register(handle_intro_next_1, Text("intro_next_1"))
    router.callback_query.register(handle_intro_next_2, Text("intro_next_2"))
    router.callback_query.register(handle_intro_start, Text("intro_start"))
    router.message.register(handle_main_menu_buttons, MenuStates.MAIN_MENU)
    router.message.register(handle_navigation_menu_buttons, MenuStates.NAVIGATION_MENU)
    router.message.register(handle_heroes_menu_buttons, MenuStates.HEROES_MENU)
    router.message.register(handle_gpt_menu_buttons, MenuStates.GPT_MENU)
    router.message.register(handle_gpt_ask_question, MenuStates.GPT_ASK_QUESTION)
    router.message.register(handle_feedback_menu_buttons, MenuStates.FEEDBACK_MENU)
    router.message.register(handle_send_feedback, MenuStates.SEND_FEEDBACK)
    router.message.register(handle_report_bug, MenuStates.REPORT_BUG)
    router.message.register(handle_suggest_topic, MenuStates.SUGGEST_TOPIC)
    router.message.register(handle_change_username, MenuStates.CHANGE_USERNAME)
    router.message.register(handle_help_menu_buttons, MenuStates.HELP_MENU)
    router.callback_query.register(handle_inline_buttons)
    router.message.register(unknown_command)

# Викликаємо функцію для налаштування обробників
setup_handlers(router)
