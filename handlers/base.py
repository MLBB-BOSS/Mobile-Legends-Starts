# handlers/base.py

import logging
from aiogram import Router, types, Bot
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
from keyboards.inline_menus import get_generic_inline_keyboard

from handlers.utils import handle_menu_transition  # Імпортуємо функцію

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

# Команда /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    user_name = message.from_user.first_name
    logger.info(f"Користувач {message.from_user.id} викликав /start")

    # Видаляємо повідомлення користувача /start
    await message.delete()

    # Відправляємо повідомлення про завантаження
    loading_message = await bot.send_message(
        chat_id=message.chat.id,
        text="🔄 Завантаження даних..."
    )

    # Імітуємо завантаження даних
    await asyncio.sleep(2)

    # Видаляємо повідомлення про завантаження
    await loading_message.delete()

    # Встановлюємо стан користувача
    await state.set_state(MenuStates.MAIN_MENU)

    # Відправляємо повідомлення з текстом і клавіатурою (Повідомлення 1)
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=(
            f"👋 Вітаємо, {user_name}, у Mobile Legends Tournament Bot!\n\n"
            "Оберіть опцію з меню нижче 👇"
        ),
        reply_markup=get_main_menu()
    )

    # Зберігаємо ID повідомлення бота (Повідомлення 1)
    await state.update_data(bot_message_id=main_message.message_id)

    # Відправляємо інтерактивне повідомлення з інлайн-кнопками (Повідомлення 2)
    interactive_message = await bot.send_message(
        chat_id=message.chat.id,
        text=(
            "🎮 Цей бот допоможе вам:\n"
            "• Організовувати турніри\n"
            "• Зберігати скріншоти персонажів\n"
            "• Відстежувати активність\n"
            "• Отримувати досягнення"
        ),
        reply_markup=get_generic_inline_keyboard()
    )

    # Зберігаємо ID інтерактивного повідомлення (Повідомлення 2)
    await state.update_data(interactive_message_id=interactive_message.message_id)

# Обробник натискання кнопок у головному меню
@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} у головному меню")

    if user_choice == MenuButton.NAVIGATION.value:
        new_state = MenuStates.NAVIGATION_MENU
        new_main_text = "🧭 **Навігація**\nОберіть розділ для подальших дій:"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Навігаційний екран"
    elif user_choice == MenuButton.PROFILE.value:
        new_state = MenuStates.PROFILE_MENU
        new_main_text = "🪪 **Мій Профіль**\nОберіть опцію для перегляду:"
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "Профіль користувача"
    else:
        new_state = MenuStates.MAIN_MENU
        new_main_text = "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче."
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Невідома команда"

    await handle_menu_transition(
        message, state, bot, new_state,
        new_main_text, new_main_keyboard, new_interactive_text
    )

# Аналогічно оновіть інші обробники, використовуючи функцію handle_menu_transition

# Приклад для MenuStates.NAVIGATION_MENU
@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Навігація")

    if user_choice == MenuButton.HEROES.value:
        new_state = MenuStates.HEROES_MENU
        new_main_text = "🥷 **Персонажі**\nОберіть категорію героїв:"
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = "Список категорій героїв"
    elif user_choice == MenuButton.GUIDES.value:
        new_state = MenuStates.GUIDES_MENU
        new_main_text = "📚 **Гайди**\nВиберіть підрозділ гайдів:"
        new_main_keyboard = get_guides_menu()
        new_interactive_text = "Список гайдів"
    # Додайте інші варіанти

    elif user_choice == MenuButton.BACK.value:
        new_state = MenuStates.MAIN_MENU
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
    else:
        new_state = MenuStates.NAVIGATION_MENU
        new_main_text = "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче."
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Невідома команда"

    await handle_menu_transition(
        message, state, bot, new_state,
        new_main_text, new_main_keyboard, new_interactive_text
    )

# Оновіть інші обробники аналогічним чином

# Обробник для інлайн-кнопок
@router.callback_query()
async def handle_inline_buttons(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = callback.data
    logger.info(f"Користувач {callback.from_user.id} натиснув інлайн-кнопку: {data}")

    # Отримуємо interactive_message_id з стану
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if interactive_message_id:
        if data == "button1":
            await bot.answer_callback_query(callback.id, text="Ви натиснули кнопку 1")
        elif data == "button2":
            await bot.answer_callback_query(callback.id, text="Ви натиснули кнопку 2")
        elif data == "menu_back":
            # Повернення до головного меню
            new_state = MenuStates.MAIN_MENU
            new_main_text = (
                f"👋 Вітаємо, {callback.from_user.first_name}, у Mobile Legends Tournament Bot!\n\n"
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
            await handle_menu_transition(
                callback, state, bot, new_state,
                new_main_text, new_main_keyboard, new_interactive_text
            )
        # Додайте обробку інших інлайн-кнопок за потребою
    else:
        logger.error("interactive_message_id не знайдено")
        await bot.answer_callback_query(callback.id, text="Сталася помилка")

# Обробник для невідомих повідомлень
@router.message()
async def unknown_command(message: Message, state: FSMContext, bot: Bot):
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")

    # Визначаємо поточний стан
    current_state = await state.get_state()

    if current_state == MenuStates.MAIN_MENU.state:
        new_state = MenuStates.MAIN_MENU
        new_main_text = "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче."
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Головне меню"
    elif current_state == MenuStates.NAVIGATION_MENU.state:
        new_state = MenuStates.NAVIGATION_MENU
        new_main_text = "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче."
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Навігаційний екран"
    else:
        new_state = MenuStates.MAIN_MENU
        new_main_text = "❗ Вибачте, я не розумію цю команду. Повертаємось до головного меню."
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Головне меню"

    await handle_menu_transition(
        message, state, bot, new_state,
        new_main_text, new_main_keyboard, new_interactive_text
    )

# Функція для налаштування обробників
def setup_handlers(dp):
    dp.include_router(router)
