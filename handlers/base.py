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
    get_heroes_menu,
    get_hero_class_menu,
    get_guides_menu,
    get_counter_picks_menu,
    get_builds_menu,
    get_voting_menu,
    get_profile_menu,
    get_statistics_menu,
    get_achievements_menu,
    get_settings_menu,
    get_feedback_menu,
    get_help_menu,
    heroes_by_class,
)
from keyboards.inline_menus import (
    get_generic_inline_keyboard,
    get_hero_class_inline_keyboard,
    get_main_inline_keyboard,
)
from aiogram.utils.markdown import bold

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
    # Додаткові стани, якщо потрібно

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
    await bot.send_message(
        chat_id=message.chat.id,
        text="Оберіть опцію з меню нижче 👇",
        reply_markup=get_main_menu()
    )

# Обробник натискання звичайних кнопок у MAIN_MENU
@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice}")

    # Видаляємо повідомлення користувача
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

    # Отримуємо interactive_message_id з стану
    data = await state.get_data()
    interactive_message_id = data.get('interactive_message_id')

    # Оновлюємо текст інтерактивного повідомлення
    if interactive_message_id:
        new_text = ""
        new_keyboard = None

        if user_choice == MenuButton.NAVIGATION.value:
            new_text = f"🧭 {bold('Навігація')}\nОберіть розділ для подальших дій:"
            new_keyboard = get_navigation_menu()
            await state.set_state(MenuStates.NAVIGATION_MENU)
        elif user_choice == MenuButton.PROFILE.value:
            new_text = f"🪪 {bold('Мій Профіль')}\nОберіть опцію для перегляду:"
            new_keyboard = get_profile_menu()
            await state.set_state(MenuStates.PROFILE_MENU)
        else:
            logger.warning("Невідома опція меню")
            return

        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_text,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="Markdown"
        )

        # Відправляємо оновлену клавіатуру
        await bot.send_message(
            chat_id=message.chat.id,
            text="Оберіть опцію з меню нижче 👇",
            reply_markup=new_keyboard
        )
    else:
        logger.error("interactive_message_id не знайдено")

# Обробники для NAVIGATION_MENU
@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice}")

    # Видаляємо повідомлення користувача
    await message.delete()

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
        new_keyboard = None

        if user_choice == MenuButton.HEROES.value:
            new_text = f"🥷 {bold('Персонажі')}\nОберіть категорію героїв:"
            new_keyboard = get_heroes_menu()
            await state.set_state(MenuStates.HEROES_MENU)
        elif user_choice == MenuButton.GUIDES.value:
            new_text = f"📚 {bold('Гайди')}\nОберіть розділ гайдів:"
            new_keyboard = get_guides_menu()
            await state.set_state(MenuStates.GUIDES_MENU)
        elif user_choice == MenuButton.BUILDS.value:
            new_text = f"⚜️ {bold('Білди')}\nОберіть опцію для перегляду:"
            new_keyboard = get_builds_menu()
            await state.set_state(MenuStates.BUILDS_MENU)
        elif user_choice == MenuButton.COUNTER_PICKS.value:
            new_text = f"⚖️ {bold('Контр-піки')}\nОберіть опцію контр-піків:"
            new_keyboard = get_counter_picks_menu()
            await state.set_state(MenuStates.COUNTER_PICKS_MENU)
        elif user_choice == MenuButton.VOTING.value:
            new_text = f"📊 {bold('Голосування')}\nОберіть опцію голосування:"
            new_keyboard = get_voting_menu()
            await state.set_state(MenuStates.VOTING_MENU)
        elif user_choice == MenuButton.BACK.value:
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

        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_text,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="Markdown"
        )

        # Відправляємо оновлену клавіатуру
        await bot.send_message(
            chat_id=message.chat.id,
            text="Оберіть опцію з меню нижче 👇",
            reply_markup=new_keyboard
        )
    else:
        logger.error("interactive_message_id не знайдено")

# Обробники для HEROES_MENU
@router.message(MenuStates.HEROES_MENU)
async def handle_heroes_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Відправляємо повідомлення про завантаження
    loading_message = await bot.send_message(
        chat_id=message.chat.id,
        text="🔄 Завантаження героїв..."
    )

    # Імітуємо завантаження даних
    await asyncio.sleep(1)

    # Видаляємо повідомлення про завантаження
    await loading_message.delete()

    # Отримуємо interactive_message_id з стану
    data = await state.get_data()
    interactive_message_id = data.get('interactive_message_id')

    if interactive_message_id:
        if user_choice in menu_button_to_class:
            hero_class = menu_button_to_class[user_choice]
            new_text = f"{user_choice} {bold(hero_class)}\nОберіть героя:"
            new_keyboard = get_hero_class_menu(hero_class)
            await state.set_state(MenuStates.HERO_CLASS_MENU)
            await state.update_data(hero_class=hero_class)
        elif user_choice == MenuButton.BACK.value:
            new_text = f"🧭 {bold('Навігація')}\nОберіть розділ для подальших дій:"
            new_keyboard = get_navigation_menu()
            await state.set_state(MenuStates.NAVIGATION_MENU)
        else:
            logger.warning("Невідома опція меню")
            return

        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_text,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="Markdown"
        )

        # Відправляємо оновлену клавіатуру
        await bot.send_message(
            chat_id=message.chat.id,
            text="Оберіть героя з меню нижче 👇",
            reply_markup=new_keyboard
        )
    else:
        logger.error("interactive_message_id не знайдено")

# Обробники для HERO_CLASS_MENU
all_heroes = set()
for heroes in heroes_by_class.values():
    all_heroes.update(heroes)

@router.message(MenuStates.HERO_CLASS_MENU)
async def handle_hero_class_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав героя {user_choice}")

    # Видаляємо повідомлення користувача
    await message.delete()

    # Відправляємо повідомлення про завантаження
    loading_message = await bot.send_message(
        chat_id=message.chat.id,
        text=f"🔄 Завантаження інформації про героя {user_choice}..."
    )

    # Імітуємо завантаження даних
    await asyncio.sleep(1)

    # Видаляємо повідомлення про завантаження
    await loading_message.delete()

    # Отримуємо interactive_message_id з стану
    data = await state.get_data()
    interactive_message_id = data.get('interactive_message_id')

    if interactive_message_id:
        if user_choice in all_heroes:
            new_text = f"Інформація про героя {bold(user_choice)}:\n(Тут буде опис героя)"
            await state.set_state(MenuStates.HEROES_MENU)
            new_keyboard = get_heroes_menu()
        elif user_choice == MenuButton.BACK.value:
            # Повертаємося до списку класів героїв
            hero_class = data.get('hero_class', 'Танк')
            new_text = f"{MenuButton[hero_class.upper()].value} {bold(hero_class)}\nОберіть героя:"
            new_keyboard = get_hero_class_menu(hero_class)
            await state.set_state(MenuStates.HEROES_MENU)
        else:
            logger.warning("Невідомий герой")
            return

        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=new_text,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="Markdown"
        )

        # Відправляємо оновлену клавіатуру
        await bot.send_message(
            chat_id=message.chat.id,
            text="Оберіть опцію з меню нижче 👇",
            reply_markup=new_keyboard
        )
    else:
        logger.error("interactive_message_id не знайдено")

# Аналогічно додайте обробники для інших станів меню (GUIDES_MENU, BUILDS_MENU, etc.)

# Обробники для інлайн-кнопок
@router.callback_query()
async def handle_inline_buttons(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = callback.data
    logger.info(f"Користувач {callback.from_user.id} натиснув інлайн-кнопку: {data}")

    # Отримуємо interactive_message_id з стану
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if interactive_message_id:
        new_text = ""
        if data == "menu_heroes":
            new_text = f"🥷 {bold('Персонажі')}\nОберіть категорію героїв:"
            await state.set_state(MenuStates.HEROES_MENU)
            new_keyboard = get_heroes_menu()
        elif data == "menu_guides":
            new_text = f"📚 {bold('Гайди')}\nОберіть розділ гайдів:"
            await state.set_state(MenuStates.GUIDES_MENU)
            new_keyboard = get_guides_menu()
        elif data == "menu_builds":
            new_text = f"⚜️ {bold('Білди')}\nОберіть опцію для перегляду:"
            await state.set_state(MenuStates.BUILDS_MENU)
            new_keyboard = get_builds_menu()
        elif data == "menu_statistics":
            new_text = f"📈 {bold('Статистика')}\nОберіть підрозділ статистики:"
            await state.set_state(MenuStates.STATISTICS_MENU)
            new_keyboard = get_statistics_menu()
        elif data == "menu_back":
            new_text = (
                f"👋 Вітаємо, {callback.from_user.first_name}, у Mobile Legends Tournament Bot!\n\n"
                "🎮 Цей бот допоможе вам:\n"
                "• Організовувати турніри\n"
                "• Зберігати скріншоти персонажів\n"
                "• Відстежувати активність\n"
                "• Отримувати досягнення\n\n"
                "Оберіть опцію з меню нижче 👇"
            )
            await state.set_state(MenuStates.MAIN_MENU)
            new_keyboard = get_main_menu()
        else:
            await callback.answer("Ця функція ще не реалізована", show_alert=True)
            return

        # Оновлюємо інтерактивне повідомлення
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=new_text,
            reply_markup=get_generic_inline_keyboard(),
            parse_mode="Markdown"
        )

        # Відправляємо нову клавіатуру
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text="Оберіть опцію з меню нижче 👇",
            reply_markup=new_keyboard
        )
    else:
        logger.error("interactive_message_id не знайдено")

    await callback.answer()

# Обробник для невідомих повідомлень
@router.message()
async def unknown_command(message: Message, state: FSMContext, bot: Bot):
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")
    current_state = await state.get_state()
    await message.delete()

    # Відправляємо повідомлення про завантаження
    loading_message = await bot.send_message(
        chat_id=message.chat.id,
        text="🔄 Обробка вашого запиту..."
    )

    # Імітуємо затримку
    await asyncio.sleep(1)

    # Видаляємо повідомлення про завантаження
    await loading_message.delete()

    # Відповідно до стану відправляємо відповідне меню
    if current_state == MenuStates.MAIN_MENU.state:
        reply_markup = get_main_menu()
    elif current_state == MenuStates.NAVIGATION_MENU.state:
        reply_markup = get_navigation_menu()
    elif current_state == MenuStates.HEROES_MENU.state:
        reply_markup = get_heroes_menu()
    elif current_state == MenuStates.HERO_CLASS_MENU.state:
        data = await state.get_data()
        hero_class = data.get('hero_class', 'Танк')
        reply_markup = get_hero_class_menu(hero_class)
    elif current_state == MenuStates.PROFILE_MENU.state:
        reply_markup = get_profile_menu()
    else:
        reply_markup = get_main_menu()
        await state.set_state(MenuStates.MAIN_MENU)

    # Відправляємо повідомлення з пропозицією скористатися меню
    await bot.send_message(
        chat_id=message.chat.id,
        text="❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче.",
        reply_markup=reply_markup
    )

# Функція для налаштування обробників
def setup_handlers(dp):
    dp.include_router(router)
