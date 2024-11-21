# File: handlers/start_command.py

from aiogram import Router, types
from aiogram.filters import Command, Text
from keyboards import MainMenu, NavigationMenu
from utils.localization import loc

router = Router()

@router.message(Command("start"))  # Changed from commands=["start"]
async def start_command(message: types.Message):
    keyboard = MainMenu.get_keyboard()
    welcome_text = loc.get_message("messages.welcome")
    await message.answer(welcome_text, reply_markup=keyboard)

@router.message(Text(text=loc.get_message("buttons.navigation")))  # Changed from lambda
async def show_navigation(message: types.Message):
    keyboard = NavigationMenu.get_keyboard()
    await message.answer("🧭 Навігація", reply_markup=keyboard)
