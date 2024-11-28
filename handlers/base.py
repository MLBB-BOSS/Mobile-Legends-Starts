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
    # Додаткові стани, якщо потрібно

# Команда /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext, bot: Bot):
    user_name = message.from_user.first_name
    logger.info(f"Користувач {message.from_user.id} викликав /start")

    # Видаляємо повідомлення користувача /start
    await message.delete()

    # Відправляємо повідомлення про завантаження (тільки перше завантаження)
    loading_message = await bot.send_message(
        chat_id=message.chat.id,
        text="🔄 Завантаження даних..."
    )

    # Імітуємо завантаження даних (можна зменшити затримку)
    await asyncio.sleep(1)

    # Видаляємо повідомлення про завантаження
    await loading_message.delete()

    # Встановлюємо стан користувача
    await state.set_state(MenuStates.MAIN_MENU)

    # Відправляємо інтерактивне повідомлення з інлайн-кнопкою "Розпочати"
    inline_keyboard = types.InlineKeyboardMarkup()
    inline_keyboard.add(types.InlineKeyboardButton(text="🚀 Розпочати", callback_data="start_main_menu"))

    # Відправляємо привітальне повідомлення з інлайн-кнопкою
    interactive_message = await bot.send_message(
        chat_id=message.chat.id,
        text=(
            "<b>🌟 Ласкаво просимо до Mobile Legends Starts! 🌟</b>\n"
            "<i>Твій незамінний помічник у світі Mobile Legends – де стратегія зустрічається з епічними битвами!</i>\n"
            "\n"
            "---\n"
            "<b>✨ Що ми пропонуємо?</b>\n"
            "Наш бот створений для того, щоб покращити твій ігровий досвід. Ось лише частина можливостей, які чекають на тебе:\n"
            "\n"
            "✔️ <b>Завдання та Нагороди:</b> Виконуй цікаві завдання, збирай бали та піднімай свій рівень. Нагороди гарантовані!\n"
            "✔️ <b>Ексклюзивні Гайди та Стратегії:</b> Отримуй доступ до унікальних гайдів, які допоможуть тобі стати майстром Mobile Legends.\n"
            "✔️ <b>Детальна Статистика:</b> Аналізуй свій прогрес і покращуй свої навички.\n"
            "✔️ <b>Стратегії та Білди:</b> Ділись своїми ідеями, вивчай стратегії інших гравців та впроваджуй їх у свою гру.\n"
            "✔️ <b>Пошук Команди:</b> Знаходь однодумців або приєднуйся до готових команд.\n"
            "✔️ <b>Організація Турнірів:</b> Бери участь у змаганнях, перемагай і отримуй визнання!\n"
            "✔️ <b>Збереження Скріншотів:</b> Фіксуй найкращі моменти своїх ігор для історії.\n"
            "✔️ <b>Досягнення:</b> Слідкуй за своїми успіхами, отримуй бейджі та бонуси за виконані цілі.\n"
            "✔️ <b>Зворотний Зв'язок:</b> Поділись своїми пропозиціями чи ідеями – ми зробимо наш бот ще кращим!\n"
            "---\n"
            "<b>🚀 Розпочни свою подорож вже зараз!</b>\n"
            "Натисни кнопку «Розпочати» і поринь у світ безмежних можливостей Mobile Legends Starts.\n"
            "\n"
            "<i>Пам'ятай, твій успіх – це наша місія!</i>\n"
            "---\n"
            "<b>Зроблено з любов'ю для гравців Mobile Legends. 💖</b>"
        ),
        reply_markup=inline_keyboard,
        parse_mode="HTML"
    )

    # Зберігаємо ID інтерактивного повідомлення в стані
    await state.update_data(interactive_message_id=interactive_message.message_id)

# Обробник для інлайн-кнопки "Розпочати"
@router.callback_query(F.data == "start_main_menu")
async def start_main_menu_callback(callback: CallbackQuery, state: FSMContext, bot: Bot):
    # Видаляємо попереднє повідомлення з привітанням
    await callback.message.delete()

    # Відправляємо головне меню
    await state.set_state(MenuStates.MAIN_MENU)
    main_menu_message = await bot.send_message(
        chat_id=callback.message.chat.id,
        text="Оберіть опцію з меню:",
        reply_markup=get_main_menu()
    )

    # Зберігаємо ID повідомлення з головним меню в стані, якщо потрібно
    await state.update_data(main_menu_message_id=main_menu_message.message_id)

    await callback.answer()

# Додаємо всі обробники з вашого попереднього коду

# Головне Меню
@router.message(MenuStates.MAIN_MENU, F.text == MenuButton.NAVIGATION.value)
async def cmd_navigation(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Навігацію")
    await state.set_state(MenuStates.NAVIGATION_MENU)
    await message.answer(
        "Виберіть опцію навігації:",
        reply_markup=get_navigation_menu(),
    )

@router.message(MenuStates.MAIN_MENU, F.text == MenuButton.PROFILE.value)
async def cmd_profile(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Мій Профіль")
    await state.set_state(MenuStates.PROFILE_MENU)
    await message.answer(
        "Виберіть опцію профілю:",
        reply_markup=get_profile_menu(),
    )

# Розділ "Навігація"
@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.HEROES.value)
async def cmd_heroes(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Персонажі")
    await state.set_state(MenuStates.HEROES_MENU)
    await message.answer(
        "Виберіть категорію героїв:",
        reply_markup=get_heroes_menu(),
    )

# ... (Додаємо всі інші обробники з вашого попереднього коду)

# Обробник для невідомих повідомлень
@router.message()
async def unknown_command(message: Message, state: FSMContext):
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")
    current_state = await state.get_state()
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
    elif current_state == MenuStates.GUIDES_MENU.state:
        reply_markup = get_guides_menu()
    elif current_state == MenuStates.COUNTER_PICKS_MENU.state:
        reply_markup = get_counter_picks_menu()
    elif current_state == MenuStates.BUILDS_MENU.state:
        reply_markup = get_builds_menu()
    elif current_state == MenuStates.VOTING_MENU.state:
        reply_markup = get_voting_menu()
    elif current_state == MenuStates.PROFILE_MENU.state:
        reply_markup = get_profile_menu()
    elif current_state == MenuStates.STATISTICS_MENU.state:
        reply_markup = get_statistics_menu()
    elif current_state == MenuStates.ACHIEVEMENTS_MENU.state:
        reply_markup = get_achievements_menu()
    elif current_state == MenuStates.SETTINGS_MENU.state:
        reply_markup = get_settings_menu()
    elif current_state == MenuStates.FEEDBACK_MENU.state:
        reply_markup = get_feedback_menu()
    elif current_state == MenuStates.HELP_MENU.state:
        reply_markup = get_help_menu()
    else:
        reply_markup = get_main_menu()
        await state.set_state(MenuStates.MAIN_MENU)
    await message.answer(
        "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче.",
        reply_markup=reply_markup,
    )

# Функція для налаштування обробників
def setup_handlers(dp):
    dp.include_router(router)
