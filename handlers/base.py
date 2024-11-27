# handlers/base.py

import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
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

# Налаштування логування
logger = logging.getLogger(__name__)
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

@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.GUIDES.value)
async def cmd_guides(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Гайди")
    await state.set_state(MenuStates.GUIDES_MENU)
    await message.answer(
        "Виберіть категорію гайдів:",
        reply_markup=get_guides_menu(),
    )

@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.COUNTER_PICKS.value)
async def cmd_counter_picks(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Контр-піки")
    await state.set_state(MenuStates.COUNTER_PICKS_MENU)
    await message.answer(
        "Виберіть опцію контр-піків:",
        reply_markup=get_counter_picks_menu(),
    )

@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.BUILDS.value)
async def cmd_builds(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Білди")
    await state.set_state(MenuStates.BUILDS_MENU)
    await message.answer(
        "Виберіть опцію білдів:",
        reply_markup=get_builds_menu(),
    )

@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.VOTING.value)
async def cmd_voting(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Голосування")
    await state.set_state(MenuStates.VOTING_MENU)
    await message.answer(
        "Виберіть опцію голосування:",
        reply_markup=get_voting_menu(),
    )

@router.message(MenuStates.NAVIGATION_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_main_from_navigation(message: Message, state: FSMContext):
    await state.set_state(MenuStates.MAIN_MENU)
    await message.answer(
        "🔙 Повернення до головного меню:",
        reply_markup=get_main_menu(),
    )

# Розділ "Персонажі"
@router.message(MenuStates.HEROES_MENU, F.text.in_([MenuButton.TANK.value, MenuButton.MAGE.value, MenuButton.MARKSMAN.value, MenuButton.ASSASSIN.value, MenuButton.SUPPORT.value]))
async def cmd_hero_class(message: Message, state: FSMContext):
    hero_class = menu_button_to_class.get(message.text)
    if hero_class:
        logger.info(f"Користувач {message.from_user.id} обрав клас {hero_class}")
        await state.set_state(MenuStates.HERO_CLASS_MENU)
        await message.answer(
            f"Виберіть героя з класу {hero_class}:",
            reply_markup=get_hero_class_menu(hero_class)
        )
    else:
        logger.warning(f"Невідомий клас героїв: {message.text}")
        await message.answer(
            "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче.",
            reply_markup=get_heroes_menu(),
        )

@router.message(MenuStates.HEROES_MENU, F.text == MenuButton.SEARCH_HERO.value)
async def cmd_search_hero(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Пошук Персонажа")
    await message.answer(
        "Будь ласка, введіть ім'я героя для пошуку:",
    )
    # Set a state for searching hero if needed

@router.message(MenuStates.HEROES_MENU, F.text == MenuButton.COMPARISON.value)
async def cmd_comparison(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Порівняння")
    await message.answer(
        "Функція порівняння героїв ще в розробці.",
        reply_markup=get_heroes_menu(),
    )

@router.message(MenuStates.HEROES_MENU, F.text == MenuButton.BACK.value)
async def cmd_back_to_navigation_from_heroes(message: Message, state: FSMContext):
    await state.set_state(MenuStates.NAVIGATION_MENU)
    await message.answer(
        "🔙 Повернення до меню Навігація:",
        reply_markup=get_navigation_menu(),
    )

# Розділ "Мій Профіль"
@router.message(MenuStates.PROFILE_MENU, F.text == MenuButton.STATISTICS.value)
async def cmd_statistics(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Статистика")
    await state.set_state(MenuStates.STATISTICS_MENU)
    await message.answer(
        "Виберіть опцію статистики:",
        reply_markup=get_statistics_menu(),
    )

@router.message(MenuStates.PROFILE_MENU, F.text == MenuButton.ACHIEVEMENTS.value)
async def cmd_achievements(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Досягнення")
    await state.set_state(MenuStates.ACHIEVEMENTS_MENU)
    await message.answer(
        "Виберіть опцію досягнень:",
        reply_markup=get_achievements_menu(),
    )

@router.message(MenuStates.PROFILE_MENU, F.text == MenuButton.SETTINGS.value)
async def cmd_settings(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Налаштування")
    await state.set_state(MenuStates.SETTINGS_MENU)
    await message.answer(
        "Виберіть опцію налаштувань:",
        reply_markup=get_settings_menu(),
    )

@router.message(MenuStates.PROFILE_MENU, F.text == MenuButton.FEEDBACK.value)
async def cmd_feedback(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Зворотний Зв'язок")
    await state.set_state(MenuStates.FEEDBACK_MENU)
    await message.answer(
        "Виберіть опцію зворотного зв'язку:",
        reply_markup=get_feedback_menu(),
    )

@router.message(MenuStates.PROFILE_MENU, F.text == MenuButton.HELP.value)
async def cmd_help(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Допомога")
    await state.set_state(MenuStates.HELP_MENU)
    await message.answer(
        "Виберіть опцію допомоги:",
        reply_markup=get_help_menu(),
    )

@router.message(MenuStates.PROFILE_MENU, F.text == MenuButton.BACK_TO_MAIN_MENU.value)
async def cmd_back_to_main_from_profile(message: Message, state: FSMContext):
    await state.set_state(MenuStates.MAIN_MENU)
    await message.answer(
        "🔙 Повернення до головного меню:",
        reply_markup=get_main_menu(),
    )

# Стани повернення з підменю Профілю
@router.message(F.text == MenuButton.BACK_TO_PROFILE.value)
async def cmd_back_to_profile(message: Message, state: FSMContext):
    await state.set_state(MenuStates.PROFILE_MENU)
    await message.answer(
        "🔙 Повернення до меню Профіль:",
        reply_markup=get_profile_menu(),
    )

# Кнопка "Назад" універсальна
@router.message(F.text == MenuButton.BACK.value)
async def cmd_back(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == MenuStates.NAVIGATION_MENU.state:
        await state.set_state(MenuStates.MAIN_MENU)
        await message.answer(
            "🔙 Повернення до головного меню:",
            reply_markup=get_main_menu(),
        )
    elif current_state in [MenuStates.HEROES_MENU.state, MenuStates.GUIDES_MENU.state, MenuStates.COUNTER_PICKS_MENU.state, MenuStates.BUILDS_MENU.state, MenuStates.VOTING_MENU.state]:
        await state.set_state(MenuStates.NAVIGATION_MENU)
        await message.answer(
            "🔙 Повернення до меню Навігація:",
            reply_markup=get_navigation_menu(),
        )
    elif current_state == MenuStates.HERO_CLASS_MENU.state:
        await state.set_state(MenuStates.HEROES_MENU)
        await message.answer(
            "🔙 Повернення до меню Персонажі:",
            reply_markup=get_heroes_menu(),
        )
    else:
        await state.set_state(MenuStates.MAIN_MENU)
        await message.answer(
            "🔙 Повернення до головного меню:",
            reply_markup=get_main_menu(),
        )

# Обробник для невідомих повідомлень
@router.message()
async def unknown_command(message: Message, state: FSMContext):
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")
    current_state = await state.get_state()
    if current_state == MenuStates.MAIN_MENU.state:
        reply_markup = get_main_menu()
    elif current_state == MenuStates.NAVIGATION_MENU.state:
        reply_markup = get_navigation_menu()
    elif current_state == MenuStates.PROFILE_MENU.state:
        reply_markup = get_profile_menu()
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
