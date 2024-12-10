# handlers/base.py

import logging
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove

from keyboards.menus import (
    MenuButton,
    get_main_menu,
    get_navigation_menu,
    get_heroes_menu,
    get_hero_class_menu,
    get_guides_menu,
    get_counter_picks_menu,
    get_builds_menu,
    get_voting_menu,
    get_m6_menu,
    get_gpt_menu,
    get_meta_menu,
    get_tournaments_menu,
    get_profile_menu_buttons,
    get_statistics_menu,
    get_achievements_menu,
    get_settings_menu,
    get_feedback_menu,
    get_help_menu
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
    USE_BUTTON_NAVIGATION_TEXT,
    SEARCH_HERO_RESPONSE_TEXT,
    SUGGESTION_RESPONSE_TEXT,
    CHANGE_USERNAME_RESPONSE_TEXT,
    FEEDBACK_RECEIVED_TEXT,
    BUG_REPORT_RECEIVED_TEXT,
    MLS_BUTTON_RESPONSE_TEXT,
    UNHANDLED_INLINE_BUTTON_TEXT
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
    SUGGEST_TOPIC = State()
    CHANGE_USERNAME = State()
    RECEIVE_FEEDBACK = State()
    REPORT_BUG = State()
    M6_MENU = State()
    GPT_MENU = State()
    META_MENU = State()
    TOURNAMENTS_MENU = State()
    # Додайте додаткові стани, якщо це необхідно

# Загальні функції

async def update_menu(
    message: Message,
    state: FSMContext,
    bot: Bot,
    new_main_text: str,
    new_main_keyboard: ReplyKeyboardMarkup,
    new_interactive_text: str,
    new_state: State
):
    """
    Оновлює основне меню та інтерактивне повідомлення.
    """
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Відправка нового основного повідомлення
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    # Видалення попереднього основного повідомлення
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Оновлення bot_message_id
    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагування інтерактивного повідомлення
    if interactive_message_id:
        try:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=interactive_message_id,
                text=new_interactive_text,
                parse_mode="HTML",
                reply_markup=ReplyKeyboardRemove()
            )
        except Exception as e:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=ReplyKeyboardRemove()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
    else:
        # Якщо interactive_message_id відсутній, створюємо нове інтерактивне повідомлення
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=ReplyKeyboardRemove()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    # Встановлення нового стану
    await state.set_state(new_state)

# Обробник команди /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
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
        reply_markup=get_generic_inline_keyboard()  # Потрібно визначити функцію для інлайн-кнопок
    )

    # Зберігаємо ID інтерактивного повідомлення
    await state.update_data(interactive_message_id=interactive_message.message_id)

# Обробники натискання інлайн-кнопок 'Далі' та 'Розпочати'
@router.callback_query(lambda c: c.data == "intro_next_1")
async def handle_intro_next_1(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # Отримуємо ID інтерактивного повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    # Редагуємо інтерактивне повідомлення на другу сторінку
    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=INTRO_PAGE_2_TEXT,
            parse_mode="HTML",
            reply_markup=get_intro_page_2_keyboard()  # Потрібно визначити функцію для інлайн-кнопок
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

@router.callback_query(lambda c: c.data == "intro_next_2")
async def handle_intro_next_2(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # Отримуємо ID інтерактивного повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    # Редагуємо інтерактивне повідомлення на третю сторінку
    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=INTRO_PAGE_3_TEXT,
            parse_mode="HTML",
            reply_markup=get_intro_page_3_keyboard()  # Потрібно визначити функцію для інлайн-кнопок
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

@router.callback_query(lambda c: c.data == "intro_start")
async def handle_intro_start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_first_name = callback.from_user.first_name

    # Відправляємо основне меню з клавіатурою
    main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
    main_menu_message = await bot.send_message(
        chat_id=callback.message.chat.id,
        text=main_menu_text_formatted,
        reply_markup=get_main_menu()
    )

    # Оновлюємо ID основного повідомлення
    await state.update_data(bot_message_id=main_menu_message.message_id)

    # Отримуємо ID інтерактивного повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    # Оновлюємо інтерактивне повідомлення з описом основного меню
    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=MAIN_MENU_DESCRIPTION,
            parse_mode="HTML",
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        # Якщо не вдалося редагувати, відправляємо нове інтерактивне повідомлення
        interactive_message = await bot.send_message(
            chat_id=callback.message.chat.id,
            text=MAIN_MENU_DESCRIPTION,
            reply_markup=ReplyKeyboardRemove()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    # Встановлюємо стан користувача на MAIN_MENU
    await state.set_state(MenuStates.MAIN_MENU)
    await callback.answer()

# Обробники натискання звичайних кнопок для різних меню

@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} у головному меню")

    # Видаляємо повідомлення користувача
    await message.delete()

    transition = {
        MenuButton.NAVIGATION.value: {
            "text": MenuButton.NAVIGATION.value,
            "keyboard": get_navigation_menu(),
            "interactive_text": "Оберіть розділ навігації.",
            "state": MenuStates.NAVIGATION_MENU
        },
        MenuButton.PROFILE.value: {
            "text": MenuButton.PROFILE.value,
            "keyboard": get_profile_menu_buttons(),
            "interactive_text": "Оберіть розділ профілю.",
            "state": MenuStates.PROFILE_MENU
        }
    }.get(user_choice)

    if transition:
        await update_menu(
            message=message,
            state=state,
            bot=bot,
            new_main_text=transition["text"],
            new_main_keyboard=transition["keyboard"],
            new_interactive_text=transition["interactive_text"],
            new_state=transition["state"]
        )
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.MAIN_MENU

        await update_menu(
            message=message,
            state=state,
            bot=bot,
            new_main_text=new_main_text,
            new_main_keyboard=new_main_keyboard,
            new_interactive_text=new_interactive_text,
            new_state=new_state
        )

@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Навігації")

    # Видаляємо повідомлення користувача
    await message.delete()

    transition = {
        MenuButton.HEROES.value: {
            "text": MenuButton.HEROES.value,
            "keyboard": get_heroes_menu(),
            "interactive_text": "Оберіть розділ Персонажів.",
            "state": MenuStates.HEROES_MENU
        },
        MenuButton.BUILDS.value: {
            "text": MenuButton.BUILDS.value,
            "keyboard": get_builds_menu(),
            "interactive_text": "Оберіть розділ Білд.",
            "state": MenuStates.BUILDS_MENU
        },
        MenuButton.COUNTER_PICKS.value: {
            "text": MenuButton.COUNTER_PICKS.value,
            "keyboard": get_counter_picks_menu(),
            "interactive_text": "Оберіть розділ Контр-піків.",
            "state": MenuStates.COUNTER_PICKS_MENU
        },
        MenuButton.GUIDES.value: {
            "text": MenuButton.GUIDES.value,
            "keyboard": get_guides_menu(),
            "interactive_text": "Оберіть розділ Гайдів.",
            "state": MenuStates.GUIDES_MENU
        },
        MenuButton.VOTING.value: {
            "text": MenuButton.VOTING.value,
            "keyboard": get_voting_menu(),
            "interactive_text": "Оберіть розділ Голосування.",
            "state": MenuStates.VOTING_MENU
        },
        MenuButton.M6.value: {
            "text": MenuButton.M6.value,
            "keyboard": get_m6_menu(),
            "interactive_text": "Оберіть розділ M6.",
            "state": MenuStates.M6_MENU
        },
        MenuButton.GPT.value: {
            "text": MenuButton.GPT.value,
            "keyboard": get_gpt_menu(),
            "interactive_text": "Оберіть розділ GPT.",
            "state": MenuStates.GPT_MENU
        },
        MenuButton.META.value: {
            "text": MenuButton.META.value,
            "keyboard": get_meta_menu(),
            "interactive_text": "Оберіть розділ META.",
            "state": MenuStates.META_MENU
        },
        MenuButton.TOURNAMENTS.value: {
            "text": MenuButton.TOURNAMENTS.value,
            "keyboard": get_tournaments_menu(),
            "interactive_text": "Оберіть розділ Турнірів.",
            "state": MenuStates.TOURNAMENTS_MENU
        },
        MenuButton.BACK_NAVIGATION.value: {
            "text": MenuButton.BACK_NAVIGATION.value,
            "keyboard": get_main_menu(),
            "interactive_text": "Повернення до Головного Меню.",
            "state": MenuStates.MAIN_MENU
        }
    }.get(user_choice)

    if transition:
        await update_menu(
            message=message,
            state=state,
            bot=bot,
            new_main_text=transition["text"],
            new_main_keyboard=transition["keyboard"],
            new_interactive_text=transition["interactive_text"],
            new_state=transition["state"]
        )
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.NAVIGATION_MENU

        await update_menu(
            message=message,
            state=state,
            bot=bot,
            new_main_text=new_main_text,
            new_main_keyboard=new_main_keyboard,
            new_interactive_text=new_interactive_text,
            new_state=new_state
        )

@router.message(MenuStates.HEROES_MENU)
async def handle_heroes_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Персонажі")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Перевіряємо, чи обрана кнопка належить до класів героїв
    hero_class = menu_button_to_class.get(user_choice)

    if hero_class:
        # Зберігаємо вибраний клас героя в стані
        await state.update_data(hero_class=hero_class)
        # Створюємо меню для обраного класу героя
        hero_class_menu = get_hero_class_menu(hero_class)
        await message.answer(
            f"Оберіть героя класу **{hero_class}**:",
            reply_markup=hero_class_menu
        )
        await state.set_state(MenuStates.HERO_CLASS_MENU)
    elif user_choice == MenuButton.COMPARISON.value:
        # Обробка порівняння героїв (функціонал ще не реалізований)
        await message.answer(
            "Порівняння героїв ще в розробці.",
            reply_markup=get_heroes_menu()
        )
        await state.set_state(MenuStates.HEROES_MENU)
    elif user_choice == MenuButton.SEARCH_HERO.value:
        # Повернення до пошуку героя
        await message.answer(
            "Введіть ім'я героя для пошуку:",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(MenuStates.SEARCH_HERO)
    elif user_choice == MenuButton.BACK_HEROES.value:
        # Повернення до меню Навігації
        await message.answer(
            "Повернення до меню Навігації.",
            reply_markup=get_navigation_menu()
        )
        await state.set_state(MenuStates.NAVIGATION_MENU)
    else:
        # Невідома команда
        await message.answer(
            UNKNOWN_COMMAND_TEXT,
            reply_markup=get_heroes_menu()
        )
        await state.set_state(MenuStates.HEROES_MENU)

@router.message(MenuStates.HERO_CLASS_MENU)
async def handle_hero_class_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    hero_name = message.text
    hero_class = (await state.get_data()).get('hero_class')

    if hero_class and hero_name in heroes_by_class.get(hero_class, []):
        # Обробка вибору героя (функціонал залежить від вашої реалізації)
        await message.answer(
            f"Ви обрали героя **{hero_name}** класу **{hero_class}**.",
            reply_markup=get_generic_inline_keyboard()  # Потрібно визначити функцію для інлайн-кнопок
        )
        # Повернення до меню Персонажів
        await message.answer(
            "Повернення до меню Персонажів.",
            reply_markup=get_heroes_menu()
        )
        await state.set_state(MenuStates.HEROES_MENU)
    else:
        # Герой не знайдений або невірний клас
        await message.answer(
            f"Герой **{hero_name}** не знайдений в класі **{hero_class}**. Будь ласка, спробуйте ще раз.",
            reply_markup=get_hero_class_menu(hero_class)
        )
        await state.set_state(MenuStates.HERO_CLASS_MENU)

@router.message(MenuStates.GUIDES_MENU)
async def handle_guides_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Гайди")

    # Видаляємо повідомлення користувача
    await message.delete()

    transition = {
        MenuButton.NEW_GUIDES.value: {
            "text": MenuButton.NEW_GUIDES.value,
            "keyboard": get_guides_menu(),
            "interactive_text": "Оберіть нові гайди.",
            "state": MenuStates.GUIDES_MENU
        },
        MenuButton.POPULAR_GUIDES.value: {
            "text": MenuButton.POPULAR_GUIDES.value,
            "keyboard": get_guides_menu(),
            "interactive_text": "Оберіть топ гайди.",
            "state": MenuStates.GUIDES_MENU
        },
        MenuButton.BEGINNER_GUIDES.value: {
            "text": MenuButton.BEGINNER_GUIDES.value,
            "keyboard": get_guides_menu(),
            "interactive_text": "Оберіть гайди для початківців.",
            "state": MenuStates.GUIDES_MENU
        },
        MenuButton.ADVANCED_TECHNIQUES.value: {
            "text": MenuButton.ADVANCED_TECHNIQUES.value,
            "keyboard": get_guides_menu(),
            "interactive_text": "Оберіть стратегії гри.",
            "state": MenuStates.GUIDES_MENU
        },
        MenuButton.TEAMPLAY_GUIDES.value: {
            "text": MenuButton.TEAMPLAY_GUIDES.value,
            "keyboard": get_guides_menu(),
            "interactive_text": "Оберіть гайди для командної гри.",
            "state": MenuStates.GUIDES_MENU
        },
        MenuButton.BACK_GUIDES.value: {
            "text": MenuButton.BACK_GUIDES.value,
            "keyboard": get_navigation_menu(),
            "interactive_text": "Повернення до меню Навігації.",
            "state": MenuStates.NAVIGATION_MENU
        }
    }.get(user_choice)

    if transition:
        await update_menu(
            message=message,
            state=state,
            bot=bot,
            new_main_text=transition["text"],
            new_main_keyboard=transition["keyboard"],
            new_interactive_text=transition["interactive_text"],
            new_state=transition["state"]
        )
    else:
        await message.answer(
            UNKNOWN_COMMAND_TEXT,
            reply_markup=get_guides_menu()
        )
        await state.set_state(MenuStates.GUIDES_MENU)

@router.message(MenuStates.COUNTER_PICKS_MENU)
async def handle_counter_picks_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Контр-піки")

    # Видаляємо повідомлення користувача
    await message.delete()

    transition = {
        MenuButton.COUNTER_SEARCH.value: {
            "text": MenuButton.COUNTER_SEARCH.value,
            "keyboard": ReplyKeyboardRemove(),
            "interactive_text": "Введіть ім'я героя для пошуку контр-піку:",
            "state": MenuStates.SEARCH_HERO
        },
        MenuButton.COUNTER_LIST.value: {
            "text": MenuButton.COUNTER_LIST.value,
            "keyboard": get_counter_picks_menu(),
            "interactive_text": "Список контр-піків доступний.",
            "state": MenuStates.COUNTER_PICKS_MENU
        },
        MenuButton.BACK_COUNTER_PICKS.value: {
            "text": MenuButton.BACK_COUNTER_PICKS.value,
            "keyboard": get_navigation_menu(),
            "interactive_text": "Повернення до меню Навігації.",
            "state": MenuStates.NAVIGATION_MENU
        }
    }.get(user_choice)

    if transition:
        if user_choice == MenuButton.COUNTER_SEARCH.value:
            await message.answer(
                transition["interactive_text"],
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            await message.answer(
                transition["interactive_text"],
                reply_markup=transition["keyboard"]
            )
        await state.set_state(transition["state"])
    else:
        await message.answer(
            UNKNOWN_COMMAND_TEXT,
            reply_markup=get_counter_picks_menu()
        )
        await state.set_state(MenuStates.COUNTER_PICKS_MENU)

@router.message(MenuStates.BUILDS_MENU)
async def handle_builds_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Білди")

    # Видаляємо повідомлення користувача
    await message.delete()

    transition = {
        MenuButton.CREATE_BUILD.value: {
            "text": MenuButton.CREATE_BUILD.value,
            "keyboard": get_builds_menu(),
            "interactive_text": "Оберіть опцію створення білду.",
            "state": MenuStates.BUILDS_MENU
        },
        MenuButton.MY_BUILDS.value: {
            "text": MenuButton.MY_BUILDS.value,
            "keyboard": get_builds_menu(),
            "interactive_text": "Ваші обрані білди.",
            "state": MenuStates.BUILDS_MENU
        },
        MenuButton.POPULAR_BUILDS.value: {
            "text": MenuButton.POPULAR_BUILDS.value,
            "keyboard": get_builds_menu(),
            "interactive_text": "Популярні білди доступні.",
            "state": MenuStates.BUILDS_MENU
        },
        MenuButton.BACK_BUILDS.value: {
            "text": MenuButton.BACK_BUILDS.value,
            "keyboard": get_navigation_menu(),
            "interactive_text": "Повернення до меню Навігації.",
            "state": MenuStates.NAVIGATION_MENU
        }
    }.get(user_choice)

    if transition:
        await update_menu(
            message=message,
            state=state,
            bot=bot,
            new_main_text=transition["text"],
            new_main_keyboard=transition["keyboard"],
            new_interactive_text=transition["interactive_text"],
            new_state=transition["state"]
        )
    else:
        await message.answer(
            UNKNOWN_COMMAND_TEXT,
            reply_markup=get_builds_menu()
        )
        await state.set_state(MenuStates.BUILDS_MENU)

@router.message(MenuStates.VOTING_MENU)
async def handle_voting_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Голосування")

    # Видаляємо повідомлення користувача
    await message.delete()

    transition = {
        MenuButton.CURRENT_VOTES.value: {
            "text": MenuButton.CURRENT_VOTES.value,
            "keyboard": get_voting_menu(),
            "interactive_text": "Оберіть поточні опитування.",
            "state": MenuStates.VOTING_MENU
        },
        MenuButton.MY_VOTES.value: {
            "text": MenuButton.MY_VOTES.value,
            "keyboard": get_voting_menu(),
            "interactive_text": "Ваші голосування.",
            "state": MenuStates.VOTING_MENU
        },
        MenuButton.SUGGEST_TOPIC.value: {
            "text": MenuButton.SUGGEST_TOPIC.value,
            "keyboard": ReplyKeyboardRemove(),
            "interactive_text": "Введіть тему для пропозиції:",
            "state": MenuStates.SUGGEST_TOPIC
        },
        MenuButton.BACK_VOTING.value: {
            "text": MenuButton.BACK_VOTING.value,
            "keyboard": get_navigation_menu(),
            "interactive_text": "Повернення до меню Навігації.",
            "state": MenuStates.NAVIGATION_MENU
        }
    }.get(user_choice)

    if transition:
        if user_choice == MenuButton.SUGGEST_TOPIC.value:
            await message.answer(
                transition["interactive_text"],
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            await message.answer(
                transition["interactive_text"],
                reply_markup=transition["keyboard"]
            )
        await state.set_state(transition["state"])
    else:
        await message.answer(
            UNKNOWN_COMMAND_TEXT,
            reply_markup=get_voting_menu()
        )
        await state.set_state(MenuStates.VOTING_MENU)

@router.message(MenuStates.PROFILE_MENU)
async def handle_profile_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Профіль")

    # Видаляємо повідомлення користувача
    await message.delete()

    transition = {
        MenuButton.STATISTICS.value: {
            "text": MenuButton.STATISTICS.value,
            "keyboard": get_statistics_menu(),
            "interactive_text": "Оберіть розділ статистики.",
            "state": MenuStates.STATISTICS_MENU
        },
        MenuButton.ACHIEVEMENTS.value: {
            "text": MenuButton.ACHIEVEMENTS.value,
            "keyboard": get_achievements_menu(),
            "interactive_text": "Оберіть розділ досягнень.",
            "state": MenuStates.ACHIEVEMENTS_MENU
        },
        MenuButton.SETTINGS.value: {
            "text": MenuButton.SETTINGS.value,
            "keyboard": get_settings_menu(),
            "interactive_text": "Оберіть розділ налаштувань.",
            "state": MenuStates.SETTINGS_MENU
        },
        MenuButton.FEEDBACK.value: {
            "text": MenuButton.FEEDBACK.value,
            "keyboard": get_feedback_menu(),
            "interactive_text": "Оберіть опцію зворотного зв'язку.",
            "state": MenuStates.FEEDBACK_MENU
        },
        MenuButton.HELP.value: {
            "text": MenuButton.HELP.value,
            "keyboard": get_help_menu(),
            "interactive_text": "Оберіть розділ допомоги.",
            "state": MenuStates.HELP_MENU
        },
        MenuButton.BACK_TO_MAIN_MENU.value: {
            "text": MenuButton.BACK_TO_MAIN_MENU.value,
            "keyboard": get_main_menu(),
            "interactive_text": "Повернення до головного меню.",
            "state": MenuStates.MAIN_MENU
        }
    }.get(user_choice)

    if transition:
        await update_menu(
            message=message,
            state=state,
            bot=bot,
            new_main_text=transition["text"],
            new_main_keyboard=transition["keyboard"],
            new_interactive_text=transition["interactive_text"],
            new_state=transition["state"]
        )
    else:
        await message.answer(
            UNKNOWN_COMMAND_TEXT,
            reply_markup=get_profile_menu_buttons()
        )
        await state.set_state(MenuStates.PROFILE_MENU)

@router.message(MenuStates.STATISTICS_MENU)
async def handle_statistics_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Статистика")

    # Видаляємо повідомлення користувача
    await message.delete()

    transition = {
        MenuButton.ACTIVITY.value: {
            "text": MenuButton.ACTIVITY.value,
            "keyboard": get_statistics_menu(),
            "interactive_text": "Оберіть опцію загальної активності.",
            "state": MenuStates.STATISTICS_MENU
        },
        MenuButton.RANKING.value: {
            "text": MenuButton.RANKING.value,
            "keyboard": get_statistics_menu(),
            "interactive_text": "Оберіть опцію рейтингу.",
            "state": MenuStates.STATISTICS_MENU
        },
        MenuButton.GAME_STATS.value: {
            "text": MenuButton.GAME_STATS.value,
            "keyboard": get_statistics_menu(),
            "interactive_text": "Оберіть ігрову статистику.",
            "state": MenuStates.STATISTICS_MENU
        },
        MenuButton.BACK_TO_PROFILE.value: {
            "text": MenuButton.BACK_TO_PROFILE.value,
            "keyboard": get_profile_menu_buttons(),
            "interactive_text": "Повернення до меню Профілю.",
            "state": MenuStates.PROFILE_MENU
        }
    }.get(user_choice)

    if transition:
        await update_menu(
            message=message,
            state=state,
            bot=bot,
            new_main_text=transition["text"],
            new_main_keyboard=transition["keyboard"],
            new_interactive_text=transition["interactive_text"],
            new_state=transition["state"]
        )
    else:
        await message.answer(
            UNKNOWN_COMMAND_TEXT,
            reply_markup=get_statistics_menu()
        )
        await state.set_state(MenuStates.STATISTICS_MENU)

@router.message(MenuStates.ACHIEVEMENTS_MENU)
async def handle_achievements_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Досягнення")

    # Видаляємо повідомлення користувача
    await message.delete()

    transition = {
        MenuButton.BADGES.value: {
            "text": MenuButton.BADGES.value,
            "keyboard": get_achievements_menu(),
            "interactive_text": "Ваші бейджі.",
            "state": MenuStates.ACHIEVEMENTS_MENU
        },
        MenuButton.PROGRESS.value: {
            "text": MenuButton.PROGRESS.value,
            "keyboard": get_achievements_menu(),
            "interactive_text": "Ваш прогрес.",
            "state": MenuStates.ACHIEVEMENTS_MENU
        },
        MenuButton.TOURNAMENT_STATS.value: {
            "text": MenuButton.TOURNAMENT_STATS.value,
            "keyboard": get_achievements_menu(),
            "interactive_text": "Турнірна статистика.",
            "state": MenuStates.ACHIEVEMENTS_MENU
        },
        MenuButton.AWARDS.value: {
            "text": MenuButton.AWARDS.value,
            "keyboard": get_achievements_menu(),
            "interactive_text": "Ваші нагороди.",
            "state": MenuStates.ACHIEVEMENTS_MENU
        },
        MenuButton.BACK_ACHIEVEMENTS.value: {
            "text": MenuButton.BACK_ACHIEVEMENTS.value,
            "keyboard": get_profile_menu_buttons(),
            "interactive_text": "Повернення до меню Профілю.",
            "state": MenuStates.PROFILE_MENU
        }
    }.get(user_choice)

    if transition:
        await update_menu(
            message=message,
            state=state,
            bot=bot,
            new_main_text=transition["text"],
            new_main_keyboard=transition["keyboard"],
            new_interactive_text=transition["interactive_text"],
            new_state=transition["state"]
        )
    else:
        await message.answer(
            UNKNOWN_COMMAND_TEXT,
            reply_markup=get_achievements_menu()
        )
        await state.set_state(MenuStates.ACHIEVEMENTS_MENU)

@router.message(MenuStates.SETTINGS_MENU)
async def handle_settings_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Налаштування")

    # Видаляємо повідомлення користувача
    await message.delete()

    transition = {
        MenuButton.LANGUAGE.value: {
            "text": MenuButton.LANGUAGE.value,
            "keyboard": get_settings_menu(),
            "interactive_text": "Оберіть мову інтерфейсу.",
            "state": MenuStates.SETTINGS_MENU
        },
        MenuButton.CHANGE_USERNAME.value: {
            "text": MenuButton.CHANGE_USERNAME.value,
            "keyboard": ReplyKeyboardRemove(),
            "interactive_text": "Введіть новий Username:",
            "state": MenuStates.CHANGE_USERNAME
        },
        MenuButton.UPDATE_ID.value: {
            "text": MenuButton.UPDATE_ID.value,
            "keyboard": ReplyKeyboardRemove(),
            "interactive_text": "Введіть новий ID:",
            "state": MenuStates.SETTINGS_MENU  # Можливо, створити окремий стан
        },
        MenuButton.NOTIFICATIONS.value: {
            "text": MenuButton.NOTIFICATIONS.value,
            "keyboard": get_settings_menu(),
            "interactive_text": "Оберіть налаштування сповіщень.",
            "state": MenuStates.SETTINGS_MENU
        },
        MenuButton.BACK_SETTINGS.value: {
            "text": MenuButton.BACK_SETTINGS.value,
            "keyboard": get_profile_menu_buttons(),
            "interactive_text": "Повернення до меню Профілю.",
            "state": MenuStates.PROFILE_MENU
        }
    }.get(user_choice)

    if transition:
        if user_choice in [MenuButton.CHANGE_USERNAME.value, MenuButton.UPDATE_ID.value]:
            # Для змін username та ID, видаляємо клавіатуру
            await message.answer(
                transition["interactive_text"],
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            await message.answer(
                transition["interactive_text"],
                reply_markup=transition["keyboard"]
            )
        await state.set_state(transition["state"])
    else:
        await message.answer(
            UNKNOWN_COMMAND_TEXT,
            reply_markup=get_settings_menu()
        )
        await state.set_state(MenuStates.SETTINGS_MENU)

@router.message(MenuStates.FEEDBACK_MENU)
async def handle_feedback_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Зворотний Зв'язок")

    # Видаляємо повідомлення користувача
    await message.delete()

    transition = {
        MenuButton.SEND_FEEDBACK.value: {
            "text": MenuButton.SEND_FEEDBACK.value,
            "keyboard": ReplyKeyboardRemove(),
            "interactive_text": "Введіть свій відгук:",
            "state": MenuStates.RECEIVE_FEEDBACK
        },
        MenuButton.REPORT_BUG.value: {
            "text": MenuButton.REPORT_BUG.value,
            "keyboard": ReplyKeyboardRemove(),
            "interactive_text": "Опишіть знайдену помилку:",
            "state": MenuStates.REPORT_BUG
        },
        MenuButton.BACK_FEEDBACK.value: {
            "text": MenuButton.BACK_FEEDBACK.value,
            "keyboard": get_profile_menu_buttons(),
            "interactive_text": "Повернення до меню Профілю.",
            "state": MenuStates.PROFILE_MENU
        }
    }.get(user_choice)

    if transition:
        await message.answer(
            transition["interactive_text"],
            reply_markup=transition["keyboard"]
        )
        await state.set_state(transition["state"])
    else:
        await message.answer(
            UNKNOWN_COMMAND_TEXT,
            reply_markup=get_feedback_menu()
        )
        await state.set_state(MenuStates.FEEDBACK_MENU)

@router.message(MenuStates.HELP_MENU)
async def handle_help_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Допомога")

    # Видаляємо повідомлення користувача
    await message.delete()

    transition = {
        MenuButton.INSTRUCTIONS.value: {
            "text": MenuButton.INSTRUCTIONS.value,
            "keyboard": get_help_menu(),
            "interactive_text": "Оберіть розділ Інструкцій.",
            "state": MenuStates.HELP_MENU
        },
        MenuButton.FAQ.value: {
            "text": MenuButton.FAQ.value,
            "keyboard": get_help_menu(),
            "interactive_text": "Оберіть розділ FAQ.",
            "state": MenuStates.HELP_MENU
        },
        MenuButton.HELP_SUPPORT.value: {
            "text": MenuButton.HELP_SUPPORT.value,
            "keyboard": get_help_menu(),
            "interactive_text": "Оберіть розділ Підтримки.",
            "state": MenuStates.HELP_MENU
        },
        MenuButton.BACK_HELP.value: {
            "text": MenuButton.BACK_HELP.value,
            "keyboard": get_profile_menu_buttons(),
            "interactive_text": "Повернення до меню Профілю.",
            "state": MenuStates.PROFILE_MENU
        }
    }.get(user_choice)

    if transition:
        await message.answer(
            transition["interactive_text"],
            reply_markup=transition["keyboard"]
        )
        await state.set_state(transition["state"])
    else:
        await message.answer(
            UNKNOWN_COMMAND_TEXT,
            reply_markup=get_help_menu()
        )
        await state.set_state(MenuStates.HELP_MENU)

@router.message(MenuStates.SEARCH_HERO)
async def handle_search_hero(message: Message, state: FSMContext, bot: Bot):
    hero_name = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} шукає героя: {hero_name}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Перевірка чи існує герой
    # Припускаємо, що heroes_by_class це словник з списками героїв
    all_heroes = [hero for heroes in heroes_by_class.values() for hero in heroes]
    if hero_name in all_heroes:
        response_text = SEARCH_HERO_RESPONSE_TEXT.format(hero_name=hero_name)
        # Тут можна додати логіку отримання інформації про героя
    else:
        response_text = f"Герой '{hero_name}' не знайдений. Будь ласка, спробуйте ще раз."

    await bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard()  # Потрібно визначити функцію для інлайн-кнопок
    )

    # Повертаємо користувача до меню Персонажів
    await message.answer(
        "Повернення до меню Персонажів.",
        reply_markup=get_heroes_menu()
    )
    await state.set_state(MenuStates.HEROES_MENU)

@router.message(MenuStates.SUGGEST_TOPIC)
async def handle_suggest_topic(message: Message, state: FSMContext, bot: Bot):
    topic = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} пропонує тему: {topic}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Тут можна додати логіку обробки пропозиції теми
    # Наприклад, збереження в базі даних або відправка адміністратору
    # Поки що відправимо повідомлення про отримання запиту

    if topic:
        response_text = SUGGESTION_RESPONSE_TEXT.format(topic=topic)
        # Тут можна додати логіку збереження пропозиції
    else:
        response_text = "Будь ласка, введіть тему для пропозиції."

    await bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard()  # Потрібно визначити функцію для інлайн-кнопок
    )

    # Повертаємо користувача до меню Голосування
    await message.answer(
        "Повернення до меню Голосування.",
        reply_markup=get_voting_menu()
    )
    await state.set_state(MenuStates.VOTING_MENU)

@router.message(MenuStates.CHANGE_USERNAME)
async def handle_change_username(message: Message, state: FSMContext, bot: Bot):
    new_username = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} змінює Username на: {new_username}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Тут можна додати логіку зміни Username
    # Наприклад, перевірка унікальності, оновлення в базі даних тощо
    # Поки що відправимо повідомлення про отримання запиту

    if new_username:
        response_text = CHANGE_USERNAME_RESPONSE_TEXT.format(new_username=new_username)
        # Тут можна додати логіку оновлення Username
    else:
        response_text = "Будь ласка, введіть новий Username."

    await bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard()  # Потрібно визначити функцію для інлайн-кнопок
    )

    # Повертаємо користувача до меню Налаштувань
    await message.answer(
        "Повернення до меню Налаштувань.",
        reply_markup=get_settings_menu()
    )
    await state.set_state(MenuStates.SETTINGS_MENU)

@router.message(MenuStates.RECEIVE_FEEDBACK)
async def handle_receive_feedback(message: Message, state: FSMContext, bot: Bot):
    feedback = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} надіслав відгук: {feedback}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Тут можна додати логіку зберігання відгуку
    # Наприклад, збереження в базі даних або відправка адміністратору
    # Поки що відправимо повідомлення про отримання відгуку

    if feedback:
        response_text = FEEDBACK_RECEIVED_TEXT
        # Тут можна додати логіку збереження відгуку
    else:
        response_text = "Будь ласка, залиште свій відгук."

    await bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard()  # Потрібно визначити функцію для інлайн-кнопок
    )

    # Повертаємо користувача до меню Зворотного Зв'язку
    await message.answer(
        "Повернення до меню Зворотного Зв'язку.",
        reply_markup=get_feedback_menu()
    )
    await state.set_state(MenuStates.FEEDBACK_MENU)

@router.message(MenuStates.REPORT_BUG)
async def handle_report_bug(message: Message, state: FSMContext, bot: Bot):
    bug_report = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} повідомив про помилку: {bug_report}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Тут можна додати логіку обробки звіту про помилку
    # Наприклад, збереження в базі даних або відправка адміністратору
    # Поки що відправимо повідомлення про отримання звіту

    if bug_report:
        response_text = BUG_REPORT_RECEIVED_TEXT
        # Тут можна додати логіку збереження звіту про помилку
    else:
        response_text = "Будь ласка, опишіть помилку, яку ви знайшли."

    await bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard()  # Потрібно визначити функцію для інлайн-кнопок
    )

    # Повертаємо користувача до меню Зворотного Зв'язку
    await message.answer(
        "Повернення до меню Зворотного Зв'язку.",
        reply_markup=get_feedback_menu()
    )
    await state.set_state(MenuStates.FEEDBACK_MENU)

@router.message(MenuStates.M6_MENU)
async def handle_m6_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню M6")

    # Видаляємо повідомлення користувача
    await message.delete()

    transition = {
        MenuButton.M6_TOURNAMENT_INFO.value: {
            "text": MenuButton.M6_TOURNAMENT_INFO.value,
            "keyboard": get_m6_menu(),
            "interactive_text": "Інформація про турніри, правила, учасники.",
            "state": MenuStates.M6_MENU
        },
        MenuButton.M6_STATISTICS.value: {
            "text": MenuButton.M6_STATISTICS.value,
            "keyboard": get_m6_menu(),
            "interactive_text": "Статистичні дані по турнірам, учасниках, перемогах.",
            "state": MenuStates.M6_MENU
        },
        MenuButton.M6_NEWS.value: {
            "text": MenuButton.M6_NEWS.value,
            "keyboard": get_m6_menu(),
            "interactive_text": "Останні новини та оновлення щодо M6.",
            "state": MenuStates.M6_MENU
        },
        MenuButton.BACK_M6.value: {
            "text": MenuButton.BACK_M6.value,
            "keyboard": get_navigation_menu(),
            "interactive_text": "Повернення до меню Навігації.",
            "state": MenuStates.NAVIGATION_MENU
        }
    }.get(user_choice)

    if transition:
        await update_menu(
            message=message,
            state=state,
            bot=bot,
            new_main_text=transition["text"],
            new_main_keyboard=transition["keyboard"],
            new_interactive_text=transition["interactive_text"],
            new_state=transition["state"]
        )
    else:
        await message.answer(
            UNKNOWN_COMMAND_TEXT,
            reply_markup=get_m6_menu()
        )
        await state.set_state(MenuStates.M6_MENU)

@router.message(MenuStates.GPT_MENU)
async def handle_gpt_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню GPT")

    # Видаляємо повідомлення користувача
    await message.delete()

    transition = {
        MenuButton.GPT_DATA_GENERATION.value: {
            "text": MenuButton.GPT_DATA_GENERATION.value,
            "keyboard": get_gpt_menu(),
            "interactive_text": "Використання GPT для генерації контенту, стратегій тощо.",
            "state": MenuStates.GPT_MENU
        },
        MenuButton.GPT_HINTS.value: {
            "text": MenuButton.GPT_HINTS.value,
            "keyboard": get_gpt_menu(),
            "interactive_text": "Отримання порад та рекомендацій від GPT.",
            "state": MenuStates.GPT_MENU
        },
        MenuButton.GPT_HERO_STATISTICS.value: {
            "text": MenuButton.GPT_HERO_STATISTICS.value,
            "keyboard": get_gpt_menu(),
            "interactive_text": "Аналіз та статистика героїв за допомогою GPT.",
            "state": MenuStates.GPT_MENU
        },
        MenuButton.BACK_GPT.value: {
            "text": MenuButton.BACK_GPT.value,
            "keyboard": get_navigation_menu(),
            "interactive_text": "Повернення до меню Навігації.",
            "state": MenuStates.NAVIGATION_MENU
        }
    }.get(user_choice)

    if transition:
        await update_menu(
            message=message,
            state=state,
            bot=bot,
            new_main_text=transition["text"],
            new_main_keyboard=transition["keyboard"],
            new_interactive_text=transition["interactive_text"],
            new_state=transition["state"]
        )
    else:
        await message.answer(
            UNKNOWN_COMMAND_TEXT,
            reply_markup=get_gpt_menu()
        )
        await state.set_state(MenuStates.GPT_MENU)

@router.message(MenuStates.META_MENU)
async def handle_meta_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню META")

    # Видаляємо повідомлення користувача
    await message.delete()

    transition = {
        MenuButton.META_HERO_LIST.value: {
            "text": MenuButton.META_HERO_LIST.value,
            "keyboard": get_meta_menu(),
            "interactive_text": "Перелік героїв, актуальних у поточній меті гри.",
            "state": MenuStates.META_MENU
        },
        MenuButton.META_RECOMMENDATIONS.value: {
            "text": MenuButton.META_RECOMMENDATIONS.value,
            "keyboard": get_meta_menu(),
            "interactive_text": "Рекомендовані герої для гри у поточній меті.",
            "state": MenuStates.META_MENU
        },
        MenuButton.META_UPDATE.value: {
            "text": MenuButton.META_UPDATE.value,
            "keyboard": get_meta_menu(),
            "interactive_text": "Інформація про останні зміни та оновлення у меті.",
            "state": MenuStates.META_MENU
        },
        MenuButton.BACK_META.value: {
            "text": MenuButton.BACK_META.value,
            "keyboard": get_navigation_menu(),
            "interactive_text": "Повернення до меню Навігації.",
            "state": MenuStates.NAVIGATION_MENU
        }
    }.get(user_choice)

    if transition:
        await update_menu(
            message=message,
            state=state,
            bot=bot,
            new_main_text=transition["text"],
            new_main_keyboard=transition["keyboard"],
            new_interactive_text=transition["interactive_text"],
            new_state=transition["state"]
        )
    else:
        await message.answer(
            UNKNOWN_COMMAND_TEXT,
            reply_markup=get_meta_menu()
        )
        await state.set_state(MenuStates.META_MENU)

@router.message(MenuStates.TOURNAMENTS_MENU)
async def handle_tournaments_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Турніри")

    # Видаляємо повідомлення користувача
    await message.delete()

    transition = {
        MenuButton.CREATE_TOURNAMENT.value: {
            "text": MenuButton.CREATE_TOURNAMENT.value,
            "keyboard": ReplyKeyboardRemove(),
            "interactive_text": "Процес Створення Турніру:\n\n1. Виберіть Тип Турніру:\n   - 5х5\n   - 2х2\n   - 1 на 1\n\n2. Введіть Деталі Турніру:\n   - Назва: Введіть назву турніру.\n   - Опис: Короткий опис турніру.\n   - Дата та Час: Вкажіть дату та час проведення.\n   - Умови Участі: Вкажіть вимоги для учасників.\n\n3. Надішліть Запит на Підтвердження адміністратору.",
            "state": MenuStates.CREATE_TOURNAMENT
        },
        MenuButton.VIEW_TOURNAMENTS.value: {
            "text": MenuButton.VIEW_TOURNAMENTS.value,
            "keyboard": ReplyKeyboardRemove(),
            "interactive_text": "Огляд Доступних Турнірів:\n\n1. Список Активних Турнірів:\n   - Назва Турніру\n   - Тип Турніру\n   - Дата та Час\n   - Статус: Активний / Завершений\n   - Кнопка: Детальніше\n\n2. Детальніше про Турнір:\n   - Інформація про турнір.\n   - Список учасників.\n   - Опції для реєстрації (якщо реєстрація відкрита).\n\n3. 📋 Зареєструватися:\n   - Процес реєстрації на турнір.",
            "state": MenuStates.VIEW_TOURNAMENTS
        },
        MenuButton.BACK_TOURNAMENTS.value: {
            "text": MenuButton.BACK_TOURNAMENTS.value,
            "keyboard": get_navigation_menu(),
            "interactive_text": "Повернення до меню Навігації.",
            "state": MenuStates.NAVIGATION_MENU
        }
    }.get(user_choice)

    if transition:
        if user_choice in [MenuButton.CREATE_TOURNAMENT.value, MenuButton.VIEW_TOURNAMENTS.value]:
            await message.answer(
                transition["interactive_text"],
                reply_markup=ReplyKeyboardRemove()
            )
        else:
            await message.answer(
                transition["interactive_text"],
                reply_markup=transition["keyboard"]
            )
        await state.set_state(transition["state"])
    else:
        await message.answer(
            UNKNOWN_COMMAND_TEXT,
            reply_markup=get_tournaments_menu()
        )
        await state.set_state(MenuStates.TOURNAMENTS_MENU)

# Обробник для невідомих повідомлень
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
        hero_class = data.get('hero_class', 'Танк')
        new_main_text = UNKNOWN_COMMAND_TEXT
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
        new_main_keyboard = get_profile_menu_buttons()
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
    elif current_state == MenuStates.FEEDBACK_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_feedback_menu()
        new_interactive_text = "Меню Зворотного Зв'язку"
        new_state = MenuStates.FEEDBACK_MENU
    elif current_state == MenuStates.HELP_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_help_menu()
        new_interactive_text = "Меню Допомоги"
        new_state = MenuStates.HELP_MENU
    elif current_state == MenuStates.M6_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_m6_menu()
        new_interactive_text = "Меню M6"
        new_state = MenuStates.M6_MENU
    elif current_state == MenuStates.GPT_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_gpt_menu()
        new_interactive_text = "Меню GPT"
        new_state = MenuStates.GPT_MENU
    elif current_state == MenuStates.META_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_meta_menu()
        new_interactive_text = "Меню META"
        new_state = MenuStates.META_MENU
    elif current_state == MenuStates.TOURNAMENTS_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_tournaments_menu()
        new_interactive_text = "Меню Турнірів"
        new_state = MenuStates.TOURNAMENTS_MENU
    elif current_state in [
        MenuStates.SEARCH_HERO.state,
        MenuStates.SUGGEST_TOPIC.state,
        MenuStates.CHANGE_USERNAME.state,
        MenuStates.RECEIVE_FEEDBACK.state,
        MenuStates.REPORT_BUG.state
    ]:
        # Якщо користувач перебуває в процесі введення, надсилаємо підказку
        await bot.send_message(
            chat_id=message.chat.id,
            text=USE_BUTTON_NAVIGATION_TEXT,
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(current_state)
        return
    else:
        # Якщо стан невідомий, повертаємо до головного меню
        user_first_name = message.from_user.first_name
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU

    # Відправляємо нове основне повідомлення
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    # Видаляємо старе повідомлення бота
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
                reply_markup=ReplyKeyboardRemove()
            )
        except Exception as e:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            interactive_message = await bot.send_message(
                chat_id=message.chat.id,
                text=new_interactive_text,
                reply_markup=ReplyKeyboardRemove()
            )
            await state.update_data(interactive_message_id=interactive_message.message_id)
    else:
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=ReplyKeyboardRemove()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    # Встановлення нового стану
    await state.set_state(new_state)

# Обробники для специфічних станів

@router.message(MenuStates.CREATE_TOURNAMENT)
async def handle_create_tournament(message: Message, state: FSMContext, bot: Bot):
    # Тут реалізуйте логіку створення турніру
    tournament_details = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} створює турнір з деталями: {tournament_details}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Припустимо, що турнір створено успішно
    response_text = "Ваш турнір успішно створено та надіслано на підтвердження адміністратору."

    await bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard()  # Потрібно визначити функцію для інлайн-кнопок
    )

    # Повертаємо користувача до меню Турнірів
    await message.answer(
        "Повернення до меню Турнірів.",
        reply_markup=get_tournaments_menu()
    )
    await state.set_state(MenuStates.TOURNAMENTS_MENU)

@router.message(MenuStates.VIEW_TOURNAMENTS)
async def handle_view_tournaments(message: Message, state: FSMContext, bot: Bot):
    # Тут реалізуйте логіку перегляду турнірів
    logger.info(f"Користувач {message.from_user.id} переглядає турніри")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Припустимо, що перелік турнірів відображено
    response_text = "Список доступних турнірів:\n\n1. Турнір А\n2. Турнір Б\n3. Турнір В\n\nОберіть турнір для детальнішої інформації."

    await bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        reply_markup=get_generic_inline_keyboard()  # Потрібно визначити функцію для інлайн-кнопок
    )

    # Повертаємо користувача до меню Турнірів
    await message.answer(
        "Повернення до меню Турнірів.",
        reply_markup=get_tournaments_menu()
    )
    await state.set_state(MenuStates.TOURNAMENTS_MENU)

# Інлайн-кнопки
def get_generic_inline_keyboard() -> ReplyKeyboardMarkup:
    # Приклад інлайн-клавіатури. Ви можете змінити її відповідно до ваших потреб.
    from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Оновити", callback_data="refresh")]
    ])
    return keyboard

@router.callback_query(lambda c: c.data == "refresh")
async def handle_refresh(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # Приклад обробки інлайн-кнопки "🔄 Оновити"
    await bot.answer_callback_query(callback.id, text="Оновлено!")
    # Можна додати логіку оновлення даних

# Обробники для інших меню (M6, GPT, META, Турніри) можна реалізувати аналогічно

# Функція для налаштування обробників
def setup_handlers(dp):
    dp.include_router(router)