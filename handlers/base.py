# handlers/base.py

import logging
from aiogram import Router, F, types, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
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
    heroes_by_class,
)
from keyboards.inline_menus import (
    get_generic_inline_keyboard,
    get_intro_page_1_keyboard,
    get_intro_page_2_keyboard,
    get_intro_page_3_keyboard
)

from texts import (
    INTRO_TEXTS,
    MAIN_MENU,
    NAVIGATION_MENU,
    PROFILE_MENU,
    HEROES_MENU,
    HERO_CLASS_MENU,
    GUIDES_MENU,
    COUNTER_PICKS_MENU,
    BUILDS_MENU,
    VOTING_MENU,
    STATISTICS_MENU,
    ACHIEVEMENTS_MENU,
    SETTINGS_MENU,
    FEEDBACK_MENU,
    HELP_MENU,
    UNKNOWN_COMMAND_TEXT,
    GENERIC_ERROR_MESSAGE_TEXT,
    ERROR_MESSAGE_TEXT,
    USE_BUTTON_NAVIGATION_TEXT,
    SEARCH_HERO_RESPONSE_TEXT,
    CHANGE_USERNAME_RESPONSE_TEXT,
    MLS_BUTTON_RESPONSE_TEXT,
    UNHANDLED_INLINE_BUTTON_TEXT,
    MAIN_MENU_BACK_TO_PROFILE_TEXT,
    HERO_COMPARISON_NOT_AVAILABLE_TEXT,
)

# Налаштування логування
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
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

# Допоміжні функції
async def send_main_message(
    bot: Bot,
    chat_id: int,
    text: str,
    keyboard: types.ReplyKeyboardMarkup,
    state: FSMContext,
    new_state: State
) -> int:
    main_message = await bot.send_message(
        chat_id=chat_id,
        text=text,
        reply_markup=keyboard
    )
    await state.update_data(bot_message_id=main_message.message_id)
    await state.set_state(new_state)
    return main_message.message_id

async def edit_interactive_message(
    bot: Bot,
    chat_id: int,
    message_id: int,
    text: str,
    keyboard: types.InlineKeyboardMarkup,
    state: FSMContext
):
    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=text,
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

async def delete_bot_message(
    bot: Bot,
    chat_id: int,
    message_id: int
):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

async def handle_unknown_command(
    message: Message,
    state: FSMContext,
    bot: Bot,
    current_state: str
):
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")
    await message.delete()

    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    interactive_message_id = state_data.get('interactive_message_id')

    # Визначаємо новий текст, клавіатуру та стан залежно від поточного стану
    state_mapping = {
        MenuStates.MAIN_MENU.state: {
            "text": UNKNOWN_COMMAND_TEXT,
            "keyboard": get_main_menu(),
            "interactive_text": "Головне меню",
            "new_state": MenuStates.MAIN_MENU
        },
        MenuStates.NAVIGATION_MENU.state: {
            "text": UNKNOWN_COMMAND_TEXT,
            "keyboard": get_navigation_menu(),
            "interactive_text": "Навігаційний екран",
            "new_state": MenuStates.NAVIGATION_MENU
        },
        MenuStates.HEROES_MENU.state: {
            "text": UNKNOWN_COMMAND_TEXT,
            "keyboard": get_heroes_menu(),
            "interactive_text": "Меню Персонажі",
            "new_state": MenuStates.HEROES_MENU
        },
        MenuStates.HERO_CLASS_MENU.state: {
            "text": UNKNOWN_COMMAND_TEXT,
            "keyboard": get_hero_class_menu(state_data.get('hero_class', 'Танк')),
            "interactive_text": f"Меню класу {state_data.get('hero_class', 'Танк')}",
            "new_state": MenuStates.HERO_CLASS_MENU
        },
        MenuStates.GUIDES_MENU.state: {
            "text": UNKNOWN_COMMAND_TEXT,
            "keyboard": get_guides_menu(),
            "interactive_text": "Меню Гайди",
            "new_state": MenuStates.GUIDES_MENU
        },
        MenuStates.COUNTER_PICKS_MENU.state: {
            "text": UNKNOWN_COMMAND_TEXT,
            "keyboard": get_counter_picks_menu(),
            "interactive_text": "Меню Контр-піки",
            "new_state": MenuStates.COUNTER_PICKS_MENU
        },
        MenuStates.BUILDS_MENU.state: {
            "text": UNKNOWN_COMMAND_TEXT,
            "keyboard": get_builds_menu(),
            "interactive_text": "Меню Білди",
            "new_state": MenuStates.BUILDS_MENU
        },
        MenuStates.VOTING_MENU.state: {
            "text": UNKNOWN_COMMAND_TEXT,
            "keyboard": get_voting_menu(),
            "interactive_text": "Меню Голосування",
            "new_state": MenuStates.VOTING_MENU
        },
        MenuStates.PROFILE_MENU.state: {
            "text": UNKNOWN_COMMAND_TEXT,
            "keyboard": get_profile_menu(),
            "interactive_text": "Меню Профіль",
            "new_state": MenuStates.PROFILE_MENU
        },
        MenuStates.STATISTICS_MENU.state: {
            "text": UNKNOWN_COMMAND_TEXT,
            "keyboard": get_statistics_menu(),
            "interactive_text": "Меню Статистика",
            "new_state": MenuStates.STATISTICS_MENU
        },
        MenuStates.ACHIEVEMENTS_MENU.state: {
            "text": UNKNOWN_COMMAND_TEXT,
            "keyboard": get_achievements_menu(),
            "interactive_text": "Меню Досягнення",
            "new_state": MenuStates.ACHIEVEMENTS_MENU
        },
        MenuStates.SETTINGS_MENU.state: {
            "text": UNKNOWN_COMMAND_TEXT,
            "keyboard": get_settings_menu(),
            "interactive_text": "Меню Налаштування",
            "new_state": MenuStates.SETTINGS_MENU
        },
    }

    if current_state in state_mapping:
        new_main_text = state_mapping[current_state]["text"]
        new_main_keyboard = state_mapping[current_state]["keyboard"]
        new_interactive_text = state_mapping[current_state]["interactive_text"]
        new_state = state_mapping[current_state]["new_state"]
    elif current_state in [
        MenuStates.SEARCH_HERO.state, 
        MenuStates.SEARCH_TOPIC.state, 
        MenuStates.CHANGE_USERNAME.state, 
        MenuStates.RECEIVE_FEEDBACK.state, 
        MenuStates.REPORT_BUG.state
    ]:
        await bot.send_message(
            chat_id=message.chat.id,
            text=USE_BUTTON_NAVIGATION_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.set_state(current_state)
        return
    else:
        new_main_text = MAIN_MENU["text"].format(user_first_name=message.from_user.first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU["description"]
        new_state = MenuStates.MAIN_MENU

    # Відправляємо нове повідомлення
    new_bot_message_id = await send_main_message(
        bot=bot,
        chat_id=message.chat.id,
        text=new_main_text,
        keyboard=new_main_keyboard,
        state=state,
        new_state=new_state
    )

    # Видаляємо старе повідомлення бота
    if bot_message_id:
        await delete_bot_message(bot, message.chat.id, bot_message_id)

    # Редагуємо інтерактивне повідомлення
    if interactive_message_id:
        await edit_interactive_message(
            bot=bot,
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_interactive_text,
            keyboard=get_generic_inline_keyboard(),
            state=state
        )
    else:
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

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
        text=INTRO_TEXTS["page_1"],
        parse_mode="HTML",
        reply_markup=get_intro_page_1_keyboard()
    )

    # Зберігаємо ID інтерактивного повідомлення
    await state.update_data(interactive_message_id=interactive_message.message_id)

# Обробники натискання інлайн-кнопок для Intro
@router.callback_query(F.data == "intro_next_1")
async def handle_intro_next_1(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # Отримуємо ID інтерактивного повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    # Редагуємо інтерактивне повідомлення на другу сторінку
    await edit_interactive_message(
        bot=bot,
        chat_id=callback.message.chat.id,
        message_id=interactive_message_id,
        text=INTRO_TEXTS["page_2"],
        keyboard=get_intro_page_2_keyboard(),
        state=state
    )

    # Оновлюємо стан
    await state.set_state(MenuStates.INTRO_PAGE_2)
    await callback.answer()

@router.callback_query(F.data == "intro_next_2")
async def handle_intro_next_2(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # Отримуємо ID інтерактивного повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    # Редагуємо інтерактивне повідомлення на третю сторінку
    await edit_interactive_message(
        bot=bot,
        chat_id=callback.message.chat.id,
        message_id=interactive_message_id,
        text=INTRO_TEXTS["page_3"],
        keyboard=get_intro_page_3_keyboard(),
        state=state
    )

    # Оновлюємо стан
    await state.set_state(MenuStates.INTRO_PAGE_3)
    await callback.answer()

@router.callback_query(F.data == "intro_start")
async def handle_intro_start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_first_name = callback.from_user.first_name

    # Відправляємо основне меню з клавіатурою
    main_menu_text_formatted = MAIN_MENU["text"].format(user_first_name=user_first_name)
    main_message_id = await send_main_message(
        bot=bot,
        chat_id=callback.message.chat.id,
        text=main_menu_text_formatted,
        keyboard=get_main_menu(),
        state=state,
        new_state=MenuStates.MAIN_MENU
    )

    # Отримуємо ID інтерактивного повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    # Оновлюємо інтерактивне повідомлення з описом основного меню
    await edit_interactive_message(
        bot=bot,
        chat_id=callback.message.chat.id,
        message_id=interactive_message_id,
        text=MAIN_MENU["description"],
        keyboard=get_generic_inline_keyboard(),
        state=state
    )

    await callback.answer()

# Загальна функція для обробки меню
async def handle_menu_buttons(
    message: Message,
    state: FSMContext,
    bot: Bot,
    menu_text: str,
    menu_keyboard,
    interactive_text: str,
    new_state: State
):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню {menu_text}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        # Надсилаємо нове повідомлення з клавіатурою
        new_bot_message_id = await send_main_message(
            bot=bot,
            chat_id=message.chat.id,
            text=MAIN_MENU["error_text"],
            keyboard=get_main_menu(),
            state=state,
            new_state=MenuStates.MAIN_MENU
        )
        return

    # Відправляємо нове повідомлення з клавіатурою
    new_bot_message_id = await send_main_message(
        bot=bot,
        chat_id=message.chat.id,
        text=menu_text,
        keyboard=menu_keyboard,
        state=state,
        new_state=new_state
    )

    # Видаляємо попереднє повідомлення з клавіатурою
    await delete_bot_message(bot, message.chat.id, bot_message_id)

    # Редагуємо інтерактивне повідомлення
    await edit_interactive_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        text=interactive_text,
        keyboard=get_generic_inline_keyboard(),
        state=state
    )

# Обробники для меню
@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} у головному меню")

    # Визначаємо новий текст та клавіатуру для повідомлень
    if user_choice == MenuButton.NAVIGATION.value:
        new_main_text = NAVIGATION_MENU["text"]
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = NAVIGATION_MENU["interactive_text"]
        new_state = MenuStates.NAVIGATION_MENU
    elif user_choice == MenuButton.PROFILE.value:
        new_main_text = PROFILE_MENU["text"]
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_MENU["interactive_text"]
        new_state = MenuStates.PROFILE_MENU
    else:
        # Невідома команда
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.MAIN_MENU

    # Викликаємо загальну функцію для обробки меню
    await handle_menu_buttons(
        message=message,
        state=state,
        bot=bot,
        menu_text=new_main_text,
        menu_keyboard=new_main_keyboard,
        interactive_text=new_interactive_text,
        new_state=new_state
    )

# Аналогічно створіть обробники для інших меню, наприклад:
@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Навігація")

    if user_choice == MenuButton.HEROES.value:
        new_main_text = HEROES_MENU["text"]
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = HEROES_MENU["interactive_text"]
        new_state = MenuStates.HEROES_MENU
    elif user_choice == MenuButton.GUIDES.value:
        new_main_text = GUIDES_MENU["text"]
        new_main_keyboard = get_guides_menu()
        new_interactive_text = GUIDES_MENU["interactive_text"]
        new_state = MenuStates.GUIDES_MENU
    elif user_choice == MenuButton.COUNTER_PICKS.value:
        new_main_text = COUNTER_PICKS_MENU["text"]
        new_main_keyboard = get_counter_picks_menu()
        new_interactive_text = COUNTER_PICKS_MENU["interactive_text"]
        new_state = MenuStates.COUNTER_PICKS_MENU
    elif user_choice == MenuButton.BUILDS.value:
        new_main_text = BUILDS_MENU["text"]
        new_main_keyboard = get_builds_menu()
        new_interactive_text = BUILDS_MENU["interactive_text"]
        new_state = MenuStates.BUILDS_MENU
    elif user_choice == MenuButton.VOTING.value:
        new_main_text = VOTING_MENU["text"]
        new_main_keyboard = get_voting_menu()
        new_interactive_text = VOTING_MENU["interactive_text"]
        new_state = MenuStates.VOTING_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = MAIN_MENU["text"].format(user_first_name=message.from_user.first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU["description"]
        new_state = MenuStates.MAIN_MENU
    else:
        # Невідома команда
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.NAVIGATION_MENU

    await handle_menu_buttons(
        message=message,
        state=state,
        bot=bot,
        menu_text=new_main_text,
        menu_keyboard=new_main_keyboard,
        interactive_text=new_interactive_text,
        new_state=new_state
    )

# Обробник для інлайн-кнопок
@router.callback_query(F.data != None)  # Ensure data is present
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
            new_interactive_text = MAIN_MENU["description"]
            new_interactive_keyboard = get_generic_inline_keyboard()

            # Редагуємо інтерактивне повідомлення
            await edit_interactive_message(
                bot=bot,
                chat_id=callback.message.chat.id,
                message_id=interactive_message_id,
                text=new_interactive_text,
                keyboard=new_interactive_keyboard,
                state=state
            )

            # Відправляємо головне меню
            main_menu_text_formatted = MAIN_MENU["text"].format(user_first_name=callback.from_user.first_name)
            main_message_id = await send_main_message(
                bot=bot,
                chat_id=callback.message.chat.id,
                text=main_menu_text_formatted,
                keyboard=get_main_menu(),
                state=state,
                new_state=MenuStates.MAIN_MENU
            )

            # Видаляємо попереднє повідомлення з клавіатурою
            old_bot_message_id = state_data.get('bot_message_id')  # Corrected to retrieve from state
            if old_bot_message_id:
                await delete_bot_message(bot, callback.message.chat.id, old_bot_message_id)
        else:
            # Додайте обробку інших інлайн-кнопок за потребою
            await bot.answer_callback_query(callback.id, text=UNHANDLED_INLINE_BUTTON_TEXT)
    else:
        logger.error("interactive_message_id не знайдено")
        await bot.answer_callback_query(callback.id, text=GENERIC_ERROR_MESSAGE_TEXT)

    await callback.answer()

# Обробник для невідомих повідомлень
@router.message()
async def unknown_command_handler(message: Message, state: FSMContext, bot: Bot):
    current_state = await state.get_state()
    await handle_unknown_command(message, state, bot, current_state)

# Обробники для прийому введення в різних станах
@router.message(MenuStates.SEARCH_HERO)
async def handle_search_hero(message: Message, state: FSMContext, bot: Bot):
    hero_name = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} шукає героя: {hero_name}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Тут додайте логіку пошуку героя
    # Наприклад, перевірка чи існує герой, відправка інформації тощо
    # Поки що відправимо повідомлення про отримання запиту

    response_text = SEARCH_HERO_RESPONSE_TEXT.format(hero_name=hero_name)

    await bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard()
    )

    # Повертаємо користувача до попереднього меню
    await state.set_state(MenuStates.HEROES_MENU)

@router.message(MenuStates.SEARCH_TOPIC)
async def handle_search_topic(message: Message, state: FSMContext, bot: Bot):
    topic = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} пропонує тему: {topic}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Тут додайте логіку обробки пропозиції теми
    # Наприклад, збереження в базі даних або відправка адміністратору
    # Поки що відправимо повідомлення про отримання запиту

    response_text = FEEDBACK_MENU["submenus"]["suggestion_response"].format(topic=topic)

    await bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard()
    )

    # Повертаємо користувача до меню Зворотний Зв'язок
    await state.set_state(MenuStates.FEEDBACK_MENU)

@router.message(MenuStates.CHANGE_USERNAME)
async def handle_change_username(message: Message, state: FSMContext, bot: Bot):
    new_username = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} змінює Username на: {new_username}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Тут додайте логіку зміни Username
    # Наприклад, перевірка унікальності, оновлення в базі даних тощо
    # Поки що відправимо повідомлення про отримання запиту

    response_text = CHANGE_USERNAME_RESPONSE_TEXT.format(new_username=new_username)

    await bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard()
    )

    # Повертаємо користувача до меню Налаштування
    await state.set_state(MenuStates.SETTINGS_MENU)

@router.message(MenuStates.RECEIVE_FEEDBACK)
async def handle_receive_feedback(message: Message, state: FSMContext, bot: Bot):
    feedback = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} надіслав відгук: {feedback}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Тут додайте логіку зберігання відгуку
    # Наприклад, збереження в базі даних або відправка адміністратору
    # Поки що відправимо повідомлення про отримання відгуку

    response_text = FEEDBACK_MENU["submenus"]["feedback_received"]

    await bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard()
    )

    # Повертаємо користувача до меню Зворотний Зв'язок
    await state.set_state(MenuStates.FEEDBACK_MENU)

@router.message(MenuStates.REPORT_BUG)
async def handle_report_bug(message: Message, state: FSMContext, bot: Bot):
    bug_report = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} повідомив про помилку: {bug_report}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Тут додайте логіку обробки звіту про помилку
    # Наприклад, збереження в базі даних або відправка адміністратору
    # Поки що відправимо повідомлення про отримання звіту

    response_text = FEEDBACK_MENU["submenus"]["bug_report_received"]

    await bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard()
    )

    # Повертаємо користувача до меню Зворотний Зв'язок
    await state.set_state(MenuStates.FEEDBACK_MENU)
