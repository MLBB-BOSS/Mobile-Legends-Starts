# handlers/menu_handlers.py

from aiogram import Router
from aiogram.filters import Text
from aiogram.types import Message
from keyboards.menus import get_main_menu
from keyboards.navigation_menu import get_navigation_menu

menu_router = Router()

@menu_router.message(Text("Головне меню"))
async def show_main_menu(message: Message):
    await message.answer("Оберіть розділ:", reply_markup=get_main_menu())

@menu_router.message(Text("Навігація"))
async def show_navigation_menu(message: Message):
    await message.answer("Оберіть категорію:", reply_markup=get_navigation_menu())
