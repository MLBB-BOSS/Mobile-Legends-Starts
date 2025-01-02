# handlers/navigation.py

from aiogram import types, Dispatcher
from aiogram.types import CallbackQuery
import logging

logger = logging.getLogger(__name__)

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

def register_navigation_handlers(dp: Dispatcher):
    """
    Реєструє хендлер для обробки callback queries.
    """
    dp.register_callback_query_handler(
        handle_navigation_callback,
        lambda c: c.data in ["navigate", "profile"],
        state="*"
    )
