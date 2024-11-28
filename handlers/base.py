# handlers/base.py

import logging
from aiogram import Router, F, types
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
from keyboards.inline_menus import get_generic_inline_keyboard, get_hero_class_inline_keyboard

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
    CHANGE_USERNAME = State()
    REPORT_BUG = State()
    SEND_FEEDBACK = State()
    SUGGEST_TOPIC = State()

async def send_menu_response(message: Message, description: str, detailed_text: str, reply_markup: types.InlineKeyboardMarkup):
    """
    Допоміжна функція для відправки парних повідомлень:
    1. Опис меню.
    2. Детальний опис та інлайн-кнопки.
    """
    await message.answer(
        description,
        parse_mode="HTML"
    )
    await message.answer(
        detailed_text,
        parse_mode="HTML",
        reply_markup=reply_markup
    )

# Команда /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user_name = message.from_user.first_name
    logger.info(f"Користувач {message.from_user.id} викликав /start")
    await state.set_state(MenuStates.MAIN_MENU)
    
    description = f"👋 <b>Вітаємо, {user_name}, у Mobile Legends Tournament Bot!</b>"
    detailed_text = (
        "🎮 <b>Цей бот допоможе вам:</b>\n"
        "• Організовувати турніри\n"
        "• Зберігати скріншоти персонажів\n"
        "• Відстежувати активність\n"
        "• Отримувати досягнення\n\n"
        "Оберіть опцію з меню нижче 👇"
    )
    await send_menu_response(message, description, detailed_text, get_main_menu())
    
    # Додаємо інлайн-кнопки
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

# Головне Меню - Навігація
@router.message(MenuStates.MAIN_MENU, F.text == MenuButton.NAVIGATION.value)
async def cmd_navigation(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Навігацію")
    await state.set_state(MenuStates.NAVIGATION_MENU)
    
    description = "🧭 <b>Навігація:</b>"
    detailed_text = (
        "У цьому меню ви можете обрати різні розділи, такі як Персонажі, Гайди, Контр-піки, Білди, та Голосування.\n\n"
        "Оберіть відповідну опцію нижче, щоб перейти до більш детальної інформації."
    )
    await send_menu_response(message, description, detailed_text, get_navigation_menu())
    
    # Додаємо інлайн-кнопки
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

# Головне Меню - Мій Профіль
@router.message(MenuStates.MAIN_MENU, F.text == MenuButton.PROFILE.value)
async def cmd_profile(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Мій Профіль")
    await state.set_state(MenuStates.PROFILE_MENU)
    
    description = "🪪 <b>Мій Профіль:</b>"
    detailed_text = (
        "У цьому розділі ви можете переглядати та редагувати свій профіль, переглядати статистику, досягнення, налаштування та інше.\n\n"
        "Оберіть опцію профілю нижче для подальших дій."
    )
    await send_menu_response(message, description, detailed_text, get_profile_menu())
    
    # Додаємо інлайн-кнопки
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

# Розділ "Навігація" - Персонажі
@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.HEROES.value)
async def cmd_heroes(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Персонажі")
    await state.set_state(MenuStates.HEROES_MENU)
    
    description = "🛡️ <b>Персонажі:</b>"
    detailed_text = (
        "У цьому розділі ви можете обрати різних персонажів гри, переглянути їхні характеристики та інші деталі.\n\n"
        "Виберіть категорію героя нижче, щоб дізнатися більше про конкретних персонажів."
    )
    await send_menu_response(message, description, detailed_text, get_heroes_menu())
    
    # Додаємо інлайн-кнопки
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

# Розділ "Персонажі" - Вибір класу героя
@router.message(MenuStates.HEROES_MENU, F.text.in_([
    MenuButton.TANK.value,
    MenuButton.MAGE.value,
    MenuButton.MARKSMAN.value,
    MenuButton.ASSASSIN.value,
    MenuButton.SUPPORT.value,
    MenuButton.FIGHTER.value
]))
async def cmd_hero_class(message: Message, state: FSMContext):
    hero_class = menu_button_to_class.get(message.text)
    if hero_class:
        logger.info(f"Користувач {message.from_user.id} обрав клас {hero_class}")
        await state.set_state(MenuStates.HERO_CLASS_MENU)
        await state.update_data(hero_class=hero_class)  # Зберігаємо клас героя в стані
        
        description = f"🧙‍♂️ <b>{hero_class} Герої:</b>"
        detailed_text = (
            f"Виберіть героя з класу **{hero_class}**, щоб переглянути його характеристики та інші деталі."
        )
        await send_menu_response(message, description, detailed_text, get_hero_class_inline_keyboard(hero_class))
    else:
        logger.warning(f"Невідомий клас героїв: {message.text}")
        description = "❗ <b>Невідома команда:</b>"
        detailed_text = (
            "Вибачте, я не розумію цю команду. Скористайтеся меню нижче, щоб обрати доступні опції."
        )
        await send_menu_response(message, description, detailed_text, get_heroes_menu())
        
        # Додаємо інлайн-кнопки
        await message.answer(
            "Ось ваші інлайн-опції:",
            reply_markup=get_generic_inline_keyboard()
        )

# Розділ "Персонажі" - Пошук героя
@router.message(MenuStates.HEROES_MENU, F.text == MenuButton.SEARCH_HERO.value)
async def cmd_search_hero(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Пошук Персонажа")
    await state.set_state(MenuStates.SEARCH_HERO)
    
    description = "🔎 <b>Пошук Персонажа:</b>"
    detailed_text = (
        "Введіть ім'я героя, якого ви шукаєте. Бот надасть інформацію про цього героя, якщо він існує."
    )
    await send_menu_response(message, description, detailed_text, get_generic_inline_keyboard())
    
    # Додатково можна налаштувати обробник для стану SEARCH_HERO

# Розділ "Персонажі" - Порівняння
@router.message(MenuStates.HEROES_MENU, F.text == MenuButton.COMPARISON.value)
async def cmd_comparison(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Порівняння")
    description = "⚖️ <b>Порівняння Героїв:</b>"
    detailed_text = (
        "Функція порівняння героїв ще в розробці. Слідкуйте за оновленнями!"
    )
    await send_menu_response(message, description, detailed_text, get_heroes_menu())
    
    # Додаємо інлайн-кнопки
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

# Розділ "Персонажі" - Назад до навігації
@router.message(MenuStates.HEROES_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_navigation_from_heroes(message: Message, state: FSMContext):
    await state.set_state(MenuStates.NAVIGATION_MENU)
    
    description = "🔙 <b>Повернення до меню Навігація:</b>"
    detailed_text = (
        "Ви повернулися до меню Навігація. Оберіть нову опцію нижче."
    )
    await send_menu_response(message, description, detailed_text, get_navigation_menu())
    
    # Додаємо інлайн-кнопки
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

# Обробники для вибору героя з класу
all_heroes = set()
for heroes in heroes_by_class.values():
    all_heroes.update(heroes)

@router.message(MenuStates.HERO_CLASS_MENU, F.text.in_(all_heroes))
async def cmd_select_hero(message: Message, state: FSMContext):
    hero_name = message.text
    logger.info(f"Користувач {message.from_user.id} обрав героя {hero_name}")
    await state.set_state(MenuStates.MAIN_MENU)
    
    description = f"🎯 <b>{hero_name}:</b>"
    detailed_text = (
        f"Ви обрали героя **{hero_name}**. Інформація про героя буде додана пізніше.\n\n"
        f"Поверніться до головного меню або оберіть іншу опцію."
    )
    await send_menu_response(message, description, detailed_text, get_main_menu())
    
    # Додаємо інлайн-кнопки
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.HERO_CLASS_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_heroes_menu(message: Message, state: FSMContext):
    await state.set_state(MenuStates.HEROES_MENU)
    
    description = "🔙 <b>Повернення до меню Персонажі:</b>"
    detailed_text = (
        "Ви повернулися до меню Персонажі. Оберіть нову категорію героя нижче."
    )
    await send_menu_response(message, description, detailed_text, get_heroes_menu())
    
    # Додаємо інлайн-кнопки
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

# Решта обробників залишаються без змін...
# Наприклад, обробники для інших меню, невідомих команд, тощо

# Обробники для інлайн-кнопок
@router.callback_query(F.data == "button1")
async def handle_button1(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Ви натиснули на Кнопку 1")
    await call.answer()

@router.callback_query(F.data == "button2")
async def handle_button2(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Ви натиснули на Кнопку 2")
    await call.answer()

# Обробник для невідомих повідомлень
@router.message()
async def unknown_command(message: Message, state: FSMContext):
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")
    current_state = await state.get_state()
    
    if current_state == MenuStates.MAIN_MENU.state:
        reply_markup = get_main_menu()
        description = "❗ <b>Невідома команда:</b>"
        detailed_text = (
            "Вибачте, я не розумію цю команду. Скористайтеся меню нижче, щоб обрати доступні опції."
        )
    elif current_state == MenuStates.NAVIGATION_MENU.state:
        reply_markup = get_navigation_menu()
        description = "❗ <b>Невідома команда:</b>"
        detailed_text = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій навігації."
        )
    elif current_state == MenuStates.HEROES_MENU.state:
        reply_markup = get_heroes_menu()
        description = "❗ <b>Невідома команда:</b>"
        detailed_text = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних категорій героїв."
        )
    elif current_state == MenuStates.HERO_CLASS_MENU.state:
        data = await state.get_data()
        hero_class = data.get('hero_class', 'Танк')
        reply_markup = get_hero_class_inline_keyboard(hero_class)
        description = "❗ <b>Невідома команда:</b>"
        detailed_text = (
            f"Вибачте, я не розумію цю команду. Виберіть героя з класу <b>{hero_class}</b>."
        )
    elif current_state == MenuStates.GUIDES_MENU.state:
        reply_markup = get_guides_menu()
        description = "❗ <b>Невідома команда:</b>"
        detailed_text = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій гайдів."
        )
    elif current_state == MenuStates.COUNTER_PICKS_MENU.state:
        reply_markup = get_counter_picks_menu()
        description = "❗ <b>Невідома команда:</b>"
        detailed_text = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій контр-піків."
        )
    elif current_state == MenuStates.BUILDS_MENU.state:
        reply_markup = get_builds_menu()
        description = "❗ <b>Невідома команда:</b>"
        detailed_text = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій білдів."
        )
    elif current_state == MenuStates.VOTING_MENU.state:
        reply_markup = get_voting_menu()
        description = "❗ <b>Невідома команда:</b>"
        detailed_text = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій голосування."
        )
    elif current_state == MenuStates.PROFILE_MENU.state:
        reply_markup = get_profile_menu()
        description = "❗ <b>Невідома команда:</b>"
        detailed_text = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій профілю."
        )
    elif current_state == MenuStates.STATISTICS_MENU.state:
        reply_markup = get_statistics_menu()
        description = "❗ <b>Невідома команда:</b>"
        detailed_text = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій статистики."
        )
    elif current_state == MenuStates.ACHIEVEMENTS_MENU.state:
        reply_markup = get_achievements_menu()
        description = "❗ <b>Невідома команда:</b>"
        detailed_text = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій досягнень."
        )
    elif current_state == MenuStates.SETTINGS_MENU.state:
        reply_markup = get_settings_menu()
        description = "❗ <b>Невідома команда:</b>"
        detailed_text = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій налаштувань."
        )
    elif current_state == MenuStates.FEEDBACK_MENU.state:
        reply_markup = get_feedback_menu()
        description = "❗ <b>Невідома команда:</b>"
        detailed_text = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій зворотного зв'язку."
        )
    elif current_state == MenuStates.HELP_MENU.state:
        reply_markup = get_help_menu()
        description = "❗ <b>Невідома команда:</b>"
        detailed_text = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій допомоги."
        )
    else:
        reply_markup = get_main_menu()
        await state.set_state(MenuStates.MAIN_MENU)
        description = "❗ <b>Невідома команда:</b>"
        detailed_text = (
            "Вибачте, я не розумію цю команду. Скористайтеся меню нижче, щоб обрати доступні опції."
        )
    
    await message.answer(
        description,
        parse_mode="HTML"
    )
    await message.answer(
        detailed_text,
        parse_mode="HTML",
        reply_markup=reply_markup
    )
    
    # Додаємо інлайн-кнопки
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

# Обробники для інлайн-кнопок
@router.callback_query(F.data == "button1")
async def handle_button1(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Ви натиснули на Кнопку 1")
    await call.answer()

@router.callback_query(F.data == "button2")
async def handle_button2(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Ви натиснули на Кнопку 2")
    await call.answer()

# Функція для налаштування обробників
def setup_handlers(dp):
    dp.include_router(router)
