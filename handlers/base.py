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
    # get_hero_class_menu,  # Видалено
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
from utils.message_formatter import MessageFormatter

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
    CHANGE_USERNAME = State()
    SEND_FEEDBACK = State()
    REPORT_BUG = State()
    SEARCH_HERO = State()
    # Додайте інші стани за потреби

async def send_formatted_menu(message: Message, title: str, description: str, options: list = None, reply_markup = None):
    """
    Надсилає відформатоване меню
     
    :param message: Об'єкт повідомлення
    :param title: Заголовок меню
    :param description: Опис меню
    :param options: Список доступних опцій (опціонально)
    :param reply_markup: Клавіатура (опціонально)
    """
    header, content = MessageFormatter.create_menu_message(title, description, options)
    
    # Надсилаємо заголовок
    await message.answer(text=header)
    
    # Надсилаємо контент з клавіатурою
    await message.answer(
        text=content,
        reply_markup=reply_markup
    )

# Команда /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user_name = message.from_user.first_name
    logger.info(f"Користувач {message.from_user.id} викликав /start")
    await state.set_state(MenuStates.MAIN_MENU)
    
    title = "👋 Вітаємо у Mobile Legends Tournament Bot!"
    description = (
        "🎮 Цей бот допоможе вам:\n"
        "• Організовувати турніри\n"
        "• Зберігати скріншоти персонажів\n"
        "• Відстежувати активність\n"
        "• Отримувати досягнення\n\n"
        "Оберіть опцію з меню нижче 👇"
    )
    options = [
        MenuButton.NAVIGATION.value,
        MenuButton.PROFILE.value
    ]
    await send_formatted_menu(
        message=message,
        title=title,
        description=description,
        options=options,
        reply_markup=get_main_menu()
    )

# Головне Меню - Навігація
@router.message(MenuStates.MAIN_MENU, F.text == MenuButton.NAVIGATION.value)
async def cmd_navigation(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Навігацію")
    await state.set_state(MenuStates.NAVIGATION_MENU)
    
    title = "🧭 Навігація"
    description = (
        "У цьому меню ви можете обрати різні розділи, такі як Персонажі, Гайди, Контр-піки, Білди, та Голосування.\n\n"
        "Оберіть відповідну опцію нижче, щоб перейти до більш детальної інформації."
    )
    options = [
        MenuButton.HEROES.value,
        MenuButton.GUIDES.value,
        MenuButton.COUNTER_PICKS.value,
        MenuButton.BUILDS.value,
        MenuButton.VOTING.value,
        MenuButton.BACK.value
    ]
    await send_formatted_menu(
        message=message,
        title=title,
        description=description,
        options=options,
        reply_markup=get_navigation_menu()
    )

# Головне Меню - Мій Профіль
@router.message(MenuStates.MAIN_MENU, F.text == MenuButton.PROFILE.value)
async def cmd_profile(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Мій Профіль")
    await state.set_state(MenuStates.PROFILE_MENU)
    
    title = "🪪 Мій Профіль"
    description = (
        "У цьому розділі ви можете переглядати та редагувати свій профіль, переглядати статистику, досягнення, налаштування та інше.\n\n"
        "Оберіть опцію профілю нижче для подальших дій."
    )
    options = [
        MenuButton.STATISTICS.value,
        MenuButton.ACHIEVEMENTS.value,
        MenuButton.SETTINGS.value,
        MenuButton.FEEDBACK.value,
        MenuButton.HELP.value,
        MenuButton.BACK_TO_MAIN_MENU.value
    ]
    await send_formatted_menu(
        message=message,
        title=title,
        description=description,
        options=options,
        reply_markup=get_profile_menu()
    )

# Розділ "Навігація" - Персонажі
@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.HEROES.value)
async def cmd_heroes(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Персонажі")
    await state.set_state(MenuStates.HEROES_MENU)
    
    title = "🛡️ Персонажі"
    description = "Оберіть категорію героїв для перегляду:"
    options = [
        "Танки - Витривалі захисники",
        "Маги - Майстри магії",
        "Стрільці - Атака здалеку",
        "Асасіни - Швидкі вбивці",
        "Підтримка - Допомога команді",
        "Бійці - Універсальні воїни",
        MenuButton.BACK.value
    ]
    await send_formatted_menu(
        message=message,
        title=title,
        description=description,
        options=options,
        reply_markup=get_heroes_menu()
    )

# Розділ "Навігація" - Гайди
@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.GUIDES.value)
async def cmd_guides(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Гайди")
    await state.set_state(MenuStates.GUIDES_MENU)
    
    title = "📚 Гайди"
    description = "Оберіть розділ гайдів:"
    options = [
        "Нові гайди - Свіжі статті",
        "Популярні гайди - Найкращі гайди",
        "Для початківців - Основи гри",
        "Просунуті техніки - Для досвідчених",
        "Командна гра - Взаємодія в команді",
        MenuButton.BACK.value
    ]
    await send_formatted_menu(
        message=message,
        title=title,
        description=description,
        options=options,
        reply_markup=get_guides_menu()
    )

# Розділ "Навігація" - Контр-піки
@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.COUNTER_PICKS.value)
async def cmd_counter_picks(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Контр-піки")
    await state.set_state(MenuStates.COUNTER_PICKS_MENU)
    
    title = "⚖️ Контр-піки"
    description = "Оберіть опцію контр-піків:"
    options = [
        "Пошук Контр-піку - 🔍",
        "Список Персонажів - 📃",
        MenuButton.BACK.value
    ]
    await send_formatted_menu(
        message=message,
        title=title,
        description=description,
        options=options,
        reply_markup=get_counter_picks_menu()
    )

# Розділ "Навігація" - Білди
@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.BUILDS.value)
async def cmd_builds(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Білди")
    await state.set_state(MenuStates.BUILDS_MENU)
    
    title = "⚜️ Білди"
    description = "Оберіть опцію білдів:"
    options = [
        "Створити Білд - ➕",
        "Мої Білди - 📁",
        "Популярні Білди - 🌟",
        MenuButton.BACK.value
    ]
    await send_formatted_menu(
        message=message,
        title=title,
        description=description,
        options=options,
        reply_markup=get_builds_menu()
    )

# Розділ "Навігація" - Голосування
@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.VOTING.value)
async def cmd_voting(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Голосування")
    await state.set_state(MenuStates.VOTING_MENU)
    
    title = "📊 Голосування"
    description = "Оберіть опцію голосування:"
    options = [
        "Поточні Опитування - 🗳️",
        "Мої Голосування - 🗳️",
        "Запропонувати Тему - 💡",
        MenuButton.BACK.value
    ]
    await send_formatted_menu(
        message=message,
        title=title,
        description=description,
        options=options,
        reply_markup=get_voting_menu()
    )

# Розділ "Навігація" - Назад до головного меню
@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_main_from_navigation(message: Message, state: FSMContext):
    await state.set_state(MenuStates.MAIN_MENU)
    
    title = "🔙 Повернення до головного меню"
    description = "Ви повернулися до головного меню. Оберіть нову опцію нижче."
    options = [
        MenuButton.NAVIGATION.value,
        MenuButton.PROFILE.value
    ]
    await send_formatted_menu(
        message=message,
        title=title,
        description=description,
        options=options,
        reply_markup=get_main_menu()
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
        
        title = f"🧙‍♂️ {hero_class} Герої"
        description = f"Виберіть героя з класу <b>{hero_class}</b>, щоб переглянути його характеристики та інші деталі."
        options = heroes_by_class.get(hero_class, []) + [MenuButton.BACK.value]
        
        await send_formatted_menu(
            message=message,
            title=title,
            description=description,
            options=options,
            reply_markup=get_hero_class_inline_keyboard(hero_class)
        )
    else:
        logger.warning(f"Невідомий клас героїв: {message.text}")
        title = "❗ Невідома команда"
        description = "Вибачте, я не розумію цю команду. Скористайтеся меню нижче."
        options = [
            MenuButton.TANK.value,
            MenuButton.MAGE.value,
            MenuButton.MARKSMAN.value,
            MenuButton.ASSASSIN.value,
            MenuButton.SUPPORT.value,
            MenuButton.FIGHTER.value,
            MenuButton.COMPARISON.value,
            MenuButton.SEARCH_HERO.value,
            MenuButton.BACK.value
        ]
        await send_formatted_menu(
            message=message,
            title=title,
            description=description,
            options=options,
            reply_markup=get_heroes_menu()
        )

# Розділ "Персонажі" - Пошук героя
@router.message(MenuStates.HEROES_MENU, F.text == MenuButton.SEARCH_HERO.value)
async def cmd_search_hero(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Пошук Персонажа")
    await state.set_state(MenuStates.SEARCH_HERO)
    
    title = "🔎 Пошук Персонажа"
    description = "Введіть ім'я героя, якого ви шукаєте. Бот надасть інформацію про цього героя, якщо він існує."
    options = []
    await send_formatted_menu(
        message=message,
        title=title,
        description=description,
        options=options,
        reply_markup=get_generic_inline_keyboard()
    )
    # Додатково налаштуйте обробник для стану SEARCH_HERO

# Розділ "Персонажі" - Порівняння
@router.message(MenuStates.HEROES_MENU, F.text == MenuButton.COMPARISON.value)
async def cmd_comparison(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Порівняння")
    title = "⚖️ Порівняння Героїв"
    description = "Функція порівняння героїв ще в розробці. Слідкуйте за оновленнями!"
    options = [
        MenuButton.BACK.value
    ]
    await send_formatted_menu(
        message=message,
        title=title,
        description=description,
        options=options,
        reply_markup=get_heroes_menu()
    )

# Розділ "Персонажі" - Назад до навігації
@router.message(MenuStates.HEROES_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_navigation_from_heroes(message: Message, state: FSMContext):
    await state.set_state(MenuStates.NAVIGATION_MENU)
    
    title = "🔙 Повернення до меню Навігація"
    description = "Ви повернулися до меню Навігація. Оберіть нову опцію нижче."
    options = [
        MenuButton.HEROES.value,
        MenuButton.GUIDES.value,
        MenuButton.COUNTER_PICKS.value,
        MenuButton.BUILDS.value,
        MenuButton.VOTING.value,
        MenuButton.BACK.value
    ]
    await send_formatted_menu(
        message=message,
        title=title,
        description=description,
        options=options,
        reply_markup=get_navigation_menu()
    )

# Обробники для вибору героя з класу через інлайн-кнопки
@router.callback_query(F.data.startswith("hero:"))
async def cmd_select_hero_callback(call: CallbackQuery, state: FSMContext):
    hero_name = call.data.split("hero:")[1]
    logger.info(f"Користувач {call.from_user.id} обрав героя {hero_name}")
    await state.set_state(MenuStates.MAIN_MENU)
    
    title = f"🎯 {hero_name}"
    description = (
        f"Ви обрали героя <b>{hero_name}</b>. Інформація про героя буде додана пізніше.\n\n"
        f"Поверніться до головного меню або оберіть іншу опцію."
    )
    options = [
        MenuButton.NAVIGATION.value,
        MenuButton.PROFILE.value
    ]
    await send_formatted_menu(
        message=call.message,
        title=title,
        description=description,
        options=options,
        reply_markup=get_main_menu()
    )
    await call.answer()

# Обробники для інлайн-кнопок
@router.callback_query(F.data == "search_hero")
async def handle_search_hero(call: CallbackQuery, state: FSMContext):
    await state.set_state(MenuStates.SEARCH_HERO)
    title = "🔎 Пошук Персонажа"
    description = "Введіть ім'я героя, якого ви шукаєте. Бот надасть інформацію про цього героя, якщо він існує."
    options = []
    await send_formatted_menu(
        message=call.message,
        title=title,
        description=description,
        options=options,
        reply_markup=get_generic_inline_keyboard()
    )
    await call.answer()

@router.callback_query(F.data == "statistics")
async def handle_statistics(call: CallbackQuery, state: FSMContext):
    await state.set_state(MenuStates.STATISTICS_MENU)
    title = "📊 Статистика"
    description = "Оберіть тип статистики, яку ви хочете переглянути."
    options = [
        MenuButton.ACTIVITY.value,
        MenuButton.RANKING.value,
        MenuButton.GAME_STATS.value,
        MenuButton.BACK_TO_PROFILE.value
    ]
    await send_formatted_menu(
        message=call.message,
        title=title,
        description=description,
        options=options,
        reply_markup=get_statistics_menu()
    )
    await call.answer()

@router.callback_query(F.data == "back")
async def handle_back(call: CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    
    if current_state == MenuStates.NAVIGATION_MENU.state:
        title = "🔙 Повернення до головного меню"
        description = "Ви повернулися до головного меню. Оберіть нову опцію нижче."
        options = [
            MenuButton.NAVIGATION.value,
            MenuButton.PROFILE.value
        ]
        reply_markup = get_main_menu()
    elif current_state == MenuStates.HERO_CLASS_MENU.state:
        data = await state.get_data()
        hero_class = data.get('hero_class', 'Танк')
        title = f"🔙 Повернення до меню Персонажі - {hero_class}"
        description = "Ви повернулися до меню Персонажі. Оберіть нову категорію героя нижче."
        options = [
            MenuButton.TANK.value,
            MenuButton.MAGE.value,
            MenuButton.MARKSMAN.value,
            MenuButton.ASSASSIN.value,
            MenuButton.SUPPORT.value,
            MenuButton.FIGHTER.value,
            MenuButton.COMPARISON.value,
            MenuButton.SEARCH_HERO.value,
            MenuButton.BACK.value
        ]
        reply_markup = get_heroes_menu()
    elif current_state == MenuStates.GUIDES_MENU.state:
        title = "🔙 Повернення до меню Гайди"
        description = "Ви повернулися до меню Гайди. Оберіть нову опцію нижче."
        options = [
            "Нові гайди - Свіжі статті",
            "Популярні гайди - Найкращі гайди",
            "Для початківців - Основи гри",
            "Просунуті техніки - Для досвідчених",
            "Командна гра - Взаємодія в команді",
            MenuButton.BACK.value
        ]
        reply_markup = get_guides_menu()
    # Додайте інші умови для інших станів при необхідності
    else:
        # Відповідь за замовчуванням
        title = "🔙 Повернення до головного меню"
        description = "Ви повернулися до головного меню. Оберіть нову опцію нижче."
        options = [
            MenuButton.NAVIGATION.value,
            MenuButton.PROFILE.value
        ]
        reply_markup = get_main_menu()
    
    await send_formatted_menu(
        message=call.message,
        title=title,
        description=description,
        options=options,
        reply_markup=reply_markup
    )
    await call.answer()

# Обробник для невідомих повідомлень
@router.message()
async def unknown_command(message: Message, state: FSMContext):
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")
    current_state = await state.get_state()
    
    if current_state == MenuStates.MAIN_MENU.state:
        title = "❗ Невідома команда"
        description = "Вибачте, я не розумію цю команду. Скористайтеся меню нижче, щоб обрати доступні опції."
        options = [
            MenuButton.NAVIGATION.value,
            MenuButton.PROFILE.value
        ]
        reply_markup = get_main_menu()
    elif current_state == MenuStates.NAVIGATION_MENU.state:
        title = "❗ Невідома команда"
        description = "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій навігації."
        options = [
            MenuButton.HEROES.value,
            MenuButton.GUIDES.value,
            MenuButton.COUNTER_PICKS.value,
            MenuButton.BUILDS.value,
            MenuButton.VOTING.value,
            MenuButton.BACK.value
        ]
        reply_markup = get_navigation_menu()
    elif current_state == MenuStates.HEROES_MENU.state:
        title = "❗ Невідома команда"
        description = "Вибачте, я не розумію цю команду. Виберіть одну з доступних категорій героїв."
        options = [
            "Танки - Витривалі захисники",
            "Маги - Майстри магії",
            "Стрільці - Атака здалеку",
            "Асасіни - Швидкі вбивці",
            "Підтримка - Допомога команді",
            "Бійці - Універсальні воїни",
            MenuButton.BACK.value
        ]
        reply_markup = get_heroes_menu()
    elif current_state == MenuStates.HERO_CLASS_MENU.state:
        data = await state.get_data()
        hero_class = data.get('hero_class', 'Танк')
        title = "❗ Невідома команда"
        description = f"Вибачте, я не розумію цю команду. Виберіть героя з класу <b>{hero_class}</b>."
        options = heroes_by_class.get(hero_class, []) + [MenuButton.BACK.value]
        reply_markup = get_hero_class_inline_keyboard(hero_class)
    elif current_state == MenuStates.GUIDES_MENU.state:
        title = "❗ Невідома команда"
        description = "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій гайдів."
        options = [
            "Нові гайди - Свіжі статті",
            "Популярні гайди - Найкращі гайди",
            "Для початківців - Основи гри",
            "Просунуті техніки - Для досвідчених",
            "Командна гра - Взаємодія в команді",
            MenuButton.BACK.value
        ]
        reply_markup = get_guides_menu()
    elif current_state == MenuStates.COUNTER_PICKS_MENU.state:
        title = "❗ Невідома команда"
        description = "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій контр-піків."
        options = [
            "Пошук Контр-піку - 🔍",
            "Список Персонажів - 📃",
            MenuButton.BACK.value
        ]
        reply_markup = get_counter_picks_menu()
    elif current_state == MenuStates.BUILDS_MENU.state:
        title = "❗ Невідома команда"
        description = "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій білдів."
        options = [
            "Створити Білд - ➕",
            "Мої Білди - 📁",
            "Популярні Білди - 🌟",
            MenuButton.BACK.value
        ]
        reply_markup = get_builds_menu()
    elif current_state == MenuStates.VOTING_MENU.state:
        title = "❗ Невідома команда"
        description = "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій голосування."
        options = [
            "Поточні Опитування - 🗳️",
            "Мої Голосування - 🗳️",
            "Запропонувати Тему - 💡",
            MenuButton.BACK.value
        ]
        reply_markup = get_voting_menu()
    elif current_state == MenuStates.PROFILE_MENU.state:
        title = "❗ Невідома команда"
        description = "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій профілю."
        options = [
            MenuButton.STATISTICS.value,
            MenuButton.ACHIEVEMENTS.value,
            MenuButton.SETTINGS.value,
            MenuButton.FEEDBACK.value,
            MenuButton.HELP.value,
            MenuButton.BACK_TO_MAIN_MENU.value
        ]
        reply_markup = get_profile_menu()
    elif current_state == MenuStates.STATISTICS_MENU.state:
        title = "❗ Невідома команда"
        description = "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій статистики."
        options = [
            MenuButton.ACTIVITY.value,
            MenuButton.RANKING.value,
            MenuButton.GAME_STATS.value,
            MenuButton.BACK_TO_PROFILE.value
        ]
        reply_markup = get_statistics_menu()
    elif current_state == MenuStates.ACHIEVEMENTS_MENU.state:
        title = "❗ Невідома команда"
        description = "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій досягнень."
        options = [
            "Мої Бейджі - 🏅",
            "Прогрес - 📊",
            "Турнірна Статистика - 🏆",
            "Отримані Нагороди - 🏆",
            MenuButton.BACK_TO_PROFILE.value
        ]
        reply_markup = get_achievements_menu()
    elif current_state == MenuStates.SETTINGS_MENU.state:
        title = "❗ Невідома команда"
        description = "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій налаштувань."
        options = [
            "Мова Інтерфейсу - 🌐",
            "Змінити Username - ✏️",
            "Оновити ID Гравця - 🔄",
            "Сповіщення - 🔔",
            MenuButton.BACK_TO_PROFILE.value
        ]
        reply_markup = get_settings_menu()
    elif current_state == MenuStates.FEEDBACK_MENU.state:
        title = "❗ Невідома команда"
        description = "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій зворотного зв'язку."
        options = [
            "Надіслати Відгук - 📤",
            "Повідомити про Помилку - 🐞",
            MenuButton.BACK_TO_PROFILE.value
        ]
        reply_markup = get_feedback_menu()
    elif current_state == MenuStates.HELP_MENU.state:
        title = "❗ Невідома команда"
        description = "Вибачте, я не розумію цю команду. Виберіть одну з доступних опцій допомоги."
        options = [
            "Інструкції - 📖",
            "FAQ - ❓",
            "Підтримка - 🆘",
            MenuButton.BACK_TO_PROFILE.value
        ]
        reply_markup = get_help_menu()
    else:
        title = "❗ Невідома команда"
        description = "Вибачте, я не розумію цю команду. Скористайтеся меню нижче, щоб обрати доступні опції."
        options = [
            MenuButton.NAVIGATION.value,
            MenuButton.PROFILE.value
        ]
        reply_markup = get_main_menu()
        await state.set_state(MenuStates.MAIN_MENU)
    
    await send_formatted_menu(
        message=message,
        title=title,
        description=description,
        options=options,
        reply_markup=reply_markup
    )

# Розділ "Підрозділи "Статистика" - Назад до профілю
@router.message(MenuStates.STATISTICS_MENU, F.text == MenuButton.BACK_TO_PROFILE.value)
async def cmd_back_to_profile_from_statistics(message: Message, state: FSMContext):
    await state.set_state(MenuStates.PROFILE_MENU)
    
    title = "🔙 Повернення до меню Профіль"
    description = "Ви повернулися до меню Профіль. Оберіть нову опцію нижче."
    options = [
        MenuButton.STATISTICS.value,
        MenuButton.ACHIEVEMENTS.value,
        MenuButton.SETTINGS.value,
        MenuButton.FEEDBACK.value,
        MenuButton.HELP.value,
        MenuButton.BACK_TO_MAIN_MENU.value
    ]
    await send_formatted_menu(
        message=message,
        title=title,
        description=description,
        options=options,
        reply_markup=get_profile_menu()
    )

# Аналогічно оновіть інші розділи: Досягнення, Налаштування, Зворотний Зв'язок, Допомога

# Додаткові Обробники для Нових Станів

@router.message(MenuStates.CHANGE_USERNAME)
async def handle_change_username(message: Message, state: FSMContext):
    new_username = message.text.strip()
    # Додайте логіку для зміни Username
    logger.info(f"Користувач {message.from_user.id} змінює Username на {new_username}")
    await message.answer(
        f"Ваш Username було успішно змінено на <b>{new_username}</b>.",
        reply_markup=get_profile_menu()
    )
    await state.set_state(MenuStates.PROFILE_MENU)

@router.message(MenuStates.SEND_FEEDBACK)
async def handle_send_feedback(message: Message, state: FSMContext):
    feedback = message.text.strip()
    # Додайте логіку для обробки відгуку, наприклад, зберігання або надсилання на електронну пошту
    logger.info(f"Користувач {message.from_user.id} надіслав відгук: {feedback}")
    await message.answer(
        "Дякуємо за ваш відгук! Ми цінуємо ваші думки.",
        reply_markup=get_profile_menu()
    )
    await state.set_state(MenuStates.PROFILE_MENU)

@router.message(MenuStates.REPORT_BUG)
async def handle_report_bug(message: Message, state: FSMContext):
    bug_report = message.text.strip()
    # Додайте логіку для обробки звіту про помилку
    logger.info(f"Користувач {message.from_user.id} повідомив про помилку: {bug_report}")
    await message.answer(
        "Дякуємо за повідомлення про помилку! Ми швидко її виправимо.",
        reply_markup=get_profile_menu()
    )
    await state.set_state(MenuStates.PROFILE_MENU)

# Функція для налаштування обробників
def setup_handlers(dp):
    dp.include_router(router)
