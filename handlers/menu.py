# handlers/menu.py

from aiogram import Router, F
from aiogram.types import Message
from keyboards.main_menu import get_main_menu
from keyboards.navigation_menu import get_navigation_menu

menu_router = Router()

@menu_router.message(F.text == "/start")
async def show_main_menu(message: Message):
    """
    Показує головне меню.
    """
    await message.answer("Ласкаво просимо! Оберіть опцію:", reply_markup=get_main_menu())

@menu_router.message(F.text == "🧭 Навігація")
async def show_navigation_menu(message: Message):
    """
    Показує меню навігації.
    """
    await message.answer("Оберіть розділ:", reply_markup=get_navigation_menu())
