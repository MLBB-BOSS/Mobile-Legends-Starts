from aiogram import Router, Bot
from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from logging import getLogger
from typing import Optional
from utils.interface_manager import update_interface, safe_delete_message, UIState


class BaseHandler:
    """Базовий клас для створення хендлерів"""

    def __init__(self, name: Optional[str] = None):
        """
        Ініціалізація базового хендлера.

        Args:
            name (Optional[str]): Назва хендлера, використовується для логування.
        """
        self.router = Router(name=name)
        self.logger = getLogger(f"handlers.{name}" if name else "handlers")

    def _setup_router(self) -> None:
        """Метод для налаштування маршрутизатора. Має бути перевизначений."""
        raise NotImplementedError("This method must be implemented in derived classes.")

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
        Обробка переходів між станами з оновленням інтерфейсу.

        Args:
            message (Message): Повідомлення від користувача.
            state (FSMContext): Контекст стану.
            bot (Bot): Екземпляр бота.
            new_state (State): Новий стан FSM.
            control_text (str): Текст для меню керування.
            control_markup (ReplyKeyboardMarkup): Клавіатура меню керування.
            screen_text (str): Текст для екрану.
            screen_markup (Optional[InlineKeyboardMarkup]): Клавіатура для екрану.
        """
        try:
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

            self.logger.info(
                f"State transition: {new_state} for user {message.from_user.id}"
            )

        except Exception as e:
            self.logger.error(f"Error during state transition: {e}")
            raise
