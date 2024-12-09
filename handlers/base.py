import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram import exceptions  # Для обробки специфічних винятків

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
    UNKNOWN_COMMAND_TEXT,
    GENERIC_ERROR_MESSAGE_TEXT,
    NAVIGATION_MENU_TEXT,
    NAVIGATION_INTERACTIVE_TEXT,
    PROFILE_MENU_TEXT,
    PROFILE_INTERACTIVE_TEXT,
    FEEDBACK_RECEIVED_TEXT,
    BUG_REPORT_RECEIVED_TEXT,
    SEND_FEEDBACK_TEXT,
    REPORT_BUG_TEXT,
    CHANGE_USERNAME_RESPONSE_TEXT,
    SEARCH_HERO_RESPONSE_TEXT,
    MLS_BUTTON_RESPONSE_TEXT,
    UNHANDLED_INLINE_BUTTON_TEXT,
    USE_BUTTON_NAVIGATION_TEXT,
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
    # Додайте додаткові стани, якщо необхідно

# Допоміжна функція для редагування інтерактивного повідомлення
async def edit_interactive_message(
    bot: Bot,
    chat_id: int,
    message_id: int,
    new_text: str,
    new_reply_markup: InlineKeyboardMarkup = None,
    parse_mode: str = "HTML"
):
    try:
        await bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=new_text,
            parse_mode=parse_mode,
            reply_markup=new_reply_markup
        )
        logger.info(f"Інтерактивне повідомлення {message_id} успішно відредаговано")
        return message_id
    except exceptions.BadRequest as e:
        if "message is not modified" in str(e):
            logger.info(f"Повідомлення {message_id} не потребує редагування")
            return message_id
        elif "message to edit not found" in str(e):
            logger.error(f"Повідомлення {message_id} не знайдено")
            # Надсилаємо нове інтерактивне повідомлення, якщо старе не знайдено
            interactive_message = await bot.send_message(
                chat_id=chat_id,
                text=new_text,
                reply_markup=new_reply_markup
            )
            logger.info(f"Нове інтерактивне повідомлення відправлено: {interactive_message.message_id}")
            return interactive_message.message_id
        else:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення {message_id}: {e}")
            return message_id
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення {message_id}: {e}")
        return message_id

# Допоміжна функція для відправки основного меню
async def send_main_menu(
    bot: Bot,
    chat_id: int,
    user_first_name: str
):
    main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
    try:
        main_menu_message = await bot.send_message(
            chat_id=chat_id,
            text=main_menu_text_formatted,
            reply_markup=get_main_menu()
        )
        logger.info(f"Основне меню відправлено: {main_menu_message.message_id}")
        return main_menu_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося відправити основне меню: {e}")
        await bot.send_message(
            chat_id=chat_id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        return None

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

    # Відправляємо перше інтерактивне повідомлення з кнопкою 'Далі'
    try:
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=INTRO_PAGE_1_TEXT,
            parse_mode="HTML",
            reply_markup=get_intro_page_1_keyboard()
        )
        # Зберігаємо ID інтерактивного повідомлення
        await state.update_data(interactive_message_id=interactive_message.message_id)
    except Exception as e:
        logger.error(f"Не вдалося відправити перше інтерактивне повідомлення: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )

# Обробник натискання інлайн-кнопки 'Далі' на першій сторінці
@router.callback_query(F.data == "intro_next_1")
async def handle_intro_next_1(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # Отримуємо ID інтерактивного повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')
    chat_id = callback.message.chat.id

    if not interactive_message_id:
        logger.error("interactive_message_id не знайдено у стані")
        await bot.send_message(
            chat_id=chat_id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await callback.answer(text="Сталася помилка. Спробуйте пізніше.")
        return

    # Редагуємо інтерактивне повідомлення на другу сторінку
    new_text = INTRO_PAGE_2_TEXT
    new_keyboard = get_intro_page_2_keyboard()

    new_interactive_message_id = await edit_interactive_message(
        bot=bot,
        chat_id=chat_id,
        message_id=interactive_message_id,
        new_text=new_text,
        new_reply_markup=new_keyboard
    )

    # Оновлюємо interactive_message_id, якщо повідомлення було створено заново
    if new_interactive_message_id != interactive_message_id:
        await state.update_data(interactive_message_id=new_interactive_message_id)

    # Оновлюємо стан
    await state.set_state(MenuStates.INTRO_PAGE_2)
    await callback.answer()

# Обробник натискання інлайн-кнопки 'Далі' на другій сторінці
@router.callback_query(F.data == "intro_next_2")
async def handle_intro_next_2(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # Отримуємо ID інтерактивного повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')
    chat_id = callback.message.chat.id

    if not interactive_message_id:
        logger.error("interactive_message_id не знайдено у стані")
        await bot.send_message(
            chat_id=chat_id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await callback.answer(text="Сталася помилка. Спробуйте пізніше.")
        return

    # Редагуємо інтерактивне повідомлення на третю сторінку
    new_text = INTRO_PAGE_3_TEXT
    new_keyboard = get_intro_page_3_keyboard()

    new_interactive_message_id = await edit_interactive_message(
        bot=bot,
        chat_id=chat_id,
        message_id=interactive_message_id,
        new_text=new_text,
        new_reply_markup=new_keyboard
    )

    # Оновлюємо interactive_message_id, якщо повідомлення було створено заново
    if new_interactive_message_id != interactive_message_id:
        await state.update_data(interactive_message_id=new_interactive_message_id)

    # Оновлюємо стан
    await state.set_state(MenuStates.INTRO_PAGE_3)
    await callback.answer()

# Обробник натискання інлайн-кнопки 'Розпочати' на третій сторінці
@router.callback_query(F.data == "intro_start")
async def handle_intro_start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_first_name = callback.from_user.first_name
    chat_id = callback.message.chat.id

    # Отримуємо ID інтерактивного повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if not interactive_message_id:
        logger.error("interactive_message_id не знайдено у стані")
        await bot.send_message(
            chat_id=chat_id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        await callback.answer(text="Сталася помилка. Спробуйте пізніше.")
        return

    # Редагуємо інтерактивне повідомлення на опис основного меню
    new_text = MAIN_MENU_DESCRIPTION
    new_keyboard = get_generic_inline_keyboard()

    new_interactive_message_id = await edit_interactive_message(
        bot=bot,
        chat_id=chat_id,
        message_id=interactive_message_id,
        new_text=new_text,
        new_reply_markup=new_keyboard
    )

    # Оновлюємо interactive_message_id, якщо повідомлення було створено заново
    if new_interactive_message_id != interactive_message_id:
        await state.update_data(interactive_message_id=new_interactive_message_id)

    # Відправляємо основне меню з клавіатурою
    main_menu_message_id = await send_main_menu(
        bot=bot,
        chat_id=chat_id,
        user_first_name=user_first_name
    )

    if main_menu_message_id:
        # Оновлюємо bot_message_id
        await state.update_data(bot_message_id=main_menu_message_id)
        # Встановлюємо стан користувача на MAIN_MENU
        await state.set_state(MenuStates.MAIN_MENU)
        await callback.answer(text="Вітаємо! Головне меню відображено.")
    else:
        await callback.answer(text="Сталася помилка. Спробуйте пізніше.")

# Обробник натискання звичайних кнопок у головному меню
@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} у головному меню")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    chat_id = message.chat.id

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        # Надсилаємо нове повідомлення з клавіатурою
        main_message_id = await send_main_menu(
            bot=bot,
            chat_id=chat_id,
            user_first_name=message.from_user.first_name
        )
        if main_message_id:
            await state.update_data(bot_message_id=main_message_id)
            await state.set_state(MenuStates.MAIN_MENU)
        else:
            await bot.send_message(
                chat_id=chat_id,
                text=GENERIC_ERROR_MESSAGE_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
        return

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
    else:
        # Невідома команда
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.MAIN_MENU

    # Відправляємо нове повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=chat_id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
        await state.update_data(bot_message_id=new_bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося відправити нове повідомлення з меню: {e}")
        await bot.send_message(
            chat_id=chat_id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        return

    # Видаляємо попереднє повідомлення з клавіатурою (звичайне повідомлення)
    try:
        await bot.delete_message(chat_id=chat_id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Редагуємо інтерактивне повідомлення, не видаляючи його
    if new_interactive_text:
        await edit_interactive_message(
            bot=bot,
            chat_id=chat_id,
            message_id=interactive_message_id,
            new_text=new_interactive_text,
            new_reply_markup=get_generic_inline_keyboard()
        )

    # Оновлюємо стан користувача
    if new_state:
        await state.set_state(new_state)
    else:
        await state.set_state(MenuStates.MAIN_MENU)

# Обробник натискання звичайних кнопок у меню Зворотний Зв'язок
@router.message(MenuStates.FEEDBACK_MENU)
async def handle_feedback_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Зворотний Зв'язок")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Отримуємо дані стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    chat_id = message.chat.id

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        # Надсилаємо нове повідомлення з клавіатурою
        main_message_id = await send_main_menu(
            bot=bot,
            chat_id=chat_id,
            user_first_name=message.from_user.first_name
        )
        if main_message_id:
            await state.update_data(bot_message_id=main_message_id)
            await state.set_state(MenuStates.MAIN_MENU)
        else:
            await bot.send_message(
                chat_id=chat_id,
                text=GENERIC_ERROR_MESSAGE_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
        return

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_feedback_menu()
    new_interactive_text = ""
    new_state = MenuStates.FEEDBACK_MENU

    if user_choice == MenuButton.SEND_FEEDBACK.value:
        new_main_text = SEND_FEEDBACK_TEXT
        new_interactive_text = "Надсилання відгуку"
        new_state = MenuStates.RECEIVE_FEEDBACK
    elif user_choice == MenuButton.REPORT_BUG.value:
        new_main_text = REPORT_BUG_TEXT
        new_interactive_text = "Повідомлення про помилку"
        new_state = MenuStates.REPORT_BUG
    elif user_choice == MenuButton.BACK.value:
        # Повертаємось до меню Профіль
        new_main_text = PROFILE_MENU_TEXT
        new_main_keyboard = get_profile_menu()
        new_interactive_text = PROFILE_INTERACTIVE_TEXT
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.FEEDBACK_MENU

    # Відправляємо нове повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=chat_id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
        await state.update_data(bot_message_id=new_bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося відправити нове повідомлення з меню: {e}")
        await bot.send_message(
            chat_id=chat_id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        return

    # Видаляємо попереднє повідомлення з клавіатурою (звичайне повідомлення)
    try:
        await bot.delete_message(chat_id=chat_id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Редагуємо інтерактивне повідомлення, не видаляючи його
    if new_interactive_text:
        await edit_interactive_message(
            bot=bot,
            chat_id=chat_id,
            message_id=interactive_message_id,
            new_text=new_interactive_text,
            new_reply_markup=get_generic_inline_keyboard()
        )

    # Оновлюємо стан користувача
    await state.set_state(new_state)

# Обробник інлайн-кнопок (залишаємо лише один обробник для інших кнопок)
@router.callback_query()
async def handle_inline_buttons(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = callback.data
    logger.info(f"Користувач {callback.from_user.id} натиснув інлайн-кнопку: {data}")

    # Отримуємо interactive_message_id з стану
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')
    chat_id = callback.message.chat.id

    if interactive_message_id:
        # Обробляємо інлайн-кнопки
        if data == "mls_button":
            await bot.answer_callback_query(callback.id, text=MLS_BUTTON_RESPONSE_TEXT)
        elif data == "menu_back":
            # Повернення до головного меню
            new_interactive_text = MAIN_MENU_DESCRIPTION
            new_interactive_keyboard = get_generic_inline_keyboard()

            new_interactive_message_id = await edit_interactive_message(
                bot=bot,
                chat_id=chat_id,
                message_id=interactive_message_id,
                new_text=new_interactive_text,
                new_reply_markup=new_interactive_keyboard
            )

            # Оновлюємо interactive_message_id, якщо повідомлення було створено заново
            if new_interactive_message_id != interactive_message_id:
                await state.update_data(interactive_message_id=new_interactive_message_id)

            # Відправляємо головне меню
            main_menu_message_id = await send_main_menu(
                bot=bot,
                chat_id=chat_id,
                user_first_name=callback.from_user.first_name
            )

            if main_menu_message_id:
                # Оновлюємо bot_message_id
                await state.update_data(bot_message_id=main_menu_message_id)
                # Видаляємо попереднє повідомлення з клавіатурою
                old_bot_message_id = state_data.get('bot_message_id')
                if old_bot_message_id:
                    try:
                        await bot.delete_message(chat_id=chat_id, message_id=old_bot_message_id)
                    except Exception as e:
                        logger.error(f"Не вдалося видалити повідомлення бота: {e}")
                # Встановлюємо стан користувача на MAIN_MENU
                await state.set_state(MenuStates.MAIN_MENU)
                await bot.answer_callback_query(callback.id, text="Повернулися до головного меню.")
            else:
                await bot.answer_callback_query(callback.id, text="Сталася помилка. Спробуйте пізніше.")
        else:
            # Додайте обробку інших інлайн-кнопок за потребою
            await bot.answer_callback_query(callback.id, text=UNHANDLED_INLINE_BUTTON_TEXT)
    else:
        logger.error("interactive_message_id не знайдено")
        await bot.answer_callback_query(callback.id, text=GENERIC_ERROR_MESSAGE_TEXT)

    await callback.answer()

# Обробник для прийому пошуку героя
@router.message(MenuStates.SEARCH_HERO)
async def handle_search_hero(message: Message, state: FSMContext, bot: Bot):
    hero_name = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} шукає героя: {hero_name}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Тут додайте логіку пошуку героя
    # Наприклад, перевірка чи існує герой, відправка інформації тощо
    # Поки що відправимо повідомлення про отримання запиту

    if hero_name:
        response_text = SEARCH_HERO_RESPONSE_TEXT.format(hero_name=hero_name)
    else:
        response_text = "Будь ласка, введіть ім'я героя для пошуку."

    await bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard()
    )

    # Повертаємо користувача до попереднього меню
    await state.set_state(MenuStates.HEROES_MENU)

# Обробник для прийому теми пропозиції
@router.message(MenuStates.SEARCH_TOPIC)
async def handle_search_topic(message: Message, state: FSMContext, bot: Bot):
    topic = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} пропонує тему: {topic}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Тут додайте логіку обробки пропозиції теми
    # Наприклад, збереження в базі даних або відправка адміністратору
    # Поки що відправимо повідомлення про отримання запиту

    if topic:
        response_text = SUGGESTION_RESPONSE_TEXT.format(topic=topic)
    else:
        response_text = "Будь ласка, введіть тему для пропозиції."

    await bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard()
    )

    # Повертаємо користувача до меню Зворотний Зв'язок
    await state.set_state(MenuStates.FEEDBACK_MENU)

# Обробник для зміни Username
@router.message(MenuStates.CHANGE_USERNAME)
async def handle_change_username(message: Message, state: FSMContext, bot: Bot):
    new_username = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} змінює Username на: {new_username}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Тут додайте логіку зміни Username
    # Наприклад, перевірка унікальності, оновлення в базі даних тощо
    # Поки що відправимо повідомлення про отримання запиту

    if new_username:
        response_text = CHANGE_USERNAME_RESPONSE_TEXT.format(new_username=new_username)
    else:
        response_text = "Будь ласка, введіть новий Username."

    await bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard()
    )

    # Повертаємо користувача до меню Налаштування
    await state.set_state(MenuStates.SETTINGS_MENU)

# Обробник для прийому відгуку
@router.message(MenuStates.RECEIVE_FEEDBACK)
async def handle_receive_feedback(message: Message, state: FSMContext, bot: Bot):
    feedback = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} надіслав відгук: {feedback}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Тут додайте логіку зберігання відгуку
    # Наприклад, збереження в базі даних або відправка адміністратору
    # Поки що відправимо повідомлення про отримання відгуку

    if feedback:
        response_text = FEEDBACK_RECEIVED_TEXT
    else:
        response_text = "Будь ласка, залиште свій відгук."

    await bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard()
    )

    # Повертаємо користувача до меню Зворотний Зв'язок
    await state.set_state(MenuStates.FEEDBACK_MENU)

# Обробник для звіту про помилку
@router.message(MenuStates.REPORT_BUG)
async def handle_report_bug(message: Message, state: FSMContext, bot: Bot):
    bug_report = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} повідомив про помилку: {bug_report}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Тут додайте логіку обробки звіту про помилку
    # Наприклад, збереження в базі даних або відправка адміністратору
    # Поки що відправимо повідомлення про отримання звіту

    if bug_report:
        response_text = BUG_REPORT_RECEIVED_TEXT
    else:
        response_text = "Будь ласка, опишіть помилку, яку ви знайшли."

    await bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard()
    )

    # Повертаємо користувача до меню Зворотний Зв'язок
    await state.set_state(MenuStates.FEEDBACK_MENU)

# Обробник для невідомих повідомлень
@router.message()
async def unknown_command(message: Message, state: FSMContext, bot: Bot):
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити невідоме повідомлення користувача: {e}")

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    chat_id = message.chat.id

    # Визначаємо поточний стан
    current_state = await state.get_state()

    # Визначаємо новий текст та клавіатуру залежно від стану
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

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
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=USE_BUTTON_NAVIGATION_TEXT,
                reply_markup=get_generic_inline_keyboard()
            )
        except Exception as e:
            logger.error(f"Не вдалося відправити підказку користувачу: {e}")
        await state.set_state(current_state)
        return
    else:
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=message.from_user.first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU

    # Відправляємо нове повідомлення з клавіатурою (Повідомлення 1)
    try:
        main_message = await bot.send_message(
            chat_id=chat_id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
        await state.update_data(bot_message_id=new_bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося відправити нове повідомлення з меню: {e}")
        await bot.send_message(
            chat_id=chat_id,
            text=GENERIC_ERROR_MESSAGE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
        return

    # Видаляємо старе повідомлення з клавіатурою (Після відправки нового)
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Редагуємо інтерактивне повідомлення (Повідомлення 2)
    if new_interactive_text:
        await edit_interactive_message(
            bot=bot,
            chat_id=chat_id,
            message_id=interactive_message_id,
            new_text=new_interactive_text,
            new_reply_markup=get_generic_inline_keyboard()
        )

    # Оновлюємо стан користувача
    if new_state:
        await state.set_state(new_state)
    else:
        await state.set_state(MenuStates.MAIN_MENU)

# Функція для налаштування обробників
def setup_handlers(dp):
    dp.include_router(router)