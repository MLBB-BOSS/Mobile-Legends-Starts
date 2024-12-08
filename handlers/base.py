# handlers/base.py

import logging
from aiogram import Router, Bot
from aiogram.filters import Command, Text
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

# Імпорт клавіатур
from keyboards.menus import (
    get_main_menu,
    get_navigation_menu,
    get_characters_menu,
    get_builds_menu,
    get_counter_picks_menu,
    get_guides_menu,
    get_voting_menu,
    get_m6_menu,
    get_gpt_menu,
    get_meta_menu,
    get_profile_menu,
    get_statistics_menu,
    get_achievements_menu,
    get_settings_menu,
    get_feedback_menu,
    get_help_menu,
    get_generic_inline_keyboard,
    get_character_inline_keyboard,
    get_guide_inline_keyboard
)

# Імпорт текстів
from keyboards.menus import (
    MainMenuButtons,
    NavigationMenuButtons,
    CharactersMenuButtons,
    BuildsMenuButtons,
    CounterPicksMenuButtons,
    GuidesMenuButtons,
    VotingMenuButtons,
    M6MenuButtons,
    GPTMenuButtons,
    MetaMenuButtons,
    ProfileMenuButtons,
    StatisticsMenuButtons,
    AchievementsMenuButtons,
    SettingsMenuButtons,
    FeedbackMenuButtons,
    HelpMenuButtons,
    InlineMenuButtons
)

# Імпорт GPT інтеграції
from gpt_integration import get_gpt_response

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = Router()


# Визначаємо стани меню
class MenuStates(StatesGroup):
    MAIN_MENU = State()
    NAVIGATION_MENU = State()
    CHARACTERS_MENU = State()
    BUILDS_MENU = State()
    COUNTER_PICKS_MENU = State()
    GUIDES_MENU = State()
    VOTING_MENU = State()
    M6_MENU = State()
    GPT_MENU = State()
    META_MENU = State()
    PROFILE_MENU = State()
    STATISTICS_MENU = State()
    ACHIEVEMENTS_MENU = State()
    SETTINGS_MENU = State()
    FEEDBACK_MENU = State()
    HELP_MENU = State()
    CHARACTER_VIEW = State()
    GUIDE_VIEW = State()
    GPT_ASK_QUESTION = State()
    SEARCH_HERO = State()


# Команда /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    user_first_name = message.from_user.first_name
    logger.info(f"Користувач {message.from_user.id} викликав /start")

    # Видаляємо повідомлення користувача /start
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення: {e}")

    # Відправляємо головне меню з клавіатурою
    main_menu_text = f"Привіт, {user_first_name}! Виберіть розділ нижче:"
    main_menu_message = await bot.send_message(
        chat_id=message.chat.id,
        text=main_menu_text,
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )

    # Відправляємо інтерактивне повідомлення
    interactive_text = "Це головний екран вашого бота. Використовуйте кнопки для навігації."
    interactive_message = await bot.send_message(
        chat_id=message.chat.id,
        text=interactive_text,
        reply_markup=get_generic_inline_keyboard(),
        parse_mode="HTML"
    )

    # Зберігаємо ID повідомлень
    await state.update_data(
        bot_message_id=main_menu_message.message_id,
        interactive_message_id=interactive_message.message_id
    )

    # Встановлюємо стан користувача на MAIN_MENU
    await state.set_state(MenuStates.MAIN_MENU)


# Обробник кнопок головного меню
@router.message(MenuStates.MAIN_MENU, Text(equals=[button.value for button in MainMenuButtons]))
async def handle_main_menu(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в головному меню")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення: {e}")

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо новий текст та клавіатуру для повідомлень
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice == MainMenuButtons.NAVIGATION.value:
        new_main_text = "🧭 <b>Меню Навігації</b>"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Виберіть розділ Навігації нижче:"
        new_state = MenuStates.NAVIGATION_MENU
    elif user_choice == MainMenuButtons.PROFILE.value:
        new_main_text = "🪪 <b>Меню Профілю</b>"
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "Виберіть розділ Профілю нижче:"
        new_state = MenuStates.PROFILE_MENU
    else:
        # Невідома команда
        new_main_text = "Вибачте, я не розумію цю команду. Будь ласка, використовуйте кнопки нижче."
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Головне меню"
        new_state = MenuStates.MAIN_MENU

    # Відправляємо нове повідомлення з клавіатурою
    new_main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML"
    )
    new_bot_message_id = new_main_message.message_id

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Оновлюємо bot_message_id в стані
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
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        # Якщо не вдалося редагувати, відправляємо нове інтерактивне повідомлення
        new_interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        await state.update_data(interactive_message_id=new_interactive_message.message_id)

    # Оновлюємо стан користувача
    await state.set_state(new_state)


# Обробник кнопок меню Навігації
@router.message(MenuStates.NAVIGATION_MENU, Text(equals=[button.value for button in NavigationMenuButtons]))
async def handle_navigation_menu(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Навігації")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення: {e}")

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice == NavigationMenuButtons.CHARACTERS.value:
        new_main_text = "🥷 <b>Меню Персонажів</b>"
        new_main_keyboard = get_characters_menu()
        new_interactive_text = "Виберіть клас персонажа нижче:"
        new_state = MenuStates.CHARACTERS_MENU
    elif user_choice == NavigationMenuButtons.BUILDS.value:
        new_main_text = "🛡️ <b>Меню Білд</b>"
        new_main_keyboard = get_builds_menu()
        new_interactive_text = "Виберіть дію з білдами нижче:"
        new_state = MenuStates.BUILDS_MENU
    elif user_choice == NavigationMenuButtons.COUNTER_PICKS.value:
        new_main_text = "⚖️ <b>Меню Контр-піків</b>"
        new_main_keyboard = get_counter_picks_menu()
        new_interactive_text = "Виберіть дію з контр-піками нижче:"
        new_state = MenuStates.COUNTER_PICKS_MENU
    elif user_choice == NavigationMenuButtons.GUIDES.value:
        new_main_text = "📚 <b>Меню Гайдів</b>"
        new_main_keyboard = get_guides_menu()
        new_interactive_text = "Виберіть тип гайду нижче:"
        new_state = MenuStates.GUIDES_MENU
    elif user_choice == NavigationMenuButtons.VOTING.value:
        new_main_text = "📊 <b>Меню Голосування</b>"
        new_main_keyboard = get_voting_menu()
        new_interactive_text = "Виберіть дію з голосуваннями нижче:"
        new_state = MenuStates.VOTING_MENU
    elif user_choice == NavigationMenuButtons.M6.value:
        new_main_text = "🏆 <b>Меню M6</b>"
        new_main_keyboard = get_m6_menu()
        new_interactive_text = "Виберіть дію з M6 нижче:"
        new_state = MenuStates.M6_MENU
    elif user_choice == NavigationMenuButtons.GPT.value:
        new_main_text = "👾 <b>Меню GPT</b>"
        new_main_keyboard = get_gpt_menu()
        new_interactive_text = "Виберіть дію з GPT нижче:"
        new_state = MenuStates.GPT_MENU
    elif user_choice == NavigationMenuButtons.META.value:
        new_main_text = "🔥 <b>Меню META</b>"
        new_main_keyboard = get_meta_menu()
        new_interactive_text = "Виберіть дію з META нижче:"
        new_state = MenuStates.META_MENU
    elif user_choice == NavigationMenuButtons.BACK.value:
        # Повертаємось до головного меню
        new_main_text = f"Привіт, {message.from_user.first_name}! Виберіть розділ нижче:"
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Це головний екран вашого бота. Використовуйте кнопки для навігації."
        new_state = MenuStates.MAIN_MENU
    else:
        # Невідома команда
        new_main_text = "Вибачте, я не розумію цю команду. Будь ласка, використовуйте кнопки нижче."
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Меню Навігації"
        new_state = MenuStates.NAVIGATION_MENU

    # Відправляємо нове повідомлення з клавіатурою
    new_main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML"
    )
    new_bot_message_id = new_main_message.message_id

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Оновлюємо bot_message_id в стані
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
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        # Якщо не вдалося редагувати, відправляємо нове інтерактивне повідомлення
        new_interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        await state.update_data(interactive_message_id=new_interactive_message.message_id)

    # Оновлюємо стан користувача
    await state.set_state(new_state)


# Обробник кнопок меню Профілю
@router.message(MenuStates.PROFILE_MENU, Text(equals=[button.value for button in ProfileMenuButtons]))
async def handle_profile_menu(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Профілю")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення: {e}")

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice == ProfileMenuButtons.STATISTICS.value:
        new_main_text = "📈 <b>Меню Статистики</b>"
        new_main_keyboard = get_statistics_menu()
        new_interactive_text = "Виберіть розділ Статистики нижче:"
        new_state = MenuStates.STATISTICS_MENU
    elif user_choice == ProfileMenuButtons.ACHIEVEMENTS.value:
        new_main_text = "🏆 <b>Меню Досягнень</b>"
        new_main_keyboard = get_achievements_menu()
        new_interactive_text = "Виберіть розділ Досягнень нижче:"
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif user_choice == ProfileMenuButtons.SETTINGS.value:
        new_main_text = "⚙️ <b>Меню Налаштувань</b>"
        new_main_keyboard = get_settings_menu()
        new_interactive_text = "Виберіть розділ Налаштувань нижче:"
        new_state = MenuStates.SETTINGS_MENU
    elif user_choice == ProfileMenuButtons.FEEDBACK.value:
        new_main_text = "💌 <b>Меню Зворотного Зв'язку</b>"
        new_main_keyboard = get_feedback_menu()
        new_interactive_text = "Виберіть дію зі зворотного зв'язку нижче:"
        new_state = MenuStates.FEEDBACK_MENU
    elif user_choice == ProfileMenuButtons.HELP.value:
        new_main_text = "❓ <b>Меню Допомоги</b>"
        new_main_keyboard = get_help_menu()
        new_interactive_text = "Виберіть розділ Допомоги нижче:"
        new_state = MenuStates.HELP_MENU
    elif user_choice == ProfileMenuButtons.BACK_TO_MAIN.value:
        # Повертаємось до головного меню
        new_main_text = f"Привіт, {message.from_user.first_name}! Виберіть розділ нижче:"
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Це головний екран вашого бота. Використовуйте кнопки для навігації."
        new_state = MenuStates.MAIN_MENU
    else:
        # Невідома команда
        new_main_text = "Вибачте, я не розумію цю команду. Будь ласка, використовуйте кнопки нижче."
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "Меню Профілю"
        new_state = MenuStates.PROFILE_MENU

    # Відправляємо нове повідомлення з клавіатурою
    new_main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML"
    )
    new_bot_message_id = new_main_message.message_id

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Оновлюємо bot_message_id в стані
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
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        # Якщо не вдалося редагувати, відправляємо нове інтерактивне повідомлення
        new_interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        await state.update_data(interactive_message_id=new_interactive_message.message_id)

    # Оновлюємо стан користувача
    await state.set_state(new_state)


# Обробник кнопок меню Персонажів
@router.message(MenuStates.CHARACTERS_MENU, Text(equals=[button.value for button in CharactersMenuButtons]))
async def handle_characters_menu(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Персонажів")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення: {e}")

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice == CharactersMenuButtons.COMPARISON.value:
        # Обробка порівняння героїв
        comparison_text = "⚖️ Функція порівняння героїв ще в розробці."
        new_main_text = comparison_text
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = comparison_text
        new_state = MenuStates.CHARACTER_VIEW  # Можливо, окремий стан
    elif user_choice == CharactersMenuButtons.SEARCH_HERO.value:
        # Обробка пошуку героя
        search_text = "🔎 Введіть ім'я героя для пошуку:"
        new_main_text = search_text
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = search_text
        new_state = MenuStates.SEARCH_HERO
    elif user_choice == CharactersMenuButtons.BACK.value:
        # Повернення до меню Навігації
        new_main_text = "🧭 <b>Меню Навігації</b>"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Виберіть розділ Навігації нижче:"
        new_state = MenuStates.NAVIGATION_MENU
    else:
        # Вибір класу персонажа
        selected_class = user_choice.replace("🥷 ", "").replace("🛡️ ", "").replace("🧙‍♂️ ", "").replace("🏹 ", "").replace("⚔️ ", "").replace("❤️ ", "").replace("🗡️ ", "")
        logger.info(f"Вибрано клас персонажа: {selected_class}")

        # Припустимо, у вас є словник класів та відповідних героїв
        heroes_by_class = {
            "Танк": ["Alice", "Tigreal", "Akai", "Franco", "Minotaur", "Lolia", "Gatotkaca", "Grock", "Hylos", "Uranus", "Belerick", "Khufra", "Esmeralda", "Terizla", "Baxia", "Masha", "Atlas", "Barats", "Edith", "Fredrinn", "Johnson", "Hilda", "Carmilla", "Gloo", "Chip"],
            "Маг": ["Маг 1", "Маг 2"],  # Додайте реальних героїв
            "Стрілець": ["Стрілець 1", "Стрілець 2"],  # Додайте реальних героїв
            "Асасін": ["Асасін 1", "Асасін 2"],  # Додайте реальних героїв
            "Підтримка": ["Підтримка 1", "Підтримка 2"],  # Додайте реальних героїв
            "Боєць": ["Боєць 1", "Боєць 2"],  # Додайте реальних героїв
        }

        heroes = heroes_by_class.get(selected_class, [])

        if heroes:
            # Формуємо клавіатуру з героями
            keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            hero_buttons = [KeyboardButton(text=hero) for hero in heroes]
            keyboard.add(*hero_buttons)
            # Додаємо кнопку назад
            keyboard.add(KeyboardButton(text=CharactersMenuButtons.BACK.value))

            # Відправляємо список героїв
            heroes_text = f"🦸‍♂️ <b>Персонажі класу {selected_class}</b>:\n" + "\n".join(f"• {hero}" for hero in heroes)
            new_main_text = heroes_text
            new_main_keyboard = keyboard
            new_interactive_text = "Виберіть героя для перегляду детальної інформації:"
            new_state = MenuStates.CHARACTER_VIEW
        else:
            # Якщо герої ще не додані
            new_main_text = "Цей клас героїв ще не доданий."
            new_main_keyboard = get_characters_menu()
            new_interactive_text = "Меню Персонажів"
            new_state = MenuStates.CHARACTERS_MENU

    # Відправляємо нове повідомлення з клавіатурою
    new_main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML"
    )
    new_bot_message_id = new_main_message.message_id

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Оновлюємо bot_message_id в стані
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
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        # Якщо не вдалося редагувати, відправляємо нове інтерактивне повідомлення
        new_interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        await state.update_data(interactive_message_id=new_interactive_message.message_id)

    # Оновлюємо стан користувача
    await state.set_state(new_state)


# Обробник кнопок меню Білд
@router.message(MenuStates.BUILDS_MENU, Text(equals=[button.value for button in BuildsMenuButtons]))
async def handle_builds_menu(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Білд")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення: {e}")

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice == BuildsMenuButtons.CREATE_BUILD.value:
        # Обробка створення білда
        create_build_text = "🏗️ <b>Створення Білда</b>\nВведіть деталі вашого білда..."
        new_main_text = create_build_text
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Введіть деталі вашого білда:"
        new_state = MenuStates.CHARACTER_VIEW  # Можливо, окремий стан
    elif user_choice == BuildsMenuButtons.MY_BUILDS.value:
        # Обробка перегляду обраних білдів
        my_builds_text = "📄 <b>Обрані Білди</b>\nВаші збережені білди..."
        new_main_text = my_builds_text
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Ваші обрані білди:"
        new_state = MenuStates.CHARACTER_VIEW  # Можливо, окремий стан
    elif user_choice == BuildsMenuButtons.POPULAR_BUILDS.value:
        # Обробка перегляду популярних білдів
        popular_builds_text = "🔥 <b>Популярні Білди</b>\nНайпопулярніші білди спільноти..."
        new_main_text = popular_builds_text
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Популярні білди:"
        new_state = MenuStates.CHARACTER_VIEW  # Можливо, окремий стан
    elif user_choice == BuildsMenuButtons.BACK.value:
        # Повернення до меню Навігації
        new_main_text = "🧭 <b>Меню Навігації</b>"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Виберіть розділ Навігації нижче:"
        new_state = MenuStates.NAVIGATION_MENU
    else:
        # Невідома команда
        new_main_text = "Вибачте, я не розумію цю команду. Будь ласка, використовуйте кнопки нижче."
        new_main_keyboard = get_builds_menu()
        new_interactive_text = "Меню Білд"
        new_state = MenuStates.BUILDS_MENU

    # Відправляємо нове повідомлення з клавіатурою
    new_main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML"
    )
    new_bot_message_id = new_main_message.message_id

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Оновлюємо bot_message_id в стані
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
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        # Якщо не вдалося редагувати, відправляємо нове інтерактивне повідомлення
        new_interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        await state.update_data(interactive_message_id=new_interactive_message.message_id)

    # Оновлюємо стан користувача
    await state.set_state(new_state)


# Обробник кнопок меню Контр-піків
@router.message(MenuStates.COUNTER_PICKS_MENU, Text(equals=[button.value for button in CounterPicksMenuButtons]))
async def handle_counter_picks_menu(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Контр-піків")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення: {e}")

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice == CounterPicksMenuButtons.COUNTER_SEARCH.value:
        # Обробка пошуку контр-піка
        search_text = "🔎 Введіть ім'я героя для пошуку контр-піка:"
        new_main_text = search_text
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = search_text
        new_state = MenuStates.SEARCH_HERO
    elif user_choice == CounterPicksMenuButtons.COUNTER_LIST.value:
        # Обробка перегляду списку персонажів
        counter_list_text = "📝 <b>Список Персонажів</b>\nОсь список персонажів для контр-піків..."
        new_main_text = counter_list_text
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Список персонажів для контр-піків:"
        new_state = MenuStates.CHARACTER_VIEW  # Можливо, окремий стан
    elif user_choice == CounterPicksMenuButtons.BACK.value:
        # Повернення до меню Навігації
        new_main_text = "🧭 <b>Меню Навігації</b>"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Виберіть розділ Навігації нижче:"
        new_state = MenuStates.NAVIGATION_MENU
    else:
        # Невідома команда
        new_main_text = "Вибачте, я не розумію цю команду. Будь ласка, використовуйте кнопки нижче."
        new_main_keyboard = get_counter_picks_menu()
        new_interactive_text = "Меню Контр-піків"
        new_state = MenuStates.COUNTER_PICKS_MENU

    # Відправляємо нове повідомлення з клавіатурою
    new_main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML"
    )
    new_bot_message_id = new_main_message.message_id

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Оновлюємо bot_message_id в стані
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
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        # Якщо не вдалося редагувати, відправляємо нове інтерактивне повідомлення
        new_interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        await state.update_data(interactive_message_id=new_interactive_message.message_id)

    # Оновлюємо стан користувача
    await state.set_state(new_state)


# Обробник кнопок меню Гайдів
@router.message(MenuStates.GUIDES_MENU, Text(equals=[button.value for button in GuidesMenuButtons]))
async def handle_guides_menu(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Гайдів")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення: {e}")

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_state = None

    if user_choice == GuidesMenuButtons.NEW_GUIDES.value:
        # Обробка нових гайдів
        new_guides_text = "🆕 <b>Нові Гайди</b>\nОсь список нових гайдів..."
        new_main_text = new_guides_text
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Нові гайди:"
        new_state = MenuStates.GUIDE_VIEW
    elif user_choice == GuidesMenuButtons.TOP_GUIDES.value:
        # Обробка топ гайдів
        top_guides_text = "🌟 <b>Топ Гайди</b>\nОсь список топових гайдів..."
        new_main_text = top_guides_text
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Топ гайди:"
        new_state = MenuStates.GUIDE_VIEW
    elif user_choice == GuidesMenuButtons.BEGINNER_GUIDES.value:
        # Обробка гайдів для початківців
        beginner_guides_text = "📘 <b>Гайди для Початківців</b>\nОсь гайди для новачків..."
        new_main_text = beginner_guides_text
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Гайди для Початківців:"
        new_state = MenuStates.GUIDE_VIEW
    elif user_choice == GuidesMenuButtons.ADVANCED_GUIDES.value:
        # Обробка стратегій гри
        advanced_guides_text = "🧙 <b>Стратегії Гри</b>\nОсь стратегічні гайди..."
        new_main_text = advanced_guides_text
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Стратегії Гри:"
        new_state = MenuStates.GUIDE_VIEW
    elif user_choice == GuidesMenuButtons.TEAMPLAY_GUIDES.value:
        # Обробка командної гри
        teamplay_guides_text = "🤝 <b>Командна Гра</b>\nОсь гайди для командної гри..."
        new_main_text = teamplay_guides_text
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Командна Гра:"
        new_state = MenuStates.GUIDE_VIEW
    elif user_choice == GuidesMenuButtons.BACK.value:
        # Повернення до меню Навігації
        new_main_text = "🧭 <b>Меню Навігації</b>"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Виберіть розділ Навігації нижче:"
        new_state = MenuStates.NAVIGATION_MENU
    else:
        # Невідома команда
        new_main_text = "Вибачте, я не розумію цю команду. Будь ласка, використовуйте кнопки нижче."
        new_main_keyboard = get_guides_menu()
        new_interactive_text = "Меню Гайдів"
        new_state = MenuStates.GUIDES_MENU

    # Відправляємо нове повідомлення з клавіатурою
    new_main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML"
    )
    new_bot_message_id = new_main_message.message_id

    # Видаляємо попереднє повідомлення з клавіатурою
    try:
        await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Оновлюємо bot_message_id в стані
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
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        # Якщо не вдалося редагувати, відправляємо нове інтерактивне повідомлення
        new_interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        await state.update_data(interactive_message_id=new_interactive_message.message_id)

    # Оновлюємо стан користувача
    await state.set_state(new_state)


# Обробник інлайн-кнопок
@router.callback_query()
async def handle_inline_buttons(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = callback.data
    logger.info(f"Користувач {callback.from_user.id} натиснув інлайн-кнопку: {data}")

    # Отримуємо interactive_message_id з стану
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if not interactive_message_id:
        logger.error("interactive_message_id не знайдено")
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text="Виникла помилка. Спробуйте ще раз.",
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        await callback.answer()
        return

    # Обробка різних типів інлайн-кнопок
    if data.startswith("guides_"):
        # Отримуємо ID персонажа
        _, character_id = data.split("_")
        character_id = int(character_id)
        # Логіка для показу гайдів персонажа
        guide_info = f"📚 Гайди для персонажа з ID {character_id} ще в розробці."
        # Редагуємо інтерактивне повідомлення
        try:
            await bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=interactive_message_id,
                text=guide_info,
                parse_mode="HTML",
                reply_markup=get_guide_inline_keyboard(character_id)
            )
            await state.set_state(MenuStates.GUIDE_VIEW)
        except Exception as e:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text="Виникла помилка. Спробуйте ще раз.",
                reply_markup=get_generic_inline_keyboard(),
                parse_mode="HTML"
            )
    elif data.startswith("next_"):
        # Навігація до наступного персонажа
        _, current_id = data.split("_")
        next_id = int(current_id) + 1  # Логіка визначення наступного ID

        # Припустимо, що у вас є функція, яка отримує інформацію про персонажа за ID
        # Тут ми використаємо загальний текст для прикладу
        character_info = f"🦸‍♂️ <b>Персонаж:</b> Герой з ID {next_id}\n🆔 <b>ID:</b> {next_id}\nДодаткова інформація..."
        try:
            await bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=interactive_message_id,
                text=character_info,
                parse_mode="HTML",
                reply_markup=get_character_inline_keyboard(next_id)
            )
            await state.set_state(MenuStates.CHARACTER_VIEW)
        except Exception as e:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text="Виникла помилка. Спробуйте ще раз.",
                reply_markup=get_generic_inline_keyboard(),
                parse_mode="HTML"
            )
    elif data.startswith("prev_"):
        # Навігація до попереднього персонажа
        _, current_id = data.split("_")
        prev_id = int(current_id) - 1  # Логіка визначення попереднього ID

        # Припустимо, що у вас є функція, яка отримує інформацію про персонажа за ID
        # Тут ми використаємо загальний текст для прикладу
        character_info = f"🦸‍♂️ <b>Персонаж:</b> Герой з ID {prev_id}\n🆔 <b>ID:</b> {prev_id}\nДодаткова інформація..."
        try:
            await bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=interactive_message_id,
                text=character_info,
                parse_mode="HTML",
                reply_markup=get_character_inline_keyboard(prev_id)
            )
            await state.set_state(MenuStates.CHARACTER_VIEW)
        except Exception as e:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text="Виникла помилка. Спробуйте ще раз.",
                reply_markup=get_generic_inline_keyboard(),
                parse_mode="HTML"
            )
    elif data.startswith("next_guide_"):
        # Навігація до наступного гайду
        _, guide_id = data.split("_guide_")
        next_guide_id = int(guide_id) + 1  # Логіка визначення наступного гайду

        # Припустимо, що у вас є функція, яка отримує інформацію про гайд за ID
        # Тут ми використаємо загальний текст для прикладу
        guide_info = f"📚 <b>Гайд:</b> Гайд з ID {next_guide_id}\n🆔 <b>ID:</b> {next_guide_id}\nДодаткова інформація..."
        try:
            await bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=interactive_message_id,
                text=guide_info,
                parse_mode="HTML",
                reply_markup=get_guide_inline_keyboard(next_guide_id)
            )
            await state.set_state(MenuStates.GUIDE_VIEW)
        except Exception as e:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text="Виникла помилка. Спробуйте ще раз.",
                reply_markup=get_generic_inline_keyboard(),
                parse_mode="HTML"
            )
    elif data == "additional_info":
        # Обробка кнопки Додаткова Інформація
        additional_info = "📄 Додаткова інформація ще в розробці."
        try:
            await bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=interactive_message_id,
                text=additional_info,
                parse_mode="HTML",
                reply_markup=get_generic_inline_keyboard()
            )
        except Exception as e:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text="Виникла помилка. Спробуйте ще раз.",
                reply_markup=get_generic_inline_keyboard(),
                parse_mode="HTML"
            )
    elif data == "back_to_menu":
        # Повернення до головного меню
        user_first_name = callback.from_user.first_name
        main_menu_text = f"Привіт, {user_first_name}! Виберіть розділ нижче:"
        main_menu_message = await bot.send_message(
            chat_id=callback.message.chat.id,
            text=main_menu_text,
            reply_markup=get_main_menu(),
            parse_mode="HTML"
        )
        new_bot_message_id = main_menu_message.message_id

        # Оновлюємо bot_message_id
        await state.update_data(bot_message_id=new_bot_message_id)

        # Редагуємо інтерактивне повідомлення
        new_interactive_text = "Це головний екран вашого бота. Використовуйте кнопки для навігації."
        try:
            await bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=interactive_message_id,
                text=new_interactive_text,
                parse_mode="HTML",
                reply_markup=get_generic_inline_keyboard()
            )
        except Exception as e:
            logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
            # Якщо не вдалося редагувати, відправляємо нове інтерактивне повідомлення
            new_interactive_message = await bot.send_message(
                chat_id=callback.message.chat.id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard(),
                parse_mode="HTML"
            )
            await state.update_data(interactive_message_id=new_interactive_message.message_id)

        # Видаляємо попереднє повідомлення з клавіатурою
        old_bot_message_id = data.get('bot_message_id')
        if old_bot_message_id:
            try:
                await bot.delete_message(chat_id=callback.message.chat.id, message_id=old_bot_message_id)
            except Exception as e:
                logger.error(f"Не вдалося видалити повідомлення бота: {e}")

        # Встановлюємо стан користувача на MAIN_MENU
        await state.set_state(MenuStates.MAIN_MENU)
    else:
        # Обробка інших інлайн-кнопок за потребою
        await bot.answer_callback_query(callback.id, text="Ця кнопка ще не реалізована.")

    await callback.answer()


# Обробник перегляду персонажа
@router.message(MenuStates.CHARACTER_VIEW)
async def handle_character_view(message: Message, state: FSMContext, bot: Bot):
    hero_name = message.text
    logger.info(f"Користувач {message.from_user.id} обрав героя: {hero_name}")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення: {e}")

    # Припустимо, у вас є функція для отримання інформації про героя
    # Наприклад, get_hero_info(hero_name)
    # Тут ми використаємо загальний текст для прикладу
    hero_id = 123  # Замініть на реальний ID героя
    hero_info = f"🦸‍♂️ <b>Персонаж:</b> {hero_name}\n🆔 <b>ID:</b> {hero_id}\nДодаткова інформація про {hero_name}..."

    # Отримуємо interactive_message_id з стану
    data = await state.get_data()
    interactive_message_id = data.get('interactive_message_id')

    # Редагуємо інтерактивне повідомлення з інформацією про героя
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=hero_info,
            parse_mode="HTML",
            reply_markup=get_character_inline_keyboard(hero_id)
        )
        await state.set_state(MenuStates.CHARACTER_VIEW)
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text="Виникла помилка. Спробуйте ще раз.",
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )


# Обробник пошуку героя
@router.message(MenuStates.SEARCH_HERO)
async def handle_search_hero(message: Message, state: FSMContext, bot: Bot):
    hero_name = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} шукає героя: {hero_name}")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення: {e}")

    if not hero_name:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Будь ласка, введіть ім'я героя для пошуку.",
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        return

    # Логіка пошуку героя (можливо, звернення до бази даних)
    # Припустимо, що герой знайдений
    hero_id = 124  # Замініть на реальний ID героя
    hero_info = f"🦸‍♂️ <b>Персонаж:</b> {hero_name}\n🆔 <b>ID:</b> {hero_id}\nДодаткова інформація про {hero_name}..."

    # Редагуємо інтерактивне повідомлення з інформацією про героя
    try:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=state_data := await state.get_data(),
            text=hero_info,
            parse_mode="HTML",
            reply_markup=get_character_inline_keyboard(hero_id)
        )
        await state.set_state(MenuStates.CHARACTER_VIEW)
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        await bot.send_message(
            chat_id=message.chat.id,
            text="Виникла помилка. Спробуйте ще раз.",
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )


# Обробник відправлення відгуку
@router.message(MenuStates.FEEDBACK_MENU, Text(equals=FeedbackMenuButtons.SEND_FEEDBACK.value))
async def handle_send_feedback(message: Message, state: FSMContext, bot: Bot):
    feedback_text = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} надсилає відгук: {feedback_text}")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення: {e}")

    if not feedback_text:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Будь ласка, введіть ваш відгук.",
            reply_markup=get_feedback_menu(),
            parse_mode="HTML"
        )
        return

    # Логіка збереження відгуку (можливо, запис у базу даних або відправка адміністратору)
    # Припустимо, що відгук успішно отримано
    await bot.send_message(
        chat_id=message.chat.id,
        text="Дякуємо за ваш відгук!",
        reply_markup=get_generic_inline_keyboard(),
        parse_mode="HTML"
    )

    # Повертаємо користувача до меню Зворотного Зв'язку
    await state.set_state(MenuStates.FEEDBACK_MENU)


# Обробник звіту про помилку
@router.message(MenuStates.FEEDBACK_MENU, Text(equals=FeedbackMenuButtons.REPORT_BUG.value))
async def handle_report_bug(message: Message, state: FSMContext, bot: Bot):
    bug_report = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} повідомив про помилку: {bug_report}")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення: {e}")

    if not bug_report:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Будь ласка, опишіть помилку, яку ви знайшли.",
            reply_markup=get_feedback_menu(),
            parse_mode="HTML"
        )
        return

    # Логіка обробки звіту про помилку (збереження або відправка адміністратору)
    # Припустимо, що звіт успішно отримано
    await bot.send_message(
        chat_id=message.chat.id,
        text="Дякуємо за ваш звіт про помилку!",
        reply_markup=get_generic_inline_keyboard(),
        parse_mode="HTML"
    )

    # Повертаємо користувача до меню Зворотного Зв'язку
    await state.set_state(MenuStates.FEEDBACK_MENU)


# Обробник генерації даних через GPT
@router.message(MenuStates.GPT_MENU, Text(equals=GPTMenuButtons.GENERATE_DATA.value))
async def handle_gpt_generate_data(message: Message, state: FSMContext, bot: Bot):
    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення: {e}")

    # Відправляємо повідомлення для введення запитання
    prompt_text = "🤖 <b>Генерація Даних</b>\nВведіть ваш запит для генерації даних:"
    await bot.send_message(
        chat_id=message.chat.id,
        text=prompt_text,
        reply_markup=ReplyKeyboardRemove(),
        parse_mode="HTML"
    )

    # Встановлюємо стан для отримання запитання
    await state.set_state(MenuStates.GPT_ASK_QUESTION)


# Обробник отримання запитання для GPT
@router.message(MenuStates.GPT_ASK_QUESTION)
async def handle_gpt_question(message: Message, state: FSMContext, bot: Bot):
    question = message.text.strip()
    logger.info(f"Користувач {message.from_user.id} задав запитання GPT: {question}")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення: {e}")

    if not question:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Будь ласка, введіть ваше запитання.",
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        return

    # Отримуємо відповідь від GPT
    response = await get_gpt_response(question)

    # Відправляємо відповідь
    await bot.send_message(
        chat_id=message.chat.id,
        text=f"<b>Відповідь AI:</b>\n{response}",
        parse_mode="HTML",
        reply_markup=get_generic_inline_keyboard()
    )

    # Повертаємо користувача до меню GPT
    await state.set_state(MenuStates.GPT_MENU)


# Обробник невідомих повідомлень
@router.message()
async def unknown_command(message: Message, state: FSMContext, bot: Bot):
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")

    # Видаляємо повідомлення користувача
    try:
        await message.delete()
    except Exception as e:
        logger.error(f"Не вдалося видалити повідомлення: {e}")

    # Отримуємо поточний стан
    current_state = await state.get_state()
    logger.info(f"Користувач {message.from_user.id} має поточний стан: {current_state}")

    # Визначаємо новий текст та клавіатуру залежно від стану
    if current_state == MenuStates.MAIN_MENU.state:
        new_main_text = "Вибачте, я не розумію цю команду. Будь ласка, використовуйте кнопки нижче."
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Головне меню"
        new_state = MenuStates.MAIN_MENU
    elif current_state == MenuStates.NAVIGATION_MENU.state:
        new_main_text = "Вибачте, я не розумію цю команду. Будь ласка, використовуйте кнопки нижче."
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Меню Навігації"
        new_state = MenuStates.NAVIGATION_MENU
    elif current_state == MenuStates.CHARACTERS_MENU.state:
        new_main_text = "Вибачте, я не розумію цю команду. Будь ласка, використовуйте кнопки нижче."
        new_main_keyboard = get_characters_menu()
        new_interactive_text = "Меню Персонажів"
        new_state = MenuStates.CHARACTERS_MENU
    elif current_state == MenuStates.CHARACTER_VIEW.state:
        new_main_text = "Вибачте, я не розумію цю команду. Будь ласка, використовуйте кнопки нижче."
        new_main_keyboard = get_generic_inline_keyboard()
        new_interactive_text = "Перегляд персонажа"
        new_state = MenuStates.CHARACTER_VIEW
    elif current_state == MenuStates.GUIDE_VIEW.state:
        new_main_text = "Вибачте, я не розумію цю команду. Будь ласка, використовуйте кнопки нижче."
        new_main_keyboard = get_generic_inline_keyboard()
        new_interactive_text = "Перегляд гайду"
        new_state = MenuStates.GUIDE_VIEW
    elif current_state == MenuStates.GPT_ASK_QUESTION.state:
        new_main_text = "Вибачте, я не розумію цю команду. Будь ласка, введіть ваше запитання."
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Введіть ваше запитання для GPT:"
        new_state = MenuStates.GPT_ASK_QUESTION
    elif current_state == MenuStates.SEARCH_HERO.state:
        new_main_text = "Вибачте, я не розумію цю команду. Будь ласка, введіть ім'я героя для пошуку."
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Введіть ім'я героя для пошуку:"
        new_state = MenuStates.SEARCH_HERO
    else:
        # В іншому випадку повертаємось до головного меню
        new_main_text = f"Привіт, {message.from_user.first_name}! Виберіть розділ нижче:"
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Це головний екран вашого бота. Використовуйте кнопки для навігації."
        new_state = MenuStates.MAIN_MENU

    # Відправляємо нове повідомлення
    new_main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard,
        parse_mode="HTML"
    )
    new_bot_message_id = new_main_message.message_id

    # Видаляємо старе повідомлення з клавіатурою, якщо є
    if 'bot_message_id' in data := await state.get_data():
        old_bot_message_id = data.get('bot_message_id')
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=old_bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    # Редагуємо інтерактивне повідомлення
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
        new_interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="HTML"
        )
        await state.update_data(interactive_message_id=new_interactive_message.message_id)

    # Оновлюємо стан користувача
    await state.set_state(new_state)


# Загальний обробник помилок
@router.errors()
async def handle_error(update: object, exception: Exception):
    logger.error(f"Сталася помилка: {exception}")
    # Можна реалізувати повідомлення користувачеві про помилку тут
    # Наприклад, якщо це повідомлення:
    if isinstance(update, CallbackQuery):
        await update.message.answer("Виникла помилка. Спробуйте ще раз.")
    elif isinstance(update, Message):
        await update.answer("Виникла помилка. Спробуйте ще раз.")