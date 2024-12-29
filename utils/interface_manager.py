#utils/interface_manager.py
from dataclasses import dataclass
from typing import Optional
from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup, ReplyKeyboardMarkup

@dataclass
class UIState:
    """Стан інтерфейсу користувача"""
    interactive_message_id: Optional[int] = None  # ID "екрану"
    control_message_id: Optional[int] = None      # ID "пульта"
    last_text: Optional[str] = None               # Останній текст
    last_keyboard: Optional[dict] = None          # Остання клавіатура

class InterfaceManager:
    """Менеджер інтерфейсу для управління екраном та пультом"""
    def __init__(self, bot: Bot):
        self.bot = bot

    async def safe_delete_message(self, chat_id: int, message_id: Optional[int]) -> bool:
        """Безпечне видалення повідомлення"""
        if message_id:
            try:
                await self.bot.delete_message(chat_id, message_id)
                return True
            except Exception as e:
                logger.warning(f"Помилка видалення повідомлення: {e}")
        return False

    async def update_interface(
        self,
        chat_id: int,
        ui_state: UIState,
        control_text: str,
        control_markup: ReplyKeyboardMarkup,
        screen_text: str,
        screen_markup: Optional[InlineKeyboardMarkup] = None
    ) -> UIState:
        """Оновлення обох компонентів інтерфейсу"""
        # Видаляємо старий пульт
        await self.safe_delete_message(chat_id, ui_state.control_message_id)

        # Відправляємо новий пульт
        new_control = await self.bot.send_message(
            chat_id=chat_id,
            text=control_text,
            reply_markup=control_markup
        )

        # Оновлюємо екран
        if ui_state.interactive_message_id:
            try:
                await self.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=ui_state.interactive_message_id,
                    text=screen_text,
                    reply_markup=screen_markup
                )
            except Exception as e:
                logger.warning(f"Помилка оновлення екрану: {e}")

        # Повертаємо новий стан інтерфейсу
        return UIState(
            interactive_message_id=ui_state.interactive_message_id,
            control_message_id=new_control.message_id,
            last_text=control_text,
            last_keyboard=control_markup
        )
