# handlers/navigation/handler.py

from typing import Optional
from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.menu_states import MenuStates
from ..interface_manager import InterfaceManager
from keyboards.navigation import (
    get_navigation_control_keyboard,
    get_navigation_screen_keyboard
)
from texts.navigation import NavigationTexts

router = Router()

@router.message(MenuStates.MAIN_MENU, F.text == "🧭 Навігація")
async def handle_navigation_transition(
    message: Message,
    state: FSMContext,
    bot: Bot
) -> None:
    """Handle transition to navigation menu"""
    try:
        # Initialize interface manager
        interface = InterfaceManager(bot, message.chat.id, state)
        
        # Delete user's message
        await message.delete()
        
        # Update interface
        await interface.update_interface(
            control_text=NavigationTexts.CONTROL_PANEL,
            control_markup=get_navigation_control_keyboard(),
            screen_text=NavigationTexts.SCREEN,
            screen_markup=get_navigation_screen_keyboard()
        )
        
        # Set new state
        await state.set_state(MenuStates.NAVIGATION_MENU)
        
    except Exception as e:
        logger.error(f"Error in navigation transition: {e}")
        await message.answer(
            "Виникла помилка. Спробуйте ще раз через /start"
        )
        raise
