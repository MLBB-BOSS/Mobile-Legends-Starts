# handlers/base.py

import logging
from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    ReplyKeyboardRemove,
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
    get_help_menu,
    menu_button_to_class  # Переконайтеся, що цей імпорт необхідний
)

from keyboards.inline_menus import get_generic_inline_keyboard  # Якщо ви використовуєте інлайн-клавіші
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
)

# Ініціалізація маршрутизатора
router = Router()

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Визначаємо ID адміністратора (замініть на фактичний)
ADMIN_CHAT_ID = 123456789  # Змініть на фактичний Chat ID адміністратора

# Зберігання тимчасових турнірів (для прикладу, використовується словник)
# У реальному застосунку рекомендується використовувати базу даних
pending_tournaments = {}

# Приклад мапінгу героїв за класами
heroes_by_class = {
    "Танк": ["Герой1", "Герой2"],
    "Дамагер": ["Герой3", "Герой4"],
    "Підтримка": ["Герой5", "Герой6"],
    # Додайте інших героїв відповідно до класів
}

# Визначаємо кнопки для підтвердження адміністратором
def get_admin_confirmation_keyboard(tournament_id: int):
    buttons = [
        InlineKeyboardButton(text="✅ Підтвердити", callback_data=f'confirm_tournament:{tournament_id}'),
        InlineKeyboardButton(text="❌ Відхилити", callback_data=f'reject_tournament:{tournament_id}')
    ]
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard

# Обробник команди /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"Користувач {message.from_user.id} викликав /start")

    # Видаляємо повідомлення користувача /start
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення /start: {e}")

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
    new_main_keyboard: ReplyKeyboardRemove | InlineKeyboardMarkup | ReplyKeyboardMarkup,
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
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    transition = {
        MenuButton.NAVIGATION.value: {
            "text": MenuButton.NAVIGATION.value,
            "keyboard": get_navigation_menu(),
            "interactive_text": NAVIGATION_INTERACTIVE_TEXT,
            "state": MenuStates.NAVIGATION_MENU
        },
        MenuButton.PROFILE.value: {
            "text": MenuButton.PROFILE.value,
            "keyboard": get_profile_menu_buttons(),
            "interactive_text": PROFILE_INTERACTIVE_TEXT,
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
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    transition = {
        MenuButton.HEROES.value: {
            "text": MenuButton.HEROES.value,
            "keyboard": get_heroes_menu(),
            "interactive_text": NAVIGATION_INTERACTIVE_TEXT,
            "state": MenuStates.HEROES_MENU
        },
        MenuButton.BUILDS.value: {
            "text": MenuButton.BUILDS.value,
            "keyboard": get_builds_menu(),
            "interactive_text": NAVIGATION_INTERACTIVE_TEXT,
            "state": MenuStates.BUILDS_MENU
        },
        MenuButton.COUNTER_PICKS.value: {
            "text": MenuButton.COUNTER_PICKS.value,
            "keyboard": get_counter_picks_menu(),
            "interactive_text": NAVIGATION_INTERACTIVE_TEXT,
            "state": MenuStates.COUNTER_PICKS_MENU
        },
        MenuButton.GUIDES.value: {
            "text": MenuButton.GUIDES.value,
            "keyboard": get_guides_menu(),
            "interactive_text": NAVIGATION_INTERACTIVE_TEXT,
            "state": MenuStates.GUIDES_MENU
        },
        MenuButton.VOTING.value: {
            "text": MenuButton.VOTING.value,
            "keyboard": get_voting_menu(),
            "interactive_text": NAVIGATION_INTERACTIVE_TEXT,
            "state": MenuStates.VOTING_MENU
        },
        MenuButton.M6.value: {
            "text": MenuButton.M6.value,
            "keyboard": get_m6_menu(),
            "interactive_text": NAVIGATION_INTERACTIVE_TEXT,
            "state": MenuStates.M6_MENU
        },
        MenuButton.GPT.value: {
            "text": MenuButton.GPT.value,
            "keyboard": get_gpt_menu(),
            "interactive_text": NAVIGATION_INTERACTIVE_TEXT,
            "state": MenuStates.GPT_MENU
        },
        MenuButton.META.value: {
            "text": MenuButton.META.value,
            "keyboard": get_meta_menu(),
            "interactive_text": NAVIGATION_INTERACTIVE_TEXT,
            "state": MenuStates.META_MENU
        },
        MenuButton.TOURNAMENTS.value: {
            "text": MenuButton.TOURNAMENTS.value,
            "keyboard": get_tournaments_menu(),
            "interactive_text": NAVIGATION_INTERACTIVE_TEXT,
            "state": MenuStates.TOURNAMENTS_MENU
        },
        MenuButton.BACK.value: {
            "text": MenuButton.BACK.value,
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
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Перевіряємо, чи обрана кнопка належить до класів героїв
    hero_class = menu_button_to_class.get(user_choice)

    if hero_class:
        # Зберігаємо вибраний клас героя в стані
        await state.update_data(hero_class=hero_class)
        # Створюємо меню для обраного класу героя
        hero_class_menu = get_hero_class_menu()
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"Оберіть героя класу **{hero_class}**:",
            reply_markup=hero_class_menu,
            parse_mode="Markdown"
        )
        await state.set_state(MenuStates.HERO_CLASS_MENU)
    elif user_choice == MenuButton.BACK.value:
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
            reply_markup=get_hero_class_menu(),
            parse_mode="Markdown"
        )
        await state.set_state(MenuStates.HERO_CLASS_MENU)

# Обробник для меню Гайди
@router.message(MenuStates.GUIDES_MENU)
async def handle_guides_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Гайди")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    transition = {
        "Нові Гайди": {
            "text": "Нові Гайди",
            "keyboard": get_guides_menu(),
            "interactive_text": "Оберіть нові гайди:",
            "state": MenuStates.GUIDES_MENU
        },
        "Популярні Гайди": {
            "text": "Популярні Гайди",
            "keyboard": get_guides_menu(),
            "interactive_text": "Оберіть топ гайди:",
            "state": MenuStates.GUIDES_MENU
        },
        "Гайди для Початківців": {
            "text": "Гайди для Початківців",
            "keyboard": get_guides_menu(),
            "interactive_text": "Оберіть гайди для початківців:",
            "state": MenuStates.GUIDES_MENU
        },
        "Розширені Техніки": {
            "text": "Розширені Техніки",
            "keyboard": get_guides_menu(),
            "interactive_text": "Оберіть стратегії гри:",
            "state": MenuStates.GUIDES_MENU
        },
        "Гайди для Командної Гри": {
            "text": "Гайди для Командної Гри",
            "keyboard": get_guides_menu(),
            "interactive_text": "Оберіть гайди для командної гри:",
            "state": MenuStates.GUIDES_MENU
        },
        MenuButton.BACK.value: {
            "text": MenuButton.BACK.value,
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
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    transition = {
        "Пошук Контр-піку": {
            "text": "Пошук Контр-піку",
            "keyboard": ReplyKeyboardRemove(),
            "interactive_text": "Введіть ім'я героя для пошуку контр-піку:",
            "state": MenuStates.SEARCH_HERO
        },
        "Список Контр-піків": {
            "text": "Список Контр-піків",
            "keyboard": get_counter_picks_menu(),
            "interactive_text": "Список контр-піків доступний.",
            "state": MenuStates.COUNTER_PICKS_MENU
        },
        MenuButton.BACK.value: {
            "text": MenuButton.BACK.value,
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
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    transition = {
        "Створити Білд": {
            "text": "Створити Білд",
            "keyboard": ReplyKeyboardRemove(),
            "interactive_text": "Введіть деталі нового білду:",
            "state": MenuStates.CREATE_BUILD
        },
        "Мої Білди": {
            "text": "Мої Білди",
            "keyboard": get_builds_menu(),
            "interactive_text": "Ваші обрані білди.",
            "state": MenuStates.BUILDS_MENU
        },
        "Популярні Білди": {
            "text": "Популярні Білди",
            "keyboard": get_builds_menu(),
            "interactive_text": "Популярні білди доступні.",
            "state": MenuStates.BUILDS_MENU
        },
        MenuButton.BACK.value: {
            "text": MenuButton.BACK.value,
            "keyboard": get_navigation_menu(),
            "interactive_text": "Повернення до меню Навігації.",
            "state": MenuStates.NAVIGATION_MENU
        }
    }.get(user_choice)

    if transition:
        if user_choice == "Створити Білд":
            await bot.send_message(
                chat_id=message.chat.id,
                text=transition["interactive_text"],
                reply_markup=ReplyKeyboardRemove()
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
            reply_markup=get_builds_menu()
        )
        await state.set_state(MenuStates.BUILDS_MENU)

# Обробник для меню Голосування
@router.message(MenuStates.VOTING_MENU)
async def handle_voting_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Голосування")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

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
        MenuButton.BACK_TO_NAVIGATION.value: {
            "text": MenuButton.BACK_TO_NAVIGATION.value,
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
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    transition = {
        MenuButton.STATISTICS.value: {
            "text": MenuButton.STATISTICS.value,
            "keyboard": get_statistics_menu(),
            "interactive_text": STATISTICS_INTERACTIVE_TEXT,
            "state": MenuStates.STATISTICS_MENU
        },
        MenuButton.ACHIEVEMENTS.value: {
            "text": MenuButton.ACHIEVEMENTS.value,
            "keyboard": get_achievements_menu(),
            "interactive_text": ACHIEVEMENTS_INTERACTIVE_TEXT,
            "state": MenuStates.ACHIEVEMENTS_MENU
        },
        MenuButton.SETTINGS.value: {
            "text": MenuButton.SETTINGS.value,
            "keyboard": get_settings_menu(),
            "interactive_text": SETTINGS_INTERACTIVE_TEXT,
            "state": MenuStates.SETTINGS_MENU
        },
        MenuButton.FEEDBACK.value: {
            "text": MenuButton.FEEDBACK.value,
            "keyboard": get_feedback_menu(),
            "interactive_text": FEEDBACK_INTERACTIVE_TEXT,
            "state": MenuStates.FEEDBACK_MENU
        },
        MenuButton.HELP.value: {
            "text": MenuButton.HELP.value,
            "keyboard": get_help_menu(),
            "interactive_text": HELP_INTERACTIVE_TEXT,
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
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    transition = {
        MenuButton.ACTIVITY.value: {
            "text": MenuButton.ACTIVITY.value,
            "keyboard": get_statistics_menu(),
            "interactive_text": ACTIVITY_TEXT,
            "state": MenuStates.STATISTICS_MENU
        },
        MenuButton.RANKING.value: {
            "text": MenuButton.RANKING.value,
            "keyboard": get_statistics_menu(),
            "interactive_text": RANKING_TEXT,
            "state": MenuStates.STATISTICS_MENU
        },
        MenuButton.GAME_STATS.value: {
            "text": MenuButton.GAME_STATS.value,
            "keyboard": get_statistics_menu(),
            "interactive_text": GAME_STATS_TEXT,
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
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    transition = {
        MenuButton.BADGES.value: {
            "text": MenuButton.BADGES.value,
            "keyboard": get_achievements_menu(),
            "interactive_text": BADGES_TEXT,
            "state": MenuStates.ACHIEVEMENTS_MENU
        },
        MenuButton.PROGRESS.value: {
            "text": MenuButton.PROGRESS.value,
            "keyboard": get_achievements_menu(),
            "interactive_text": PROGRESS_TEXT,
            "state": MenuStates.ACHIEVEMENTS_MENU
        },
        MenuButton.TOURNAMENT_STATS.value: {
            "text": MenuButton.TOURNAMENT_STATS.value,
            "keyboard": get_achievements_menu(),
            "interactive_text": TOURNAMENT_STATS_TEXT,
            "state": MenuStates.ACHIEVEMENTS_MENU
        },
        MenuButton.AWARDS.value: {
            "text": MenuButton.AWARDS.value,
            "keyboard": get_achievements_menu(),
            "interactive_text": AWARDS_TEXT,
            "state": MenuStates.ACHIEVEMENTS_MENU
        },
        MenuButton.BACK.value: {
            "text": MenuButton.BACK.value,
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
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    transition = {
        MenuButton.LANGUAGE.value: {
            "text": MenuButton.LANGUAGE.value,
            "keyboard": get_settings_menu(),
            "interactive_text": LANGUAGE_TEXT,
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
            "interactive_text": NOTIFICATIONS_TEXT,
            "state": MenuStates.SETTINGS_MENU
        },
        MenuButton.BACK.value: {
            "text": MenuButton.BACK.value,
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
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

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
        MenuButton.BACK.value: {
            "text": MenuButton.BACK.value,
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
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    transition = {
        MenuButton.INSTRUCTIONS.value: {
            "text": MenuButton.INSTRUCTIONS.value,
            "keyboard": get_help_menu(),
            "interactive_text": INSTRUCTIONS_TEXT,
            "state": MenuStates.HELP_MENU
        },
        MenuButton.FAQ.value: {
            "text": MenuButton.FAQ.value,
            "keyboard": get_help_menu(),
            "interactive_text": FAQ_TEXT,
            "state": MenuStates.HELP_MENU
        },
        MenuButton.HELP_SUPPORT.value: {
            "text": MenuButton.HELP_SUPPORT.value,
            "keyboard": get_help_menu(),
            "interactive_text": HELP_SUPPORT_TEXT,
            "state": MenuStates.HELP_MENU
        },
        MenuButton.BACK.value: {
            "text": MenuButton.BACK.value,
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
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

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
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Перевірка введеної теми
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
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Перевірка введеного Username
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
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Перевірка введеного ID
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
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Перевірка введеного відгуку
    if feedback:
        response_text = FEEDBACK_RECEIVED_TEXT
        # Тут можна додати логіку збереження відгуку або відправки адміністратору
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
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Перевірка введеного звіту
    if bug_report:
        response_text = BUG_REPORT_RECEIVED_TEXT
        # Тут можна додати логіку збереження звіту або відправки адміністратору
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
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

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
            "interactive_text": "Статистика M6.",
            "state": MenuStates.M6_MENU
        },
        MenuButton.M6_NEWS.value: {
            "text": MenuButton.M6_NEWS.value,
            "keyboard": get_m6_menu(),
            "interactive_text": "Новини M6.",
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
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

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
            "interactive_text": "Поради GPT.",
            "state": MenuStates.GPT_MENU
        },
        MenuButton.GPT_HERO_STATISTICS.value: {
            "text": MenuButton.GPT_HERO_STATISTICS.value,
            "keyboard": get_gpt_menu(),
            "interactive_text": "Статистика Героїв GPT.",
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
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

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
            "interactive_text": "Рекомендації META.",
            "state": MenuStates.META_MENU
        },
        MenuButton.META_UPDATE.value: {
            "text": MenuButton.META_UPDATE.value,
            "keyboard": get_meta_menu(),
            "interactive_text": "Оновлення META.",
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
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    transition = {
        MenuButton.CREATE_TOURNAMENT.value: {
            "text": MenuButton.CREATE_TOURNAMENT.value,
            "keyboard": ReplyKeyboardRemove(),
            "interactive_text": (
                "Процес Створення Турніру:\n\n"
                "Будь ласка, введіть деталі турніру у наступному форматі:\n"
                "1. Тип Турніру (5х5, 2х2, 1 на 1)\n"
                "2. Назва Турніру\n"
                "3. Опис Турніру\n"
                "4. Дата та Час Проведення (ДД.ММ.РРРР ЧЧ:ММ)\n"
                "5. Умови Участі\n\n"
                "Приклад:\n"
                "5х5\nМайстер Турнір\nОпис турніру...\n25.12.2024 18:00\nВимоги..."
            ),
            "state": MenuStates.CREATE_TOURNAMENT
        },
        MenuButton.VIEW_TOURNAMENTS.value: {
            "text": MenuButton.VIEW_TOURNAMENTS.value,
            "keyboard": ReplyKeyboardRemove(),
            "interactive_text": (
                "Огляд Доступних Турнірів:\n\n"
                "1. Турнір А - Тип: 5х5 - Дата: 25.12.2024 - Статус: Активний\n"
                "2. Турнір Б - Тип: 2х2 - Дата: 30.12.2024 - Статус: Активний\n"
                "3. Турнір В - Тип: 1 на 1 - Дата: 05.01.2025 - Статус: Завершений\n\n"
                "Оберіть турнір для детальнішої інформації."
            ),
            "state": MenuStates.VIEW_TOURNAMENTS
        },
        MenuButton.BACK.value: {
            "text": MenuButton.BACK.value,
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
            reply_markup=get_tournaments_menu()
        )
        await state.set_state(MenuStates.TOURNAMENTS_MENU)

# Обробник для створення турніру
@router.message(MenuStates.CREATE_TOURNAMENT)
async def handle_create_tournament(message: Message, state: FSMContext, bot: Bot):
    tournament_details = message.text.strip().split('\n')
    logger.info(f"Користувач {message.from_user.id} створює турнір з деталями: {tournament_details}")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Перевірка формату введених даних
    if len(tournament_details) < 5:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Неправильний формат. Будь ласка, введіть деталі турніру у вказаному форматі.",
            reply_markup=get_tournaments_menu()
        )
        await state.set_state(MenuStates.TOURNAMENTS_MENU)
        return

    tournament_type, name, description, date_time, conditions = tournament_details[:5]

    # Створення унікального ID для турніру (просто приклад)
    tournament_id = len(pending_tournaments) + 1

    # Зберігаємо турнір у тимчасовому сховищі
    pending_tournaments[tournament_id] = {
        "type": tournament_type,
        "name": name,
        "description": description,
        "date_time": date_time,
        "conditions": conditions,
        "creator_id": message.from_user.id
    }

    # Відправляємо повідомлення адміністратору для підтвердження
    admin_message_text = (
        f"Новий турнір для підтвердження:\n\n"
        f"**Тип:** {tournament_type}\n"
        f"**Назва:** {name}\n"
        f"**Опис:** {description}\n"
        f"**Дата та Час:** {date_time}\n"
        f"**Умови Участі:** {conditions}\n\n"
        f"ID Турніру: {tournament_id}"
    )

    admin_keyboard = get_admin_confirmation_keyboard(tournament_id)

    try:
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=admin_message_text,
            parse_mode="Markdown",
            reply_markup=admin_keyboard
        )
    except Exception as e:
        logger.error(f"Не вдалося відправити повідомлення адміністратору: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text="Сталася помилка при надсиланні турніру на підтвердження. Спробуйте ще раз пізніше.",
            reply_markup=get_tournaments_menu()
        )
        # Видаляємо турнір з тимчасового сховища
        del pending_tournaments[tournament_id]
        await state.set_state(MenuStates.TOURNAMENTS_MENU)
        return

    # Відправляємо користувачу повідомлення про успішне створення
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
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    # Тут реалізуйте логіку перегляду турнірів
    # Наприклад, отримання списку турнірів з бази даних або з тимчасового сховища
    # Поки що відправимо приклад списку турнірів

    active_tournaments = [
        {
            "id": 1,
            "name": "Турнір А",
            "type": "5х5",
            "date_time": "25.12.2024 18:00",
            "status": "Активний"
        },
        {
            "id": 2,
            "name": "Турнір Б",
            "type": "2х2",
            "date_time": "30.12.2024 20:00",
            "status": "Активний"
        },
        {
            "id": 3,
            "name": "Турнір В",
            "type": "1 на 1",
            "date_time": "05.01.2025 15:00",
            "status": "Завершений"
        }
    ]

    response_text = "Список доступних турнірів:\n\n"
    for tournament in active_tournaments:
        response_text += f"{tournament['id']}. **{tournament['name']}** - Тип: {tournament['type']} - Дата: {tournament['date_time']} - Статус: {tournament['status']}\n"

    response_text += "\nОберіть турнір для детальнішої інформації."

    await bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        parse_mode="Markdown",
        reply_markup=get_tournaments_menu()
    )

    # Повертаємо користувача до меню Турнірів
    await state.set_state(MenuStates.TOURNAMENTS_MENU)

# Обробник для підтвердження турніру адміністратором
@router.callback_query(lambda c: c.data.startswith('confirm_tournament:'))
async def handle_confirm_tournament(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = callback.data.split(':')
    if len(data) != 2:
        await callback.answer("Невірний формат даних.", show_alert=True)
        return

    action, tournament_id_str = data
    try:
        tournament_id = int(tournament_id_str)
    except ValueError:
        await callback.answer("Невірний ID турніру.", show_alert=True)
        return

    tournament = pending_tournaments.get(tournament_id)
    if not tournament:
        await callback.answer("Турнір не знайдено або вже підтверджено.", show_alert=True)
        return

    # Тут можна додати логіку підтвердження турніру
    # Наприклад, збереження в базі даних
    # Для прикладу, ми просто видалимо його з тимчасового сховища та повідомимо користувача

    creator_id = tournament["creator_id"]
    del pending_tournaments[tournament_id]

    # Відправляємо повідомлення користувачу про підтвердження турніру
    try:
        await bot.send_message(
            chat_id=creator_id,
            text=f"Ваш турнір **{tournament['name']}** було підтверджено адміністратором.",
            parse_mode="Markdown",
            reply_markup=get_tournaments_menu()
        )
    except Exception as e:
        logger.error(f"Не вдалося відправити повідомлення користувачу {creator_id}: {e}")

    # Відповідаємо адміністратору, що турнір підтверджено
    await callback.answer("Турнір підтверджено.", show_alert=True)

# Обробник для відхилення турніру адміністратором
@router.callback_query(lambda c: c.data.startswith('reject_tournament:'))
async def handle_reject_tournament(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = callback.data.split(':')
    if len(data) != 2:
        await callback.answer("Невірний формат даних.", show_alert=True)
        return

    action, tournament_id_str = data
    try:
        tournament_id = int(tournament_id_str)
    except ValueError:
        await callback.answer("Невірний ID турніру.", show_alert=True)
        return

    tournament = pending_tournaments.get(tournament_id)
    if not tournament:
        await callback.answer("Турнір не знайдено або вже відхилено.", show_alert=True)
        return

    # Тут можна додати логіку відхилення турніру
    # Наприклад, відправка повідомлення користувачу про відхилення
    creator_id = tournament["creator_id"]
    del pending_tournaments[tournament_id]

    try:
        await bot.send_message(
            chat_id=creator_id,
            text=f"Ваш турнір **{tournament['name']}** було відхилено адміністратором.",
            parse_mode="Markdown",
            reply_markup=get_tournaments_menu()
        )
    except Exception as e:
        logger.error(f"Не вдалося відправити повідомлення користувачу {creator_id}: {e}")

    # Відповідаємо адміністратору, що турнір відхилено
    await callback.answer("Турнір відхилено.", show_alert=True)

# Обробник для перегляду детальної інформації про турнір (опціонально)
@router.message(MenuStates.VIEW_TOURNAMENTS)
async def handle_view_tournaments_detail(message: Message, state: FSMContext, bot: Bot):
    tournament_id_str = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} переглядає деталі турніру з ID: {tournament_id_str}")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення користувача: {e}")

    try:
        tournament_id = int(tournament_id_str)
    except ValueError:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Невірний формат ID турніру. Будь ласка, введіть числовий ID.",
            reply_markup=get_tournaments_menu()
        )
        await state.set_state(MenuStates.VIEW_TOURNAMENTS)
        return

    tournament = pending_tournaments.get(tournament_id)
    if not tournament:
        # Якщо турнір не знайдений у тимчасовому сховищі, можливо, він підтверджений та збережений у базі даних
        # Тут можна реалізувати логіку пошуку у базі даних
        # Поки що відправимо повідомлення про відсутність турніру
        response_text = f"Турнір з ID {tournament_id} не знайдений."
    else:
        # Відправляємо деталі турніру
        response_text = (
            f"**Турнір:** {tournament['name']}\n"
            f"**Тип:** {tournament['type']}\n"
            f"**Дата та Час:** {tournament['date_time']}\n"
            f"**Опис:** {tournament['description']}\n"
            f"**Умови Участі:** {tournament['conditions']}\n\n"
            f"📋 Зареєструватися на турнір можна за посиланням: [Реєстрація](https://example.com/register)"
        )

    await bot.send_message(
        chat_id=message.chat.id,
        text=response_text,
        parse_mode="Markdown",
        disable_web_page_preview=True,
        reply_markup=get_tournaments_menu()
    )

    # Повертаємо користувача до меню Турнірів
    await state.set_state(MenuStates.TOURNAMENTS_MENU)

# Обробник для невідомих повідомлень
@router.message()
async def unknown_command(message: Message, state: FSMContext, bot: Bot):
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити невідоме повідомлення: {e}")

    # Отримуємо поточний стан
    current_state = await state.get_state()

    # Визначаємо новий текст та клавіатуру залежно від стану
    transitions = {
        MenuStates.MAIN_MENU.state: {
            "new_main_text": UNKNOWN_COMMAND_TEXT,
            "new_main_keyboard": get_main_menu(),
            "new_interactive_text": "Головне меню",
            "new_state": MenuStates.MAIN_MENU
        },
        MenuStates.NAVIGATION_MENU.state: {
            "new_main_text": UNKNOWN_COMMAND_TEXT,
            "new_main_keyboard": get_navigation_menu(),
            "new_interactive_text": "Меню Навігації",
            "new_state": MenuStates.NAVIGATION_MENU
        },
        MenuStates.HEROES_MENU.state: {
            "new_main_text": UNKNOWN_COMMAND_TEXT,
            "new_main_keyboard": get_heroes_menu(),
            "new_interactive_text": "Меню Персонажів",
            "new_state": MenuStates.HEROES_MENU
        },
        MenuStates.HERO_CLASS_MENU.state: {
            "new_main_text": UNKNOWN_COMMAND_TEXT,
            "new_main_keyboard": get_hero_class_menu(),
            "new_interactive_text": f"Меню класу {(await state.get_data()).get('hero_class', 'Танк')}",
            "new_state": MenuStates.HERO_CLASS_MENU
        },
        MenuStates.GUIDES_MENU.state: {
            "new_main_text": UNKNOWN_COMMAND_TEXT,
            "new_main_keyboard": get_guides_menu(),
            "new_interactive_text": "Меню Гайди",
            "new_state": MenuStates.GUIDES_MENU
        },
        MenuStates.COUNTER_PICKS_MENU.state: {
            "new_main_text": UNKNOWN_COMMAND_TEXT,
            "new_main_keyboard": get_counter_picks_menu(),
            "new_interactive_text": "Меню Контр-піки",
            "new_state": MenuStates.COUNTER_PICKS_MENU
        },
        MenuStates.BUILDS_MENU.state: {
            "new_main_text": UNKNOWN_COMMAND_TEXT,
            "new_main_keyboard": get_builds_menu(),
            "new_interactive_text": "Меню Білди",
            "new_state": MenuStates.BUILDS_MENU
        },
        MenuStates.VOTING_MENU.state: {
            "new_main_text": UNKNOWN_COMMAND_TEXT,
            "new_main_keyboard": get_voting_menu(),
            "new_interactive_text": "Меню Голосування",
            "new_state": MenuStates.VOTING_MENU
        },
        MenuStates.PROFILE_MENU.state: {
            "new_main_text": UNKNOWN_COMMAND_TEXT,
            "new_main_keyboard": get_profile_menu_buttons(),
            "new_interactive_text": "Меню Профіль",
            "new_state": MenuStates.PROFILE_MENU
        },
        MenuStates.STATISTICS_MENU.state: {
            "new_main_text": UNKNOWN_COMMAND_TEXT,
            "new_main_keyboard": get_statistics_menu(),
            "new_interactive_text": "Меню Статистика",
            "new_state": MenuStates.STATISTICS_MENU
        },
        MenuStates.ACHIEVEMENTS_MENU.state: {
            "new_main_text": UNKNOWN_COMMAND_TEXT,
            "new_main_keyboard": get_achievements_menu(),
            "new_interactive_text": "Меню Досягнення",
            "new_state": MenuStates.ACHIEVEMENTS_MENU
        },
        MenuStates.SETTINGS_MENU.state: {
            "new_main_text": UNKNOWN_COMMAND_TEXT,
            "new_main_keyboard": get_settings_menu(),
            "new_interactive_text": "Меню Налаштування",
            "new_state": MenuStates.SETTINGS_MENU
        },
        MenuStates.FEEDBACK_MENU.state: {
            "new_main_text": UNKNOWN_COMMAND_TEXT,
            "new_main_keyboard": get_feedback_menu(),
            "new_interactive_text": "Меню Зворотного Зв'язку",
            "new_state": MenuStates.FEEDBACK_MENU
        },
        MenuStates.HELP_MENU.state: {
            "new_main_text": UNKNOWN_COMMAND_TEXT,
            "new_main_keyboard": get_help_menu(),
            "new_interactive_text": "Меню Допомоги",
            "new_state": MenuStates.HELP_MENU
        },
        MenuStates.M6_MENU.state: {
            "new_main_text": UNKNOWN_COMMAND_TEXT,
            "new_main_keyboard": get_m6_menu(),
            "new_interactive_text": "Меню M6",
            "new_state": MenuStates.M6_MENU
        },
        MenuStates.GPT_MENU.state: {
            "new_main_text": UNKNOWN_COMMAND_TEXT,
            "new_main_keyboard": get_gpt_menu(),
            "new_interactive_text": "Меню GPT",
            "new_state": MenuStates.GPT_MENU
        },
        MenuStates.META_MENU.state: {
            "new_main_text": UNKNOWN_COMMAND_TEXT,
            "new_main_keyboard": get_meta_menu(),
            "new_interactive_text": "Меню META",
            "new_state": MenuStates.META_MENU
        },
        MenuStates.TOURNAMENTS_MENU.state: {
            "new_main_text": UNKNOWN_COMMAND_TEXT,
            "new_main_keyboard": get_tournaments_menu(),
            "new_interactive_text": "Меню Турнірів",
            "new_state": MenuStates.TOURNAMENTS_MENU
        }
    }

    transition = transitions.get(current_state)

    if transition:
        if current_state in [
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
            # Оновлюємо меню
            await update_menu(
                message=message,
                state=state,
                bot=bot,
                new_main_text=transition["new_main_text"],
                new_main_keyboard=transition["new_main_keyboard"],
                new_interactive_text=transition["new_interactive_text"],
                new_state=transition["new_state"]
            )
    else:
        # Якщо стан невідомий, повертаємося до головного меню
        user_first_name = message.from_user.first_name
        new_main_text = MAIN_MENU_TEXT.format(user_first_name=user_first_name)
        new_main_keyboard = get_main_menu()
        new_interactive_text = MAIN_MENU_DESCRIPTION
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

# Обробник для створення турніру (можливо, додатковий)
# Вже обробляється у handle_create_tournament

# Обробник для перегляду турнірів
# Вже обробляється у handle_view_tournaments

# Обробник для підтвердження турніру адміністратором
# Вже обробляється раніше

# Обробник для відхилення турніру адміністратором
# Вже обробляється раніше

# Обробник для перегляду детальної інформації про турнір
# Вже обробляється раніше

# Обробник для невідомих повідомлень
# Вже обробляється раніше
