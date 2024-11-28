# handlers/base.py

import logging
import asyncio
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
from keyboards.inline_menus import get_generic_inline_keyboard

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

    # Відправляємо інтерактивне повідомлення з інлайн-кнопками
    interactive_message = await bot.send_message(
        chat_id=message.chat.id,
        text=(
            f"👋 Вітаємо, {user_name}, у Mobile Legends Tournament Bot!\n\n"
            "🎮 Цей бот допоможе вам:\n"
            "• Організовувати турніри\n"
            "• Зберігати скріншоти персонажів\n"
            "• Відстежувати активність\n"
            "• Отримувати досягнення\n\n"
            "Оберіть опцію з меню нижче 👇"
        ),
        reply_markup=get_generic_inline_keyboard()
    )

    # Зберігаємо ID інтерактивного повідомлення в стані
    await state.update_data(interactive_message_id=interactive_message.message_id)

    # Відправляємо звичайну клавіатуру
    keyboard_message = await bot.send_message(
        chat_id=message.chat.id,
        text="Оберіть опцію з меню нижче 👇",
        reply_markup=get_main_menu()
    )

    # Зберігаємо ID повідомлення з клавіатурою
    await state.update_data(last_keyboard_message_id=keyboard_message.message_id)

# Функція для видалення попередньої клавіатури
async def delete_last_keyboard_message(state: FSMContext, chat_id: int, bot: Bot):
    data = await state.get_data()
    last_keyboard_message_id = data.get('last_keyboard_message_id')
    if last_keyboard_message_id:
        try:
            await bot.delete_message(chat_id=chat_id, message_id=last_keyboard_message_id)
        except:
            pass  # Ігноруємо помилки

# Обробник натискання звичайних кнопок у головному меню
@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} у головному меню")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Видаляємо попереднє повідомлення з клавіатурою
    await delete_last_keyboard_message(state, message.chat.id, bot)

    # Відправляємо повідомлення про завантаження
    loading_message = await bot.send_message(
        chat_id=message.chat.id,
        text="🔄 Завантаження даних..."
    )

    # Імітуємо завантаження даних
    await asyncio.sleep(1)

    # Видаляємо повідомлення про завантаження
    await loading_message.delete()

    # Отримуємо interactive_message_id з стану
    data = await state.get_data()
    interactive_message_id = data.get('interactive_message_id')

    # Оновлюємо текст інтерактивного повідомлення
    if interactive_message_id:
        new_text = ""

        if user_choice == MenuButton.NAVIGATION.value:
            new_text = "🧭 **Навігація**\nОберіть розділ для подальших дій:"
            new_keyboard = get_navigation_menu()
            await state.set_state(MenuStates.NAVIGATION_MENU)
        elif user_choice == MenuButton.PROFILE.value:
            new_text = "🪪 **Мій Профіль**\nОберіть опцію для перегляду:"
            new_keyboard = get_profile_menu()
            await state.set_state(MenuStates.PROFILE_MENU)
        else:
            logger.warning("Невідома опція меню")
            return

        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_text,
            reply_markup=get_generic_inline_keyboard()
        )

        # Відправляємо оновлену клавіатуру
        keyboard_message = await bot.send_message(
            chat_id=message.chat.id,
            text="",
            reply_markup=new_keyboard
        )

        # Зберігаємо ID повідомлення з клавіатурою
        await state.update_data(last_keyboard_message_id=keyboard_message.message_id)
    else:
        logger.error("interactive_message_id не знайдено")

# Обробник натискання звичайних кнопок у меню Навігація
@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Навігація")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Видаляємо попереднє повідомлення з клавіатурою
    await delete_last_keyboard_message(state, message.chat.id, bot)

    # Відправляємо повідомлення про завантаження
    loading_message = await bot.send_message(
        chat_id=message.chat.id,
        text="🔄 Завантаження даних..."
    )

    # Імітуємо завантаження даних
    await asyncio.sleep(1)

    # Видаляємо повідомлення про завантаження
    await loading_message.delete()

    # Отримуємо interactive_message_id з стану
    data = await state.get_data()
    interactive_message_id = data.get('interactive_message_id')

    if interactive_message_id:
        new_text = ""

        if user_choice == MenuButton.HEROES.value:
            new_text = "🥷 **Персонажі**\nОберіть категорію героїв:"
            new_keyboard = get_heroes_menu()
            await state.set_state(MenuStates.HEROES_MENU)
        elif user_choice == MenuButton.GUIDES.value:
            new_text = "📚 **Гайди**\nВиберіть підрозділ гайдів:"
            new_keyboard = get_guides_menu()
            await state.set_state(MenuStates.GUIDES_MENU)
        elif user_choice == MenuButton.COUNTER_PICKS.value:
            new_text = "🔄 **Контр-піки**\nВиберіть опцію контр-піків:"
            new_keyboard = get_counter_picks_menu()
            await state.set_state(MenuStates.COUNTER_PICKS_MENU)
        elif user_choice == MenuButton.BUILDS.value:
            new_text = "🛠️ **Білди**\nВиберіть опцію білдів:"
            new_keyboard = get_builds_menu()
            await state.set_state(MenuStates.BUILDS_MENU)
        elif user_choice == MenuButton.VOTING.value:
            new_text = "🗳️ **Голосування**\nВиберіть опцію голосування:"
            new_keyboard = get_voting_menu()
            await state.set_state(MenuStates.VOTING_MENU)
        elif user_choice == MenuButton.BACK.value:
            # Повертаємось до головного меню
            new_text = (
                f"👋 Вітаємо, {message.from_user.first_name}, у Mobile Legends Tournament Bot!\n\n"
                "🎮 Цей бот допоможе вам:\n"
                "• Організовувати турніри\n"
                "• Зберігати скріншоти персонажів\n"
                "• Відстежувати активність\n"
                "• Отримувати досягнення\n\n"
                "Оберіть опцію з меню нижче 👇"
            )
            new_keyboard = get_main_menu()
            await state.set_state(MenuStates.MAIN_MENU)
        else:
            logger.warning("Невідома опція меню")
            return

        # Оновлюємо інтерактивне повідомлення
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_text,
            reply_markup=get_generic_inline_keyboard()
        )

        # Відправляємо нову клавіатуру
        keyboard_message = await bot.send_message(
            chat_id=message.chat.id,
            text="",
            reply_markup=new_keyboard
        )

        # Зберігаємо ID повідомлення з клавіатурою
        await state.update_data(last_keyboard_message_id=keyboard_message.message_id)
    else:
        logger.error("interactive_message_id не знайдено")

# Обробник натискання звичайних кнопок у меню Персонажі
@router.message(MenuStates.HEROES_MENU)
async def handle_heroes_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню Персонажі")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Видаляємо попереднє повідомлення з клавіатурою
    await delete_last_keyboard_message(state, message.chat.id, bot)

    # Відправляємо повідомлення про завантаження
    loading_message = await bot.send_message(
        chat_id=message.chat.id,
        text="🔄 Завантаження даних..."
    )

    # Імітуємо завантаження даних
    await asyncio.sleep(1)

    # Видаляємо повідомлення про завантаження
    await loading_message.delete()

    # Отримуємо interactive_message_id з стану
    data = await state.get_data()
    interactive_message_id = data.get('interactive_message_id')

    hero_classes = [MenuButton.TANK.value, MenuButton.MAGE.value, MenuButton.MARKSMAN.value,
                    MenuButton.ASSASSIN.value, MenuButton.SUPPORT.value, MenuButton.FIGHTER.value]

    if interactive_message_id:
        new_text = ""

        if user_choice in hero_classes:
            hero_class = menu_button_to_class.get(user_choice)
            new_text = f"🥷 **{hero_class}**\nВиберіть героя з класу {hero_class}:"
            new_keyboard = get_hero_class_menu(hero_class)
            await state.set_state(MenuStates.HERO_CLASS_MENU)
            await state.update_data(hero_class=hero_class)
        elif user_choice == MenuButton.SEARCH_HERO.value:
            new_text = "🔎 **Пошук Персонажа**\nБудь ласка, введіть ім'я героя для пошуку:"
            new_keyboard = None  # Немає клавіатури
            await state.set_state(MenuStates.SEARCH_HERO)
        elif user_choice == MenuButton.COMPARISON.value:
            new_text = "⚖️ **Порівняння**\nФункція порівняння героїв ще в розробці."
            new_keyboard = get_heroes_menu()
            # Залишаємося в HEROES_MENU
        elif user_choice == MenuButton.BACK.value:
            # Повертаємось до NAVIGATION_MENU
            new_text = "🧭 **Навігація**\nОберіть розділ для подальших дій:"
            new_keyboard = get_navigation_menu()
            await state.set_state(MenuStates.NAVIGATION_MENU)
        else:
            logger.warning("Невідома опція меню")
            return

        # Оновлюємо інтерактивне повідомлення
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_text,
            reply_markup=get_generic_inline_keyboard()
        )

        # Відправляємо оновлену клавіатуру, якщо є
        if new_keyboard:
            keyboard_message = await bot.send_message(
                chat_id=message.chat.id,
                text="",
                reply_markup=new_keyboard
            )

            # Зберігаємо ID повідомлення з клавіатурою
            await state.update_data(last_keyboard_message_id=keyboard_message.message_id)
    else:
        logger.error("interactive_message_id не знайдено")

# Обробник натискання звичайних кнопок у меню класу героїв
@router.message(MenuStates.HERO_CLASS_MENU)
async def handle_hero_class_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    data = await state.get_data()
    hero_class = data.get('hero_class')
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в меню класу героїв {hero_class}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Видаляємо попереднє повідомлення з клавіатурою
    await delete_last_keyboard_message(state, message.chat.id, bot)

    # Відправляємо повідомлення про завантаження
    loading_message = await bot.send_message(
        chat_id=message.chat.id,
        text="🔄 Завантаження даних..."
    )

    # Імітуємо завантаження даних
    await asyncio.sleep(1)

    # Видаляємо повідомлення про завантаження
    await loading_message.delete()

    # Отримуємо interactive_message_id з стану
    interactive_message_id = data.get('interactive_message_id')

    if interactive_message_id:
        new_text = ""

        if hero_class and hero_class in heroes_by_class:
            if user_choice in heroes_by_class[hero_class]:
                # Користувач обрав героя
                new_text = f"Ви обрали героя {user_choice}. Інформація про героя буде додана пізніше."
                new_keyboard = get_main_menu()
                await state.set_state(MenuStates.MAIN_MENU)
            elif user_choice == MenuButton.BACK.value:
                # Повертаємось до HEROES_MENU
                new_text = "🥷 **Персонажі**\nОберіть категорію героїв:"
                new_keyboard = get_heroes_menu()
                await state.set_state(MenuStates.HEROES_MENU)
            else:
                logger.warning("Невідомий герой")
                return
        else:
            logger.error("hero_class не знайдено або невідомий")

        # Оновлюємо інтерактивне повідомлення
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_text,
            reply_markup=get_generic_inline_keyboard()
        )

        # Відправляємо нову клавіатуру
        if new_keyboard:
            keyboard_message = await bot.send_message(
                chat_id=message.chat.id,
                text="",
                reply_markup=new_keyboard
            )

            # Зберігаємо ID повідомлення з клавіатурою
            await state.update_data(last_keyboard_message_id=keyboard_message.message_id)
    else:
        logger.error("interactive_message_id не знайдено")

# Аналогічно додаємо обробники для інших меню, використовуючи той самий підхід
# Наприклад, для MENU_GUIDES, MENU_PROFILE та інших.

# Обробник для невідомих повідомлень
@router.message()
async def unknown_command(message: Message, state: FSMContext, bot: Bot):
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")
    current_state = await state.get_state()
    data = await state.get_data()
    interactive_message_id = data.get('interactive_message_id')

    # Видаляємо повідомлення користувача
    await message.delete()

    # Видаляємо попереднє повідомлення з клавіатурою
    await delete_last_keyboard_message(state, message.chat.id, bot)

    if interactive_message_id:
        # Встановлюємо відповідні змінні залежно від поточного стану
        if current_state == MenuStates.MAIN_MENU.state:
            new_text = (
                f"👋 Вітаємо, {message.from_user.first_name}, у Mobile Legends Tournament Bot!\n\n"
                "🎮 Цей бот допоможе вам:\n"
                "• Організовувати турніри\n"
                "• Зберігати скріншоти персонажів\n"
                "• Відстежувати активність\n"
                "• Отримувати досягнення\n\n"
                "Оберіть опцію з меню нижче 👇"
            )
            new_keyboard = get_main_menu()
        elif current_state == MenuStates.NAVIGATION_MENU.state:
            new_text = "🧭 **Навігація**\nОберіть розділ для подальших дій:"
            new_keyboard = get_navigation_menu()
        elif current_state == MenuStates.HEROES_MENU.state:
            new_text = "🥷 **Персонажі**\nОберіть категорію героїв:"
            new_keyboard = get_heroes_menu()
        elif current_state == MenuStates.HERO_CLASS_MENU.state:
            hero_class = data.get('hero_class', 'Танк')
            new_text = f"🥷 **{hero_class}**\nВиберіть героя з класу {hero_class}:"
            new_keyboard = get_hero_class_menu(hero_class)
        else:
            new_text = (
                f"👋 Вітаємо, {message.from_user.first_name}, у Mobile Legends Tournament Bot!\n\n"
                "🎮 Цей бот допоможе вам:\n"
                "• Організовувати турніри\n"
                "• Зберігати скріншоти персонажів\n"
                "• Відстежувати активність\n"
                "• Отримувати досягнення\n\n"
                "Оберіть опцію з меню нижче 👇"
            )
            new_keyboard = get_main_menu()
            await state.set_state(MenuStates.MAIN_MENU)

        # Оновлюємо інтерактивне повідомлення
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_text,
            reply_markup=get_generic_inline_keyboard()
        )

        # Відправляємо клавіатуру
        keyboard_message = await bot.send_message(
            chat_id=message.chat.id,
            text="❗ Вибачте, я не розумію цю команду.",
            reply_markup=new_keyboard
        )

        # Зберігаємо ID повідомлення з клавіатурою
        await state.update_data(last_keyboard_message_id=keyboard_message.message_id)
    else:
        logger.error("interactive_message_id не знайдено")

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
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text="Ви натиснули на Кнопку 1"
            )
        elif data == "button2":
            await bot.send_message(
                chat_id=callback.message.chat.id,
                text="Ви натиснули на Кнопку 2"
            )
        elif data == "menu_back":
            # Повернення до головного меню
            await state.set_state(MenuStates.MAIN_MENU)
            new_text = (
                f"👋 Вітаємо, {callback.from_user.first_name}, у Mobile Legends Tournament Bot!\n\n"
                "🎮 Цей бот допоможе вам:\n"
                "• Організовувати турніри\n"
                "• Зберігати скріншоти персонажів\n"
                "• Відстежувати активність\n"
                "• Отримувати досягнення\n\n"
                "Оберіть опцію з меню нижче 👇"
            )
            await bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=interactive_message_id,
                text=new_text,
                reply_markup=get_generic_inline_keyboard()
            )

            # Видаляємо попереднє повідомлення з клавіатурою
            await delete_last_keyboard_message(state, callback.message.chat.id, bot)

            # Відправляємо головне меню
            keyboard_message = await bot.send_message(
                chat_id=callback.message.chat.id,
                text="",
                reply_markup=get_main_menu()
            )

            # Зберігаємо ID повідомлення з клавіатурою
            await state.update_data(last_keyboard_message_id=keyboard_message.message_id)
        # Додайте обробку інших інлайн-кнопок
    else:
        logger.error("interactive_message_id не знайдено")

    await callback.answer()

# Функція для налаштування обробників
def setup_handlers(dp):
    dp.include_router(router)
