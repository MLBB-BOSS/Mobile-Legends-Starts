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
from utils.message_formatter import MessageFormatter  # Переконайтесь, що цей файл існує та містить клас

# Налаштування логування
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Ініціалізація Router
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
    SEARCH_HERO = State()  # Додатковий стан для пошуку героя
    CHANGE_USERNAME = State()
    REPORT_BUG = State()
    SEND_FEEDBACK = State()
    SUGGEST_TOPIC = State()
    # Додайте інші стани за потребою

# Команда /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Команда /start"""
    await state.set_state(MenuStates.MAIN_MENU)
    await MessageFormatter.update_menu_message(
        message=message,
        title="🎮 Ласкаво просимо до Mobile Legends Bot!",
        description=(
            "Цей бот допоможе вам:\n"
            "🔹 Знайти інформацію про героїв\n"
            "🔹 Отримати корисні гайди\n"
            "🔹 Створювати та ділитися білдами\n"
            "🔹 Відстежувати свою статистику"
        ),
        keyboard=get_main_menu()
    )
    # Відправляємо повідомлення з інлайн-кнопками
    await message.answer(
        "ㅤㅤㅤㅤ      ┈ MLS ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

# Команда /help
@router.message(Command("help"))
async def cmd_help(message: Message, state: FSMContext):
    """Команда /help"""
    help_text = (
        "<b>📋 Доступні команди:</b>\n\n"
        "/start - Запустити бота\n"
        "/heroes - Меню героїв\n"
        "/guides - Гайди по грі\n"
        "/builds - Менеджер білдів\n"
        "/stats - Моя статистика\n"
        "/help - Показати це повідомлення"
    )
    await message.answer(help_text, parse_mode="HTML")

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
        "ㅤㅤㅤ  ㅤ    ┈ MLS ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.MAIN_MENU, F.text == MenuButton.PROFILE.value)
async def cmd_profile(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Мій Профіль")
    await state.set_state(MenuStates.PROFILE_MENU)
    await message.answer(
        "ㅤㅤㅤ  ㅤ    ┈ MLS ┈ㅤㅤㅤㅤㅤㅤ",
        reply_markup=get_profile_menu(),
    )
    # Відправляємо повідомлення з інлайн-кнопками
    await message.answer(
        "ㅤㅤㅤ  ㅤ    ┈ MLS ┈ㅤㅤㅤㅤㅤㅤ:",
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
        "Ось ваші інлайн-опції:",
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
        "Ось ваші інлайн-опції:",
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
        "Ось ваші інлайн-опції:",
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
        "Ось ваші інлайн-опції:",
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
        "Ось ваші інлайн-опції:",
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
        "Ось ваші інлайн-опції:",
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
            "Ось ваші інлайн-опції:",
            reply_markup=get_generic_inline_keyboard()
        )
    else:
        logger.warning(f"Невідомий клас героїв: {message.text}")
        await message.answer(
            "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче.",
            reply_markup=get_heroes_menu(),
        )
        await message.answer(
            "Ось ваші інлайн-опції:",
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
        "Ось ваші інлайн-опції:",
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
        "Ось ваші інлайн-опції:",
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
    await message.answer(
        f"Ви обрали героя {hero_name}. Інформація про героя буде додана пізніше.",
        reply_markup=get_main_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
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
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

# Розділ "Гайди"
@router.message(MenuStates.GUIDES_MENU, F.text == MenuButton.NEW_GUIDES.value)
async def cmd_new_guides(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Нові Гайди")
    await message.answer(
        "Список нових гайдів ще не доступний.",
        reply_markup=get_guides_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
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
        "Ось ваші інлайн-опції:",
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
        "Ось ваші інлайн-опції:",
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
        "Ось ваші інлайн-опції:",
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
        "Ось ваші інлайн-опції:",
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
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

# Розділ "Контр-піки"
@router.message(MenuStates.COUNTER_PICKS_MENU, F.text == MenuButton.COUNTER_SEARCH.value)
async def cmd_counter_search(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Пошук Контр-піку")
    await message.answer(
        "Введіть ім'я персонажа для пошуку контр-піку:",
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )
    # Додатково можна налаштувати обробник для пошуку контр-піку

@router.message(MenuStates.COUNTER_PICKS_MENU, F.text == MenuButton.COUNTER_LIST.value)
async def cmd_counter_list(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Список Персонажів")
    await message.answer(
        "Список персонажів для контр-піків ще не доступний.",
        reply_markup=get_counter_picks_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
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
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

# Розділ "Білди"
@router.message(MenuStates.BUILDS_MENU, F.text == MenuButton.CREATE_BUILD.value)
async def cmd_create_build(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Створити Білд")
    await message.answer(
        "Функція створення білду ще в розробці.",
        reply_markup=get_builds_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
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
        "Ось ваші інлайн-опції:",
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
        "Ось ваші інлайн-опції:",
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
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

# Розділ "Голосування"
@router.message(MenuStates.VOTING_MENU, F.text == MenuButton.CURRENT_VOTES.value)
async def cmd_current_votes(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Поточні Опитування")
    await message.answer(
        "Список поточних опитувань ще не доступний.",
        reply_markup=get_voting_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
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
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.VOTING_MENU, F.text == MenuButton.SUGGEST_TOPIC.value)
async def cmd_suggest_topic(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Запропонувати Тему")
    await state.set_state(MenuStates.SUGGEST_TOPIC)
    await message.answer(
        "Будь ласка, введіть тему для пропозиції:",
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
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
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

# Розділ "Профіль"
@router.message(MenuStates.PROFILE_MENU, F.text == MenuButton.STATISTICS.value)
async def cmd_statistics(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Статистика")
    await state.set_state(MenuStates.STATISTICS_MENU)
    await message.answer(
        "Виберіть підрозділ статистики:",
        reply_markup=get_statistics_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
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
        "Ось ваші інлайн-опції:",
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
        "Ось ваші інлайн-опції:",
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
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.PROFILE_MENU, F.text == MenuButton.HELP.value)
async def cmd_help_menu(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Допомогу")
    await state.set_state(MenuStates.HELP_MENU)
    await message.answer(
        "Виберіть опцію допомоги:",
        reply_markup=get_help_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
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
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

# Підрозділи "Статистика"
@router.message(MenuStates.STATISTICS_MENU, F.text == MenuButton.ACTIVITY.value)
async def cmd_activity(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Загальну Активність")
    await message.answer(
        "Статистика загальної активності ще не доступна.",
        reply_markup=get_statistics_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.STATISTICS_MENU, F.text == MenuButton.RANKING.value)
async def cmd_ranking(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Рейтинг")
    await message.answer(
        "Рейтинг ще не доступний.",
        reply_markup=get_statistics_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.STATISTICS_MENU, F.text == MenuButton.GAME_STATS.value)
async def cmd_game_stats(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Ігрову Статистику")
    await message.answer(
        "Ігрова статистика ще не доступна.",
        reply_markup=get_statistics_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.STATISTICS_MENU, F.text == MenuButton.BACK_TO_PROFILE.value)
async def cmd_back_to_profile_from_statistics(message: Message, state: FSMContext):
    await state.set_state(MenuStates.PROFILE_MENU)
    await message.answer(
        "🔙 Повернення до меню Профіль:",
        reply_markup=get_profile_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

# Підрозділи "Досягнення"
@router.message(MenuStates.ACHIEVEMENTS_MENU, F.text == MenuButton.BADGES.value)
async def cmd_badges(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Мої Бейджі")
    await message.answer(
        "Список ваших бейджів ще не доступний.",
        reply_markup=get_achievements_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.ACHIEVEMENTS_MENU, F.text == MenuButton.PROGRESS.value)
async def cmd_progress(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Прогрес")
    await message.answer(
        "Ваш прогрес ще не доступний.",
        reply_markup=get_achievements_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.ACHIEVEMENTS_MENU, F.text == MenuButton.TOURNAMENT_STATS.value)
async def cmd_tournament_stats(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Турнірну Статистику")
    await message.answer(
        "Турнірна статистика ще не доступна.",
        reply_markup=get_achievements_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.ACHIEVEMENTS_MENU, F.text == MenuButton.AWARDS.value)
async def cmd_awards(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Отримані Нагороди")
    await message.answer(
        "Список отриманих нагород ще не доступний.",
        reply_markup=get_achievements_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.ACHIEVEMENTS_MENU, F.text == MenuButton.BACK_TO_PROFILE.value)
async def cmd_back_to_profile_from_achievements(message: Message, state: FSMContext):
    await state.set_state(MenuStates.PROFILE_MENU)
    await message.answer(
        "🔙 Повернення до меню Профіль:",
        reply_markup=get_profile_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

# Підрозділи "Налаштування"
@router.message(MenuStates.SETTINGS_MENU, F.text == MenuButton.LANGUAGE.value)
async def cmd_language(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Мову Інтерфейсу")
    await message.answer(
        "Функція зміни мови ще в розробці.",
        reply_markup=get_settings_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.SETTINGS_MENU, F.text == MenuButton.CHANGE_USERNAME.value)
async def cmd_change_username(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Змінити Username")
    await state.set_state(MenuStates.CHANGE_USERNAME)
    await message.answer(
        "Будь ласка, введіть новий Username:",
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )
    # Додатково можна налаштувати обробник для зміни Username

@router.message(MenuStates.SETTINGS_MENU, F.text == MenuButton.UPDATE_ID.value)
async def cmd_update_id(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Оновити ID Гравця")
    await message.answer(
        "Функція оновлення ID ще в розробці.",
        reply_markup=get_settings_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.SETTINGS_MENU, F.text == MenuButton.NOTIFICATIONS.value)
async def cmd_notifications(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Сповіщення")
    await message.answer(
        "Функція налаштування сповіщень ще в розробці.",
        reply_markup=get_settings_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.SETTINGS_MENU, F.text == MenuButton.BACK_TO_PROFILE.value)
async def cmd_back_to_profile_from_settings(message: Message, state: FSMContext):
    await state.set_state(MenuStates.PROFILE_MENU)
    await message.answer(
        "🔙 Повернення до меню Профіль:",
        reply_markup=get_profile_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

# Підрозділи "Зворотний Зв'язок"
@router.message(MenuStates.FEEDBACK_MENU, F.text == MenuButton.SEND_FEEDBACK.value)
async def cmd_send_feedback(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Надіслати Відгук")
    await state.set_state(MenuStates.SEND_FEEDBACK)
    await message.answer(
        "Будь ласка, введіть ваш відгук:",
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )
    # Додатково можна налаштувати обробник для прийому відгуку

@router.message(MenuStates.FEEDBACK_MENU, F.text == MenuButton.REPORT_BUG.value)
async def cmd_report_bug(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Повідомити про Помилку")
    await state.set_state(MenuStates.REPORT_BUG)
    await message.answer(
        "Будь ласка, опишіть помилку, яку ви знайшли:",
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )
    # Додатково можна налаштувати обробник для прийому звіту про помилку

@router.message(MenuStates.FEEDBACK_MENU, F.text == MenuButton.BACK_TO_PROFILE.value)
async def cmd_back_to_profile_from_feedback(message: Message, state: FSMContext):
    await state.set_state(MenuStates.PROFILE_MENU)
    await message.answer(
        "🔙 Повернення до меню Профіль:",
        reply_markup=get_profile_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

# Підрозділи "Допомога"
@router.message(MenuStates.HELP_MENU, F.text == MenuButton.INSTRUCTIONS.value)
async def cmd_instructions(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Інструкції")
    await message.answer(
        "Інструкції ще не доступні.",
        reply_markup=get_help_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.HELP_MENU, F.text == MenuButton.FAQ.value)
async def cmd_faq(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав FAQ")
    await message.answer(
        "FAQ ще не доступне.",
        reply_markup=get_help_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.HELP_MENU, F.text == MenuButton.HELP_SUPPORT.value)
async def cmd_help_support(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Підтримку")
    await message.answer(
        "Зв'яжіться з підтримкою через наш канал або електронну пошту.",
        reply_markup=get_help_menu(),
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

@router.message(MenuStates.HELP_MENU, F.text == MenuButton.BACK_TO_PROFILE.value)
async def cmd_back_to_profile_from_help(message: Message, state: FSMContext):
    await state.set_state(MenuStates.PROFILE_MENU)
    await message.answer(
        "🔙 Повернення до меню Профіль:",
        reply_markup=get_profile_menu(),
    )
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

# Обробник для невідомих повідомлень
@router.message()
async def unknown_command(message: Message, state: FSMContext):
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")
    current_state = await state.get_state()
    reply_markup = get_main_menu()  # За замовчуванням

    if current_state:
        state_mapping = {
            MenuStates.MAIN_MENU.state: get_main_menu(),
            MenuStates.NAVIGATION_MENU.state: get_navigation_menu(),
            MenuStates.HEROES_MENU.state: get_heroes_menu(),
            MenuStates.HERO_CLASS_MENU.state: get_hero_class_menu(
                (await state.get_data()).get('hero_class', 'Танк')
            ),
            MenuStates.GUIDES_MENU.state: get_guides_menu(),
            MenuStates.COUNTER_PICKS_MENU.state: get_counter_picks_menu(),
            MenuStates.BUILDS_MENU.state: get_builds_menu(),
            MenuStates.VOTING_MENU.state: get_voting_menu(),
            MenuStates.PROFILE_MENU.state: get_profile_menu(),
            MenuStates.STATISTICS_MENU.state: get_statistics_menu(),
            MenuStates.ACHIEVEMENTS_MENU.state: get_achievements_menu(),
            MenuStates.SETTINGS_MENU.state: get_settings_menu(),
            MenuStates.FEEDBACK_MENU.state: get_feedback_menu(),
            MenuStates.HELP_MENU.state: get_help_menu(),
            # Додайте інші стани за потребою
        }
        reply_markup = state_mapping.get(current_state, get_main_menu())

    await message.answer(
        "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче.",
        reply_markup=reply_markup,
    )
    await message.answer(
        "Ось ваші інлайн-опції:",
        reply_markup=get_generic_inline_keyboard()
    )

# Функція для налаштування обробників
def setup_handlers(dp):
    dp.include_router(router)
