from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from states.menu_states import IntroState, MainMenuState
from keyboards.intro_kb import get_intro_kb_1, get_intro_kb_2, get_intro_kb_3
from constants.intro_texts import INTRO_PAGE_1_TEXT, INTRO_PAGE_2_TEXT, INTRO_PAGE_3_TEXT
from utils.interface_manager import safe_delete_message
from models.user import User
import logging

logger = logging.getLogger(__name__)

class IntroHandler:
    def __init__(self):
        self.router = Router(name="intro_handler")
        self.register_handlers()

    def register_handlers(self):
        """Реєстрація обробників інтро"""
        # Використовуємо декоратор middleware
        @self.router.message(CommandStart())
        async def cmd_start(message: Message, state: FSMContext, session=None):
            """Обробка команди /start"""
            try:
                # Перевірка, чи користувач новий
                user_id = message.from_user.id
                user = None
                if session:
                    user = await session.get(User, user_id)

                if user:
                    logger.info(f"Existing user {user_id} - redirecting to main menu")
                    await self.goto_main_menu(message, state)
                else:
                    logger.info(f"New user {user_id} - starting intro")
                    await self.start_intro(message, state)
            except Exception as e:
                logger.error(f"Error in cmd_start: {e}")
                await message.answer("Виникла помилка. Спробуйте ще раз.")

        @self.router.callback_query(F.data == "intro_next_1")
        async def next_page_1(callback: CallbackQuery, state: FSMContext):
            await self._handle_next_page(
                callback, state, INTRO_PAGE_2_TEXT, get_intro_kb_2(), IntroState.page_2
            )

        @self.router.callback_query(F.data == "intro_next_2")
        async def next_page_2(callback: CallbackQuery, state: FSMContext):
            await self._handle_next_page(
                callback, state, INTRO_PAGE_3_TEXT, get_intro_kb_3(), IntroState.page_3
            )

        @self.router.callback_query(F.data == "intro_finish")
        async def finish_intro(callback: CallbackQuery, state: FSMContext):
            await callback.answer()
            await self.goto_main_menu(callback.message, state)

    async def start_intro(self, message: Message, state: FSMContext):
        """Початок інтро"""
        try:
            await safe_delete_message(message.bot, message.chat.id, message.message_id)
            intro_message = await message.answer(
                text=INTRO_PAGE_1_TEXT,
                reply_markup=get_intro_kb_1()
            )
            await state.set_state(IntroState.page_1)
            await state.update_data(intro_message_id=intro_message.message_id)
            logger.info(f"Started intro for user {message.from_user.id}")
        except Exception as e:
            logger.error(f"Error in start_intro: {e}")
            await message.answer("Виникла помилка. Спробуйте /start")

    async def _handle_next_page(
        self, callback: CallbackQuery, state: FSMContext, 
        text: str, keyboard, next_state: IntroState
    ):
        """Обробка переходу між сторінками"""
        try:
            await callback.answer()
            data = await state.get_data()
            intro_message_id = data.get('intro_message_id')
            if intro_message_id:
                await callback.message.edit_text(
                    text=text,
                    reply_markup=keyboard
                )
                await state.set_state(next_state)
                logger.info(f"User {callback.from_user.id} moved to state {next_state}")
        except Exception as e:
            logger.error(f"Error in _handle_next_page: {e}")
            await callback.message.answer("Виникла помилка. Спробуйте /start")

    async def goto_main_menu(self, message: Message, state: FSMContext):
        """Перехід до головного меню"""
        from handlers.main_menu import MainMenuHandler
        await state.clear()
        main_menu_handler = MainMenuHandler()
        await main_menu_handler.cmd_start(message, state)
