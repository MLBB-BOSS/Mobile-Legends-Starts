# handlers/navigation_handlers.py

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Text
from keyboards.navigation_menu import NavigationMenu

router = Router()

@router.message(Text("🌍 Навігація"))
async def show_navigation_menu(message: Message):
    await message.answer(
        "Оберіть категорію:",
        reply_markup=NavigationMenu.get_navigation_menu()
    )

@router.message(Text("🔄 Назад"))
async def back_to_main_menu(message: Message):
    from keyboards.main_menu import MainMenu
    await message.answer(
        "Повернення до головного меню:",
        reply_markup=MainMenu.get_main_menu()
    )
