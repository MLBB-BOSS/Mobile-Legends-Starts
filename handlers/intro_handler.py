# handlers/intro_handler.py
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from logging import getLogger

from .fsm_handler import FSMContextManager
from states.menu_states import IntroState
from keyboards.intro import get_intro_keyboard
from utils.message_utils import safe_delete_message

class IntroHandler:
    """Handler for intro sequence"""
    
    def __init__(self):
        self.router = Router(name="intro")
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
            
            # Initialize FSM manager
            fsm = FSMContextManager(state)
            
            # Set initial state
            await fsm.set_state(IntroState.page_1)
            
            # Send first intro message
            await message.answer(
                "Ласкаво просимо! Це перша сторінка знайомства.",
                reply_markup=get_intro_keyboard(1)
            )
            
            self.logger.info(
                f"Started intro sequence for user {message.from_user.id}"
            )
            
        except Exception as e:
            self.logger.error(f"Error in start_intro: {e}")
            await message.answer(
                "Виникла помилка. Спробуйте ще раз через /start"
            )

    async def handle_intro_navigation(
        self,
        callback: types.CallbackQuery,
        state: FSMContext
    ) -> None:
        """Handle intro navigation"""
        try:
            # Initialize FSM manager
            fsm = FSMContextManager(state)
            
            # Get current state
            current_state = await fsm.get_current_state()
            if not current_state:
                await callback.answer("Помилка стану. Почніть спочатку через /start")
                return
                
            # Handle navigation
            if callback.data == "intro_next":
                # Logic for next page
                if current_state == "IntroState:page_1":
                    await fsm.set_state(IntroState.page_2)
                    page = 2
                elif current_state == "IntroState:page_2":
                    await fsm.set_state(IntroState.page_3)
                    page = 3
                else:
                    await callback.answer("Помилка навігації")
                    return
                    
            elif callback.data == "intro_prev":
                # Logic for previous page
                if current_state == "IntroState:page_2":
                    await fsm.set_state(IntroState.page_1)
                    page = 1
                elif current_state == "IntroState:page_3":
                    await fsm.set_state(IntroState.page_2)
                    page = 2
                else:
                    await callback.answer("Помилка навігації")
                    return
            
            # Update message
            await callback.message.edit_text(
                f"Сторінка {page} знайомства",
                reply_markup=get_intro_keyboard(page)
            )
            
        except Exception as e:
            self.logger.error(
                f"Error in handle_intro_navigation for user {callback.from_user.id}: {e}"
            )
            await callback.answer("Сталася помилка. Спробуйте /start")
