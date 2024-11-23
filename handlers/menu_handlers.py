# handlers/menu_handlers.py

from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_menu import get_main_menu
from keyboards.navigation_menu import get_navigation_menu

menu_router = Router()

@menu_router.message(F.text == "/start")
async def handle_start(message: Message):
    """
    Показує головне меню.
    """
    await message.answer("Вітаємо у головному меню! Оберіть опцію:", reply_markup=get_main_menu())

@menu_router.message(F.text == "🧭 Навігація")
async def handle_navigation(message: Message):
    """
    Показує меню «Навігація».
    """
    await message.answer("Оберіть категорію для навігації:", reply_markup=get_navigation_menu())
