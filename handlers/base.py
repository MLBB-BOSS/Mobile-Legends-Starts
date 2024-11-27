# handlers.py

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

@router.message(F.text == MenuButton.COUNTER_PICKS.value)
async def cmd_counter_picks(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Контр-піки")
    await message.answer(
        "Виберіть контр-піки:",
        reply_markup=get_counter_picks_menu(),
    )

@router.message(F.text == MenuButton.BUILDS.value)
async def cmd_builds(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Білди")
    await message.answer(
        "Виберіть білди:",
        reply_markup=get_builds_menu(),
    )

@router.message(F.text == MenuButton.VOTING.value)
async def cmd_voting(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Голосування")
    await message.answer(
        "Виберіть опцію голосування:",
        reply_markup=get_voting_menu(),
    )

# Кнопка "Назад"
@router.message(F.text == MenuButton.BACK.value)
async def cmd_back(message: Message):
    logger.info(f"Користувач {message.from_user.id} натиснув 'Назад'")
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
