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
    # Додаткові стани
    SEARCH_HERO = State()

# Команда /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    user_name = message.from_user.first_name
    logger.info(f"Користувач {message.from_user.id} викликав /start")
    await state.set_state(MenuStates.MAIN_MENU)
    await message.answer(
        f"👋 Вітаємо, {user_name}, у Mobile Legends Tournament Bot!\n\n"
        "🎮 Цей бот допоможе вам:\n"
        "• Організовувати турніри\n"
        "• Зберігати скріншоти персонажів\n"
        "• Відстежувати активність\n"
        "• Отримувати досягнення\n\n"
        "Оберіть опцію з меню нижче 👇",
        reply_markup=get_main_menu(),
    )
    # Відправляємо повідомлення з інлайн-кнопками
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ MLS ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

# Головне Меню
@router.message(MenuStates.MAIN_MENU, F.text == MenuButton.NAVIGATION.value)
async def cmd_navigation(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Навігацію")
    await state.set_state(MenuStates.NAVIGATION_MENU)
    await message.answer(
        "Виберіть опцію навігації:",
        reply_markup=get_navigation_menu(),
    )
    # Відправляємо повідомлення з інлайн-кнопками
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ MLS ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.MAIN_MENU, F.text == MenuButton.PROFILE.value)
async def cmd_profile(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Мій Профіль")
    await state.set_state(MenuStates.PROFILE_MENU)
    await message.answer(
        "Виберіть опцію профілю:",
        reply_markup=get_profile_menu(),
    )
    # Відправляємо повідомлення з інлайн-кнопками
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ MLS ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
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
    # Відправляємо повідомлення з інлайн-кнопками
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Heroes ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.GUIDES.value)
async def cmd_guides(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Гайди")
    await state.set_state(MenuStates.GUIDES_MENU)
    await message.answer(
        "Виберіть підрозділ гайдів:",
        reply_markup=get_guides_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Guides ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.COUNTER_PICKS.value)
async def cmd_counter_picks(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Контр-піки")
    await state.set_state(MenuStates.COUNTER_PICKS_MENU)
    await message.answer(
        "Виберіть опцію контр-піків:",
        reply_markup=get_counter_picks_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Counter Picks ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.BUILDS.value)
async def cmd_builds(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Білди")
    await state.set_state(MenuStates.BUILDS_MENU)
    await message.answer(
        "Виберіть опцію білдів:",
        reply_markup=get_builds_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Builds ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.VOTING.value)
async def cmd_voting(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Голосування")
    await state.set_state(MenuStates.VOTING_MENU)
    await message.answer(
        "Виберіть опцію голосування:",
        reply_markup=get_voting_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Voting ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_main_from_navigation(message: Message, state: FSMContext):
    await state.set_state(MenuStates.MAIN_MENU)
    await message.answer(
        "🔙 Повернення до головного меню:",
        reply_markup=get_main_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ MLS ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

# Розділ "Персонажі"
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
        await message.answer(
            f"Виберіть героя з класу {hero_class}:",
            reply_markup=get_hero_class_menu(hero_class)
        )
        # Відправляємо повідомлення з інлайн-кнопками
        await message.answer(
            f"ㅤㅤㅤㅤ      ┈ {hero_class} ┈ㅤㅤㅤㅤㅤㅤ",
            reply_markup=get_generic_inline_keyboard()
        )
    else:
        logger.warning(f"Невідомий клас героїв: {message.text}")
        await message.answer(
            "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче.",
            reply_markup=get_heroes_menu(),
        )
        await message.answer(
            "ㅤㅤㅤㅤ      ┈ Heroes ┈ㅤㅤㅤㅤㅤㅤ",
            reply_markup=get_generic_inline_keyboard()
        )

@router.message(MenuStates.HEROES_MENU, F.text == MenuButton.SEARCH_HERO.value)
async def cmd_search_hero(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Пошук Персонажа")
    await state.set_state(MenuStates.SEARCH_HERO)
    await message.answer(
        "Будь ласка, введіть ім'я героя для пошуку:",
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Search Hero ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )
    # Додатково можна налаштувати обробник для стану SEARCH_HERO

@router.message(MenuStates.HEROES_MENU, F.text == MenuButton.COMPARISON.value)
async def cmd_comparison(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Порівняння")
    await message.answer(
        "Функція порівняння героїв ще в розробці.",
        reply_markup=get_heroes_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Comparison ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.HEROES_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_navigation_from_heroes(message: Message, state: FSMContext):
    await state.set_state(MenuStates.NAVIGATION_MENU)
    await message.answer(
        "🔙 Повернення до меню Навігація:",
        reply_markup=get_navigation_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Navigation ┈ㅤㅤㅤㅤㅤㅤ",
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
    await message.answer(
        f"Ви обрали героя {hero_name}. Інформація про героя буде додана пізніше.",
        reply_markup=get_main_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ MLS ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.HERO_CLASS_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_heroes_menu(message: Message, state: FSMContext):
    await state.set_state(MenuStates.HEROES_MENU)
    await message.answer(
        "🔙 Повернення до меню Персонажі:",
        reply_markup=get_heroes_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Heroes ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

# Розділ "Гайди"
# (Додаємо всі обробники з першого коду)

@router.message(MenuStates.GUIDES_MENU, F.text == MenuButton.NEW_GUIDES.value)
async def cmd_new_guides(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Нові Гайди")
    await message.answer(
        "Список нових гайдів ще не доступний.",
        reply_markup=get_guides_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ New Guides ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.GUIDES_MENU, F.text == MenuButton.POPULAR_GUIDES.value)
async def cmd_popular_guides(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Популярні Гайди")
    await message.answer(
        "Список популярних гайдів ще не доступний.",
        reply_markup=get_guides_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Popular Guides ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.GUIDES_MENU, F.text == MenuButton.BEGINNER_GUIDES.value)
async def cmd_beginner_guides(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Гайди для Початківців")
    await message.answer(
        "Список гайдів для початківців ще не доступний.",
        reply_markup=get_guides_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Beginner Guides ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.GUIDES_MENU, F.text == MenuButton.ADVANCED_TECHNIQUES.value)
async def cmd_advanced_techniques(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Просунуті Техніки")
    await message.answer(
        "Список просунутих технік ще не доступний.",
        reply_markup=get_guides_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Advanced Techniques ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.GUIDES_MENU, F.text == MenuButton.TEAMPLAY_GUIDES.value)
async def cmd_teamplay_guides(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Командну Гру")
    await message.answer(
        "Список гайдів по командній грі ще не доступний.",
        reply_markup=get_guides_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Teamplay Guides ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.GUIDES_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_navigation_from_guides(message: Message, state: FSMContext):
    await state.set_state(MenuStates.NAVIGATION_MENU)
    await message.answer(
        "🔙 Повернення до меню Навігація:",
        reply_markup=get_navigation_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Navigation ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

# Розділ "Контр-піки"
# (Додаємо обробники з першого коду)

@router.message(MenuStates.COUNTER_PICKS_MENU, F.text == MenuButton.COUNTER_SEARCH.value)
async def cmd_counter_search(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Пошук Контр-піку")
    await message.answer(
        "Введіть ім'я персонажа для пошуку контр-піку:",
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Counter Search ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.COUNTER_PICKS_MENU, F.text == MenuButton.COUNTER_LIST.value)
async def cmd_counter_list(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Список Персонажів")
    await message.answer(
        "Список персонажів для контр-піків ще не доступний.",
        reply_markup=get_counter_picks_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Counter List ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.COUNTER_PICKS_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_navigation_from_counter_picks(message: Message, state: FSMContext):
    await state.set_state(MenuStates.NAVIGATION_MENU)
    await message.answer(
        "🔙 Повернення до меню Навігація:",
        reply_markup=get_navigation_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Navigation ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

# Розділ "Білди"
# (Додаємо обробники з першого коду)

@router.message(MenuStates.BUILDS_MENU, F.text == MenuButton.CREATE_BUILD.value)
async def cmd_create_build(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Створити Білд")
    await message.answer(
        "Функція створення білду ще в розробці.",
        reply_markup=get_builds_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Create Build ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.BUILDS_MENU, F.text == MenuButton.MY_BUILDS.value)
async def cmd_my_builds(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Мої Білди")
    await message.answer(
        "Список ваших білдів ще не доступний.",
        reply_markup=get_builds_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ My Builds ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.BUILDS_MENU, F.text == MenuButton.POPULAR_BUILDS.value)
async def cmd_popular_builds(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Популярні Білди")
    await message.answer(
        "Список популярних білдів ще не доступний.",
        reply_markup=get_builds_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Popular Builds ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.BUILDS_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_navigation_from_builds(message: Message, state: FSMContext):
    await state.set_state(MenuStates.NAVIGATION_MENU)
    await message.answer(
        "🔙 Повернення до меню Навігація:",
        reply_markup=get_navigation_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Navigation ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

# Розділ "Голосування"
# (Додаємо обробники з першого коду)

@router.message(MenuStates.VOTING_MENU, F.text == MenuButton.CURRENT_VOTES.value)
async def cmd_current_votes(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Поточні Опитування")
    await message.answer(
        "Список поточних опитувань ще не доступний.",
        reply_markup=get_voting_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Current Votes ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.VOTING_MENU, F.text == MenuButton.MY_VOTES.value)
async def cmd_my_votes(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Мої Голосування")
    await message.answer(
        "Список ваших голосувань ще не доступний.",
        reply_markup=get_voting_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ My Votes ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.VOTING_MENU, F.text == MenuButton.SUGGEST_TOPIC.value)
async def cmd_suggest_topic(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Запропонувати Тему")
    await message.answer(
        "Будь ласка, введіть тему для пропозиції:",
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Suggest Topic ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )
    # Додатково можна налаштувати обробник для прийому теми

@router.message(MenuStates.VOTING_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_navigation_from_voting(message: Message, state: FSMContext):
    await state.set_state(MenuStates.NAVIGATION_MENU)
    await message.answer(
        "🔙 Повернення до меню Навігація:",
        reply_markup=get_navigation_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Navigation ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

# Розділ "Профіль"
# (Додаємо обробники з першого коду)

@router.message(MenuStates.PROFILE_MENU, F.text == MenuButton.STATISTICS.value)
async def cmd_statistics(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Статистика")
    await state.set_state(MenuStates.STATISTICS_MENU)
    await message.answer(
        "Виберіть підрозділ статистики:",
        reply_markup=get_statistics_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Statistics ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.PROFILE_MENU, F.text == MenuButton.ACHIEVEMENTS.value)
async def cmd_achievements(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Досягнення")
    await state.set_state(MenuStates.ACHIEVEMENTS_MENU)
    await message.answer(
        "Виберіть підрозділ досягнень:",
        reply_markup=get_achievements_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Achievements ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.PROFILE_MENU, F.text == MenuButton.SETTINGS.value)
async def cmd_settings(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Налаштування")
    await state.set_state(MenuStates.SETTINGS_MENU)
    await message.answer(
        "Виберіть опцію налаштувань:",
        reply_markup=get_settings_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Settings ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.PROFILE_MENU, F.text == MenuButton.FEEDBACK.value)
async def cmd_feedback(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Зворотний Зв'язок")
    await state.set_state(MenuStates.FEEDBACK_MENU)
    await message.answer(
        "Виберіть опцію зворотного зв'язку:",
        reply_markup=get_feedback_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Feedback ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.PROFILE_MENU, F.text == MenuButton.HELP.value)
async def cmd_help(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Допомогу")
    await state.set_state(MenuStates.HELP_MENU)
    await message.answer(
        "Виберіть опцію допомоги:",
        reply_markup=get_help_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ Help ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.PROFILE_MENU, F.text == MenuButton.BACK_TO_MAIN_MENU.value)
async def cmd_back_to_main_from_profile(message: Message, state: FSMContext):
    await state.set_state(MenuStates.MAIN_MENU)
    await message.answer(
        "🔙 Повернення до головного меню:",
        reply_markup=get_main_menu(),
    )
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ MLS ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

# Додаємо інші обробники з першого коду для підрозділів та інлайн-кнопок...

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
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ MLS ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

# Функція для налаштування обробників
def setup_handlers(dp):
    dp.include_router(router)
