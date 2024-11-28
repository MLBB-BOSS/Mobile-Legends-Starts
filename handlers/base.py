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
from keyboards.inline_menus import (
    get_generic_inline_keyboard,
    get_hero_class_inline_keyboard,
)

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

async def send_header(message: Message, description: str, reply_markup: types.ReplyKeyboardMarkup):
    """
    Відправляє заголовок меню з відповідною клавіатурою.
    """
    await message.answer(
        description,
        parse_mode="HTML",
        reply_markup=reply_markup
    )

async def send_inline_menu(message: Message, detailed_text: str, inline_markup: types.InlineKeyboardMarkup):
    """
    Відправляє детальний текст з інлайн-кнопками.
    """
    await message.answer(
        detailed_text,
        parse_mode="HTML",
        reply_markup=inline_markup
    )

# Команда /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user_name = message.from_user.first_name
    logger.info(f"Користувач {message.from_user.id} викликав /start")
    await state.set_state(MenuStates.MAIN_MENU)
    
    header = f"👋 <b>Вітаємо, {user_name}, у Mobile Legends Tournament Bot!</b>"
    description = (
        "🎮 <b>Цей бот допоможе вам:</b>\n"
        "• Організовувати турніри\n"
        "• Зберігати скріншоти персонажів\n"
        "• Відстежувати активність\n"
        "• Отримувати досягнення\n\n"
        "Оберіть опцію з меню нижче 👇"
    )
    
    # Відправка заголовка з основною клавіатурою
    await send_header(message, header + "\n\n" + description, get_main_menu())
    
    # Відправка інлайн-кнопок
    await send_inline_menu(message, "Ось ваші інлайн-опції:", get_generic_inline_keyboard())

# Головне Меню - Навігація
@router.message(MenuStates.MAIN_MENU, F.text == MenuButton.NAVIGATION.value)
async def cmd_navigation(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Навігацію")
    await state.set_state(MenuStates.NAVIGATION_MENU)
    
    header = "🧭 <b>Навігація:</b>"
    description = (
        "У цьому меню ви можете обрати різні розділи, такі як Персонажі, Гайди, Контр-піки, Білди, та Голосування.\n\n"
        "Оберіть відповідну опцію нижче, щоб перейти до більш детальної інформації."
    )
    
    # Відправка заголовка з навігаційною клавіатурою
    await send_header(message, header + "\n\n" + description, get_navigation_menu())
    
    # Відправка інлайн-кнопок
    await send_inline_menu(message, "Ось ваші інлайн-опції:", get_generic_inline_keyboard())

# Головне Меню - Мій Профіль
@router.message(MenuStates.MAIN_MENU, F.text == MenuButton.PROFILE.value)
async def cmd_profile(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Мій Профіль")
    await state.set_state(MenuStates.PROFILE_MENU)
    
    header = "🪪 <b>Мій Профіль:</b>"
    description = (
        "У цьому розділі ви можете переглядати та редагувати свій профіль, переглядати статистику, досягнення, налаштування та інше.\n\n"
        "Оберіть опцію профілю нижче для подальших дій."
    )
    
    # Відправка заголовка з профільною клавіатурою
    await send_header(message, header + "\n\n" + description, get_profile_menu())
    
    # Відправка інлайн-кнопок
    await send_inline_menu(message, "Ось ваші інлайн-опції:", get_generic_inline_keyboard())

# Розділ "Навігація" - Персонажі
@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.HEROES.value)
async def cmd_heroes(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Персонажі")
    await state.set_state(MenuStates.HEROES_MENU)
    
    header = "🛡️ <b>Персонажі:</b>"
    description = (
        "У цьому розділі ви можете обрати різних персонажів гри, переглянути їхні характеристики та інші деталі.\n\n"
        "Виберіть категорію героя нижче, щоб дізнатися більше про конкретних персонажів."
    )
    
    # Відправка заголовка з героями клавіатурою
    await send_header(message, header + "\n\n" + description, get_heroes_menu())
    
    # Відправка інлайн-кнопок
    await send_inline_menu(message, "Ось ваші інлайн-опції:", get_generic_inline_keyboard())

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
        
        header = f"🧙‍♂️ <b>{hero_class} Герої:</b>"
        description = (
            f"Виберіть героя з класу **{hero_class}**, щоб переглянути його характеристики та інші деталі."
        )
        
        # Відправка заголовка з класовою клавіатурою
        await send_header(message, header + "\n\n" + description, get_hero_class_menu(hero_class))
        
        # Відправка інлайн-кнопок
        await send_inline_menu(message, "Ось ваші інлайн-опції:", get_generic_inline_keyboard())
    else:
        logger.warning(f"Невідомий клас героїв: {message.text}")
        header = "❗ <b>Невідома команда:</b>"
        description = (
            "Вибачте, я не розумію цю команду. Скористайтеся меню нижче, щоб обрати доступні опції."
        )
        
        # Відправка заголовка з героями клавіатурою
        await send_header(message, header + "\n\n" + description, get_heroes_menu())
        
        # Відправка інлайн-кнопок
        await send_inline_menu(message, "Ось ваші інлайн-опції:", get_generic_inline_keyboard())

# Розділ "Персонажі" - Пошук героя
@router.message(MenuStates.HEROES_MENU, F.text == MenuButton.SEARCH_HERO.value)
async def cmd_search_hero(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Пошук Персонажа")
    await state.set_state(MenuStates.SEARCH_HERO)
    
    header = "🔎 <b>Пошук Персонажа:</b>"
    description = (
        "Введіть ім'я героя, якого ви шукаєте. Бот надасть інформацію про цього героя, якщо він існує."
    )
    
    # Відправка заголовка без спеціальної клавіатури (можна залишити пустою)
    await send_header(message, header + "\n\n" + description, types.ReplyKeyboardRemove())
    
    # Відправка інлайн-кнопок
    await send_inline_menu(message, "Ось ваші інлайн-опції:", get_generic_inline_keyboard())

# Розділ "Персонажі" - Порівняння
@router.message(MenuStates.HEROES_MENU, F.text == MenuButton.COMPARISON.value)
async def cmd_comparison(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Порівняння")
    
    header = "⚖️ <b>Порівняння Героїв:</b>"
    description = (
        "Функція порівняння героїв ще в розробці. Слідкуйте за оновленнями!"
    )
    
    # Відправка заголовка з героями клавіатурою
    await send_header(message, header + "\n\n" + description, get_heroes_menu())
    
    # Відправка інлайн-кнопок
    await send_inline_menu(message, "Ось ваші інлайн-опції:", get_generic_inline_keyboard())

# Розділ "Персонажі" - Назад до навігації
@router.message(MenuStates.HEROES_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_navigation_from_heroes(message: Message, state: FSMContext):
    await state.set_state(MenuStates.NAVIGATION_MENU)
    
    header = "🔙 <b>Повернення до меню Навігація:</b>"
    description = (
        "Ви повернулися до меню Навігація. Оберіть нову опцію нижче."
    )
    
    # Відправка заголовка з навігаційною клавіатурою
    await send_header(message, header + "\n\n" + description, get_navigation_menu())
    
    # Відправка інлайн-кнопок
    await send_inline_menu(message, "Ось ваші інлайн-опції:", get_generic_inline_keyboard())

# Обробники для вибору героя з класу
all_heroes = set()
for heroes in heroes_by_class.values():
    all_heroes.update(heroes)

@router.message(MenuStates.HERO_CLASS_MENU, F.text.in_(all_heroes))
async def cmd_select_hero(message: Message, state: FSMContext):
    hero_name = message.text
    logger.info(f"Користувач {message.from_user.id} обрав героя {hero_name}")
    await state.set_state(MenuStates.MAIN_MENU)
    
    header = f"🎯 <b>{hero_name}:</b>"
    description = (
        f"Ви обрали героя **{hero_name}**. Інформація про героя буде додана пізніше.\n\n"
        f"Поверніться до головного меню або оберіть іншу опцію."
    )
    
    # Відправка заголовка з основною клавіатурою
    await send_header(message, header + "\n\n" + description, get_main_menu())
    
    # Відправка інлайн-кнопок
    await send_inline_menu(message, "Ось ваші інлайн-опції:", get_generic_inline_keyboard())

@router.message(MenuStates.HERO_CLASS_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_heroes_menu(message: Message, state: FSMContext):
    await state.set_state(MenuStates.HEROES_MENU)
    
    header = "🔙 <b>Повернення до меню Персонажі:</b>"
    description = (
        "Ви повернулися до меню Персонажі. Оберіть нову категорію героя нижче."
    )
    
    # Відправка заголовка з героями клавіатурою
    await send_header(message, header + "\n\n" + description, get_heroes_menu())
    
    # Відправка інлайн-кнопок
    await send_inline_menu(message, "Ось ваші інлайн-опції:", get_generic_inline_keyboard())

# Решта обробників меню, профілю, гайдів, білдів, голосувань тощо,
# повинні бути оновлені аналогічно: використовувати send_header та send_inline_menu,
# щоб відправляти лише два повідомлення.

# Обробники для інлайн-кнопок
@router.callback_query(F.data == CallbackData.HEROES.value)
async def handle_inline_heroes(call: CallbackQuery, state: FSMContext):
    logger.info(f"Користувач {call.from_user.id} натиснув інлайн-кнопку Персонажі")
    await call.message.answer("Ви натиснули на інлайн-кнопку Персонажі")
    await call.answer()

@router.callback_query(F.data == CallbackData.GUIDES.value)
async def handle_inline_guides(call: CallbackQuery, state: FSMContext):
    logger.info(f"Користувач {call.from_user.id} натиснув інлайн-кнопку Гайди")
    await call.message.answer("Ви натиснули на інлайн-кнопку Гайди")
    await call.answer()

@router.callback_query(F.data == CallbackData.BUILDS.value)
async def handle_inline_builds(call: CallbackQuery, state: FSMContext):
    logger.info(f"Користувач {call.from_user.id} натиснув інлайн-кнопку Білди")
    await call.message.answer("Ви натиснули на інлайн-кнопку Білди")
    await call.answer()

@router.callback_query(F.data == CallbackData.STATISTICS.value)
async def handle_inline_statistics(call: CallbackQuery, state: FSMContext):
    logger.info(f"Користувач {call.from_user.id} натиснув інлайн-кнопку Статистика")
    await call.message.answer("Ви натиснули на інлайн-кнопку Статистика")
    await call.answer()

@router.callback_query(F.data == CallbackData.BACK.value)
async def handle_inline_back(call: CallbackQuery, state: FSMContext):
    logger.info(f"Користувач {call.from_user.id} натиснув інлайн-кнопку Назад")
    await call.message.answer("Ви натиснули на інлайн-кнопку Назад")
    await call.answer()

# Обробник для вибору героя через інлайн-кнопки
@router.callback_query(F.data.startswith("hero_"))
async def handle_hero_selection(call: CallbackQuery, state: FSMContext):
    hero_name = call.data.split("_", 1)[1].capitalize()
    logger.info(f"Користувач {call.from_user.id} обрав героя {hero_name}")
    await call.message.answer(f"Ви обрали героя {hero_name}. Інформація про героя буде додана пізніше.")
    await call.answer()

# Обробник для невідомих повідомлень
@router.message()
async def unknown_command(message: Message, state: FSMContext):
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")
    current_state = await state.get_state()
    
    if current_state == MenuStates.MAIN_MENU.state:
        reply_markup = get_main_menu()
        header = "❗ <b>Невідома команда:</b>"
        description = (
            "Вибачте, я не розумію цю команду. Скористайтеся меню нижче, щоб обрати доступні опції."
        )
    elif current_state == MenuStates.NAVIGATION_MENU.state:
        reply_markup = get_navigation_menu()
        header = "❗ <b>Невідома команда:</b>"
        description = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій навігації."
        )
    elif current_state == MenuStates.HEROES_MENU.state:
        reply_markup = get_heroes_menu()
        header = "❗ <b>Невідома команда:</b>"
        description = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних категорій героїв."
        )
    elif current_state == MenuStates.HERO_CLASS_MENU.state:
        data = await state.get_data()
        hero_class = data.get('hero_class', 'Танк')
        reply_markup = get_hero_class_inline_keyboard(hero_class)
        header = "❗ <b>Невідома команда:</b>"
        description = (
            f"Вибачте, я не розумію цю команду. Виберіть героя з класу <b>{hero_class}</b>."
        )
    elif current_state == MenuStates.GUIDES_MENU.state:
        reply_markup = get_guides_menu()
        header = "❗ <b>Невідома команда:</b>"
        description = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій гайдів."
        )
    elif current_state == MenuStates.COUNTER_PICKS_MENU.state:
        reply_markup = get_counter_picks_menu()
        header = "❗ <b>Невідома команда:</b>"
        description = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій контр-піків."
        )
    elif current_state == MenuStates.BUILDS_MENU.state:
        reply_markup = get_builds_menu()
        header = "❗ <b>Невідома команда:</b>"
        description = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій білдів."
        )
    elif current_state == MenuStates.VOTING_MENU.state:
        reply_markup = get_voting_menu()
        header = "❗ <b>Невідома команда:</b>"
        description = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій голосування."
        )
    elif current_state == MenuStates.PROFILE_MENU.state:
        reply_markup = get_profile_menu()
        header = "❗ <b>Невідома команда:</b>"
        description = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій профілю."
        )
    elif current_state == MenuStates.STATISTICS_MENU.state:
        reply_markup = get_statistics_menu()
        header = "❗ <b>Невідома команда:</b>"
        description = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій статистики."
        )
    elif current_state == MenuStates.ACHIEVEMENTS_MENU.state:
        reply_markup = get_achievements_menu()
        header = "❗ <b>Невідома команда:</b>"
        description = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій досягнень."
        )
    elif current_state == MenuStates.SETTINGS_MENU.state:
        reply_markup = get_settings_menu()
        header = "❗ <b>Невідома команда:</b>"
        description = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій налаштувань."
        )
    elif current_state == MenuStates.FEEDBACK_MENU.state:
        reply_markup = get_feedback_menu()
        header = "❗ <b>Невідома команда:</b>"
        description = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій зворотного зв'язку."
        )
    elif current_state == MenuStates.HELP_MENU.state:
        reply_markup = get_help_menu()
        header = "❗ <b>Невідома команда:</b>"
        description = (
            "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій допомоги."
        )
    else:
        reply_markup = get_main_menu()
        await state.set_state(MenuStates.MAIN_MENU)
        header = "❗ <b>Невідома команда:</b>"
        description = (
            "Вибачте, я не розумію цю команду. Скористайтеся меню нижче, щоб обрати доступні опції."
        )
    
    # Відправка заголовка з відповідною клавіатурою
    await send_header(message, header + "\n\n" + description, reply_markup)
    
    # Відправка інлайн-кнопок
    await send_inline_menu(message, "Ось ваші інлайн-опції:", get_generic_inline_keyboard())

# Функція для налаштування обробників
def setup_handlers(dp):
    dp.include_router(router)
