# handlers/main_menu_handler.py
from aiogram import types
from aiogram.fsm.context import FSMContext

from .base import BaseHandler
from .fsm_handler import AsyncFSMHandler
from states.menu_states import MainMenuState
from keyboards.menus import get_main_menu

class MainMenuHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self._setup_router()

    def _setup_router(self):
        self.router.message.register(self.cmd_main_menu, MainMenuState.main)

    async def cmd_main_menu(self, message: types.Message, state: FSMContext):
        """Обробка головного меню"""
        fsm = AsyncFSMHandler(state)

        # Відправляємо головне меню
        msg = await message.bot.send_message(
            chat_id=message.chat.id,
            text="Головне меню",
            reply_markup=get_main_menu()
        )
        
        # Зберігаємо ID повідомлення
        await fsm.update_data(
            interactive_message_id=msg.message_id,
            last_text="Головне меню",
            last_keyboard=get_main_menu()
        )
