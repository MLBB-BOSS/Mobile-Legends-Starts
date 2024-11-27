import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
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

# Налаштування логування
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Створюємо роутер
router = Router()

# Команда /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    """
    Обробник команди /start.
    Відправляє привітальне повідомлення та показує головне меню.
    """
    user_name = message.from_user.first_name
    logger.info(f"Користувач {message.from_user.id} викликав /start")
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

# Обробники для кнопок меню
@router.message(F.text == MenuButton.NAVIGATION.value)
async def cmd_navigation(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Навігацію")
    await message.answer(
        "Виберіть опцію навігації:",
        reply_markup=get_navigation_menu(),
    )

@router.message(F.text == MenuButton.PROFILE.value)
async def cmd_profile(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Мій Профіль")
    await message.answer(
        "Виберіть опцію профілю:",
        reply_markup=get_profile_menu(),
    )

# Додані обробники для меню "Мій Профіль"
@router.message(F.text == MenuButton.ACTIVITY.value)
async def cmd_activity(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Загальна Активність")
    await message.answer(
        "Ваша загальна активність: [дані будуть доступні пізніше]",
        reply_markup=get_profile_menu(),
    )

@router.message(F.text == MenuButton.RANKING.value)
async def cmd_ranking(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Рейтинг")
    await message.answer(
        "Ваш поточний рейтинг: [дані будуть доступні пізніше]",
        reply_markup=get_profile_menu(),
    )

@router.message(F.text == MenuButton.GAME_STATS.value)
async def cmd_game_stats(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Ігрова Статистика")
    await message.answer(
        "Ваша ігрова статистика: [дані будуть доступні пізніше]",
        reply_markup=get_profile_menu(),
    )

@router.message(F.text == MenuButton.HEROES.value)
async def cmd_heroes(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Персонажі")
    await message.answer(
        "Виберіть категорію героїв:",
        reply_markup=get_heroes_menu(),
    )

# Список кнопок класів
class_buttons = list(menu_button_to_class.keys())

@router.message(F.text.in_(class_buttons))
async def cmd_hero_class(message: Message):
    hero_class = menu_button_to_class.get(message.text)
    if hero_class:
        logger.info(f"Користувач {message.from_user.id} обрав клас {hero_class}")
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

# Обробник для кнопки "Порівняння"
@router.message(F.text == MenuButton.COMPARISON.value)
async def cmd_comparison(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Порівняння")
    # Додайте тут логіку для обробки порівняння героїв
    await message.answer(
        "Функція порівняння героїв ще в розробці.",
        reply_markup=get_heroes_menu(),
    )

# Список усіх героїв
all_heroes = set()
for heroes in heroes_by_class.values():
    all_heroes.update(heroes)

@router.message(F.text.in_(all_heroes))
async def cmd_hero_selected(message: Message):
    hero_name = message.text
    logger.info(f"Користувач {message.from_user.id} обрав героя {hero_name}")
    # Тут можна додати логіку для відображення інформації про героя
    await message.answer(
        f"Ви обрали героя {hero_name}. Інформація про героя буде додана пізніше.",
        reply_markup=get_main_menu(),
    )

@router.message(F.text == MenuButton.GUIDES.value)
async def cmd_guides(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Гайди")
    await message.answer(
        "Виберіть гайди:",
        reply_markup=get_guides_menu(),
    )

# Додамо обробники для кнопок меню "Гайди"
@router.message(F.text == MenuButton.NEW_GUIDES.value)
async def cmd_new_guides(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Нові Гайди")
    await message.answer(
        "Нові гайди ще в розробці.",
        reply_markup=get_guides_menu(),
    )

@router.message(F.text == MenuButton.POPULAR_GUIDES.value)
async def cmd_popular_guides(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Популярні Гайди")
    await message.answer(
        "Популярні гайди ще в розробці.",
        reply_markup=get_guides_menu(),
    )

@router.message(F.text == MenuButton.BEGINNER_GUIDES.value)
async def cmd_beginner_guides(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Для Початківців")
    await message.answer(
        "Гайди для початківців ще в розробці.",
        reply_markup=get_guides_menu(),
    )

@router.message(F.text == MenuButton.ADVANCED_TECHNIQUES.value)
async def cmd_advanced_techniques(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Просунуті Техніки")
    await message.answer(
        "Просунуті техніки ще в розробці.",
        reply_markup=get_guides_menu(),
    )

@router.message(F.text == MenuButton.TEAMPLAY_GUIDES.value)
async def cmd_teamplay_guides(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Командна Гра")
    await message.answer(
        "Гайди по командній грі ще в розробці.",
        reply_markup=get_guides_menu(),
    )

@router.message(F.text == MenuButton.COUNTER_PICKS.value)
async def cmd_counter_picks(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Контр-піки")
    await message.answer(
        "Виберіть контр-піки:",
        reply_markup=get_counter_picks_menu(),
    )

# Додамо обробники для кнопок меню "Контр-піки"
@router.message(F.text == MenuButton.COUNTER_SEARCH.value)
async def cmd_counter_search(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Пошук Контр-піку")
    await message.answer(
        "Функція пошуку контр-піків ще в розробці.",
        reply_markup=get_counter_picks_menu(),
    )

@router.message(F.text == MenuButton.COUNTER_LIST.value)
async def cmd_counter_list(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Список Персонажів")
    await message.answer(
        "Список контр-піків ще в розробці.",
        reply_markup=get_counter_picks_menu(),
    )

@router.message(F.text == MenuButton.BUILDS.value)
async def cmd_builds(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Білди")
    await message.answer(
        "Виберіть білди:",
        reply_markup=get_builds_menu(),
    )

# Додамо обробники для кнопок меню "Білди"
@router.message(F.text == MenuButton.CREATE_BUILD.value)
async def cmd_create_build(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Створити Білд")
    await message.answer(
        "Функція створення білдів ще в розробці.",
        reply_markup=get_builds_menu(),
    )

@router.message(F.text == MenuButton.MY_BUILDS.value)
async def cmd_my_builds(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Мої Білди")
    await message.answer(
        "Ваші білди ще в розробці.",
        reply_markup=get_builds_menu(),
    )

@router.message(F.text == MenuButton.POPULAR_BUILDS.value)
async def cmd_popular_builds(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Популярні Білди")
    await message.answer(
        "Популярні білди ще в розробці.",
        reply_markup=get_builds_menu(),
    )

@router.message(F.text == MenuButton.VOTING.value)
async def cmd_voting(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Голосування")
    await message.answer(
        "Виберіть опцію голосування:",
        reply_markup=get_voting_menu(),
    )

# Додамо обробники для кнопок меню "Голосування"
@router.message(F.text == MenuButton.CURRENT_VOTES.value)
async def cmd_current_votes(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Поточні Опитування")
    await message.answer(
        "Поточні опитування ще в розробці.",
        reply_markup=get_voting_menu(),
    )

@router.message(F.text == MenuButton.MY_VOTES.value)
async def cmd_my_votes(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Мої Голосування")
    await message.answer(
        "Ваші голосування ще в розробці.",
        reply_markup=get_voting_menu(),
    )

@router.message(F.text == MenuButton.SUGGEST_TOPIC.value)
async def cmd_suggest_topic(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Запропонувати Тему")
    await message.answer(
        "Функція пропозиції тем ще в розробці.",
        reply_markup=get_voting_menu(),
    )

# Кнопка "Назад"
@router.message(F.text == MenuButton.BACK.value)
async def cmd_back(message: Message):
    logger.info(f"Користувач {message.from_user.id} натиснув 'Назад'")
    # Ви можете додати логіку для повернення до попереднього меню
    # Наприклад, якщо користувач знаходиться в меню профілю, повернути його до навігаційного меню
    await message.answer(
        "🔙 Повернення до головного меню:",
        reply_markup=get_main_menu(),
    )

# Обробник для невідомих повідомлень
@router.message()
async def unknown_command(message: Message):
    logger.warning(f"Невідоме повідомлення від {message.from_user.id}: {message.text}")
    await message.answer(
        "❗ Вибачте, я не розумію цю команду. Скористайтеся меню нижче.",
        reply_markup=get_main_menu(),
    )
