#handlers/base_handler.py
from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from utils.interface_manager import InterfaceManager, UIState

class BaseHandler:
    """Базовий клас для всіх обробників меню"""
    def __init__(self, bot: Bot):
        self.router = Router()
        self.interface = InterfaceManager(bot)

    async def handle_transition(
        self,
        message: Message,
        state: FSMContext,
        new_state: State,
        control_text: str,
        control_markup: ReplyKeyboardMarkup,
        screen_text: str,
        screen_markup: Optional[InlineKeyboardMarkup] = None
    ):
        """Базовий метод для обробки переходів між станами"""
        # Видаляємо повідомлення користувача
        await self.interface.safe_delete_message(
            message.chat.id,
            message.message_id
        )

        # Отримуємо поточний стан інтерфейсу
        data = await state.get_data()
        current_ui = UIState(**data.get('ui_state', {}))

        # Оновлюємо інтерфейс
        new_ui = await self.interface.update_interface(
            chat_id=message.chat.id,
            ui_state=current_ui,
            control_text=control_text,
            control_markup=control_markup,
            screen_text=screen_text,
            screen_markup=screen_markup
        )

        # Зберігаємо новий стан
        await state.set_state(new_state)
        await state.update_data(ui_state=new_ui)
