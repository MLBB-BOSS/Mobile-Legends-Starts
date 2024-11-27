from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.menus import get_main_menu, get_navigation_menu, get_heroes_menu, get_guides_menu, get_counter_picks_menu, get_builds_menu, get_voting_menu, get_profile_menu

# Створюємо роутер
router = Router()

# Базові команди
@router.message(Command("start"))
async def cmd_start(message: Message):
    """
    Обробник команди /start
    Відправляє привітальне повідомлення та показує головне меню
    """
    await message.answer(
        "👋 Вітаємо у Mobile Legends Tournament Bot!\n\n"
        "🎮 Цей бот допоможе вам:\n"
        "• Організовувати турніри\n"
        "• Зберігати скріншоти персонажів\n"
        "• Відстежувати активність\n"
        "• Отримувати досягнення\n\n"
        "Оберіть опцію з меню нижче 👇",
        reply_markup=get_main_menu()
    )

@router.message(F.text == "🧭 Навігація")
async def cmd_navigation(message: Message):
    """
    Обробник кнопки Навігація
    Показує меню навігації
    """
    await message.answer(
        "Виберіть опцію навігації:",
        reply_markup=get_navigation_menu()
    )

@router.message(F.text == "🛡️ Персонажі")
async def cmd_heroes(message: Message):
    """
    Обробник кнопки Персонажі
    Показує меню вибору героїв
    """
    await message.answer(
        "Виберіть категорію героїв:",
        reply_markup=get_heroes_menu()
    )

@router.message(F.text == "📚 Гайди")
async def cmd_guides(message: Message):
    """
    Обробник кнопки Гайди
    Показує меню гайдів
    """
    await message.answer(
        "Виберіть гайди:",
        reply_markup=get_guides_menu()
    )

@router.message(F.text == "⚖️ Контр-піки")
async def cmd_counter_picks(message: Message):
    """
    Обробник кнопки Контр-піки
    Показує меню контр-піків
    """
    await message.answer(
        "Виберіть контр-піки:",
        reply_markup=get_counter_picks_menu()
    )

@router.message(F.text == "⚜️ Білди")
async def cmd_builds(message: Message):
    """
    Обробник кнопки Білди
    Показує меню білдів
    """
    await message.answer(
        "Виберіть білди:",
        reply_markup=get_builds_menu()
    )

@router.message(F.text == "📊 Голосування")
async def cmd_voting(message: Message):
    """
    Обробник кнопки Голосування
    Показує меню голосування
    """
    await message.answer(
        "Виберіть опцію голосування:",
        reply_markup=get_voting_menu()
    )

@router.message(F.text == "🪪 Профіль")
async def cmd_profile(message: Message):
    """
    Обробник кнопки Профіль
    Показує меню профілю
    """
    await message.answer(
        "Виберіть опцію профілю:",
        reply_markup=get_profile_menu()
    )
