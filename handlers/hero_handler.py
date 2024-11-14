# handlers/hero_handler.py

from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.types import CallbackQuery, Message
from services.keyboard_service import get_class_keyboard, get_heroes_keyboard
import logging

logger = logging.getLogger(__name__)

# Ініціалізація маршрутизатора
router = Router()

@router.message(Command("heroes"))
async def heroes_command(message: Message):
    """Виводить клавіатуру для вибору класу героїв."""
    logger.info(f"Користувач {message.from_user.id} обрав команду /heroes.")
    await message.reply("Оберіть клас персонажів:", reply_markup=get_class_keyboard())

@router.callback_query(Text(startswith="class_"))
async def process_class_selection(call: CallbackQuery):
    """Обробляє вибір класу та виводить персонажів цього класу."""
    try:
        hero_class = call.data.split("_")[1]
        logger.info(f"Користувач {call.from_user.id} обрав клас: {hero_class}.")
        await call.message.edit_text(f"Оберіть персонажа з класу {hero_class}:", reply_markup=get_heroes_keyboard(hero_class))
    except IndexError:
        logger.error(f"Невірний формат callback_data: {call.data}")
        await call.answer("Сталася помилка при виборі класу.", show_alert=True)

@router.callback_query(Text(equals="back_to_classes"))
async def back_to_classes(call: CallbackQuery):
    """Повертає користувача до вибору класу."""
    logger.info(f"Користувач {call.from_user.id} повернувся до вибору класу.")
    await call.message.edit_text("Оберіть клас персонажів:", reply_markup=get_class_keyboard())

@router.callback_query(Text(startswith="hero_"))
async def process_hero_selection(call: CallbackQuery):
    """Обробляє вибір конкретного персонажа та показує деталі."""
    try:
        hero_name = call.data.split("_")[1]
        logger.info(f"Користувач {call.from_user.id} обрав героя: {hero_name}.")
        await call.message.edit_text(f"Ви обрали героя {hero_name}. Додаткова інформація буде додана.")
    except IndexError:
        logger.error(f"Невірний формат callback_data: {call.data}")
        await call.answer("Сталася помилка при виборі героя.", show_alert=True)

@router.callback_query(Text(equals="no_data"))
async def handle_no_data(call: CallbackQuery):
    """Обробляє випадок, коли немає даних про вибраний клас."""
    logger.warning(f"Користувач {call.from_user.id} обрав клас без даних.")
    await call.answer("На жаль, інформація про цей клас ще не доступна.", show_alert=True)
