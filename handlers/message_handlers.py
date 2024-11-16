# File: handlers/message_handlers.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards import NavigationMenu, ProfileMenu, MainMenu
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обробляє команду /start"""
    await message.answer(
        "Вітаю! Оберіть розділ:",
        reply_markup=MainMenu.get_main_menu()
    )

@router.message(F.text == "🧭 Навігація")
async def handle_navigation(message: Message):
    """Обробляє натискання кнопки Навігація"""
    logger.info(f"Отримано команду навігації: {message.text}")
    await message.answer(
        "Оберіть розділ навігації:",
        reply_markup=NavigationMenu.get_navigation_menu()
    )

@router.message(F.text == "🪧 Мій Кабінет")
async def handle_profile(message: Message):
    """Обробляє натискання кнопки Мій Кабінет"""
    logger.info(f"Отримано команду профілю: {message.text}")
    await message.answer(
        "Ваш особистий кабінет:",
        reply_markup=ProfileMenu.get_profile_menu()
    )

@router.message(F.text == "🔙 Головне меню")
async def handle_back_to_main(message: Message):
    """Обробляє повернення до головного меню"""
    logger.info(f"Отримано команду повернення: {message.text}")
    await message.answer(
        "Головне меню:",
        reply_markup=MainMenu.get_main_menu()
    )

# Обробник для логування необроблених повідомлень
@router.message()
async def handle_unknown(message: Message):
    """Логує необроблені повідомлення"""
    logger.info(f"Необроблене повідомлення: '{message.text}'")
    await message.answer(
        "Вибачте, але я не розумію цю команду. Будь ласка, використовуйте кнопки меню.",
        reply_markup=MainMenu.get_main_menu()
    )
