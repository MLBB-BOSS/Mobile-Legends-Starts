from aiogram import Router, F
from aiogram.types import Message
from keyboards.navigation_menu import NavigationMenu
from keyboards.main_menu import MainMenu

router = Router()

@router.message(F.text == "🧭 Навігація")
async def handle_navigation(message: Message):
    """Обробка кнопки 'Навігація'."""
    await message.reply(
        "Це розділ навігації. Оберіть опцію:",
        reply_markup=NavigationMenu.get_navigation_menu()
    )

@router.message(F.text == "🔙 Назад")
async def handle_back(message: Message):
    """Обробка кнопки 'Назад' для повернення до головного меню."""
    await message.reply(
        "Повернення до головного меню. Оберіть дію:",
        reply_markup=MainMenu.get_main_menu()
    )
