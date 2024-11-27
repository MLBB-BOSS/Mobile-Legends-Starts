# handlers/base.py

import logging
from aiogram import Router, F
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
    get_guides_menu,
    get_counter_picks_menu,
    get_builds_menu,
    get_voting_menu,
    get_profile_menu,
    get_hero_class_menu,
    heroes_by_class,
)
from keyboards.inline_menus import (
    get_navigation_inline_menu,
    get_profile_inline_menu,
)

logger = logging.getLogger(__name__)
router = Router()

class MenuStates(StatesGroup):
    MAIN_MENU = State()
    NAVIGATION_MENU = State()
    HEROES_MENU = State()
    HERO_CLASS_MENU = State()
    GUIDES_MENU = State()
    PROFILE_MENU = State()
    COUNTER_PICKS_MENU = State()
    BUILDS_MENU = State()
    VOTING_MENU = State()

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

@router.message(F.text == MenuButton.NAVIGATION.value)
async def cmd_navigation(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Навігацію")
    await state.set_state(MenuStates.NAVIGATION_MENU)
    await message.answer(
        "У розділі 'Навігація' ви можете знайти різні опції для перегляду героїв, гайдів, білдів тощо.",
        reply_markup=get_navigation_inline_menu()
    )

@router.callback_query(F.data == "go_navigation")
async def callback_go_navigation(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.set_state(MenuStates.NAVIGATION_MENU)
    await callback_query.message.answer(
        "Виберіть опцію навігації:",
        reply_markup=get_navigation_menu(),
    )

@router.callback_query(F.data == "more_navigation")
async def callback_more_navigation(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer(
        "У розділі 'Навігація' ви можете:\n"
        "- Переглядати героїв за класами\n"
        "- Читати гайди\n"
        "- Створювати білди\n"
        "Оберіть 'Перейти до Навігації', щоб почати.",
    )

@router.message(F.text == MenuButton.PROFILE.value)
async def cmd_profile(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Мій Профіль")
    await state.set_state(MenuStates.PROFILE_MENU)
    await message.answer(
        "У розділі 'Мій Профіль' ви можете переглянути свою активність, рейтинг та ігрову статистику.",
        reply_markup=get_profile_inline_menu()
    )

@router.callback_query(F.data == "go_profile")
async def callback_go_profile(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await state.set_state(MenuStates.PROFILE_MENU)
    await callback_query.message.answer(
        "Виберіть опцію профілю:",
        reply_markup=get_profile_menu(),
    )

@router.callback_query(F.data == "more_profile")
async def callback_more_profile(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer()
    await callback_query.message.answer(
        "У розділі 'Мій Профіль' ви можете:\n"
        "- Переглянути загальну активність\n"
        "- Подивитися свій рейтинг\n"
        "- Переглянути ігрову статистику",
    )

@router.message(F.text == MenuButton.ACTIVITY.value)
async def cmd_activity(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Загальна Активність")
    await message.answer(
        "Ваша загальна активність: [дані будуть доступні пізніше]",
        reply_markup=get_profile_menu(),
    )

@router.message(F.text == MenuButton.RANKING.value)
async def cmd_ranking(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Рейтинг")
    await message.answer(
        "Ваш поточний рейтинг: [дані будуть доступні пізніше]",
        reply_markup=get_profile_menu(),
    )

@router.message(F.text == MenuButton.GAME_STATS.value)
async def cmd_game_stats(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Ігрова Статистика")
    await message.answer(
        "Ваша ігрова статистика: [дані будуть доступні пізніше]",
        reply_markup=get_profile_menu(),
    )

@router.message(F.text == MenuButton.HEROES.value)
async def cmd_heroes(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Персонажі")
    await state.set_state(MenuStates.HEROES_MENU)
    await message.answer(
        "Виберіть категорію героїв:",
        reply_markup=get_heroes_menu(),
    )

class_buttons = list(menu_button_to_class.keys())

@router.message(F.text.in_(class_buttons))
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

@router.message(F.text == MenuButton.COMPARISON.value)
async def cmd_comparison(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Порівняння")
    await message.answer(
        "Функція порівняння героїв ще в розробці.",
        reply_markup=get_heroes_menu(),
    )

all_heroes = set()
for heroes in heroes_by_class.values():
    all_heroes.update(heroes)

@router.message(F.text.in_(all_heroes))
async def cmd_hero_selected(message: Message, state: FSMContext):
    hero_name = message.text
    logger.info(f"Користувач {message.from_user.id} обрав героя {hero_name}")
    await state.set_state(MenuStates.MAIN_MENU)
    await message.answer(
        f"Ви обрали героя {hero_name}. Інформація про героя буде додана пізніше.",
        reply_markup=get_main_menu(),
    )

@router.message(F.text == MenuButton.GUIDES.value)
async def cmd_guides(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Гайди")
    await state.set_state(MenuStates.GUIDES_MENU)
    await message.answer(
        "Виберіть гайди:",
        reply_markup=get_guides_menu(),
    )

@router.message(F.text == MenuButton.NEW_GUIDES.value)
async def cmd_new_guides(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Нові Гайди")
    await message.answer(
        "Нові гайди ще в розробці.",
        reply_markup=get_guides_menu(),
    )

@router.message(F.text == MenuButton.POPULAR_GUIDES.value)
async def cmd_popular_guides(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Популярні Гайди")
    await message.answer(
        "Популярні гайди ще в розробці.",
        reply_markup=get_guides_menu(),
    )

@router.message(F.text == MenuButton.BEGINNER_GUIDES.value)
async def cmd_beginner_guides(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Для Початківців")
    await message.answer(
        "Гайди для початківців ще в розробці.",
        reply_markup=get_guides_menu(),
    )

@router.message(F.text == MenuButton.ADVANCED_TECHNIQUES.value)
async def cmd_advanced_techniques(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Просунуті Техніки")
    await message.answer(
        "Просунуті техніки ще в розробці.",
        reply_markup=get_guides_menu(),
    )

@router.message(F.text == MenuButton.TEAMPLAY_GUIDES.value)
async def cmd_teamplay_guides(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Командна Гра")
    await message.answer(
        "Гайди по командній грі ще в розробці.",
        reply_markup=get_guides_menu(),
    )

@router.message(F.text == MenuButton.COUNTER_PICKS.value)
async def cmd_counter_picks(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Контр-піки")
    await state.set_state(MenuStates.COUNTER_PICKS_MENU)
    await message.answer(
        "Виберіть контр-піки:",
        reply_markup=get_counter_picks_menu(),
    )

@router.message(F.text == MenuButton.COUNTER_SEARCH.value)
async def cmd_counter_search(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Пошук Контр-піку")
    await message.answer(
        "Функція пошуку контр-піків ще в розробці.",
        reply_markup=get_counter_picks_menu(),
    )

@router.message(F.text == MenuButton.COUNTER_LIST.value)
async def cmd_counter_list(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Список Персонажів")
    await message.answer(
        "Список контр-піків ще в розробці.",
        reply_markup=get_counter_picks_menu(),
    )

@router.message(F.text == MenuButton.BUILDS.value)
async def cmd_builds(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Білди")
    await state.set_state(MenuStates.BUILDS_MENU)
    await message.answer(
        "Виберіть білди:",
        reply_markup=get_builds_menu(),
    )

@router.message(F.text == MenuButton.CREATE_BUILD.value)
async def cmd_create_build(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Створити Білд")
    await message.answer(
        "Функція створення білдів ще в розробці.",
        reply_markup=get_builds_menu(),
    )

@router.message(F.text == MenuButton.MY_BUILDS.value)
async def cmd_my_builds(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Мої Білди")
    await message.answer(
        "Ваші білди ще в розробці.",
        reply_markup=get_builds_menu(),
    )

@router.message(F.text == MenuButton.POPULAR_BUILDS.value)
async def cmd_popular_builds(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Популярні Білди")
    await message.answer(
        "Популярні білди ще в розробці.",
        reply_markup=get_builds_menu(),
    )

@router.message(F.text == MenuButton.VOTING.value)
async def cmd_voting(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Голосування")
    await state.set_state(MenuStates.VOTING_MENU)
    await message.answer(
        "Виберіть опцію голосування:",
        reply_markup=get_voting_menu(),
    )

@router.message(F.text == MenuButton.CURRENT_VOTES.value)
async def cmd_current_votes(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Поточні Опитування")
    await message.answer(
        "Поточні опитування ще в розробці.",
        reply_markup=get_voting_menu(),
    )

@router.message(F.text == MenuButton.MY_VOTES.value)
async def cmd_my_votes(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Мої Голосування")
    await message.answer(
        "Ваші голосування ще в розробці.",
        reply_markup=get_voting_menu(),
    )

@router.message(F.text == MenuButton.SUGGEST_TOPIC.value)
async def cmd_suggest_topic(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Запропонувати Тему")
    await message.answer(
        "Функція пропозиції тем ще в розробці.",
        reply_markup=get_voting_menu(),
    )

@router.message(F.text == MenuButton.BACK.value)
async def cmd_back(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} натиснув 'Назад'")
    current_state = await state.get_state()
    
    if current_state == MenuStates.NAVIGATION_MENU.state:
        await state.set_state(MenuStates.MAIN_MENU)
        await message.answer(
            "🔙 Повернення до головного меню:",
            reply_markup=get_main_menu(),
        )
    elif current_state == MenuStates.HEROES_MENU.state:
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
    elif current_state == MenuStates.PROFILE_MENU.state:
        await state.set_state(MenuStates.MAIN_MENU)
        await message.answer(
            "🔙 Повернення до головного меню:",
            reply_markup=get_main_menu(),
        )
    elif current_state == MenuStates.GUIDES_MENU.state:
        await state.set_state(MenuStates.NAVIGATION_MENU)
        await message.answer(
            "🔙 Повернення до меню Навігація:",
            reply_markup=get_navigation_menu(),
        )
    elif current_state == MenuStates.COUNTER_PICKS_MENU.state:
        await state.set_state(MenuStates.NAVIGATION_MENU)
        await message.answer(
            "🔙 Повернення до меню Навігація:",
            reply_markup=get_navigation_menu(),
        )
    elif current_state == MenuStates.BUILDS_MENU.state:
        await state.set_state(MenuStates.NAVIGATION_MENU)
        await message.answer(
            "🔙 Повернення до меню Навігація:",
            reply_markup=get_navigation_menu(),
        )
    elif current_state == MenuStates.VOTING_MENU.state:
        await state.set_state(MenuStates.NAVIGATION_MENU)
        await message.answer(
            "🔙 Повернення до меню Навігація:",
            reply_markup=get_navigation_menu(),
        )
    else:
        await state.set_state(MenuStates.MAIN_MENU)
        await message.answer(
            "🔙 Повернення до головного меню:",
            reply_markup=get_main_menu(),
        )

@router.message()
async def unknown_command(message: Message, state: FSMContext):
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")
    await state.set_state(MenuStates.MAIN_MENU)
    await message.answer(
        "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче.",
        reply_markup=get_main_menu(),
    )

def setup_handlers(dp):
    dp.include_router(router)
