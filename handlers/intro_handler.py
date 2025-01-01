# handlers/intro_handler.py
from aiogram import types, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from .base import BaseHandler
from .fsm_handler import AsyncFSMHandler
from states.menu_states import IntroState, MainMenuState
from keyboards.inline_menus import (
    get_intro_page_1_keyboard,
    get_intro_page_2_keyboard,
    get_intro_page_3_keyboard
)
from texts import (
    INTRO_PAGE_1_TEXT,
    INTRO_PAGE_2_TEXT,
    INTRO_PAGE_3_TEXT,
    MAIN_MENU_TEXT
)

class IntroHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self._setup_router()

    def _setup_router(self):
        self.router.message.register(self.cmd_start, Command("start"))
        self.router.callback_query.register(self.handle_intro_navigation)

    async def cmd_start(self, message: types.Message, state: FSMContext, db: AsyncSession):
        """Обробка команди /start"""
        fsm = AsyncFSMHandler(state)
        
        # Видаляємо повідомлення користувача
        await message.delete()
        
        # Встановлюємо стан першої сторінки інтро
        await fsm.set_state(IntroState.page_1)
        
        # Відправляємо першу сторінку інтро
        msg = await message.bot.send_message(
            chat_id=message.chat.id,
            text=INTRO_PAGE_1_TEXT,
            reply_markup=get_intro_page_1_keyboard()
        )
        
        # Зберігаємо ID повідомлення
        await fsm.update_data(
            interactive_message_id=msg.message_id,
            last_text=INTRO_PAGE_1_TEXT,
            last_keyboard=get_intro_page_1_keyboard()
        )

    async def handle_intro_navigation(self, callback: types.CallbackQuery, state: FSMContext):
        """Обробка навігації по інтро"""
        fsm = AsyncFSMHandler(state)
        data = callback.data
        current_state = await fsm.get_current_state()
        
        if data == "intro_next_1" and current_state == IntroState.page_1.state:
            await fsm.set_state(IntroState.page_2)
            await self.edit_intro_message(callback, fsm, INTRO_PAGE_2_TEXT, get_intro_page_2_keyboard())

        elif data == "intro_next_2" and current_state == IntroState.page_2.state:
            await fsm.set_state(IntroState.page_3)
            await self.edit_intro_message(callback, fsm, INTRO_PAGE_3_TEXT, get_intro_page_3_keyboard())

        elif data == "intro_start" and current_state == IntroState.page_3.state:
            await fsm.set_state(MainMenuState.main)
            # Завершуємо інтро, переходимо в головне меню
            await callback.message.edit_text(
                text=MAIN_MENU_TEXT,
                reply_markup=None  # Видаляємо клавіатуру
            )
            await callback.message.answer(MAIN_MENU_TEXT)

        await callback.answer()

    async def edit_intro_message(self, callback: types.CallbackQuery, fsm: AsyncFSMHandler, new_text: str, new_keyboard):
        """Редагування повідомлення з інтро"""
        await callback.message.edit_text(
            text=new_text,
            reply_markup=new_keyboard
        )
        await fsm.update_data(
            last_text=new_text,
            last_keyboard=new_keyboard
        )
