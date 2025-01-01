# handlers/intro_handler.py
from typing import Optional
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from logging import getLogger

from utils.message_utils import MessageManager
from states.menu_states import IntroState, MainMenuState
from keyboards.intro import get_intro_keyboard
from keyboards.menu import get_main_menu_keyboard

class IntroHandler:
    def __init__(self, message_manager: Optional[MessageManager] = None):
        self.router = Router(name="intro")
        self.message_manager = message_manager
        self.logger = getLogger(__name__)
        self._setup_router()

    def _setup_router(self) -> None:
        self.router.message.register(self.start_intro, Command("start"))
        self.router.callback_query.register(
            self.handle_intro_navigation,
            F.data.startswith("intro_")
        )

    async def show_main_menu(
        self,
        chat_id: int,
        message_id: Optional[int],
        state: FSMContext
    ) -> None:
        """Show main menu"""
        try:
            # Set main menu state
            await state.set_state(MainMenuState.main)
            
            # Prepare menu text
            menu_text = (
                "🎮 <b>Головне меню</b>\n\n"
                "Виберіть потрібний розділ:\n\n"
                "👤 <b>Профіль</b> - Ваша інформація та налаштування\n"
                "📊 <b>Статистика</b> - Ваші показники та досягнення\n"
                "👥 <b>Команда</b> - Управління командою\n"
                "🏆 <b>Турніри</b> - Участь у турнірах"
            )
            
            # Show menu
            if self.message_manager:
                await self.message_manager.send_or_edit(
                    chat_id=chat_id,
                    text=menu_text,
                    message_id=message_id,
                    keyboard=get_main_menu_keyboard()
                )
            else:
                # Fallback to direct bot API
                if message_id:
                    await self.bot.edit_message_text(
                        chat_id=chat_id,
                        message_id=message_id,
                        text=menu_text,
                        reply_markup=get_main_menu_keyboard()
                    )
                else:
                    await self.bot.send_message(
                        chat_id=chat_id,
                        text=menu_text,
                        reply_markup=get_main_menu_keyboard()
                    )
                    
        except Exception as e:
            self.logger.error(f"Error showing main menu: {e}")
            if self.message_manager:
                await self.message_manager.send_or_edit(
                    chat_id=chat_id,
                    text="❌ Помилка відображення меню. Спробуйте /start",
                    message_id=message_id
                )

    async def handle_intro_navigation(
        self,
        callback: types.CallbackQuery,
        state: FSMContext
    ) -> None:
        """Handle intro navigation"""
        try:
            current_state = await state.get_state()
            if not current_state:
                await callback.answer("❌ Помилка стану. Почніть спочатку через /start")
                return
                
            action = callback.data.split("_")[1]
            
            if action == "complete":
                # Show main menu
                await self.show_main_menu(
                    chat_id=callback.message.chat.id,
                    message_id=callback.message.message_id,
                    state=state
                )
                await callback.answer("✅ Ласкаво просимо до головного меню!")
                return
                
            # Rest of navigation handling...
            # (previous code for next/prev navigation)
            
        except Exception as e:
            self.logger.error(f"Error in navigation: {e}")
            await callback.answer("❌ Помилка. Спробуйте /start")
