# handlers/base_handler.py

import logging
from typing import Optional

from aiogram import Router, Bot
from aiogram.types import Message, InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

# Імпорт власних утиліт (з вашого проєкту)
from utils.interface_manager import UIState, update_interface, safe_delete_message

logger = logging.getLogger(__name__)

class BaseHandler:
    """
    Базовий клас для всіх обробників меню.
    Забезпечує спільний Router та метод handle_transition(...)
    для переходу між станами та оновлення інтерфейсу.
    """

    def __init__(self, name: str):
        """
        :param name: Назва обробника, яка використовується для логування.
        """
        # Створюємо Router з даним іменем,
        # аби уникнути конфліктів і для кращої організації хендлерів.
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
        """
        Універсальний метод для обробки переходів між станами та 
        оновлення двох повідомлень бота: «екран» та «пульт».

        :param message: Об'єкт повідомлення від користувача.
        :param state: Поточний контекст стану (FSMContext).
        :param bot: Екземпляр бота.
        :param new_state: Новий стан FSM, куди необхідно перейти.
        :param control_text: Текст для «пульта» (Reply-клавіатура).
        :param control_markup: Reply-клавіатура для «пульта».
        :param screen_text: Текст для «екрану» (Inline-клавіатура).
        :param screen_markup: (опційно) Inline-клавіатура для «екрану».
        """

        # 1. Видаляємо повідомлення користувача, щоб не засмічувати чат.
        await safe_delete_message(bot, message.chat.id, message.message_id)

        # 2. Витягуємо поточний стан інтерфейсу з FSM
        data = await state.get_data()
        current_ui = UIState(**data)  # UIState - ваша структура з interface_manager

        # 3. Оновлюємо інтерфейс (два повідомлення: екран + пульт)
        new_ui = await update_interface(
            bot=bot,
            chat_id=message.chat.id,
            ui_state=current_ui,
            control_text=control_text,
            control_markup=control_markup,
            screen_text=screen_text,
            screen_markup=screen_markup
        )

        # 4. Встановлюємо новий стан FSM
        await state.set_state(new_state)

        # 5. Зберігаємо оновлений стан UI у FSM
        await state.update_data(
            bot_message_id=new_ui.bot_message_id,
            interactive_message_id=new_ui.interactive_message_id,
            last_text=new_ui.last_text,
            last_keyboard=new_ui.last_keyboard
        )

        # Логування переходу
        self.logger.info(
            f"[handle_transition] User {message.from_user.id} -> State {new_state}"
        )