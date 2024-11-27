# utils/message_formatter.py

from aiogram.types import Message, InlineKeyboardMarkup

class MessageFormatter:
    @staticmethod
    async def update_menu_message(
        message: Message,
        title: str,
        description: str,
        keyboard: InlineKeyboardMarkup
    ):
        """Оновлює існуюче повідомлення меню"""
        formatted_text = (
            f"<b>{title}</b>\n\n"
            f"{description}"
        )
        
        try:
            await message.edit_text(
                text=formatted_text,
                reply_markup=keyboard,
                parse_mode="HTML"
            )
        except Exception as e:
            # Якщо не можемо відредагувати, надсилаємо нове
            await message.answer(
                text=formatted_text,
                reply_markup=keyboard,
                parse_mode="HTML"
            )
