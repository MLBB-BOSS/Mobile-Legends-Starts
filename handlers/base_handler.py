#handlers/base_handler.py
from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.interface_manager import UIState, update_interface, safe_delete_message
import logging

logger = logging.getLogger(__name__)

class BaseHandler:
    """Базовий клас для всіх обробників меню"""
    def __init__(self, name: str):
        self.router = Router(name=name)
        self.logger = logging.getLogger(f"handlers.{name}")

    async def handle_transition(
        self,
        message: Message,
        state: FSMContext,
        bot: Bot,
        new_state: State,
        control_text: str,
        control_markup: ReplyKeyboardMarkup,
        screen_text: str,
        screen_markup: Optional[InlineKeyboardMarkup] = None
    ):
        """Базовий метод для обробки переходів між станами"""
        # Видаляємо повідомлення користувача
        await safe_delete_message(bot, message.chat.id, message.message_id)

        # Отримуємо поточний стан інтерфейсу
        data = await state.get_data()
        current_ui = UIState(**data)

        # Оновлюємо інтерфейс
        new_ui = await update_interface(
            bot=bot,
            chat_id=message.chat.id,
            ui_state=current_ui,
            control_text=control_text,
            control_markup=control_markup,
            screen_text=screen_text,
            screen_markup=screen_markup
        )

        # Зберігаємо новий стан
        await state.set_state(new_state)
        await state.update_data(
            bot_message_id=new_ui.bot_message_id,
            interactive_message_id=new_ui.interactive_message_id,
            last_text=new_ui.last_text,
            last_keyboard=new_ui.last_keyboard
        )

        self.logger.info(f"State transition: {new_state} for user {message.from_user.id}")
