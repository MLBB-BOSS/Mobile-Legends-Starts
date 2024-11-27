# utils/message_formatter.py

from aiogram.types import Message
from aiogram.types import InlineKeyboardMarkup

class MessageFormatter:
    @staticmethod
    async def update_menu_message(message: Message, title: str, description: str, keyboard: InlineKeyboardMarkup):
        """
        Відправляє форматоване повідомлення з меню.
        :param message: Об'єкт повідомлення.
        :param title: Заголовок меню.
        :param description: Опис меню.
        :param keyboard: Клавіатура меню.
        """
        await message.answer(
            f"<b>{title}</b>\n\n{description}",
            parse_mode="HTML",
            reply_markup=keyboard
        )
