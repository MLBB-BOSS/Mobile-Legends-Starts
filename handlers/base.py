# handlers/base.py

import logging
import asyncio
from aiogram import Router, F, types
from aiogram.filters import Command
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
async def cmd_start(message: types.Message, state: FSMContext, bot: Bot):
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
async def handle_welcome_buttons(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
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
        if isinstance(new_keyboard, types.InlineKeyboardMarkup):
            # Якщо використовуємо InlineKeyboardMarkup
            await bot.edit_message_text(
                chat_id=callback.message.chat.id,
                message_id=bot_message_id,
                text=new_text,
                parse_mode="Markdown",
                reply_markup=new_keyboard
            )
        elif isinstance(new_keyboard, types.ReplyKeyboardMarkup):
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

# Інші обробники меню (Наприклад, Навігація, Персонажі, Гайди тощо)
# Переконайтеся, що всі вони визначені як async функції та використовують правильні стани та клавіатури

# Приклад одного з обробників
@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu_buttons(message: types.Message, state: FSMContext, bot: Bot):
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

# Інші обробники меню (GUIDES_MENU, COUNTER_PICKS_MENU, BUILDS_MENU, VOTING_MENU, PROFILE_MENU, STATISTICS_MENU, ACHIEVEMENTS_MENU, SETTINGS_MENU, FEEDBACK_MENU, HELP_MENU)
# Переконайтеся, що всі вони визначені як async функції та використовують правильні стани та клавіатури

# Обробник для інлайн-кнопок
@router.callback_query()
async def handle_inline_buttons(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
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
async def unknown_command(message: types.Message, state: FSMContext, bot: Bot):
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
def setup_handlers(app: Application):
    app.include_router(router)
    # Додайте інші маршрути, якщо є
