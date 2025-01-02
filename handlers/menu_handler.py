# handlers/menu_handler.py
from typing import Optional
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from logging import getLogger
from keyboards.helpers import get_main_menu_keyboard

from utils.message_utils import MessageManager
from states.menu_states import MainMenuState

router = Router(name="menu")  # Define router here

class MenuHandler:
    def __init__(self, message_manager: Optional[MessageManager] = None):
        self.router = router  # Use the defined router
        self.message_manager = message_manager
        self.logger = getLogger(__name__)
        self._setup_router()

    def _setup_router(self) -> None:
        self.router.callback_query.register(
            self.handle_menu_navigation,
            F.data.startswith("menu_")
        )

    async def handle_menu_navigation(
        self,
        callback: types.CallbackQuery,
        state: FSMContext
    ) -> None:
        """Handle menu navigation"""
        try:
            action = callback.data.split("_")[1]
            
            if action == "profile":
                await state.set_state(MainMenuState.profile)
                text = "👤 Ваш профіль"
            elif action == "stats":
                await state.set_state(MainMenuState.stats)
                text = "📊 Ваша статистика"
            elif action == "team":
                await state.set_state(MainMenuState.team)
                text = "👥 Управління командою"
            elif action == "tournament":
                await state.set_state(MainMenuState.tournament)
                text = "🏆 Турніри"
            else:
                await callback.answer("❌ Невідома команда")
                return
            
            if self.message_manager:
                await self.message_manager.send_or_edit(
                    chat_id=callback.message.chat.id,
                    text=text,
                    message_id=callback.message.message_id,
                    keyboard=get_main_menu_keyboard()
                )
            else:
                await callback.message.edit_text(
                    text=text,
                    reply_markup=get_main_menu_keyboard()
                )
                
            await callback.answer()
            
        except Exception as e:
            self.logger.error(f"Error in menu navigation: {e}")
            await callback.answer("❌ Помилка. Спробуйте /start")
