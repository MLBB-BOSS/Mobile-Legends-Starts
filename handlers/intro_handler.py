# handlers/intro_handler.py

from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from logging import getLogger
from typing import Optional

from utils.message_utils import MessageManager
from states.menu_states import IntroState, MainMenuState
from keyboards.menus import Keyboards
from texts.messages import Messages  # Змінено імпорт

class IntroHandler:
    def __init__(self, message_manager: Optional[MessageManager] = None):
        self.router = Router(name="intro")
        self.message_manager = message_manager
        self.logger = getLogger(__name__)
        self.keyboards = Keyboards()
        self._setup_router()

    def _setup_router(self) -> None:
        self.router.message.register(self.start_intro, Command("start"))
        self.router.callback_query.register(
            self.handle_intro_navigation,
            F.data.startswith("intro_")
        )

    async def start_intro(self, message: types.Message, state: FSMContext) -> None:
        try:
            self.logger.info(f"Starting intro for user {message.from_user.id}")
            await state.set_state(IntroState.page_1)
            
            if self.message_manager:
                await self.message_manager.send_or_edit(
                    chat_id=message.chat.id,
                    text=Messages.Intro.PAGE_1,
                    keyboard=self.keyboards.intro_keyboard(1)
                )
            else:
                await message.answer(
                    text=Messages.Intro.PAGE_1,
                    reply_markup=self.keyboards.intro_keyboard(1)
                )
        except Exception as e:
            self.logger.error(f"Error in start_intro: {e}")
            await message.answer(Messages.Error.GENERAL)

    # ... інші методи класу
