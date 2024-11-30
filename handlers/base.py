# handlers/base.py

import logging
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
from keyboards.inline_menus import (
    get_generic_inline_keyboard,
    get_intro_page_1_keyboard,
    get_intro_page_2_keyboard,
    get_intro_page_3_keyboard
)

# Налаштування логування
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
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

# Команда /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    user_name = message.from_user.first_name
    logger.info(f"Користувач {message.from_user.id} викликав /start")

    # Видаляємо повідомлення користувача /start
    await message.delete()

    # Встановлюємо стан користувача на INTRO_PAGE_1
    await state.set_state(MenuStates.INTRO_PAGE_1)

    # Відправляємо перше інтерктивне повідомлення з кнопкою 'Далі'
    intro_page_1_text = (
        "🌟 Ласкаво просимо до Mobile Legends Starts! 🌟\n\n"
        "Твій незамінний помічник у світі Mobile Legends – де стратегія зустрічається з епічними битвами!\n\n"
        "---\n\n"
        "✨ <b>Що вас чекає?</b>\n\n"
        "• 🗺️ <b>Завдання:</b> Виконуй місії, заробляй бали, підвищуй рівень!\n"
        "• 📘 <b>Гайди:</b> Доступ до унікальних порад і стратегій.\n"
        "• 📊 <b>Статистика:</b> Аналізуй свій прогрес.\n"
        "• ⚙️ <b>Білди:</b> Створюй ідеальне спорядження для героїв.\n"
        "• 🤝 <b>Команди:</b> Шукай союзників для гри.\n"
        "• 🏆 <b>Турніри:</b> Організовуй або долучайся до змагань.\n"
        "• 🎖️ <b>Досягнення:</b> Відстежуй успіхи, отримуй нагороди.\n"
        "• 🥷 <b>Персонажі:</b> Обирай героїв, порівнюй їх здібності та досягай перемог!\n\n"
        "---\n\n"
        "🚀 <b>Розпочни свою подорож вже зараз!</b>\n\n"
        "Натисни кнопку «Далі» і поринь у світ безмежних можливостей Mobile Legends Starts.\n\n"
        "Пам'ятай, твій успіх – це наша місія!\n\n"
        "---\n\n"
        "<b>Зроблено з любов'ю для гравців Mobile Legends. 💖</b>"
    )

    interactive_message = await bot.send_message(
        chat_id=message.chat.id,
        text=intro_page_1_text,
        parse_mode="HTML",
        reply_markup=get_intro_page_1_keyboard()
    )

    # Зберігаємо ID інтерактивного повідомлення
    await state.update_data(interactive_message_id=interactive_message.message_id)

# Обробник натискання інлайн-кнопки 'Далі' на першій сторінці
@router.callback_query(F.data == "intro_next_1")
async def handle_intro_next_1(callback: CallbackQuery, state: FSMContext, bot: Bot):
    intro_page_2_text = (
        "💡 <b>Функції нашого бота:</b>\n\n"
        "• 🧭 <b>Навігація:</b> Легко орієнтуйся у всіх можливостях бота.\n"
        "• 🪪 <b>Мій профіль:</b> Переглядай і редагуй свої дані.\n"
        "• 🥷 <b>Персонажі:</b> Дізнавайся більше про героїв та їхні можливості.\n"
        "• 📚 <b>Гайди:</b> Отримуй корисні поради та стратегії.\n"
        "• 📊 <b>Статистика:</b> Відстежуй свій прогрес і досягнення.\n"
        "• ⚙️ <b>Білди:</b> Створюй оптимальні спорядження для героїв.\n"
        "• 🏆 <b>Турніри:</b> Беріть участь у змаганнях та вигравайте нагороди.\n\n"
        "---\n\n"
        "Натисни кнопку «Далі», щоб продовжити ознайомлення."
    )

    # Отримуємо ID інтерактивного повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    # Редагуємо інтерактивне повідомлення на другу сторінку
    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=intro_page_2_text,
            parse_mode="HTML",
            reply_markup=get_intro_page_2_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text="Сталася помилка. Будь ласка, спробуйте знову.",
            reply_markup=get_generic_inline_keyboard()
        )
        await callback.answer()
        return

    # Оновлюємо стан
    await state.set_state(MenuStates.INTRO_PAGE_2)
    await callback.answer()

# Обробник натискання інлайн-кнопки 'Далі' на другій сторінці
@router.callback_query(F.data == "intro_next_2")
async def handle_intro_next_2(callback: CallbackQuery, state: FSMContext, bot: Bot):
    intro_page_3_text = (
        "🚀 <b>Готові розпочати?</b>\n\n"
        "Натисни кнопку «Розпочати», щоб перейти до основного меню і розпочати використання бота.\n\n"
        "---\n\n"
        "<b>Залишайся з нами, і разом досягнемо нових висот у Mobile Legends!</b>"
    )

    # Отримуємо ID інтерактивного повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    # Редагуємо інтерактивне повідомлення на третю сторінку
    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=intro_page_3_text,
            parse_mode="HTML",
            reply_markup=get_intro_page_3_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        await bot.send_message(
            chat_id=callback.message.chat.id,
            text="Сталася помилка. Будь ласка, спробуйте знову.",
            reply_markup=get_generic_inline_keyboard()
        )
        await callback.answer()
        return

    # Оновлюємо стан
    await state.set_state(MenuStates.INTRO_PAGE_3)
    await callback.answer()

# Обробник натискання інлайн-кнопки 'Розпочати' на третій сторінці
@router.callback_query(F.data == "intro_start")
async def handle_intro_start(callback: CallbackQuery, state: FSMContext, bot: Bot):
    user_first_name = callback.from_user.first_name

    # Відправляємо основне меню з клавіатурою
    main_menu_text = (
        f"👋 Вітаємо, {user_first_name}, у Mobile Legends Tournament Bot!\n\n"
        "Оберіть опцію з меню нижче 👇"
    )

    main_menu_message = await bot.send_message(
        chat_id=callback.message.chat.id,
        text=main_menu_text,
        reply_markup=get_main_menu()
    )

    # Оновлюємо ID основного повідомлення
    await state.update_data(bot_message_id=main_menu_message.message_id)

    # Отримуємо ID інтерактивного повідомлення
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    # Оновлюємо інтерактивне повідомлення з описом основного меню
    main_menu_description = (
        "🎮 Цей бот допоможе вам:\n"
        "• Організовувати турніри\n"
        "• Зберігати скріншоти персонажів\n"
        "• Відстежувати активність\n"
        "• Отримувати досягнення"
    )

    try:
        await bot.edit_message_text(
            chat_id=callback.message.chat.id,
            message_id=interactive_message_id,
            text=main_menu_description,
            parse_mode="HTML",
            reply_markup=get_generic_inline_keyboard()
        )
    except Exception as e:
        logger.error(f"Не вдалося редагувати інтерактивне повідомлення: {e}")
        # Якщо не вдалося редагувати, відправляємо нове інтерактивне повідомлення
        interactive_message = await bot.send_message(
            chat_id=callback.message.chat.id,
            text=main_menu_description,
            reply_markup=get_generic_inline_keyboard()
        )
        await state.update_data(interactive_message_id=interactive_message.message_id)

    # Встановлюємо стан користувача на MAIN_MENU
    await state.set_state(MenuStates.MAIN_MENU)
    await callback.answer()

# Обробник натискання звичайних кнопок у головному меню
@router.message(MenuStates.MAIN_MENU)
async def handle_main_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} у головному меню")

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

    # Визначаємо новий текст та клавіатуру для повідомлень
    new_main_text = ""
    new_main_keyboard = None
    new_interactive_text = ""
    new_interactive_keyboard = get_generic_inline_keyboard()
    new_state = None

    if user_choice == MenuButton.NAVIGATION.value:
        new_main_text = "🧭 Навігація\nОберіть розділ для подальших дій:"
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = (
            "🧭 <b>Доступні розділи:</b>\n\n"
            "🥷 <b>Персонажі:</b> Оберіть героя, щоб дізнатися про його здібності.\n"
            "📘 <b>Гайди:</b> Ознайомтесь із гайдами та стратегіями.\n"
            "⚙️ <b>Білди:</b> Створіть чи перегляньте спорядження для героїв.\n"
            "⚖️ <b>Контр-піки:</b> Дізнайтесь, як протистояти героям-суперникам.\n"
            "📊 <b>Голосування:</b> Висловлюйте свою думку або пропонуйте ідеї.\n\n"
            "👇 Оберіть кнопку нижче, щоб продовжити."
        )
        new_state = MenuStates.NAVIGATION_MENU
    elif user_choice == MenuButton.PROFILE.value:
        new_main_text = "🪪 Мій Профіль\nОберіть опцію для перегляду:"
        new_main_keyboard = get_profile_menu()
        new_interactive_text = "Профіль користувача"
        new_state = MenuStates.PROFILE_MENU
    else:
        # Невідома команда
        new_main_text = "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче."
        new_main_keyboard = get_main_menu()
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.MAIN_MENU

    # Відправляємо нове повідомлення з клавіатурою (Повідомлення 1)
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    # Зберігаємо новий bot_message_id
    new_bot_message_id = main_message.message_id

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
            parse_mode="HTML",
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
        new_main_keyboard = types.ReplyKeyboardRemove()
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
        new_main_keyboard = get_hero_class_menu(data.get('hero_class', 'Танк'))
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.HEROES_MENU

    # Відправляємо нове повідомлення з клавіатурою
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

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

    # Оновлюємо стан користувача
    await state.set_state(new_state)

# Обробник натискання звичайних кнопок у меню класу героїв
@router.message(MenuStates.HERO_CLASS_MENU)
async def handle_hero_class_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    hero_name = message.text
    logger.info(f"Користувач {message.from_user.id} обрав героя {hero_name}")

    # Видаляємо повідомлення користувача
    await message.delete()

    data = await state.get_data()
    bot_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    hero_class = data.get('hero_class', 'Танк')

    all_heroes = set()
    for heroes in heroes_by_class.values():
        all_heroes.update(heroes)

    if hero_name in all_heroes:
        new_main_text = f"Ви обрали героя {hero_name}. Інформація про героя буде додана пізніше."
        new_main_keyboard = get_main_menu()
        new_interactive_text = f"Інформація про героя {hero_name}"
        new_state = MenuStates.MAIN_MENU
    elif hero_name == MenuButton.BACK.value:
        new_main_text = "🔙 Повернення до меню Персонажі:"
        new_main_keyboard = get_heroes_menu()
        new_interactive_text = "Список категорій героїв"
        new_state = MenuStates.HEROES_MENU
    else:
        new_main_text = "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче."
        new_main_keyboard = get_hero_class_menu(hero_class)
        new_interactive_text = "Невідома команда"
        new_state = MenuStates.HERO_CLASS_MENU

    # Відправляємо нове повідомлення
    main_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_main_text,
        reply_markup=new_main_keyboard
    )
    new_bot_message_id = main_message.message_id

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

# Додайте обробники для інших меню (Гайди, Контр-піки, Білди, Голосування, Профіль тощо)
# ... Ваш існуючий код для інших обробників меню ...

# Обробник натискання інлайн-кнопок
@router.callback_query()
async def handle_inline_buttons(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = callback.data
    logger.info(f"Користувач {callback.from_user.id} натиснув інлайн-кнопку: {data}")

    # Отримуємо interactive_message_id з стану
    state_data = await state.get_data()
    interactive_message_id = state_data.get('interactive_message_id')

    if interactive_message_id:
        # Обробляємо інлайн-кнопки
        if data == "mls_button":
            await bot.answer_callback_query(callback.id, text="---MLS--- кнопка натиснута.")
        elif data == "intro_next_1":
            # Цей випадок вже обробляється окремим обробником
            pass
        elif data == "intro_next_2":
            # Цей випадок вже обробляється окремим обробником
            pass
        elif data == "intro_start":
            # Цей випадок вже обробляється окремим обробником
            pass
        elif data == "menu_back":
            # Повернення до головного меню (якщо потрібно)
            # Наприклад, ви можете реалізувати логіку повернення
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
        else:
            # Додайте обробку інших інлайн-кнопок за потребою
            await bot.answer_callback_query(callback.id, text="Ця кнопка поки не оброблена.")
    else:
        logger.error("interactive_message_id не знайдено")
        await bot.answer_callback_query(callback.id, text="Сталася помилка.")

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
    elif current_state in [MenuStates.INTRO_PAGE_1.state, MenuStates.INTRO_PAGE_2.state, MenuStates.INTRO_PAGE_3.state]:
        # Якщо користувач перебуває в процесі введення, можна надсилати підказку або просто ігнорувати
        await bot.send_message(
            chat_id=message.chat.id,
            text="Будь ласка, використовуйте кнопки для навігації.",
            reply_markup=get_generic_inline_keyboard()
        )
        await state.set_state(current_state)
        return
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

    # Видаляємо старе повідомлення
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
def setup_handlers(dp):
    dp.include_router(router)
