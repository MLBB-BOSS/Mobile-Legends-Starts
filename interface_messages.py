from dataclasses import dataclass
from typing import Optional
from aiogram import Bot  # Додайте цей імпорт

@dataclass
class InterfaceMessages:
    """Клас для управління повідомленнями інтерфейсу."""
    bot_message_id: Optional[int] = None
    interactive_message_id: Optional[int] = None
    last_text: str = ""
    last_keyboard: Optional[dict] = None

    async def update(
        self,
        bot: Bot,  # Використовуємо імпортований клас Bot
        chat_id: int,
        new_message_id: int,
        new_interactive_id: int,
        text: str,
        keyboard: dict
    ) -> None:
        """Оновлення даних повідомлень."""
        self.bot_message_id = new_message_id
        self.interactive_message_id = new_interactive_id
        self.last_text = text
        self.last_keyboard = keyboard
