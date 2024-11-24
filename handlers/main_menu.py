# handlers/main_menu.py
# Created: 2024-11-24
# Author: MLBB-BOSS
# Description: Обробники команд головного меню

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from keyboards.main_menu import MainMenuKeyboard

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обробник команди /start"""
    await message.answer(
        "Вітаємо в MLS Bot! 🎮\n"
        "Це ваш помічник для організації турнірів Mobile Legends.\n"
        "Оберіть опцію з меню нижче:",
        reply_markup=MainMenuKeyboard.get_keyboard()
    )

@router.callback_query(F.data == "tournaments")
async def show_tournaments(callback: CallbackQuery):
    """Обробник кнопки турнірів"""
    await callback.answer("Відкриваю список турнірів...")
    # Додайте вашу логіку тут

@router.callback_query(F.data == "profile")
async def show_profile(callback: CallbackQuery):
    """Обробник кнопки профілю"""
    await callback.answer("Відкриваю ваш профіль...")
    # Додайте вашу логіку тут
