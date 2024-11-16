# File: handlers/message_handlers.py
from aiogram import Router, F
from aiogram.types import Message
from keyboards import NavigationMenu, ProfileMenu, MainMenu

router = Router()

@router.message(F.text == "🧭 Навігація")
async def handle_navigation(message: Message):
    """Обробляє натискання кнопки Навігація"""
    await message.answer(
        "Оберіть розділ навігації:",
        reply_markup=NavigationMenu.get_navigation_menu()
    )

@router.message(F.text == "🪧 Мій Кабінет")  # Переконайтесь, що текст точно співпадає
async def handle_profile(message: Message):
    """Обробляє натискання кнопки Мій Кабінет"""
    await message.answer(
        "Ваш особистий кабінет:",
        reply_markup=ProfileMenu.get_profile_menu()
    )

@router.message(F.text == "🔙 Головне меню")
async def handle_back_to_main(message: Message):
    """Обробляє повернення до головного меню"""
    await message.answer(
        "Головне меню:",
        reply_markup=MainMenu.get_main_menu()
    )
