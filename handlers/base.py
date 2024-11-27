import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from enum import Enum
from keyboards.menus import (
    get_main_menu,
    get_navigation_menu,
    get_heroes_menu,
    get_guides_menu,
    get_counter_picks_menu,
    get_builds_menu,
    get_voting_menu,
    get_profile_menu,
)

# Налаштування логування
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Enum для тексту кнопок
class MenuTexts(Enum):
    NAVIGATION = "🧭 Навігація"
    HEROES = "🛡️ Персонажі"
    GUIDES = "📚 Гайди"
    COUNTER_PICKS = "⚖️ Контр-піки"
    BUILDS = "⚜️ Білди"
    VOTING = "📊 Голосування"
    PROFILE = "🪪 Профіль"
    BACK = "🔄 Назад"

# Створюємо роутер
router = Router()

# Команда /start
@router.message(Command("start"))
async def cmd_start(message: Message):
    """
    Обробник команди /start.
    Відправляє привітальне повідомлення та показує головне меню.
    """
    logger.info(f"Користувач {message.from_user.id} викликав /start")
    await message.answer(
        "👋 Вітаємо у Mobile Legends Tournament Bot!\n\n"
        "🎮 Цей бот допоможе вам:\n"
        "• Організовувати турніри\n"
        "• Зберігати скріншоти персонажів\n"
        "• Відстежувати активність\n"
        "• Отримувати досягнення\n\n"
        "Оберіть опцію з меню нижче 👇",
        reply_markup=get_main_menu(),
    )

# Обробники для кнопок меню
@router.message(F.text == MenuTexts.NAVIGATION.value)
async def cmd_navigation(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Навігацію")
    await message.answer(
        "Виберіть опцію навігації:",
        reply_markup=get_navigation_menu(),
    )

@router.message(F.text == MenuTexts.HEROES.value)
async def cmd_heroes(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Персонажі")
    await message.answer(
        "Виберіть категорію героїв:",
        reply_markup=get_heroes_menu(),
    )

@router.message(F.text == MenuTexts.GUIDES.value)
async def cmd_guides(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Гайди")
    await message.answer(
        "Виберіть гайди:",
        reply_markup=get_guides_menu(),
    )

@router.message(F.text == MenuTexts.COUNTER_PICKS.value)
async def cmd_counter_picks(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Контр-піки")
    await message.answer(
        "Виберіть контр-піки:",
        reply_markup=get_counter_picks_menu(),
    )

@router.message(F.text == MenuTexts.BUILDS.value)
async def cmd_builds(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Білди")
    await message.answer(
        "Виберіть білди:",
        reply_markup=get_builds_menu(),
    )

@router.message(F.text == MenuTexts.VOTING.value)
async def cmd_voting(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Голосування")
    await message.answer(
        "Виберіть опцію голосування:",
        reply_markup=get_voting_menu(),
    )

@router.message(F.text == MenuTexts.PROFILE.value)
async def cmd_profile(message: Message):
    logger.info(f"Користувач {message.from_user.id} обрав Профіль")
    await message.answer(
        "Виберіть опцію профілю:",
        reply_markup=get_profile_menu(),
    )

# Кнопка "Назад"
@router.message(F.text == MenuTexts.BACK.value)
async def cmd_back(message: Message):
    logger.info(f"Користувач {message.from_user.id} натиснув 'Назад'")
    await message.answer(
        "🔙 Повернення до попереднього меню:",
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
