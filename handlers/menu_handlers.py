# File: handlers/menu_handlers.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards import MainMenu
from utils.localization import loc

router = Router()

@router.message(Command("start", "menu"))
async def show_main_menu(message: Message):
    keyboard = MainMenu.get_main_menu()
    await message.answer(
        loc.get_message("messages.start_command"),
        reply_markup=keyboard
    )

@router.message(lambda message: message.text == loc.get_message("buttons.navigation"))
async def navigation_menu(message: Message):
    await message.answer("Меню навігації в розробці...")

@router.message(lambda message: message.text == loc.get_message("buttons.profile"))
async def profile_menu(message: Message):
    await message.answer("Особистий кабінет в розробці...")
