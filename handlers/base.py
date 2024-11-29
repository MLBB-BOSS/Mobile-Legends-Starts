# handlers/base.py

import logging
import asyncio
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
    heroes_by_class,
)
from keyboards.inline_menus import get_generic_inline_keyboard, get_welcome_keyboard
from keyboards.reply_menus import get_reply_keyboard

# Налаштування логування
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
router = Router()

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
    
    # Додані стани для привітального процесу
    WELCOME_PAGE_1 = State()
    WELCOME_PAGE_2 = State()
    WELCOME_PAGE_3 = State()

# Команда /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    user_name = message.from_user.first_name
    logger.info(f"Користувач {message.from_user.id} викликав /start")
    
    # Видаляємо повідомлення користувача /start
    await message.delete()
    
    # Встановлюємо стан на першу сторінку привітання
    await state.set_state(MenuStates.WELCOME_PAGE_1)
    
    # Відправляємо першу сторінку привітання з кнопкою "Продовжити"
    welcome_page_1 = await bot.send_message(
        chat_id=message.chat.id,
        text=(
            f"👋 Вітаємо, {user_name}, у **Mobile Legends Tournament Bot**!\n\n"
            "Цей бот створений, щоб покращити ваш ігровий досвід.\n"
            "Натисніть «Продовжити», щоб дізнатися більше."
        ),
        parse_mode="Markdown",
        reply_markup=get_welcome_keyboard(page=1)  # InlineKeyboardMarkup
    )
    
    # Зберігаємо ID повідомлення бота
    await state.update_data(bot_message_id=welcome_page_1.message_id)

# Обробник для інлайн-кнопок привітання
@router.callback_query(F.data.startswith("welcome_"))
async def handle_welcome_buttons(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = callback.data
    logger.info(f"Користувач {callback.from_user.id} натиснув інлайн-кнопку: {data}")
    
    # Отримуємо поточний стан
    current_state = await state.get_state()
    
    # Отримуємо ID повідомлення, яке потрібно редагувати
    state_data = await state.get_data()
    bot_message_id = state_data.get('bot_message_id')
    
    if not bot_message_id:
        logger.error("bot_message_id не знайдено")
        await bot.answer_callback_query(callback.id, text="Сталася помилка. Спробуйте ще раз.")
        return
    
    if data == "welcome_continue_1" and current_state == MenuStates.WELCOME_PAGE_1.state:
        # Перехід до другої сторінки привітання
        await state.set_state(MenuStates.WELCOME_PAGE_2)
        new_text = (
            "🎮 **Mobile Legends Tournament Bot** пропонує вам:\n"
            "• Організовувати турніри\n"
            "• Зберігати скріншоти персонажів\n"
            "• Відстежувати активність\n"
            "• Отримувати досягнення\n\n"
            "Натисніть «Продовжити», щоб дізнатися більше."
        )
        new_keyboard = get_welcome_keyboard(page=2)  # InlineKeyboardMarkup
        
    elif data == "welcome_continue_2" and current_state == MenuStates.WELCOME_PAGE_2.state:
        # Перехід до третьої сторінки привітання
        await state.set_state(MenuStates.WELCOME_PAGE_3)
        new_text = (
            "📊 **Детальна Статистика:** Аналізуйте свій прогрес і покращуйте навички.\n"
            "⚙️ **Стратегії та Білди:** Діляться ідеями та вивчайте стратегії інших гравців.\n"
            "🤝 **Пошук Команди:** Знаходьте однодумців або приєднуйтесь до готових команд.\n"
            "🏆 **Організація Турнірів:** Беріть участь у змаганнях та отримуйте визнання.\n\n"
            "Натисніть «Продовжити», щоб завершити привітання."
        )
        new_keyboard = get_welcome_keyboard(page=3)  # InlineKeyboardMarkup
        
    elif data == "welcome_start" and current_state == MenuStates.WELCOME_PAGE_3.state:
        # Завершення привітального процесу та перехід до головного меню
        await state.set_state(MenuStates.MAIN_MENU)
        new_text = (
            f"👋 Вітаємо, {callback.from_user.first_name}, у **Mobile Legends Tournament Bot**!\n\n"
            "Оберіть опцію з меню нижче 👇"
        )
        new_keyboard = get_main_menu()  # ReplyKeyboardMarkup
        
    else:
        # Невідома кнопка або стан
        logger.error("Невідома кнопка або стан")
        await bot.answer_callback_query(callback.id, text="Сталася помилка. Спробуйте ще раз.")
        return
    
    # Редагування існуючого повідомлення
    try:
        if isinstance(new_keyboard, InlineKeyboardMarkup):
            # Якщо використовуємо InlineKeyboardMarkup
            await bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=bot_message_id,
                text=new_text,
                parse_mode="Markdown",
                reply_markup=new_keyboard
            )
        elif isinstance(new_keyboard, ReplyKeyboardMarkup):
            # Якщо використовуємо ReplyKeyboardMarkup
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text=new_text,
                parse_mode="Markdown",
                reply_markup=new_keyboard
            )
            # Видаляємо старе повідомлення, якщо потрібно
            await bot.delete_message(chat_id=callback.message.chat.id, message_id=bot_message_id)
        
        await bot.answer_callback_query(callback.id)
    except Exception as e:
        logger.error(f"Не вдалося редагувати повідомлення: {e}")
        await bot.answer_callback_query(callback.id, text="Сталася помилка. Спробуйте ще раз.")

# Обробник натискання звичайних кнопок у меню Навігація
@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Навігація")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        # Надсилаємо нове повідомлення з клавіатурою
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text="Щось пішло не так. Почнімо спочатку.",
            reply_markup=get_main_menu()
        )
        # Зберігаємо ID повідомлення бота
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

    # Відправляємо повідомлення про завантаження
    loading_message = await bot.send_message(
        chat_id=message.chat.id,
        text="🔄 Завантаження даних..."
    )

    # Імітуємо завантаження даних
    await asyncio.sleep(1)

    # Видаляємо повідомлення про завантаження
    await loading_message.delete()

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = None

    if user_choice == MenuButton.HEROES.value:
        new_main_text = "🥷 **Персонажі**\nОберіть категорію героїв:"
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = "Список категорій героїв"
        new_state = MenuStates.HEROES_MENU
    elif user_choice == MenuButton.GUIDES.value:
        new_main_text = "📚 **Гайди**\nВиберіть підрозділ гайдів:"
        new_main_keyboard = get_guides_menu()
        new_interactive_text = "Список гайдів"
        new_state = MenuStates.GUIDES_MENU
    elif user_choice == MenuButton.COUNTER_PICKS.value:
        new_main_text = "🔄 **Контр-піки**\nВиберіть опцію контр-піків:"
        new_main_keyboard = get_counter_picks_menu()
        new_interactive_text = "Список контр-піків"
        new_state = MenuStates.COUNTER_PICKS_MENU
    elif user_choice == MenuButton.BUILDS.value:
        new_main_text = "🛠️ **Білди**\nВиберіть опцію білдів:"
        new_main_keyboard = get_builds_menu()
        new_interactive_text = "Список білдів"
        new_state = MenuStates.BUILDS_MENU
    elif user_choice == MenuButton.VOTING.value:
        new_main_text = "🗳️ **Голосування**\nВиберіть опцію голосування:"
        new_main_keyboard = get_voting_menu()
        new_interactive_text = "Список голосувань"
        new_state = MenuStates.VOTING_MENU
    elif user_choice == MenuButton.BACK.value:
        # Повертаємось до головного меню
        new_main_text = (
            f"👋 Вітаємо, {message.from_user.first_name}, у Mobile Legends Tournament Bot!\n\n"
            "Оберіть опцію з меню нижче 👇"
        )
        new_main_keyboard = get_main_menu()
        new_interactive_text = (
            "🎮 Цей бот допоможе вам:\n"
            "• Організовувати турніри\n"
            "• Зберігати скріншоти персонажів\n"
            "• Відстежувати активність\n"
            "• Отримувати досягнення"
        )
        new_state = MenuStates.MAIN_MENU
    else:
        # Невідома команда
        new_main_text = "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче."
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.NAVIGATION_MENU

    # Відправляємо нове повідомлення з клавіатурою (Повідомлення 1)
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    # Зберігаємо новий bot_message_id
    new_bot_message_id = main_message.message_id

    # Додаємо невелику затримку для плавності
    await asyncio.sleep(0.1)

    # Видаляємо попереднє повідомлення з клавіатурою (Після відправки нового)
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
            reply_markup=new_interactive_keyboard
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        # Якщо не вдалося редагувати, відправляємо нове повідомлення
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=new_interactive_keyboard
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    # Оновлюємо стан користувача
    await state.set_state(new_state)

# Обробник натискання звичайних кнопок у меню Персонажі
@router.message(MenuStates.HEROES_MENU)
async def handle_heroes_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Персонажі")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Отримуємо IDs повідомлень з стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    if not bot_message_id or not interactive_message_id:
        logger.error("bot_message_id або interactive_message_id не знайдено")
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text="Щось пішло не так. Почнімо спочатку.",
            reply_markup=get_main_menu()
        )
        await state.update_data(bot_message_id=main_message.message_id)
        await state.set_state(MenuStates.MAIN_MENU)
        return

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
        new_main_text = f"Виберіть героя з класу {hero_class}:"
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = f"Список героїв класу {hero_class}"
        new_state = MenuStates.HERO_CLASS_MENU
        await state.update_data(hero_class=hero_class)
    elif user_choice == MenuButton.SEARCH_HERO.value:
        new_main_text = "Будь ласка, введіть ім'я героя для пошуку:"
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Пошук героя"
        new_state = MenuStates.SEARCH_HERO
    elif user_choice == MenuButton.COMPARISON.value:
        new_main_text = "Функція порівняння героїв ще в розробці."
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = "Порівняння героїв"
        new_state = MenuStates.HEROES_MENU
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🔙 Повернення до меню Навігація:"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Навігаційний екран"
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче."
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

    await asyncio.sleep(0.1)

    # Видаляємо старе повідомлення
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
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Обробник натискання звичайних кнопок у меню Гайди
@router.message(MenuStates.GUIDES_MENU)
async def handle_guides_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Гайди")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Отримуємо дані стану
    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    # Визначаємо новий текст та клавіатуру
    new_main_text = ""
    new_main_keyboard = get_guides_menu()
    new_interactive_text = ""
    new_state = MenuStates.GUIDES_MENU

    if user_choice == MenuButton.NEW_GUIDES.value:
        new_main_text = "Список нових гайдів ще не доступний."
        new_interactive_text = "Нові гайди"
    elif user_choice == MenuButton.POPULAR_GUIDES.value:
        new_main_text = "Список популярних гайдів ще не доступний."
        new_interactive_text = "Популярні гайди"
    elif user_choice == MenuButton.BEGINNER_GUIDES.value:
        new_main_text = "Список гайдів для початківців ще не доступний."
        new_interactive_text = "Гайди для початківців"
    elif user_choice == MenuButton.ADVANCED_TECHNIQUES.value:
        new_main_text = "Список просунутих технік ще не доступний."
        new_interactive_text = "Просунуті техніки"
    elif user_choice == MenuButton.TEAMPLAY_GUIDES.value:
        new_main_text = "Список гайдів по командній грі ще не доступний."
        new_interactive_text = "Командна гра"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🔙 Повернення до меню Навігація:"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Навігаційний екран"
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче."
        new_interactive_text = "Невідома команда"

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    await asyncio.sleep(0.1)

    # Видаляємо старе повідомлення
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
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Обробник натискання звичайних кнопок у меню Контр-піки
@router.message(MenuStates.COUNTER_PICKS_MENU)
async def handle_counter_picks_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Контр-піки")

    # Видаляємо повідомлення користувача
    await message.delete()

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    new_main_text = ""
    new_main_keyboard = get_counter_picks_menu()
    new_interactive_text = ""
    new_state = MenuStates.COUNTER_PICKS_MENU

    if user_choice == MenuButton.COUNTER_SEARCH.value:
        new_main_text = "Введіть ім'я персонажа для пошуку контр-піку:"
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Пошук контр-піку"
        new_state = MenuStates.SEARCH_HERO
    elif user_choice == MenuButton.COUNTER_LIST.value:
        new_main_text = "Список персонажів для контр-піків ще не доступний."
        new_interactive_text = "Список контр-піків"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🔙 Повернення до меню Навігація:"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Навігаційний екран"
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче."
        new_interactive_text = "Невідома команда"

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    await asyncio.sleep(0.1)

    # Видаляємо старе повідомлення
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
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Обробник натискання звичайних кнопок у меню Білди
@router.message(MenuStates.BUILDS_MENU)
async def handle_builds_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Білди")

    # Видаляємо повідомлення користувача
    await message.delete()

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    new_main_text = ""
    new_main_keyboard = get_builds_menu()
    new_interactive_text = ""
    new_state = MenuStates.BUILDS_MENU

    if user_choice == MenuButton.CREATE_BUILD.value:
        new_main_text = "Функція створення білду ще в розробці."
        new_interactive_text = "Створення білду"
    elif user_choice == MenuButton.MY_BUILDS.value:
        new_main_text = "Список ваших білдів ще не доступний."
        new_interactive_text = "Мої білди"
    elif user_choice == MenuButton.POPULAR_BUILDS.value:
        new_main_text = "Список популярних білдів ще не доступний."
        new_interactive_text = "Популярні білди"
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🔙 Повернення до меню Навігація:"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Навігаційний екран"
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче."
        new_interactive_text = "Невідома команда"

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    await asyncio.sleep(0.1)

    # Видаляємо старе повідомлення
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
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Обробник натискання звичайних кнопок у меню Голосування
@router.message(MenuStates.VOTING_MENU)
async def handle_voting_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Голосування")

    # Видаляємо повідомлення користувача
    await message.delete()

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    new_main_text = ""
    new_main_keyboard = get_voting_menu()
    new_interactive_text = ""
    new_state = MenuStates.VOTING_MENU

    if user_choice == MenuButton.CURRENT_VOTES.value:
        new_main_text = "Список поточних опитувань ще не доступний."
        new_interactive_text = "Поточні опитування"
    elif user_choice == MenuButton.MY_VOTES.value:
        new_main_text = "Список ваших голосувань ще не доступний."
        new_interactive_text = "Мої голосування"
    elif user_choice == MenuButton.SUGGEST_TOPIC.value:
        new_main_text = "Будь ласка, введіть тему для пропозиції:"
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Пропозиція теми"
        new_state = MenuStates.SEARCH_HERO  # Можливо, створіть окремий стан для прийому теми
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🔙 Повернення до меню Навігація:"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Навігаційний екран"
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче."
        new_interactive_text = "Невідома команда"

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    await asyncio.sleep(0.1)

    # Видаляємо старе повідомлення
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
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Обробник натискання звичайних кнопок у меню Профіль
@router.message(MenuStates.PROFILE_MENU)
async def handle_profile_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Профіль")

    # Видаляємо повідомлення користувача
    await message.delete()

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    new_main_text = ""
    new_main_keyboard = get_profile_menu()
    new_interactive_text = ""
    new_state = MenuStates.PROFILE_MENU

    if user_choice == MenuButton.STATISTICS.value:
        new_main_text = "Виберіть підрозділ статистики:"
        new_main_keyboard = get_statistics_menu()
        new_interactive_text = "Статистика"
        new_state = MenuStates.STATISTICS_MENU
    elif user_choice == MenuButton.ACHIEVEMENTS.value:
        new_main_text = "Виберіть підрозділ досягнень:"
        new_main_keyboard = get_achievements_menu()
        new_interactive_text = "Досягнення"
        new_state = MenuStates.ACHIEVEMENTS_MENU
    elif user_choice == MenuButton.SETTINGS.value:
        new_main_text = "Виберіть опцію налаштувань:"
        new_main_keyboard = get_settings_menu()
        new_interactive_text = "Налаштування"
        new_state = MenuStates.SETTINGS_MENU
    elif user_choice == MenuButton.FEEDBACK.value:
        new_main_text = "Виберіть опцію зворотного зв'язку:"
        new_main_keyboard = get_feedback_menu()
        new_interactive_text = "Зворотний зв'язок"
        new_state = MenuStates.FEEDBACK_MENU
    elif user_choice == MenuButton.HELP.value:
        new_main_text = "Виберіть опцію допомоги:"
        new_main_keyboard = get_help_menu()
        new_interactive_text = "Допомога"
        new_state = MenuStates.HELP_MENU
    elif user_choice == MenuButton.BACK_TO_MAIN_MENU.value:
        new_main_text = (
            f"👋 Вітаємо, {message.from_user.first_name}, у Mobile Legends Tournament Bot!\n\n"
            "Оберіть опцію з меню нижче 👇"
        )
        new_main_keyboard = get_main_menu()
        new_interactive_text = (
            "🎮 Цей бот допоможе вам:\n"
            "• Організовувати турніри\n"
            "• Зберігати скріншоти персонажів\n"
            "• Відстежувати активність\n"
            "• Отримувати досягнення"
        )
        new_state = MenuStates.MAIN_MENU
    else:
        new_main_text = "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче."
        new_interactive_text = "Невідома команда"

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    await asyncio.sleep(0.1)

    # Видаляємо старе повідомлення
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
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Підрозділи "Статистика"
@router.message(MenuStates.STATISTICS_MENU)
async def handle_statistics_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Статистика")

    # Видаляємо повідомлення користувача
    await message.delete()

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    new_main_text = ""
    new_main_keyboard = get_statistics_menu()
    new_interactive_text = ""
    new_state = MenuStates.STATISTICS_MENU

    if user_choice == MenuButton.ACTIVITY.value:
        new_main_text = "Статистика загальної активності ще не доступна."
        new_interactive_text = "Загальна активність"
    elif user_choice == MenuButton.RANKING.value:
        new_main_text = "Рейтинг ще не доступний."
        new_interactive_text = "Рейтинг"
    elif user_choice == MenuButton.GAME_STATS.value:
        new_main_text = "Ігрова статистика ще не доступна."
        new_interactive_text = "Ігрова статистика"
    elif user_choice == MenuButton.BACK_TO_PROFILE.value:
        new_main_text = "🔙 Повернення до меню Профіль:"
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "Профіль"
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче."
        new_interactive_text = "Невідома команда"

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    await asyncio.sleep(0.1)

    # Видаляємо старе повідомлення
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
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Підрозділи "Досягнення"
@router.message(MenuStates.ACHIEVEMENTS_MENU)
async def handle_achievements_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Досягнення")

    # Видаляємо повідомлення користувача
    await message.delete()

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    new_main_text = ""
    new_main_keyboard = get_achievements_menu()
    new_interactive_text = ""
    new_state = MenuStates.ACHIEVEMENTS_MENU

    if user_choice == MenuButton.BADGES.value:
        new_main_text = "Список ваших бейджів ще не доступний."
        new_interactive_text = "Мої бейджі"
    elif user_choice == MenuButton.PROGRESS.value:
        new_main_text = "Ваш прогрес ще не доступний."
        new_interactive_text = "Прогрес"
    elif user_choice == MenuButton.TOURNAMENT_STATS.value:
        new_main_text = "Турнірна статистика ще не доступна."
        new_interactive_text = "Турнірна статистика"
    elif user_choice == MenuButton.AWARDS.value:
        new_main_text = "Список отриманих нагород ще не доступний."
        new_interactive_text = "Отримані нагороди"
    elif user_choice == MenuButton.BACK_TO_PROFILE.value:
        new_main_text = "🔙 Повернення до меню Профіль:"
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "Профіль"
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче."
        new_interactive_text = "Невідома команда"

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    await asyncio.sleep(0.1)

    # Видаляємо старе повідомлення
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
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Підрозділи "Налаштування"
@router.message(MenuStates.SETTINGS_MENU)
async def handle_settings_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Налаштування")

    # Видаляємо повідомлення користувача
    await message.delete()

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    new_main_text = ""
    new_main_keyboard = get_settings_menu()
    new_interactive_text = ""
    new_state = MenuStates.SETTINGS_MENU

    if user_choice == MenuButton.LANGUAGE.value:
        new_main_text = "Функція зміни мови ще в розробці."
        new_interactive_text = "Мова інтерфейсу"
    elif user_choice == MenuButton.CHANGE_USERNAME.value:
        new_main_text = "Будь ласка, введіть новий Username:"
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Зміна Username"
        new_state = MenuStates.SEARCH_HERO  # Можливо, створіть окремий стан для прийому Username
    elif user_choice == MenuButton.UPDATE_ID.value:
        new_main_text = "Функція оновлення ID ще в розробці."
        new_interactive_text = "Оновити ID гравця"
    elif user_choice == MenuButton.NOTIFICATIONS.value:
        new_main_text = "Функція налаштування сповіщень ще в розробці."
        new_interactive_text = "Сповіщення"
    elif user_choice == MenuButton.BACK_TO_PROFILE.value:
        new_main_text = "🔙 Повернення до меню Профіль:"
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "Профіль"
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче."
        new_interactive_text = "Невідома команда"

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    await asyncio.sleep(0.1)

    # Видаляємо старе повідомлення
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
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Підрозділи "Зворотний Зв'язок"
@router.message(MenuStates.FEEDBACK_MENU)
async def handle_feedback_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Зворотний Зв'язок")

    # Видаляємо повідомлення користувача
    await message.delete()

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    new_main_text = ""
    new_main_keyboard = get_feedback_menu()
    new_interactive_text = ""
    new_state = MenuStates.FEEDBACK_MENU

    if user_choice == MenuButton.SEND_FEEDBACK.value:
        new_main_text = "Будь ласка, введіть ваш відгук:"
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Надіслати відгук"
        new_state = MenuStates.SEARCH_HERO  # Можливо, створіть окремий стан для прийому відгуку
    elif user_choice == MenuButton.REPORT_BUG.value:
        new_main_text = "Будь ласка, опишіть помилку, яку ви знайшли:"
        new_main_keyboard = ReplyKeyboardRemove()
        new_interactive_text = "Повідомити про помилку"
        new_state = MenuStates.SEARCH_HERO  # Можливо, створіть окремий стан для прийому звіту
    elif user_choice == MenuButton.BACK_TO_PROFILE.value:
        new_main_text = "🔙 Повернення до меню Профіль:"
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "Профіль"
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче."
        new_interactive_text = "Невідома команда"

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    await asyncio.sleep(0.1)

    # Видаляємо старе повідомлення
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
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Підрозділи "Допомога"
@router.message(MenuStates.HELP_MENU)
async def handle_help_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Допомога")

    # Видаляємо повідомлення користувача
    await message.delete()

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')

    new_main_text = ""
    new_main_keyboard = get_help_menu()
    new_interactive_text = ""
    new_state = MenuStates.HELP_MENU

    if user_choice == MenuButton.INSTRUCTIONS.value:
        new_main_text = "Інструкції ще не доступні."
        new_interactive_text = "Інструкції"
    elif user_choice == MenuButton.FAQ.value:
        new_main_text = "FAQ ще не доступне."
        new_interactive_text = "FAQ"
    elif user_choice == MenuButton.HELP_SUPPORT.value:
        new_main_text = "Зв'яжіться з підтримкою через наш канал або електронну пошту."
        new_interactive_text = "Підтримка"
    elif user_choice == MenuButton.BACK_TO_PROFILE.value:
        new_main_text = "🔙 Повернення до меню Профіль:"
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "Профіль"
        new_state = MenuStates.PROFILE_MENU
    else:
        new_main_text = "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче."
        new_interactive_text = "Невідома команда"

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    await asyncio.sleep(0.1)

    # Видаляємо старе повідомлення
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
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        interactive_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_interactive_text,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    await state.set_state(new_state)

# Обробник для інлайн-кнопок
@router.callback_query()
async def handle_inline_buttons(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = callback.data
    logger.info(f"Користувач {callback.from_user.id} натиснув інлайн-кнопку: {data}")

    # Отримуємо interactive_message_id з стану
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if interactive_message_id:
        # Обробляємо інлайн-кнопки
        if data == "button1":
            await bot.answer_callback_query(callback.id, text="Ви натиснули кнопку 1")
        elif data == "button2":
            await bot.answer_callback_query(callback.id, text="Ви натиснули кнопку 2")
        elif data == "menu_back":
            # Повернення до головного меню
            await state.set_state(MenuStates.MAIN_MENU)
            new_interactive_text = (
                "🎮 Цей бот допоможе вам:\n"
                "• Організовувати турніри\n"
                "• Зберігати скріншоти персонажів\n"
                "• Відстежувати активність\n"
                "• Отримувати досягнення"
            )
            new_interactive_keyboard = get_generic_inline_keyboard()

            # Редагуємо інтерактивне повідомлення
            try:
                await bot.edit_message_text(
                    chat_id=callback.message.chat.id,
                    message_id=interactive_message_id,
                    text=new_interactive_text,
                    reply_markup=new_interactive_keyboard
                )
            except Exception as e:
                logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")

            # Відправляємо головне меню
            main_message = await bot.send_message(
                chat_id=callback.message.chat.id,
                text=(
                    f"👋 Вітаємо, {callback.from_user.first_name}, у Mobile Legends Tournament Bot!\n\n"
                    "Оберіть опцію з меню нижче 👇"
                ),
                reply_markup=get_main_menu()
            )
            # Оновлюємо bot_message_id
            await state.update_data(bot_message_id=main_message.message_id)

            # Видаляємо попереднє повідомлення з клавіатурою
            data = await state.get_data()
            old_bot_message_id = data.get('bot_message_id')
            if old_bot_message_id:
                try:
                    await bot.delete_message(chat_id=callback.message.chat.id, message_id=old_bot_message_id)
                except Exception as e:
                    logger.error(f"Не вдалося видалити повідомлення бота: {e}")
        # Додайте обробку інших інлайн-кнопок за потребою
    else:
        logger.error("interactive_message_id не знайдено")
        await bot.answer_callback_query(callback.id, text="Сталася помилка")

    await callback.answer()

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
        new_main_text = "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче."
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Головне меню"
        new_state = MenuStates.MAIN_MENU
    elif current_state == MenuStates.NAVIGATION_MENU.state:
        new_main_text = "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче."
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Навігаційний екран"
        new_state = MenuStates.NAVIGATION_MENU
    # Додайте перевірки для інших станів
    else:
        new_main_text = "❗ Вибачте, я не розумію цю команду. Повертаємось до головного меню."
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Головне меню"
        new_state = MenuStates.MAIN_MENU

    # Відправляємо нове повідомлення
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

    await asyncio.sleep(0.1)

    # Видаляємо старе повідомлення
    if bot_message_id:
        try:
            await bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
        except Exception as e:
            logger.error(f"Не вдалося видалити повідомлення бота: {e}")

    await state.update_data(bot_message_id=new_bot_message_id)

    # Редагуємо інтерактивне повідомлення
    if interactive_message_id:
        try:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=interactive_message_id,
                text=new_interactive_text,
                reply_markup=get_generic_inline_keyboard()
            )
        except Exception as e:
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

# Функція для налаштування обробників
def setup_handlers(dp: Dispatcher):
    dp.include_router(router)
    # Додайте інші маршрути, якщо є
