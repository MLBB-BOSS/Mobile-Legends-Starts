# UTC:20:42
# 2024-11-24
# handlers/main_menu.py
# Author: MLBB-BOSS
# Description: Main menu message handlers
# The era of artificial intelligence.

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards.main_menu import main_menu_keyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Handler for /start command"""
    await message.answer(
        "Вітаємо в MLS Bot! 🎮\n"
        "Ваш помічник у світі Mobile Legends!\n"
        "Оберіть опцію:",
        reply_markup=main_menu_keyboard()
    )

@router.callback_query(F.data == "help")
async def help_handler(callback: CallbackQuery):
    """Handler for help button"""
    await callback.answer(
        "Це бот для організації турнірів Mobile Legends.\n"
        "Використовуйте меню для навігації.",
        show_alert=True
    )

@router.callback_query(F.data == "tournaments")
async def tournaments_handler(callback: CallbackQuery):
    """Handler for tournaments button"""
    await callback.answer("Відкриваю список турнірів...")
    # Add tournament logic here

@router.callback_query(F.data == "profile")
async def profile_handler(callback: CallbackQuery):
    """Handler for profile button"""
    await callback.answer("Відкриваю ваш профіль...")
    # Add profile logic here
