# UTC:21:40
# 2024-11-24
# handlers/main_menu.py
# Author: MLBB-BOSS
# Description: Main menu message handlers
# The era of artificial intelligence.

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.main_menu import get_main_keyboard
from keyboards.navigation_menu import get_navigation_keyboard
from keyboards.profile_menu import get_profile_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Вітаю в MLS Bot! 🎮\n"
        "Ваш помічник у світі Mobile Legends!\n"
        "Оберіть опцію з меню нижче:",
        reply_markup=get_main_keyboard()
    )

@router.message(F.text == "🧭 Навігація")
async def navigation_menu(message: Message):
    await message.answer(
        "Меню навігації:\n"
        "Оберіть потрібний розділ:",
        reply_markup=get_navigation_keyboard()
    )

@router.message(F.text == "🪪 Профіль")
async def profile_menu(message: Message):
    await message.answer(
        "Ваш профіль:\n"
        "Оберіть потрібний розділ:",
        reply_markup=get_profile_keyboard()
    )

@router.message(F.text == "🔙 Назад до Головного")
async def return_to_main(message: Message):
    await message.answer(
        "Головне меню:",
        reply_markup=get_main_keyboard()
    )
