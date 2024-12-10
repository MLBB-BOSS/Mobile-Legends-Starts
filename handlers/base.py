# handlers/base.py

import logging
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

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

router = Router()

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Визначаємо стани меню
class MenuStates(StatesGroup):
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
    UPDATE_ID = State()
    RECEIVE_FEEDBACK = State()
    REPORT_BUG = State()
    M6_MENU = State()
    GPT_MENU = State()
    META_MENU = State()
    TOURNAMENTS_MENU = State()
    CREATE_TOURNAMENT = State()
    VIEW_TOURNAMENTS = State()
    # Додайте додаткові стани, якщо це необхідно

# Визначаємо тексти повідомлень
MAIN_MENU_TEXT = "Вітаємо, {user_first_name}! Оберіть розділ:"
MAIN_MENU_DESCRIPTION = "Це головне меню вашого бота. Оберіть один з доступних розділів."

UNKNOWN_COMMAND_TEXT = "Невідома команда. Будь ласка, оберіть опцію з меню."

USE_BUTTON_NAVIGATION_TEXT = "Будь ласка, використовуйте кнопки меню для навігації."

SEARCH_HERO_RESPONSE_TEXT = "Інформація про героя **{hero_name}** ще в розробці."

SUGGESTION_RESPONSE_TEXT = "Дякуємо за пропозицію теми **{topic}**! Ваша пропозиція була прийнята."

CHANGE_USERNAME_RESPONSE_TEXT = "Ваш Username було змінено на **{new_username}**."

FEEDBACK_RECEIVED_TEXT = "Дякуємо за ваш відгук! Ми обов'язково його розглянемо."

BUG_REPORT_RECEIVED_TEXT = "Дякуємо за повідомлення про помилку! Ми її виправимо найближчим часом."

# Обробник команди /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"Користувач {message.from_user.id} викликав /start")

    # Видаляємо повідомлення користувача /start
    await message.delete()

    # Відправляємо основне меню з клавіатурою
    user_first_name = message.from_user.first_name
    main_menu_text_formatted = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
    main_menu_keyboard = get_main_menu()
    main_menu_message = await bot.send_message(
        chat_id=message.chat.id,
        text=main_menu_text_formatted,
        reply_markup=main_menu_keyboard
    )

    # Зберігаємо ID основного повідомлення
    await state.update_data(main_message_id=main_menu_message.message_id)

    # Встановлюємо стан користувача на MAIN_MENU
    await state.set_state(MenuStates.MAIN_MENU)

# Універсальна функція для оновлення меню
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
    main_message_id = data.get('main_message_id')

    # Видаляємо попереднє основне повідомлення
    if main_message_id:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=main_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Відправляємо нове основне повідомлення
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_main_message_id = main_message.message_id

    # Оновлюємо ID основного повідомлення
    await state.update_data(main_message_id=new_main_message_id)

    # Відправляємо інтерактивне повідомлення
    interactive_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_interactive_text,
        reply_markup=ReplyKeyboardRemove()
    )
    interactive_message_id = interactive_message.message_id

    # Зберігаємо ID інтерактивного повідомлення
    await state.update_data(interactive_message_id=interactive_message_id)

    # Встановлюємо новий стан
    await state.set_state(new_state)

# Обробник для головного меню
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
            "interactive_text": "Оберіть опцію навігації:",
            "state": MenuStates.NAVIGATION_MENU
        },
        MenuButton.PROFILE.value: {
            "text": MenuButton.PROFILE.value,
            "keyboard": get_profile_menu_buttons(),
            "interactive_text": "Оберіть опцію профілю:",
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
        await bot.send_message(
            chat_id=message.chat.id,
            text=UNKNOWN_COMMAND_TEXT,
            reply_markup=get_main_menu()
        )
        await state.set_state(MenuStates.MAIN_MENU)

# Обробник для меню Навігація
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
            "interactive_text": "Оберіть розділ Персонажів:",
            "state": MenuStates.HEROES_MENU
        },
        MenuButton.BUILDS.value: {
            "text": MenuButton.BUILDS.value,
            "keyboard": get_builds_menu(),
            "interactive_text": "Оберіть розділ Білд:",
            "state": MenuStates.BUILDS_MENU
        },
        MenuButton.COUNTER_PICKS.value: {
            "text": MenuButton.COUNTER_PICKS.value,
            "keyboard": get_counter_picks_menu(),
            "interactive_text": "Оберіть розділ Контр-піків:",
            "state": MenuStates.COUNTER_PICKS_MENU
        },
        MenuButton.GUIDES.value: {
            "text": MenuButton.GUIDES.value,
            "keyboard": get_guides_menu(),
            "interactive_text": "Оберіть розділ Гайдів:",
            "state": MenuStates.GUIDES_MENU
        },
        MenuButton.VOTING.value: {
            "text": MenuButton.VOTING.value,
            "keyboard": get_voting_menu(),
            "interactive_text": "Оберіть розділ Голосування:",
            "state": MenuStates.VOTING_MENU
        },
        MenuButton.M6.value: {
            "text": MenuButton.M6.value,
            "keyboard": get_m6_menu(),
            "interactive_text": "Оберіть розділ M6:",
            "state": MenuStates.M6_MENU
        },
        MenuButton.GPT.value: {
            "text": MenuButton.GPT.value,
            "keyboard": get_gpt_menu(),
            "interactive_text": "Оберіть розділ GPT:",
            "state": MenuStates.GPT_MENU
        },
        MenuButton.META.value: {
            "text": MenuButton.META.value,
            "keyboard": get_meta_menu(),
            "interactive_text": "Оберіть розділ META:",
            "state": MenuStates.META_MENU
        },
        MenuButton.TOURNAMENTS.value: {
            "text": MenuButton.TOURNAMENTS.value,
            "keyboard": get_tournaments_menu(),
            "interactive_text": "Оберіть розділ Турнірів:",
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
        await bot.send_message(
            chat_id=message.chat.id,
            text=UNKNOWN_COMMAND_TEXT,
            reply_markup=get_navigation_menu()
        )
        await state.set_state(MenuStates.NAVIGATION_MENU)

# Обробник для меню Персонажі
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
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Оберіть героя класу **{hero_class}**:",
            reply_markup=hero_class_menu,
            parse_mode="Markdown"
        )
        await state.set_state(MenuStates.HERO_CLASS_MENU)
    elif user_choice == MenuButton.COMPARISON.value:
        # Обробка порівняння героїв (функціонал ще не реалізований)
        await bot.send_message(
            chat_id=message.chat.id,
            text="Порівняння героїв ще в розробці.",
            reply_markup=get_heroes_menu()
        )
        await state.set_state(MenuStates.HEROES_MENU)
    elif user_choice == MenuButton.SEARCH_HERO.value:
        # Повернення до пошуку героя
        await bot.send_message(
            chat_id=message.chat.id,
            text="Введіть ім'я героя для пошуку:",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(MenuStates.SEARCH_HERO)
    elif user_choice == MenuButton.BACK_HEROES.value:
        # Повернення до меню Навігації
        await bot.send_message(
            chat_id=message.chat.id,
            text="Повернення до меню Навігації.",
            reply_markup=get_navigation_menu()
        )
        await state.set_state(MenuStates.NAVIGATION_MENU)
    else:
        # Невідома команда
        await bot.send_message(
            chat_id=message.chat.id,
            text=UNKNOWN_COMMAND_TEXT,
            reply_markup=get_heroes_menu()
        )
        await state.set_state(MenuStates.HEROES_MENU)

# Обробник для меню класу героя
@router.message(MenuStates.HERO_CLASS_MENU)
async def handle_hero_class_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    hero_name = message.text
    hero_class = (await state.get_data()).get('hero_class')

    if hero_class and hero_name in heroes_by_class.get(hero_class, []):
        # Обробка вибору героя (функціонал залежить від вашої реалізації)
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Ви обрали героя **{hero_name}** класу **{hero_class}**.",
            parse_mode="Markdown"
        )
        # Повернення до меню Персонажів
        await bot.send_message(
            chat_id=message.chat.id,
            text="Повернення до меню Персонажів.",
            reply_markup=get_heroes_menu()
        )
        await state.set_state(MenuStates.HEROES_MENU)
    else:
        # Герой не знайдений або невірний клас
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Герой **{hero_name}** не знайдений в класі **{hero_class}**. Будь ласка, спробуйте ще раз.",
            reply_markup=get_hero_class_menu(hero_class),
            parse_mode="Markdown"
        )
        await state.set_state(MenuStates.HERO_CLASS_MENU)

# Обробник для меню Гайди
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
            "interactive_text": "Оберіть нові гайди:",
            "state": MenuStates.GUIDES_MENU
        },
        MenuButton.POPULAR_GUIDES.value: {
            "text": MenuButton.POPULAR_GUIDES.value,
            "keyboard": get_guides_menu(),
            "interactive_text": "Оберіть топ гайди:",
            "state": MenuStates.GUIDES_MENU
        },
        MenuButton.BEGINNER_GUIDES.value: {
            "text": MenuButton.BEGINNER_GUIDES.value,
            "keyboard": get_guides_menu(),
            "interactive_text": "Оберіть гайди для початківців:",
            "state": MenuStates.GUIDES_MENU
        },
        MenuButton.ADVANCED_TECHNIQUES.value: {
            "text": MenuButton.ADVANCED_TECHNIQUES.value,
            "keyboard": get_guides_menu(),
            "interactive_text": "Оберіть стратегії гри:",
            "state": MenuStates.GUIDES_MENU
        },
        MenuButton.TEAMPLAY_GUIDES.value: {
            "text": MenuButton.TEAMPLAY_GUIDES.value,
            "keyboard": get_guides_menu(),
            "interactive_text": "Оберіть гайди для командної гри:",
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
        await bot.send_message(
            chat_id=message.chat.id,
            text=transition["interactive_text"],
            reply_markup=transition["keyboard"]
        )
        await state.set_state(transition["state"])
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=UNKNOWN_COMMAND_TEXT,
            reply_markup=get_guides_menu()
        )
        await state.set_state(MenuStates.GUIDES_MENU)

# Обробник для меню Контр-піки
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
        await bot.send_message(
            chat_id=message.chat.id,
            text=transition["interactive_text"],
            reply_markup=transition["keyboard"]
        )
        await state.set_state(transition["state"])
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=UNKNOWN_COMMAND_TEXT,
            reply_markup=get_counter_picks_menu()
        )
        await state.set_state(MenuStates.COUNTER_PICKS_MENU)

# Обробник для меню Білди
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
            "interactive_text": "Оберіть опцію створення білду:",
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
        await bot.send_message(
            chat_id=message.chat.id,
            text=transition["interactive_text"],
            reply_markup=transition["keyboard"]
        )
        await state.set_state(transition["state"])
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=UNKNOWN_COMMAND_TEXT,
            reply_markup=get_builds_menu()
        )
        await state.set_state(MenuStates.BUILDS_MENU)

# Обробник для меню Голосування
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
            "interactive_text": "Оберіть поточні опитування:",
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
            await bot.send_message(
                chat_id=message.chat.id,
                text=transition["interactive_text"],
                reply_markup=transition["keyboard"]
            )
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=transition["interactive_text"],
                reply_markup=transition["keyboard"]
            )
        await state.set_state(transition["state"])
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=UNKNOWN_COMMAND_TEXT,
            reply_markup=get_voting_menu()
        )
        await state.set_state(MenuStates.VOTING_MENU)

# Обробник для меню Профіль
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
            "interactive_text": "Оберіть розділ статистики:",
            "state": MenuStates.STATISTICS_MENU
        },
        MenuButton.ACHIEVEMENTS.value: {
            "text": MenuButton.ACHIEVEMENTS.value,
            "keyboard": get_achievements_menu(),
            "interactive_text": "Оберіть розділ досягнень:",
            "state": MenuStates.ACHIEVEMENTS_MENU
        },
        MenuButton.SETTINGS.value: {
            "text": MenuButton.SETTINGS.value,
            "keyboard": get_settings_menu(),
            "interactive_text": "Оберіть розділ налаштувань:",
            "state": MenuStates.SETTINGS_MENU
        },
        MenuButton.FEEDBACK.value: {
            "text": MenuButton.FEEDBACK.value,
            "keyboard": get_feedback_menu(),
            "interactive_text": "Оберіть опцію зворотного зв'язку:",
            "state": MenuStates.FEEDBACK_MENU
        },
        MenuButton.HELP.value: {
            "text": MenuButton.HELP.value,
            "keyboard": get_help_menu(),
            "interactive_text": "Оберіть розділ допомоги:",
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
        await bot.send_message(
            chat_id=message.chat.id,
            text=transition["interactive_text"],
            reply_markup=transition["keyboard"]
        )
        await state.set_state(transition["state"])
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=UNKNOWN_COMMAND_TEXT,
            reply_markup=get_profile_menu_buttons()
        )
        await state.set_state(MenuStates.PROFILE_MENU)

# Обробник для меню Статистика
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
            "interactive_text": "Оберіть опцію загальної активності:",
            "state": MenuStates.STATISTICS_MENU
        },
        MenuButton.RANKING.value: {
            "text": MenuButton.RANKING.value,
            "keyboard": get_statistics_menu(),
            "interactive_text": "Оберіть опцію рейтингу:",
            "state": MenuStates.STATISTICS_MENU
        },
        MenuButton.GAME_STATS.value: {
            "text": MenuButton.GAME_STATS.value,
            "keyboard": get_statistics_menu(),
            "interactive_text": "Оберіть ігрову статистику:",
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
        await bot.send_message(
            chat_id=message.chat.id,
            text=transition["interactive_text"],
            reply_markup=transition["keyboard"]
        )
        await state.set_state(transition["state"])
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=UNKNOWN_COMMAND_TEXT,
            reply_markup=get_statistics_menu()
        )
        await state.set_state(MenuStates.STATISTICS_MENU)

# Обробник для меню Досягнення
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
        await bot.send_message(
            chat_id=message.chat.id,
            text=transition["interactive_text"],
            reply_markup=transition["keyboard"]
        )
        await state.set_state(transition["state"])
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=UNKNOWN_COMMAND_TEXT,
            reply_markup=get_achievements_menu()
        )
        await state.set_state(MenuStates.ACHIEVEMENTS_MENU)

# Обробник для меню Налаштування
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
            "interactive_text": "Оберіть мову інтерфейсу:",
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
            "state": MenuStates.UPDATE_ID
        },
        MenuButton.NOTIFICATIONS.value: {
            "text": MenuButton.NOTIFICATIONS.value,
            "keyboard": get_settings_menu(),
            "interactive_text": "Оберіть налаштування сповіщень:",
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
            await bot.send_message(
                chat_id=message.chat.id,
                text=transition["interactive_text"],
                reply_markup=transition["keyboard"]
            )
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text=transition["interactive_text"],
                reply_markup=transition["keyboard"]
            )
        await state.set_state(transition["state"])
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=UNKNOWN_COMMAND_TEXT,
            reply_markup=get_settings_menu()
        )
        await state.set_state(MenuStates.SETTINGS_MENU)

# Обробник для меню Зворотний Зв'язок
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
        await bot.send_message(
            chat_id=message.chat.id,
            text=transition["interactive_text"],
            reply_markup=transition["keyboard"]
        )
        await state.set_state(transition["state"])
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=UNKNOWN_COMMAND_TEXT,
            reply_markup=get_feedback_menu()
        )
        await state.set_state(MenuStates.FEEDBACK_MENU)

# Обробник для меню Допомога
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
            "interactive_text": "Оберіть розділ Інструкцій:",
            "state": MenuStates.HELP_MENU
        },
        MenuButton.FAQ.value: {
            "text": MenuButton.FAQ.value,
            "keyboard": get_help_menu(),
            "interactive_text": "Оберіть розділ FAQ:",
            "state": MenuStates.HELP_MENU
        },
        MenuButton.HELP_SUPPORT.value: {
            "text": MenuButton.HELP_SUPPORT.value,
            "keyboard": get_help_menu(),
            "interactive_text": "Оберіть розділ Підтримки:",
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
        await bot.send_message(
            chat_id=message.chat.id,
            text=transition["interactive_text"],
            reply_markup=transition["keyboard"]
        )
        await state.set_state(transition["state"])
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=UNKNOWN_COMMAND_TEXT,
            reply_markup=get_help_menu()
        )
        await state.set_state(MenuStates.HELP_MENU)

# Обробник для пошуку героя
@router.message(MenuStates.SEARCH_HERO)
async def handle_search_hero(message: Message, state: FSMContext, bot: Bot):
    hero_name = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} шукає героя: {hero_name}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Перевірка чи існує герой
    all_heroes = [hero for heroes in heroes_by_class.values() for hero in heroes]
    if hero_name in all_heroes:
        response_text = SEARCH_HERO_RESPONSE_TEXT.format(hero_name=hero_name)
        # Тут можна додати логіку отримання інформації про героя
    else:
        response_text = f"Герой '{hero_name}' не знайдений. Будь ласка, спробуйте ще раз."

    await bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        parse_mode="Markdown",
        reply_markup=get_heroes_menu()
    )

    # Повертаємо користувача до меню Персонажів
    await state.set_state(MenuStates.HEROES_MENU)

# Обробник для пропозиції теми голосування
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
        parse_mode="Markdown",
        reply_markup=get_voting_menu()
    )

    # Повертаємо користувача до меню Голосування
    await state.set_state(MenuStates.VOTING_MENU)

# Обробник для зміни Username
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
        parse_mode="Markdown",
        reply_markup=get_settings_menu()
    )

    # Повертаємо користувача до меню Налаштувань
    await state.set_state(MenuStates.SETTINGS_MENU)

# Обробник для оновлення ID
@router.message(MenuStates.UPDATE_ID)
async def handle_update_id(message: Message, state: FSMContext, bot: Bot):
    new_id = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} оновлює ID на: {new_id}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Тут можна додати логіку оновлення ID
    # Наприклад, перевірка формату, оновлення в базі даних тощо
    # Поки що відправимо повідомлення про отримання запиту

    if new_id:
        response_text = f"Ваш ID було успішно оновлено на **{new_id}**."
        # Тут можна додати логіку оновлення ID
    else:
        response_text = "Будь ласка, введіть новий ID."

    await bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        parse_mode="Markdown",
        reply_markup=get_settings_menu()
    )

    # Повертаємо користувача до меню Налаштувань
    await state.set_state(MenuStates.SETTINGS_MENU)

# Обробник для отримання відгуку
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
        parse_mode="Markdown",
        reply_markup=get_feedback_menu()
    )

    # Повертаємо користувача до меню Зворотного Зв'язку
    await state.set_state(MenuStates.FEEDBACK_MENU)

# Обробник для звіту про помилку
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
        parse_mode="Markdown",
        reply_markup=get_feedback_menu()
    )

    # Повертаємо користувача до меню Зворотного Зв'язку
    await state.set_state(MenuStates.FEEDBACK_MENU)

# Обробник для меню M6
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
        await bot.send_message(
            chat_id=message.chat.id,
            text=transition["interactive_text"],
            reply_markup=transition["keyboard"]
        )
        await state.set_state(transition["state"])
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=UNKNOWN_COMMAND_TEXT,
            reply_markup=get_m6_menu()
        )
        await state.set_state(MenuStates.M6_MENU)

# Обробник для меню GPT
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
        await bot.send_message(
            chat_id=message.chat.id,
            text=transition["interactive_text"],
            reply_markup=transition["keyboard"]
        )
        await state.set_state(transition["state"])
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=UNKNOWN_COMMAND_TEXT,
            reply_markup=get_gpt_menu()
        )
        await state.set_state(MenuStates.GPT_MENU)

# Обробник для меню META
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
        await bot.send_message(
            chat_id=message.chat.id,
            text=transition["interactive_text"],
            reply_markup=transition["keyboard"]
        )
        await state.set_state(transition["state"])
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=UNKNOWN_COMMAND_TEXT,
            reply_markup=get_meta_menu()
        )
        await state.set_state(MenuStates.META_MENU)

# Обробник для меню Турніри
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
            "interactive_text": (
                "Процес Створення Турніру:\n\n"
                "1. Виберіть Тип Турніру:\n"
                "   - 5х5\n"
                "   - 2х2\n"
                "   - 1 на 1\n\n"
                "2. Введіть Деталі Турніру:\n"
                "   - Назва: Введіть назву турніру.\n"
                "   - Опис: Короткий опис турніру.\n"
                "   - Дата та Час: Вкажіть дату та час проведення.\n"
                "   - Умови Участі: Вкажіть вимоги для учасників.\n\n"
                "3. Надішліть Запит на Підтвердження адміністратору."
            ),
            "state": MenuStates.CREATE_TOURNAMENT
        },
        MenuButton.VIEW_TOURNAMENTS.value: {
            "text": MenuButton.VIEW_TOURNAMENTS.value,
            "keyboard": ReplyKeyboardRemove(),
            "interactive_text": (
                "Огляд Доступних Турнірів:\n\n"
                "1. Список Активних Турнірів:\n"
                "   - Назва Турніру\n"
                "   - Тип Турніру\n"
                "   - Дата та Час\n"
                "   - Статус: Активний / Завершений\n"
                "   - Кнопка: Детальніше\n\n"
                "2. Детальніше про Турнір:\n"
                "   - Інформація про турнір.\n"
                "   - Список учасників.\n"
                "   - Опції для реєстрації (якщо реєстрація відкрита).\n\n"
                "3. 📋 Зареєструватися:\n"
                "   - Процес реєстрації на турнір."
            ),
            "state": MenuStates.VIEW_TOURNAMENTS
        },
        MenuButton.BACK_TOURNAMENTS.value: {
            "text": MenuButton.BACK_TOURNAMENTS.value,
            "keyboard": get_navigation_menu(),
            "interactive_text": "Повернення до меню Навігації.",
            "state": MenuStates.NAVIGATION_MENU
        }
    }.get(user_choice)

    if user_choice == MenuButton.CREATE_TOURNAMENT.value:
        # Встановлюємо стан для створення турніру
        await bot.send_message(
            chat_id=message.chat.id,
            text=transition["interactive_text"],
            reply_markup=transition["keyboard"]
        )
        await state.set_state(transition["state"])
    elif user_choice == MenuButton.VIEW_TOURNAMENTS.value:
        # Встановлюємо стан для перегляду турнірів
        await bot.send_message(
            chat_id=message.chat.id,
            text=transition["interactive_text"],
            reply_markup=transition["keyboard"]
        )
        await state.set_state(transition["state"])
    elif transition:
        await bot.send_message(
            chat_id=message.chat.id,
            text=transition["interactive_text"],
            reply_markup=transition["keyboard"]
        )
        await state.set_state(transition["state"])
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text=UNKNOWN_COMMAND_TEXT,
            reply_markup=get_tournaments_menu()
        )
        await state.set_state(MenuStates.TOURNAMENTS_MENU)

# Обробник для створення турніру
@router.message(MenuStates.CREATE_TOURNAMENT)
async def handle_create_tournament(message: Message, state: FSMContext, bot: Bot):
    tournament_details = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} створює турнір з деталями: {tournament_details}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Тут реалізуйте логіку створення турніру
    # Наприклад, збереження в базі даних та відправка адміністратору на підтвердження
    # Поки що відправимо повідомлення про успішне створення

    response_text = "Ваш турнір успішно створено та надіслано на підтвердження адміністратору."

    await bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        parse_mode="Markdown",
        reply_markup=get_tournaments_menu()
    )

    # Повертаємо користувача до меню Турнірів
    await state.set_state(MenuStates.TOURNAMENTS_MENU)

# Обробник для перегляду турнірів
@router.message(MenuStates.VIEW_TOURNAMENTS)
async def handle_view_tournaments(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"Користувач {message.from_user.id} переглядає турніри")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Тут реалізуйте логіку перегляду турнірів
    # Наприклад, отримання списку турнірів з бази даних
    # Поки що відправимо приклад списку турнірів

    response_text = (
        "Список доступних турнірів:\n\n"
        "1. Турнір А - Тип: 5х5 - Дата: 25.12.2024 - Статус: Активний\n"
        "2. Турнір Б - Тип: 2х2 - Дата: 30.12.2024 - Статус: Активний\n"
        "3. Турнір В - Тип: 1 на 1 - Дата: 05.01.2025 - Статус: Завершений\n\n"
        "Оберіть турнір для детальнішої інформації."
    )

    await bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove()
    )

    # Повертаємо користувача до меню Турнірів
    await state.set_state(MenuStates.TOURNAMENTS_MENU)

# Обробник для невідомих повідомлень
@router.message()
async def unknown_command(message: Message, state: FSMContext, bot: Bot):
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Отримуємо поточний стан
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
        new_interactive_text = "Меню Навігації"
        new_state = MenuStates.NAVIGATION_MENU
    elif current_state == MenuStates.HEROES_MENU.state:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = "Меню Персонажів"
        new_state = MenuStates.HEROES_MENU
    elif current_state == MenuStates.HERO_CLASS_MENU.state:
        hero_class = (await state.get_data()).get('hero_class', 'Танк')
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
        MenuStates.UPDATE_ID.state,
        MenuStates.RECEIVE_FEEDBACK.state,
        MenuStates.REPORT_BUG.state
    ]:
        # Якщо користувач перебуває в процесі введення, надсилаємо підказку
        await bot.send_message(
            chat_id=message.chat.id,
            text=USE_BUTTON_NAVIGATION_TEXT,
            reply_markup=ReplyKeyboardRemove()
        )
        # Залишаємо стан без змін
        return
    else:
        # Якщо стан невідомий, повертаємо до головного меню
        user_first_name = message.from_user.first_name
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
        new_state = MenuStates.MAIN_MENU

    # Оновлюємо меню
    await update_menu(
        message=message,
        state=state,
        bot=bot,
        new_main_text=new_main_text,
        new_main_keyboard=new_main_keyboard,
        new_interactive_text=new_interactive_text,
        new_state=new_state
    )