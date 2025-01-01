# handlers/intro_handler.py
from typing import Optional  # Додаємо імпорт Optional
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from logging import getLogger

from utils.message_utils import safe_delete_message, MessageManager
from states.menu_states import IntroState
from keyboards.intro import get_intro_keyboard

class IntroHandler:
    """Handler for intro sequence"""
    
    def __init__(self, message_manager: Optional[MessageManager] = None):
        self.router = Router(name="intro")
        self.message_manager = message_manager
        self.logger = getLogger(__name__)
        self._setup_router()

    def _setup_router(self) -> None:
        """Setup message handlers"""
        self.router.message.register(
            self.start_intro,
            Command("start")
        )
        
        self.router.callback_query.register(
            self.handle_intro_navigation,
            F.data.startswith("intro_")
        )

    async def start_intro(
        self,
        message: types.Message,
        state: FSMContext
    ) -> None:
        """Handle /start command"""
        try:
            self.logger.info(
                f"Processing /start command for user {message.from_user.id}"
            )
            
            # Set initial state
            await state.set_state(IntroState.page_1)
            
            # Send first intro message
            msg_text = (
                "👋 Вітаю! Я бот для Mobile Legends: Bang Bang.\n\n"
                "🎮 Я допоможу вам:\n"
                "- Знайти команду\n"
                "- Відстежувати статистику\n"
                "- Організовувати турніри\n"
                "- Та багато іншого!"
            )
            
            if self.message_manager:
                await self.message_manager.send_or_edit(
                    chat_id=message.chat.id,
                    text=msg_text,
                    keyboard=get_intro_keyboard(1)
                )
            else:
                await message.answer(
                    text=msg_text,
                    reply_markup=get_intro_keyboard(1)
                )
            
            self.logger.info(
                f"Started intro sequence for user {message.from_user.id}"
            )
            
        except Exception as e:
            self.logger.error(f"Error in start_intro: {e}")
            await message.answer(
                "❌ Виникла помилка. Спробуйте ще раз через /start"
            )

    async def handle_intro_navigation(
        self,
        callback: types.CallbackQuery,
        state: FSMContext
    ) -> None:
        """Handle intro navigation"""
        try:
            # Get current state
            current_state = await state.get_state()
            if not current_state:
                await callback.answer(
                    "❌ Помилка стану. Почніть спочатку через /start"
                )
                return
                
            # Get action from callback
            action = callback.data.split("_")[1]
            
            # Handle navigation
            if action == "next":
                if current_state == "IntroState:page_1":
                    next_state = IntroState.page_2
                    page = 2
                    msg_text = (
                        "📊 Статистика та прогрес:\n\n"
                        "- Відстежуйте свій WR\n"
                        "- Аналізуйте свою гру\n"
                        "- Порівнюйте результати"
                    )
                elif current_state == "IntroState:page_2":
                    next_state = IntroState.page_3
                    page = 3
                    msg_text = (
                        "🏆 Турніри та команди:\n\n"
                        "- Створюйте команди\n"
                        "- Організовуйте турніри\n"
                        "- Знаходьте гравців"
                    )
                else:
                    await callback.answer("❌ Помилка навігації")
                    return
                    
                await state.set_state(next_state)
                    
            elif action == "prev":
                if current_state == "IntroState:page_2":
                    next_state = IntroState.page_1
                    page = 1
                    msg_text = (
                        "👋 Вітаю! Я бот для Mobile Legends: Bang Bang.\n\n"
                        "🎮 Я допоможу вам:\n"
                        "- Знайти команду\n"
                        "- Відстежувати статистику\n"
                        "- Організовувати турніри\n"
                        "- Та багато іншого!"
                    )
                elif current_state == "IntroState:page_3":
                    next_state = IntroState.page_2
                    page = 2
                    msg_text = (
                        "📊 Статистика та прогрес:\n\n"
                        "- Відстежуйте свій WR\n"
                        "- Аналізуйте свою гру\n"
                        "- Порівнюйте результати"
                    )
                else:
                    await callback.answer("❌ Помилка навігації")
                    return
                    
                await state.set_state(next_state)
            
            elif action == "complete":
                # Handle completion
                await state.clear()
                msg_text = (
                    "✅ Знайомство завершено!\n\n"
                    "Використовуйте меню для навігації."
                )
                
            # Update message
            if self.message_manager:
                await self.message_manager.send_or_edit(
                    chat_id=callback.message.chat.id,
                    text=msg_text,
                    message_id=callback.message.message_id,
                    keyboard=get_intro_keyboard(page)
                )
            else:
                await callback.message.edit_text(
                    text=msg_text,
                    reply_markup=get_intro_keyboard(page)
                )
            
            await callback.answer()
            
        except Exception as e:
            self.logger.error(
                f"Error in handle_intro_navigation for user {callback.from_user.id}: {e}"
            )
            await callback.answer(
                "❌ Сталася помилка. Спробуйте /start"
            )
