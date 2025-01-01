from typing import Any, Dict, Optional
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from logging import getLogger
from aiogram.types import InlineKeyboardMarkup

from .base import BaseHandler
from .fsm_handler import AsyncFSMHandler
from states.menu_states import IntroState, MainMenuState
from keyboards.inline_menus import (
    get_intro_page_1_keyboard,
    get_intro_page_2_keyboard,
    get_intro_page_3_keyboard
)
from keyboards.menus import (
    get_main_menu_inline,
    MenuCallbackData
)
from texts import (
    INTRO_PAGE_1_TEXT,
    INTRO_PAGE_2_TEXT,
    INTRO_PAGE_3_TEXT,
    MAIN_MENU_TEXT
)

logger = getLogger(__name__)

class IntroHandler(BaseHandler):
    """Handler for intro section of the bot"""
    
    def __init__(self) -> None:
        """Initialize the handler and setup router"""
        super().__init__()
        self._setup_router()
        logger.info("IntroHandler initialized")

    def _setup_router(self) -> None:
        """Setup command and callback handlers"""
        self.router.message.register(self.cmd_start, Command("start"))
        self.router.callback_query.register(
            self.handle_intro_navigation,
            lambda c: c.data.startswith("intro_")
        )
        logger.debug("Router configured for IntroHandler")

    async def cmd_start(
        self,
        message: types.Message,
        state: FSMContext,
        db: AsyncSession
    ) -> None:
        """
        Handle /start command
        
        Args:
            message: Telegram message
            state: FSM context
            db: Database session
        """
        fsm = AsyncFSMHandler(state)
        
        try:
            user_id = message.from_user.id
            logger.info(f"Processing /start command for user {user_id}")
            
            # Delete user's command message
            await message.delete()
            
            # Set initial state
            await fsm.set_state(IntroState.page_1)
            
            # Send first intro page
            msg = await message.bot.send_message(
                chat_id=message.chat.id,
                text=INTRO_PAGE_1_TEXT,
                reply_markup=get_intro_page_1_keyboard()
            )
            
            # Save message data
            await fsm.update_data(
                interactive_message_id=msg.message_id,
                last_text=INTRO_PAGE_1_TEXT,
                last_keyboard=get_intro_page_1_keyboard()
            )
            
            logger.info(f"Started intro sequence for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error in cmd_start for user {message.from_user.id}: {e}")
            await message.answer("Виникла помилка. Спробуйте ще раз через /start")
            raise

    async def handle_intro_navigation(
        self,
        callback: types.CallbackQuery,
        state: FSMContext
    ) -> None:
        """
        Handle intro navigation callbacks
        
        Args:
            callback: Callback query
            state: FSM context
        """
        fsm = AsyncFSMHandler(state)
        user_id = callback.from_user.id
        
        try:
            data = callback.data
            current_state = await fsm.get_current_state()
            logger.info(f"Processing intro navigation for user {user_id}: {data} in state {current_state}")
            
            match (data, current_state):
                case ("intro_next_1", IntroState.page_1.state):
                    await fsm.set_state(IntroState.page_2)
                    await self._edit_intro_message(
                        callback=callback,
                        fsm=fsm,
                        new_text=INTRO_PAGE_2_TEXT,
                        new_keyboard=get_intro_page_2_keyboard()
                    )
                    logger.debug(f"User {user_id} moved to intro page 2")
                
                case ("intro_next_2", IntroState.page_2.state):
                    await fsm.set_state(IntroState.page_3)
                    await self._edit_intro_message(
                        callback=callback,
                        fsm=fsm,
                        new_text=INTRO_PAGE_3_TEXT,
                        new_keyboard=get_intro_page_3_keyboard()
                    )
                    logger.debug(f"User {user_id} moved to intro page 3")
                
                case ("intro_start", IntroState.page_3.state):
                    await fsm.set_state(MainMenuState.main)
                    await callback.message.edit_text(
                        text=MAIN_MENU_TEXT,
                        reply_markup=get_main_menu_inline()
                    )
                    await callback.answer("Вітаємо! Ви перейшли до головного меню.")
                    logger.info(f"User {user_id} completed intro and moved to main menu")
                
                case _:
                    logger.warning(
                        f"Unexpected callback data for user {user_id}: {data} in state: {current_state}"
                    )
                    await callback.answer("Невідома команда")
                    return
            
            await callback.answer()
            
        except Exception as e:
            logger.error(f"Error in handle_intro_navigation for user {user_id}: {e}")
            await callback.answer("Виникла помилка. Спробуйте ще раз через /start")
            await self._handle_error(callback, e)
            raise

    async def _edit_intro_message(
        self,
        callback: types.CallbackQuery,
        fsm: AsyncFSMHandler,
        new_text: str,
        new_keyboard: InlineKeyboardMarkup
    ) -> None:
        """
        Edit intro message with new text and keyboard
        
        Args:
            callback: Callback query
            fsm: FSM handler
            new_text: New message text
            new_keyboard: New inline keyboard
        """
        user_id = callback.from_user.id
        
        try:
            await callback.message.edit_text(
                text=new_text,
                reply_markup=new_keyboard
            )
            await fsm.update_data(
                last_text=new_text,
                last_keyboard=new_keyboard
            )
            logger.debug(f"Successfully edited intro message for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error editing intro message for user {user_id}: {e}")
            await self._handle_error(callback, e)
            raise

    async def _handle_error(
        self,
        callback: types.CallbackQuery,
        error: Exception
    ) -> None:
        """
        Handle errors in intro handler
        
        Args:
            callback: Callback query where error occurred
            error: The exception that was raised
        """
        user_id = callback.from_user.id
        error_msg = f"Помилка при обробці запиту. Спробуйте ще раз через /start"
        
        try:
            await callback.message.answer(error_msg)
            logger.error(f"Handled error for user {user_id}: {str(error)}")
            
        except Exception as e:
            logger.critical(
                f"Failed to handle error for user {user_id}. Original error: {str(error)}. "
                f"Handler error: {str(e)}"
            )
