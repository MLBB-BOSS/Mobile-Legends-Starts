#utils/interface_manager.py
from dataclasses import dataclass
from typing import Optional
from aiogram import Bot
from aiogram.types import Message, InlineKeyboardMarkup, ReplyKeyboardMarkup
import logging

logger = logging.getLogger(__name__)

@dataclass
class UIState:
    """Стан інтерфейсу користувача"""
    bot_message_id: Optional[int] = None  # ID "пульта"
    interactive_message_id: Optional[int] = None  # ID "екрану"
    last_text: Optional[str] = None
    last_keyboard: Optional[dict] = None

async def safe_delete_message(bot: Bot, chat_id: int, message_id: Optional[int]) -> bool:
    """Безпечне видалення повідомлення"""
    if message_id:
        try:
            await bot.delete_message(chat_id, message_id)
            return True
        except Exception as e:
            logger.warning(f"Failed to delete message: {e}")
    return False

async def update_interface(
    bot: Bot,
    chat_id: int,
    ui_state: UIState,
    control_text: str,
    control_markup: ReplyKeyboardMarkup,
    screen_text: str,
    screen_markup: Optional[InlineKeyboardMarkup] = None
) -> UIState:
    """Оновлення компонентів інтерфейсу"""
    # Видаляємо старий пульт
    await safe_delete_message(bot, chat_id, ui_state.bot_message_id)

    # Відправляємо новий пульт
    new_control = await bot.send_message(
        chat_id=chat_id,
        text=control_text,
        reply_markup=control_markup
    )

    # Оновлюємо екран
    if ui_state.interactive_message_id:
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=ui_state.interactive_message_id,
                text=screen_text,
                reply_markup=screen_markup
            )
        except Exception as e:
            logger.warning(f"Failed to update screen: {e}")

    # Повертаємо новий стан інтерфейсу
    return UIState(
        bot_message_id=new_control.message_id,
        interactive_message_id=ui_state.interactive_message_id,
        last_text=control_text,
        last_keyboard=control_markup
    )
