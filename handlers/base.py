from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.menus import get_main_menu, get_navigation_menu

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

@router.message(Command("help"))
async def cmd_help(message: Message):
    """
    Обробник команди /help
    Показує довідкову інформацію
    """
    await message.answer(
        "📖 Довідка по використанню бота:\n\n"
        "/start - Запустити бота і показати головне меню\n"
        "/help - Показати цю довідку\n"
        "/tournament - Управління турнірами\n"
        "/profile - Ваш профіль та досягнення\n"
        "/heroes - Галерея скріншотів героїв\n\n"
        "Для навігації використовуйте кнопки меню внизу екрану."
    )

@router.message(Command("tournament"))
async def cmd_tournament(message: Message):
    """
    Обробник команди /tournament
    Показує меню управління турнірами
    """
    await message.answer(
        "🏆 Меню управління турнірами:\n\n"
        "Тут ви можете:\n"
        "• Створити новий турнір\n"
        "• Переглянути активні турніри\n"
        "• Зареєструватися на турнір\n"
        "• Переглянути результати"
    )

@router.message(Command("profile"))
async def cmd_profile(message: Message):
    """
    Обробник команди /profile
    Показує профіль користувача
    """
    await message.answer(
        "👤 Ваш профіль\n\n"
        "Тут буде відображатися:\n"
        "• Ваша статистика\n"
        "• Досягнення\n"
        "• Історія участі в турнірах"
    )

@router.message(Command("heroes"))
async def cmd_heroes(message: Message):
    """
    Обробник команди /heroes
    Показує меню галереї героїв
    """
    await message.answer(
        "🦸‍♂️ Галерея героїв\n\n"
        "Тут ви можете:\n"
        "• Завантажити скріншоти\n"
        "• Переглянути галерею\n"
        "• Шукати героїв"
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

@router.message(F.text == "🪪 Профіль")
async def cmd_profile_button(message: Message):
    """
    Обробник кнопки Профіль
    Показує профіль користувача
    """
    await message.answer(
        "👤 Ваш профіль\n\n"
        "Тут буде відображатися:\n"
        "• Ваша статистика\n"
        "• Досягнення\n"
        "• Історія участі в турнірах"
    )

# Обробник невідомих команд
@router.message(Command(commands=["*"]))
async def cmd_unknown(message: Message):
    """
    Обробник невідомих команд
    """
    await message.answer(
        "❌ Невідома команда.\n"
        "Використайте /help для перегляду доступних команд."
    )
