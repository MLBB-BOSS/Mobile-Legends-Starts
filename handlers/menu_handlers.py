# File: handlers/menu_handlers.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards import MainMenu  # Змінено з NavigationMenu, ProfileMenu на MainMenu

router = Router()

@router.message(Command("start", "menu"))
async def show_main_menu(message: Message):
    """Показує головне меню"""
    keyboard = MainMenu.get_main_menu()
    await message.answer(
        "Ласкаво просимо!\nОберіть опцію:",
        reply_markup=keyboard
    )

@router.message(F.text == "🧭 Навігація")
async def navigation_menu(message: Message):
    await message.answer("Меню навігації в розробці...")

@router.message(F.text == "🪪 Мій Кабінет")
async def profile_menu(message: Message):
    await message.answer("Особистий кабінет в розробці...")
