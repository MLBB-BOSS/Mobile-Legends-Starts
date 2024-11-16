# Path: handlers/message_handlers.py
# Description: Основні обробники повідомлень для телеграм бота
# Author: MLBB-BOSS
# Last modified: 2024-11-16

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from config.messages.base import get_messages
from keyboards import MainMenu, NavigationMenu, ProfileMenu
import logging

# Налаштування логування
logger = logging.getLogger(__name__)

# Ініціалізація роутера та завантаження повідомлень
router = Router()
messages = get_messages()

@router.message(Command("start"))
async def cmd_start(message: Message):
    """
    Обробник команди /start
    Відправляє привітальне повідомлення та показує головне меню
    """
    await message.answer(
        messages.welcome_message,
        parse_mode="HTML",
        reply_markup=MainMenu.get_main_menu()
    )

@router.message(F.text == "🧭 Навігація")
async def handle_navigation(message: Message):
    """
    Обробник кнопки навігації
    Показує меню навігації з доступними опціями
    """
    await message.answer(
        messages.navigation.main,
        parse_mode="HTML",
        reply_markup=NavigationMenu.get_navigation_menu()
    )

@router.message(F.text == "🪧 Мій Кабінет")
async def handle_profile(message: Message):
    """
    Обробник кнопки профілю
    Показує меню особистого кабінету користувача
    """
    await message.answer(
        messages.profile.main,
        parse_mode="HTML",
        reply_markup=ProfileMenu.get_profile_menu()
    )

@router.message()
async def handle_unknown(message: Message):
    """
    Обробник невідомих повідомлень
    Логує невідомі команди та повертає користувача до головного меню
    """
    logger.info(f"Отримано необроблене повідомлення: {message.text}")
    await message.answer(
        "Вибачте, я не розумію цю команду. Використовуйте меню для навігації.",
        reply_markup=MainMenu.get_main_menu()
    )
