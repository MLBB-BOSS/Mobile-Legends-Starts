# File: handlers/navigation_handlers.py
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Text
from keyboards.navigation_menu import NavigationMenu

router = Router()

@router.message(Text("Навігація"))
async def handle_navigation(message: Message):
    await message.answer(
        "Це розділ навігації. Оберіть опцію:",
        reply_markup=NavigationMenu.get_navigation_menu()
    )
