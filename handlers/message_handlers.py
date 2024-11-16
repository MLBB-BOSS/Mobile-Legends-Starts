# File: handlers/message_handlers.py
from aiogram import Router, F
from aiogram.filters import Command  # Додаємо цей імпорт
from aiogram.types import Message
from config.messages.base import get_messages
from keyboards import MainMenu, NavigationMenu, ProfileMenu

router = Router()
messages = get_messages()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        messages.welcome_message,
        parse_mode="HTML",
        reply_markup=MainMenu.get_main_menu()
    )

@router.message(F.text == "🧭 Навігація")
async def handle_navigation(message: Message):
    await message.answer(
        messages.navigation.main,
        parse_mode="HTML",
        reply_markup=NavigationMenu.get_navigation_menu()
    )

@router.message(F.text == "🪧 Мій Кабінет")
async def handle_profile(message: Message):
    await message.answer(
        messages.profile.main,
        parse_mode="HTML",
        reply_markup=ProfileMenu.get_profile_menu()
    )
