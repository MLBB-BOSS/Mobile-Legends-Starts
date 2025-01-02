# handlers/navigation.py

from aiogram import types, Router
from aiogram.types import CallbackQuery
import logging

# Create a router instance
router = Router()

logger = logging.getLogger(__name__)

@router.callback_query(lambda c: c.data in ["navigate", "profile"])
async def handle_navigation_callback(query: CallbackQuery):
    """
    Обробляє натискання інтерактивних кнопок.
    """
    data = query.data
    user_id = query.from_user.id
    logger.info(f"Користувач {user_id} натиснув кнопку: {data}")

    if data == "navigate":
        await query.message.edit_text("Ви обрали навігацію.", reply_markup=None)
        # Додайте логіку для навігації
    elif data == "profile":
        await query.message.edit_text("Ви обрали профіль.", reply_markup=None)
        # Додайте логіку для профілю
    else:
        await query.answer("Невідома дія.")
