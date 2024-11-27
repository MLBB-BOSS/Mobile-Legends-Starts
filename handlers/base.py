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
    get_language_selection_menu,
    get_notifications_menu,
    get_statistics_menu,
    get_achievements_menu,
    get_settings_menu,
    get_feedback_menu,
    get_help_menu,
)
from keyboards.inline_menus import (
    get_navigation_inline_menu,
    get_profile_inline_menu,
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
    CHANGE_USERNAME = State()
    UPDATE_ID = State()
    NOTIFICATIONS_MENU = State()

# Команда /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """
    Обробник команди /start.
    Відправляє привітальне повідомлення та показує головне меню.
    """
    user_name = message.from_user.first_name
    logger.info(f"Користувач {message.from_user.id} викликав /start")
    await state.set_state(MenuStates.MAIN_MENU)  # Встановлюємо стан
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

# Обробник для кнопки "Навігація"
@router.message(F.text == MenuButton.NAVIGATION.value)
async def cmd_navigation(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Навігацію")
    await state.set_state(MenuStates.NAVIGATION_MENU)
    await message.answer(
        "У розділі 'Навігація' ви можете знайти різні опції для перегляду героїв, гайдів, білдів тощо.",
        reply_markup=get_navigation_menu()
    )

# Обробник для кнопки "Мій Профіль"
@router.message(F.text == MenuButton.PROFILE.value)
async def cmd_profile(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Мій Профіль")
    await state.set_state(MenuStates.PROFILE_MENU)
    await message.answer(
        "У розділі 'Мій Профіль' ви можете переглянути свою статистику, досягнення, налаштування та іншу інформацію.",
        reply_markup=get_profile_menu()
    )

# Обробник для кнопок розділу "Навігація"
@router.message(F.text == MenuButton.HEROES.value)
async def cmd_heroes(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Персонажі")
    await state.set_state(MenuStates.HEROES_MENU)
    await message.answer(
        "Виберіть категорію героїв:",
        reply_markup=get_heroes_menu(),
    )

@router.message(F.text == MenuButton.GUIDES.value)
async def cmd_guides(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Гайди")
    await state.set_state(MenuStates.GUIDES_MENU)
    await message.answer(
        "Виберіть категорію гайдів:",
        reply_markup=get_guides_menu(),
    )

@router.message(F.text == MenuButton.COUNTER_PICKS.value)
async def cmd_counter_picks(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Контр-піки")
    await state.set_state(MenuStates.COUNTER_PICKS_MENU)
    await message.answer(
        "Виберіть опцію Контр-піків:",
        reply_markup=get_counter_picks_menu(),
    )

@router.message(F.text == MenuButton.BUILDS.value)
async def cmd_builds(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Білди")
    await state.set_state(MenuStates.BUILDS_MENU)
    await message.answer(
        "Виберіть опцію Білдів:",
        reply_markup=get_builds_menu(),
    )

@router.message(F.text == MenuButton.VOTING.value)
async def cmd_voting(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Голосування")
    await state.set_state(MenuStates.VOTING_MENU)
    await message.answer(
        "Виберіть опцію Голосування:",
        reply_markup=get_voting_menu(),
    )

# Обробники для розділу "Персонажі"
@router.message(F.text == MenuButton.SEARCH_HERO.value)
async def cmd_search_hero(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Пошук Персонажа")
    await message.answer(
        "Будь ласка, введіть ім'я персонажа для пошуку:",
    )
    await state.set_state(MenuStates.HERO_CLASS_MENU)  # Можливо, створити окремий стан

@router.message(F.text.in_(heroes_by_class.keys()))
async def cmd_select_class(message: Message, state: FSMContext):
    hero_class = message.text
    logger.info(f"Користувач {message.from_user.id} обрав клас {hero_class}")
    await state.set_state(MenuStates.HERO_CLASS_MENU)
    await message.answer(
        f"Виберіть героя з класу {hero_class}:",
        reply_markup=get_hero_class_menu(hero_class)
    )

@router.message(F.text == MenuButton.COMPARISON.value)
async def cmd_comparison(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Порівняння")
    await message.answer(
        "Функція порівняння героїв ще в розробці.",
        reply_markup=get_heroes_menu(),
    )

# Обробник вибору конкретного героя
@router.message(F.text.in_(sum(heroes_by_class.values(), [])))
async def cmd_hero_selected(message: Message, state: FSMContext):
    hero_name = message.text
    logger.info(f"Користувач {message.from_user.id} обрав героя {hero_name}")
    await state.set_state(MenuStates.MAIN_MENU)
    await message.answer(
        f"Ви обрали героя {hero_name}. Інформація про героя буде додана пізніше.",
        reply_markup=get_main_menu(),
    )

# Обробники для розділу "Гайди"
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

# Обробники для розділу "Контр-піки"
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

# Обробники для розділу "Білди"
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

# Обробники для розділу "Голосування"
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

# Обробник для розділу "Профіль"
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

@router.message(F.text == MenuButton.BADGES.value)
async def cmd_badges(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Мої Бейджі")
    await message.answer(
        "Ваші бейджі: [дані будуть доступні пізніше]",
        reply_markup=get_profile_menu(),
    )

@router.message(F.text == MenuButton.PROGRESS.value)
async def cmd_progress(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Прогрес")
    await message.answer(
        "Ваш прогрес: [дані будуть доступні пізніше]",
        reply_markup=get_profile_menu(),
    )

@router.message(F.text == MenuButton.TOURNAMENT_STATS.value)
async def cmd_tournament_stats(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Турнірна Статистика")
    await message.answer(
        "Турнірна статистика: [дані будуть доступні пізніше]",
        reply_markup=get_profile_menu(),
    )

@router.message(F.text == MenuButton.AWARDS.value)
async def cmd_awards(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Отримані Нагороди")
    await message.answer(
        "Отримані нагороди: [дані будуть доступні пізніше]",
        reply_markup=get_profile_menu(),
    )

@router.message(F.text == MenuButton.LANGUAGE.value)
async def cmd_language_selection(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Мова Інтерфейсу")
    await message.answer(
        "Виберіть мову інтерфейсу:",
        reply_markup=get_language_selection_menu(),
    )
    await state.set_state(MenuStates.SETTINGS_MENU)

@router.message(F.text == MenuButton.CHANGE_USERNAME.value)
async def cmd_change_username(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Змінити Username")
    await message.answer(
        "Будь ласка, введіть новий Username:",
    )
    await state.set_state(MenuStates.CHANGE_USERNAME)

@router.message(F.text == MenuButton.UPDATE_ID.value)
async def cmd_update_id(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Оновити ID Гравця")
    await message.answer(
        "Будь ласка, введіть ваш ID гравця:",
    )
    await state.set_state(MenuStates.UPDATE_ID)

@router.message(F.text == MenuButton.NOTIFICATIONS.value)
async def cmd_notifications(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Сповіщення")
    await message.answer(
        "Налаштування сповіщень:",
        reply_markup=get_notifications_menu(),
    )
    await state.set_state(MenuStates.NOTIFICATIONS_MENU)

@router.message(F.text == MenuButton.SEND_FEEDBACK.value)
async def cmd_send_feedback(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Надіслати Відгук")
    await message.answer(
        "Будь ласка, поділіться своїм відгуком або ідеєю:",
    )
    await state.set_state(MenuStates.FEEDBACK_MENU)

@router.message(F.text == MenuButton.REPORT_BUG.value)
async def cmd_report_bug(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Повідомити про Помилку")
    await message.answer(
        "Будь ласка, опишіть знайдену помилку:",
    )
    await state.set_state(MenuStates.FEEDBACK_MENU)

@router.message(F.text == MenuButton.INSTRUCTIONS.value)
async def cmd_instructions(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Інструкції")
    await message.answer(
        "Інструкції: [дані будуть доступні пізніше]",
        reply_markup=get_help_menu(),
    )

@router.message(F.text == MenuButton.FAQ.value)
async def cmd_faq(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав FAQ")
    await message.answer(
        "FAQ: [дані будуть доступні пізніше]",
        reply_markup=get_help_menu(),
    )

@router.message(F.text == MenuButton.HELP_SUPPORT.value)
async def cmd_help_support(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Підтримку")
    await message.answer(
        "Підтримка: [дані будуть доступні пізніше]",
        reply_markup=get_help_menu(),
    )

# Кнопка "Назад"
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
    elif current_state in [MenuStates.HEROES_MENU.state, MenuStates.GUIDES_MENU.state,
                           MenuStates.COUNTER_PICKS_MENU.state, MenuStates.BUILDS_MENU.state,
                           MenuStates.VOTING_MENU.state]:
        await state.set_state(MenuStates.NAVIGATION_MENU)
        await message.answer(
            "🔙 Повернення до меню 'Навігація':",
            reply_markup=get_navigation_menu(),
        )
    elif current_state == MenuStates.HERO_CLASS_MENU.state:
        await state.set_state(MenuStates.HEROES_MENU)
        await message.answer(
            "🔙 Повернення до меню 'Персонажі':",
            reply_markup=get_heroes_menu(),
        )
    elif current_state in [MenuStates.PROFILE_MENU.state, MenuStates.STATISTICS_MENU.state,
                           MenuStates.ACHIEVEMENTS_MENU.state, MenuStates.SETTINGS_MENU.state,
                           MenuStates.FEEDBACK_MENU.state, MenuStates.HELP_MENU.state]:
        await state.set_state(MenuStates.PROFILE_MENU)
        await message.answer(
            "🔙 Повернення до меню 'Мій Профіль':",
            reply_markup=get_profile_menu(),
        )
    elif current_state in [MenuStates.CHANGE_USERNAME.state, MenuStates.UPDATE_ID.state,
                           MenuStates.NOTIFICATIONS_MENU.state]:
        await state.set_state(MenuStates.SETTINGS_MENU)
        await message.answer(
            "🔙 Повернення до меню 'Налаштування':",
            reply_markup=get_settings_menu(),
        )
    else:
        # Якщо стан невідомий, повертаємо до головного меню
        await state.set_state(MenuStates.MAIN_MENU)
        await message.answer(
            "🔙 Повернення до головного меню:",
            reply_markup=get_main_menu(),
        )

# Кнопка "Повернутися до Головного Меню"
@router.message(F.text == MenuButton.RETURN_TO_MAIN.value)
async def cmd_return_to_main(message: Message, state: FSMContext):
    logger.info(f"Користувач {message.from_user.id} обрав Повернутися до Головного Меню")
    await state.set_state(MenuStates.MAIN_MENU)
    await message.answer(
        "🔙 Повернення до головного меню:",
        reply_markup=get_main_menu(),
    )

# Обробник для невідомих повідомлень
@router.message()
async def unknown_command(message: Message, state: FSMContext):
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")
    await state.set_state(MenuStates.MAIN_MENU)
    await message.answer(
        "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче.",
        reply_markup=get_main_menu(),
    )

# Функція для налаштування обробників
def setup_handlers(dp):
    dp.include_router(router)
