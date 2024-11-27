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
    # Додайте інші стани за потреби

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

# Розділ "Навігація" - Гайди
@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.GUIDES.value)
async def cmd_guides(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Гайди")
    await state.set_state(MenuStates.GUIDES_MENU)
    
    description = "📚 <b>Гайди:</b>"
    detailed_text = (
        "У цьому розділі ви можете знайти різноманітні гайди для покращення вашої гри, навчання новим стратегіям та технікам.\n\n"
        "Виберіть підрозділ гайдів нижче для більш детальної інформації."
    )
    await send_menu_response(message, description, detailed_text, get_guides_menu())

# Розділ "Навігація" - Контр-піки
@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.COUNTER_PICKS.value)
async def cmd_counter_picks(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Контр-піки")
    await state.set_state(MenuStates.COUNTER_PICKS_MENU)
    
    description = "⚖️ <b>Контр-піки:</b>"
    detailed_text = (
        "У цьому розділі ви можете дізнатися, які персонажі є ефективними контр-піками проти інших героїв.\n\n"
        "Виберіть опцію контр-піків нижче для перегляду списку."
    )
    await send_menu_response(message, description, detailed_text, get_counter_picks_menu())

# Розділ "Навігація" - Білди
@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.BUILDS.value)
async def cmd_builds(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Білди")
    await state.set_state(MenuStates.BUILDS_MENU)
    
    description = "⚜️ <b>Білди:</b>"
    detailed_text = (
        "У цьому розділі ви можете переглядати та створювати білди для різних персонажів.\n\n"
        "Виберіть опцію білдів нижче для подальших дій."
    )
    await send_menu_response(message, description, detailed_text, get_builds_menu())

# Розділ "Навігація" - Голосування
@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.VOTING.value)
async def cmd_voting(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Голосування")
    await state.set_state(MenuStates.VOTING_MENU)
    
    description = "📊 <b>Голосування:</b>"
    detailed_text = (
        "У цьому розділі ви можете брати участь у голосуваннях, пропонувати теми для обговорення та переглядати результати.\n\n"
        "Виберіть опцію голосування нижче для подальших дій."
    )
    await send_menu_response(message, description, detailed_text, get_voting_menu())

# Розділ "Навігація" - Назад до головного меню
@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_main_from_navigation(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} повернувся до головного меню")
    await state.set_state(MenuStates.MAIN_MENU)
    
    description = "🔙 <b>Повернення до головного меню:</b>"
    detailed_text = (
        "Ви повернулися до головного меню. Оберіть нову опцію нижче."
    )
    await send_menu_response(message, description, detailed_text, get_main_menu())

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
            f"Виберіть героя з класу <b>{hero_class}</b>, щоб переглянути його характеристики та інші деталі."
        )
        await send_menu_response(message, description, detailed_text, get_hero_class_inline_keyboard(hero_class))
    else:
        logger.warning(f"Невідомий клас героїв: {message.text}")
        description = "❗ <b>Невідома команда:</b>"
        detailed_text = (
            "Вибачте, я не розумію цю команду. Скористайтеся меню нижче, щоб обрати доступні опції."
        )
        await send_menu_response(message, description, detailed_text, get_heroes_menu())

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

# Розділ "Персонажі" - Порівняння
@router.message(MenuStates.HEROES_MENU, F.text == MenuButton.COMPARISON.value)
async def cmd_comparison(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Порівняння")
    description = "⚖️ <b>Порівняння Героїв:</b>"
    detailed_text = (
        "Функція порівняння героїв ще в розробці. Слідкуйте за оновленнями!"
    )
    await send_menu_response(message, description, detailed_text, get_heroes_menu())

# Розділ "Персонажі" - Назад до навігації
@router.message(MenuStates.HEROES_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_navigation_from_heroes(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} повернувся до меню Навігація")
    await state.set_state(MenuStates.NAVIGATION_MENU)
    
    description = "🔙 <b>Повернення до меню Навігація:</b>"
    detailed_text = (
        "Ви повернулися до меню Навігація. Оберіть нову опцію нижче."
    )
    await send_menu_response(message, description, detailed_text, get_navigation_menu())

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
        f"Ви обрали героя <b>{hero_name}</b>. Інформація про героя буде додана пізніше.\n\n"
        f"Поверніться до головного меню або оберіть іншу опцію."
    )
    await send_menu_response(message, description, detailed_text, get_main_menu())

@router.message(MenuStates.HERO_CLASS_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_heroes_menu(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} повернувся до меню Персонажі")
    await state.set_state(MenuStates.HEROES_MENU)
    
    description = "🔙 <b>Повернення до меню Персонажі:</b>"
    detailed_text = (
        "Ви повернулися до меню Персонажі. Оберіть нову категорію героя нижче."
    )
    await send_menu_response(message, description, detailed_text, get_heroes_menu())

# Розділ "Гайди" - Нові Гайди
@router.message(MenuStates.GUIDES_MENU, F.text == MenuButton.NEW_GUIDES.value)
async def cmd_new_guides(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Нові Гайди")
    description = "🆕 <b>Нові Гайди:</b>"
    detailed_text = (
        "Список нових гайдів ще не доступний. Будь ласка, перевірте пізніше."
    )
    await send_menu_response(message, description, detailed_text, get_guides_menu())

# Розділ "Гайди" - Популярні Гайди
@router.message(MenuStates.GUIDES_MENU, F.text == MenuButton.POPULAR_GUIDES.value)
async def cmd_popular_guides(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Популярні Гайди")
    description = "🌟 <b>Популярні Гайди:</b>"
    detailed_text = (
        "Список популярних гайдів ще не доступний. Будь ласка, перевірте пізніше."
    )
    await send_menu_response(message, description, detailed_text, get_guides_menu())

# Розділ "Гайди" - Гайди для Початківців
@router.message(MenuStates.GUIDES_MENU, F.text == MenuButton.BEGINNER_GUIDES.value)
async def cmd_beginner_guides(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Гайди для Початківців")
    description = "👶 <b>Гайди для Початківців:</b>"
    detailed_text = (
        "Список гайдів для початківців ще не доступний. Будь ласка, перевірте пізніше."
    )
    await send_menu_response(message, description, detailed_text, get_guides_menu())

# Розділ "Гайди" - Просунуті Техніки
@router.message(MenuStates.GUIDES_MENU, F.text == MenuButton.ADVANCED_TECHNIQUES.value)
async def cmd_advanced_techniques(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Просунуті Техніки")
    description = "🚀 <b>Просунуті Техніки:</b>"
    detailed_text = (
        "Список просунутих технік ще не доступний. Будь ласка, перевірте пізніше."
    )
    await send_menu_response(message, description, detailed_text, get_guides_menu())

# Розділ "Гайди" - Командна Гра
@router.message(MenuStates.GUIDES_MENU, F.text == MenuButton.TEAMPLAY_GUIDES.value)
async def cmd_teamplay_guides(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Командну Гру")
    description = "🤝 <b>Командна Гра:</b>"
    detailed_text = (
        "Список гайдів по командній грі ще не доступний. Будь ласка, перевірте пізніше."
    )
    await send_menu_response(message, description, detailed_text, get_guides_menu())

# Розділ "Гайди" - Назад до навігації
@router.message(MenuStates.GUIDES_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_navigation_from_guides(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} повернувся до меню Навігація з Гайдів")
    await state.set_state(MenuStates.NAVIGATION_MENU)
    
    description = "🔙 <b>Повернення до меню Навігація:</b>"
    detailed_text = (
        "Ви повернулися до меню Навігація. Оберіть нову опцію нижче."
    )
    await send_menu_response(message, description, detailed_text, get_navigation_menu())

# Розділ "Контр-піки" - Пошук Контр-піку
@router.message(MenuStates.COUNTER_PICKS_MENU, F.text == MenuButton.COUNTER_SEARCH.value)
async def cmd_counter_search(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Пошук Контр-піку")
    description = "🔍 <b>Пошук Контр-піку:</b>"
    detailed_text = (
        "Введіть ім'я персонажа, для якого ви хочете знайти контр-пік. Бот надасть список ефективних контр-піків."
    )
    await send_menu_response(message, description, detailed_text, get_generic_inline_keyboard())
    # Додатково можна налаштувати обробник для пошуку контр-піку

# Розділ "Контр-піки" - Список Персонажів
@router.message(MenuStates.COUNTER_PICKS_MENU, F.text == MenuButton.COUNTER_LIST.value)
async def cmd_counter_list(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Список Персонажів для Контр-піків")
    description = "📜 <b>Список Персонажів:</b>"
    detailed_text = (
        "Список персонажів для контр-піків ще не доступний. Будь ласка, перевірте пізніше."
    )
    await send_menu_response(message, description, detailed_text, get_counter_picks_menu())

# Розділ "Контр-піки" - Назад до навігації
@router.message(MenuStates.COUNTER_PICKS_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_navigation_from_counter_picks(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} повернувся до меню Навігація з Контр-піків")
    await state.set_state(MenuStates.NAVIGATION_MENU)
    
    description = "🔙 <b>Повернення до меню Навігація:</b>"
    detailed_text = (
        "Ви повернулися до меню Навігація. Оберіть нову опцію нижче."
    )
    await send_menu_response(message, description, detailed_text, get_navigation_menu())

# Розділ "Білди" - Створити Білд
@router.message(MenuStates.BUILDS_MENU, F.text == MenuButton.CREATE_BUILD.value)
async def cmd_create_build(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Створити Білд")
    description = "🛠️ <b>Створити Білд:</b>"
    detailed_text = (
        "Функція створення білді ще в розробці. Слідкуйте за оновленнями!"
    )
    await send_menu_response(message, description, detailed_text, get_builds_menu())

# Розділ "Білди" - Мої Білди
@router.message(MenuStates.BUILDS_MENU, F.text == MenuButton.MY_BUILDS.value)
async def cmd_my_builds(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Мої Білди")
    description = "📁 <b>Мої Білди:</b>"
    detailed_text = (
        "Список ваших білдів ще не доступний. Будь ласка, перевірте пізніше."
    )
    await send_menu_response(message, description, detailed_text, get_builds_menu())

# Розділ "Білди" - Популярні Білди
@router.message(MenuStates.BUILDS_MENU, F.text == MenuButton.POPULAR_BUILDS.value)
async def cmd_popular_builds(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Популярні Білди")
    description = "🔥 <b>Популярні Білди:</b>"
    detailed_text = (
        "Список популярних білдів ще не доступний. Будь ласка, перевірте пізніше."
    )
    await send_menu_response(message, description, detailed_text, get_builds_menu())

# Розділ "Білди" - Назад до навігації
@router.message(MenuStates.BUILDS_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_navigation_from_builds(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} повернувся до меню Навігація з Білдів")
    await state.set_state(MenuStates.NAVIGATION_MENU)
    
    description = "🔙 <b>Повернення до меню Навігація:</b>"
    detailed_text = (
        "Ви повернулися до меню Навігація. Оберіть нову опцію нижче."
    )
    await send_menu_response(message, description, detailed_text, get_navigation_menu())

# Розділ "Голосування" - Поточні Опитування
@router.message(MenuStates.VOTING_MENU, F.text == MenuButton.CURRENT_VOTES.value)
async def cmd_current_votes(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Поточні Опитування")
    description = "🗳️ <b>Поточні Опитування:</b>"
    detailed_text = (
        "Список поточних опитувань ще не доступний. Будь ласка, перевірте пізніше."
    )
    await send_menu_response(message, description, detailed_text, get_voting_menu())

# Розділ "Голосування" - Мої Голосування
@router.message(MenuStates.VOTING_MENU, F.text == MenuButton.MY_VOTES.value)
async def cmd_my_votes(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Мої Голосування")
    description = "📈 <b>Мої Голосування:</b>"
    detailed_text = (
        "Список ваших голосувань ще не доступний. Будь ласка, перевірте пізніше."
    )
    await send_menu_response(message, description, detailed_text, get_voting_menu())

# Розділ "Голосування" - Запропонувати Тему
@router.message(MenuStates.VOTING_MENU, F.text == MenuButton.SUGGEST_TOPIC.value)
async def cmd_suggest_topic(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Запропонувати Тему")
    description = "📝 <b>Запропонувати Тему:</b>"
    detailed_text = (
        "Будь ласка, введіть тему для пропозиції. Ваша пропозиція буде розглянута адміністрацією."
    )
    await send_menu_response(message, description, detailed_text, get_generic_inline_keyboard())
    # Додатково можна налаштувати обробник для прийому теми

# Розділ "Голосування" - Назад до навігації
@router.message(MenuStates.VOTING_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_navigation_from_voting(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} повернувся до меню Навігація з Голосувань")
    await state.set_state(MenuStates.NAVIGATION_MENU)
    
    description = "🔙 <b>Повернення до меню Навігація:</b>"
    detailed_text = (
        "Ви повернулися до меню Навігація. Оберіть нову опцію нижче."
    )
    await send_menu_response(message, description, detailed_text, get_navigation_menu())

# Розділ "Профіль" - Статистика
@router.message(MenuStates.PROFILE_MENU, F.text == MenuButton.STATISTICS.value)
async def cmd_statistics(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Статистика")
    await state.set_state(MenuStates.STATISTICS_MENU)
    
    description = "📊 <b>Статистика:</b>"
    detailed_text = (
        "У цьому розділі ви можете переглядати різноманітну статистику, пов'язану з вашою грою.\n\n"
        "Виберіть підрозділ статистики нижче для перегляду деталей."
    )
    await send_menu_response(message, description, detailed_text, get_statistics_menu())

# Розділ "Профіль" - Досягнення
@router.message(MenuStates.PROFILE_MENU, F.text == MenuButton.ACHIEVEMENTS.value)
async def cmd_achievements(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Досягнення")
    await state.set_state(MenuStates.ACHIEVEMENTS_MENU)
    
    description = "🏆 <b>Досягнення:</b>"
    detailed_text = (
        "У цьому розділі ви можете переглядати свої досягнення та бейджі, а також відстежувати свій прогрес.\n\n"
        "Виберіть підрозділ досягнень нижче для перегляду деталей."
    )
    await send_menu_response(message, description, detailed_text, get_achievements_menu())

# Розділ "Профіль" - Налаштування
@router.message(MenuStates.PROFILE_MENU, F.text == MenuButton.SETTINGS.value)
async def cmd_settings(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Налаштування")
    await state.set_state(MenuStates.SETTINGS_MENU)
    
    description = "⚙️ <b>Налаштування:</b>"
    detailed_text = (
        "У цьому розділі ви можете налаштувати параметри вашого профілю, змінити мову інтерфейсу, оновити свій Username та інше.\n\n"
        "Виберіть опцію налаштувань нижче для подальших дій."
    )
    await send_menu_response(message, description, detailed_text, get_settings_menu())

# Розділ "Профіль" - Зворотний Зв'язок
@router.message(MenuStates.PROFILE_MENU, F.text == MenuButton.FEEDBACK.value)
async def cmd_feedback(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Зворотний Зв'язок")
    await state.set_state(MenuStates.FEEDBACK_MENU)
    
    description = "💌 <b>Зворотний Зв'язок:</b>"
    detailed_text = (
        "У цьому розділі ви можете надсилати відгуки, пропозиції або повідомляти про помилки.\n\n"
        "Виберіть опцію зворотного зв'язку нижче для подальших дій."
    )
    await send_menu_response(message, description, detailed_text, get_feedback_menu())

# Розділ "Профіль" - Допомога
@router.message(MenuStates.PROFILE_MENU, F.text == MenuButton.HELP.value)
async def cmd_help(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Допомогу")
    await state.set_state(MenuStates.HELP_MENU)
    
    description = "❓ <b>Допомога:</b>"
    detailed_text = (
        "У цьому розділі ви можете знайти інструкції, FAQ або зв'язатися з підтримкою для отримання допомоги.\n\n"
        "Виберіть опцію допомоги нижче для подальших дій."
    )
    await send_menu_response(message, description, detailed_text, get_help_menu())

# Розділ "Профіль" - Назад до головного меню
@router.message(MenuStates.PROFILE_MENU, F.text == MenuButton.BACK_TO_MAIN_MENU.value)
async def cmd_back_to_main_from_profile(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} повернувся до головного меню з Профілю")
    await state.set_state(MenuStates.MAIN_MENU)
    
    description = "🔙 <b>Повернення до головного меню:</b>"
    detailed_text = (
        "Ви повернулися до головного меню. Оберіть нову опцію нижче."
    )
    await send_menu_response(message, description, detailed_text, get_main_menu())

# Підрозділи "Статистика" - Загальна Активність
@router.message(MenuStates.STATISTICS_MENU, F.text == MenuButton.ACTIVITY.value)
async def cmd_activity(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Загальну Активність")
    description = "📈 <b>Загальна Активність:</b>"
    detailed_text = (
        "Статистика загальної активності ще не доступна. Будь ласка, перевірте пізніше."
    )
    await send_menu_response(message, description, detailed_text, get_statistics_menu())

# Підрозділи "Статистика" - Рейтинг
@router.message(MenuStates.STATISTICS_MENU, F.text == MenuButton.RANKING.value)
async def cmd_ranking(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Рейтинг")
    description = "🏅 <b>Рейтинг:</b>"
    detailed_text = (
        "Рейтинг ще не доступний. Будь ласка, перевірте пізніше."
    )
    await send_menu_response(message, description, detailed_text, get_statistics_menu())

# Підрозділи "Статистика" - Ігрова Статистика
@router.message(MenuStates.STATISTICS_MENU, F.text == MenuButton.GAME_STATS.value)
async def cmd_game_stats(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Ігрову Статистику")
    description = "🎮 <b>Ігрова Статистика:</b>"
    detailed_text = (
        "Ігрова статистика ще не доступна. Будь ласка, перевірте пізніше."
    )
    await send_menu_response(message, description, detailed_text, get_statistics_menu())

# Підрозділи "Статистика" - Назад до профілю
@router.message(MenuStates.STATISTICS_MENU, F.text == MenuButton.BACK_TO_PROFILE.value)
async def cmd_back_to_profile_from_statistics(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} повернувся до Профілю з Статистики")
    await state.set_state(MenuStates.PROFILE_MENU)
    
    description = "🔙 <b>Повернення до меню Профіль:</b>"
    detailed_text = (
        "Ви повернулися до меню Профіль. Оберіть нову опцію нижче."
    )
    await send_menu_response(message, description, detailed_text, get_profile_menu())

# Підрозділи "Досягнення" - Мої Бейджі
@router.message(MenuStates.ACHIEVEMENTS_MENU, F.text == MenuButton.BADGES.value)
async def cmd_badges(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Мої Бейджі")
    description = "🎖️ <b>Мої Бейджі:</b>"
    detailed_text = (
        "Список ваших бейджів ще не доступний. Будь ласка, перевірте пізніше."
    )
    await send_menu_response(message, description, detailed_text, get_achievements_menu())

# Підрозділи "Досягнення" - Прогрес
@router.message(MenuStates.ACHIEVEMENTS_MENU, F.text == MenuButton.PROGRESS.value)
async def cmd_progress(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Прогрес")
    description = "📈 <b>Прогрес:</b>"
    detailed_text = (
        "Ваш прогрес ще не доступний. Будь ласка, перевірте пізніше."
    )
    await send_menu_response(message, description, detailed_text, get_achievements_menu())

# Підрозділи "Досягнення" - Турнірна Статистика
@router.message(MenuStates.ACHIEVEMENTS_MENU, F.text == MenuButton.TOURNAMENT_STATS.value)
async def cmd_tournament_stats(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Турнірну Статистику")
    description = "📊 <b>Турнірна Статистика:</b>"
    detailed_text = (
        "Турнірна статистика ще не доступна. Будь ласка, перевірте пізніше."
    )
    await send_menu_response(message, description, detailed_text, get_achievements_menu())

# Підрозділи "Досягнення" - Отримані Нагороди
@router.message(MenuStates.ACHIEVEMENTS_MENU, F.text == MenuButton.AWARDS.value)
async def cmd_awards(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Отримані Нагороди")
    description = "🎖️ <b>Отримані Нагороди:</b>"
    detailed_text = (
        "Список отриманих нагород ще не доступний. Будь ласка, перевірте пізніше."
    )
    await send_menu_response(message, description, detailed_text, get_achievements_menu())

# Підрозділи "Досягнення" - Назад до профілю
@router.message(MenuStates.ACHIEVEMENTS_MENU, F.text == MenuButton.BACK_TO_PROFILE.value)
async def cmd_back_to_profile_from_achievements(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} повернувся до Профілю з Досягнень")
    await state.set_state(MenuStates.PROFILE_MENU)
    
    description = "🔙 <b>Повернення до меню Профіль:</b>"
    detailed_text = (
        "Ви повернулися до меню Профіль. Оберіть нову опцію нижче."
    )
    await send_menu_response(message, description, detailed_text, get_profile_menu())

# Підрозділи "Налаштування" - Мова Інтерфейсу
@router.message(MenuStates.SETTINGS_MENU, F.text == MenuButton.LANGUAGE.value)
async def cmd_language(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Мову Інтерфейсу")
    description = "🌐 <b>Мова Інтерфейсу:</b>"
    detailed_text = (
        "Функція зміни мови ще в розробці. Будь ласка, перевірте пізніше."
    )
    await send_menu_response(message, description, detailed_text, get_settings_menu())

# Підрозділи "Налаштування" - Змінити Username
@router.message(MenuStates.SETTINGS_MENU, F.text == MenuButton.CHANGE_USERNAME.value)
async def cmd_change_username(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Змінити Username")
    description = "🔄 <b>Змінити Username:</b>"
    detailed_text = (
        "Будь ласка, введіть новий Username:"
    )
    await send_menu_response(message, description, detailed_text, get_generic_inline_keyboard())
    # Додатково можна налаштувати обробник для зміни Username

# Підрозділи "Налаштування" - Оновити ID Гравця
@router.message(MenuStates.SETTINGS_MENU, F.text == MenuButton.UPDATE_ID.value)
async def cmd_update_id(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Оновити ID Гравця")
    description = "🆔 <b>Оновити ID Гравця:</b>"
    detailed_text = (
        "Функція оновлення ID ще в розробці. Будь ласка, перевірте пізніше."
    )
    await send_menu_response(message, description, detailed_text, get_settings_menu())

# Підрозділи "Налаштування" - Сповіщення
@router.message(MenuStates.SETTINGS_MENU, F.text == MenuButton.NOTIFICATIONS.value)
async def cmd_notifications(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Сповіщення")
    description = "🔔 <b>Сповіщення:</b>"
    detailed_text = (
        "Функція налаштування сповіщень ще в розробці. Будь ласка, перевірте пізніше."
    )
    await send_menu_response(message, description, detailed_text, get_settings_menu())

# Підрозділи "Налаштування" - Назад до профілю
@router.message(MenuStates.SETTINGS_MENU, F.text == MenuButton.BACK_TO_PROFILE.value)
async def cmd_back_to_profile_from_settings(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} повернувся до Профілю з Налаштувань")
    await state.set_state(MenuStates.PROFILE_MENU)
    
    description = "🔙 <b>Повернення до меню Профіль:</b>"
    detailed_text = (
        "Ви повернулися до меню Профіль. Оберіть нову опцію нижче."
    )
    await send_menu_response(message, description, detailed_text, get_profile_menu())

# Підрозділи "Зворотний Зв'язок" - Надіслати Відгук
@router.message(MenuStates.FEEDBACK_MENU, F.text == MenuButton.SEND_FEEDBACK.value)
async def cmd_send_feedback(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Надіслати Відгук")
    description = "✉️ <b>Надіслати Відгук:</b>"
    detailed_text = (
        "Будь ласка, введіть ваш відгук. Ваші коментарі допоможуть нам покращити бот."
    )
    await send_menu_response(message, description, detailed_text, get_generic_inline_keyboard())
    # Додатково можна налаштувати обробник для прийому відгуку

# Підрозділи "Зворотний Зв'язок" - Повідомити про Помилку
@router.message(MenuStates.FEEDBACK_MENU, F.text == MenuButton.REPORT_BUG.value)
async def cmd_report_bug(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Повідомити про Помилку")
    description = "🐞 <b>Повідомити про Помилку:</b>"
    detailed_text = (
        "Будь ласка, опишіть помилку, яку ви знайшли. Ваші звіти допоможуть нам виправити проблеми."
    )
    await send_menu_response(message, description, detailed_text, get_generic_inline_keyboard())
    # Додатково можна налаштувати обробник для прийому звіту про помилку

# Підрозділи "Зворотний Зв'язок" - Назад до профілю
@router.message(MenuStates.FEEDBACK_MENU, F.text == MenuButton.BACK_TO_PROFILE.value)
async def cmd_back_to_profile_from_feedback(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} повернувся до Профілю з Зворотного Зв'язку")
    await state.set_state(MenuStates.PROFILE_MENU)
    
    description = "🔙 <b>Повернення до меню Профіль:</b>"
    detailed_text = (
        "Ви повернулися до меню Профіль. Оберіть нову опцію нижче."
    )
    await send_menu_response(message, description, detailed_text, get_profile_menu())

# Підрозділи "Допомога" - Інструкції
@router.message(MenuStates.HELP_MENU, F.text == MenuButton.INSTRUCTIONS.value)
async def cmd_instructions(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Інструкції")
    description = "📄 <b>Інструкції:</b>"
    detailed_text = (
        "Інструкції ще не доступні. Будь ласка, перевірте пізніше."
    )
    await send_menu_response(message, description, detailed_text, get_help_menu())

# Підрозділи "Допомога" - FAQ
@router.message(MenuStates.HELP_MENU, F.text == MenuButton.FAQ.value)
async def cmd_faq(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав FAQ")
    description = "❓ <b>FAQ:</b>"
    detailed_text = (
        "FAQ ще не доступне. Будь ласка, перевірте пізніше."
    )
    await send_menu_response(message, description, detailed_text, get_help_menu())

# Підрозділи "Допомога" - Підтримка
@router.message(MenuStates.HELP_MENU, F.text == MenuButton.HELP_SUPPORT.value)
async def cmd_help_support(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Підтримку")
    description = "🆘 <b>Підтримка:</b>"
    detailed_text = (
        "Зв'яжіться з підтримкою через наш канал або електронну пошту для отримання допомоги."
    )
    await send_menu_response(message, description, detailed_text, get_help_menu())

# Підрозділи "Допомога" - Назад до профілю
@router.message(MenuStates.HELP_MENU, F.text == MenuButton.BACK_TO_PROFILE.value)
async def cmd_back_to_profile_from_help(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} повернувся до Профілю з Допомоги")
    await state.set_state(MenuStates.PROFILE_MENU)
    
    description = "🔙 <b>Повернення до меню Профіль:</b>"
    detailed_text = (
        "Ви повернулися до меню Профіль. Оберіть нову опцію нижче."
    )
    await send_menu_response(message, description, detailed_text, get_profile_menu())

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

# Функція для налаштування обробників
def setup_handlers(dp):
    dp.include_router(router)
