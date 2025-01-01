# handlers/intro_handler.py
from typing import Optional
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from logging import getLogger

from utils.message_utils import MessageManager
from states.menu_states import IntroState, MainMenuState
from keyboards.menus import Keyboards
from texts import Messages

class IntroHandler:
    def __init__(self, message_manager: Optional[MessageManager] = None):
        self.router = Router(name="intro")
        self.message_manager = message_manager
        self.logger = getLogger(__name__)
        self._setup_router()

    async def start_intro(
        self,
        message: types.Message,
        state: FSMContext
    ) -> None:
        try:
            self.logger.info(f"Starting intro for user {message.from_user.id}")
            
            await state.set_state(IntroState.page_1)
            
            if self.message_manager:
                await self.message_manager.send_or_edit(
                    chat_id=message.chat.id,
                    text=Messages.Intro.PAGE_1,
                    keyboard=Keyboards.intro_keyboard(1)
                )
            else:
                await message.answer(
                    text=Messages.Intro.PAGE_1,
                    reply_markup=Keyboards.intro_keyboard(1)
                )
                
        except Exception as e:
            self.logger.error(f"Error in start_intro: {e}")
            await message.answer(Messages.Intro.ERROR)

    async def handle_intro_navigation(
        self,
        callback: types.CallbackQuery,
        state: FSMContext
    ) -> None:
        try:
            current_state = await state.get_state()
            if not current_state:
                await callback.answer(Messages.Intro.STATE_ERROR)
                return
                
            action = callback.data.split("_")[1]
            
            if action == "next":
                if current_state == "IntroState:page_1":
                    next_state = IntroState.page_2
                    page = 2
                    text = Messages.Intro.PAGE_2
                elif current_state == "IntroState:page_2":
                    next_state = IntroState.page_3
                    page = 3
                    text = Messages.Intro.PAGE_3
                else:
                    await callback.answer(Messages.Intro.NAV_ERROR)
                    return
                    
                await state.set_state(next_state)
                
            elif action == "prev":
                if current_state == "IntroState:page_2":
                    next_state = IntroState.page_1
                    page = 1
                    text = Messages.Intro.PAGE_1
                elif current_state == "IntroState:page_3":
                    next_state = IntroState.page_2
                    page = 2
                    text = Messages.Intro.PAGE_2
                else:
                    await callback.answer(Messages.Intro.NAV_ERROR)
                    return
                    
                await state.set_state(next_state)
                
            elif action == "complete":
                await state.set_state(MainMenuState.main)
                text = Messages.MainMenu.WELCOME
                keyboard = Keyboards.main_menu()
            
            # Update message
            if self.message_manager:
                await self.message_manager.send_or_edit(
                    chat_id=callback.message.chat.id,
                    text=text,
                    message_id=callback.message.message_id,
                    keyboard=Keyboards.intro_keyboard(page) if action != "complete" else keyboard
                )
            else:
                await callback.message.edit_text(
                    text=text,
                    reply_markup=Keyboards.intro_keyboard(page) if action != "complete" else keyboard
                )
            
            await callback.answer()
            
        except Exception as e:
            self.logger.error(f"Error in navigation: {e}")
            await callback.answer(Messages.Intro.ERROR)
