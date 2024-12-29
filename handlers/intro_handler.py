from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from states.menu_states import IntroState, MainMenuState
from keyboards.intro_kb import get_intro_kb_1, get_intro_kb_2, get_intro_kb_3
from constants.intro_texts import INTRO_PAGE_1_TEXT, INTRO_PAGE_2_TEXT, INTRO_PAGE_3_TEXT
from utils.interface_manager import safe_delete_message
from models.user import User
import logging

logger = logging.getLogger(__name__)

class IntroHandler:
    def __init__(self):
        self.router = Router()
        self.register_handlers()

    def register_handlers(self):
        """Реєстрація обробників інтро"""
        self.router.message.register(self.cmd_start, CommandStart())
        self.router.callback_query.register(self.next_page_1, F.data == "intro_next_1")
        self.router.callback_query.register(self.next_page_2, F.data == "intro_next_2")
        self.router.callback_query.register(self.finish_intro, F.data == "intro_finish")

    async def cmd_start(self, message: Message, state: FSMContext, session: AsyncSession):
        """Обробка команди /start"""
        logger.info(f"Start command received from user {message.from_user.id}")
        try:
            # Перевірка, чи користувач новий
            user_id = message.from_user.id
            user = await session.get(User, user_id)

            if user:
                logger.info(f"Existing user {user_id} - redirecting to main menu")
                await self.goto_main_menu(message, state)
            else:
                logger.info(f"New user {user_id} - starting intro")
                await self.start_intro(message, state)
        except Exception as e:
            logger.error(f"Error in cmd_start: {e}")
            raise

    async def start_intro(self, message: Message, state: FSMContext):
        """Початок інтро"""
        await safe_delete_message(message.bot, message.chat.id, message.message_id)
        intro_message = await message.bot.send_message(
            chat_id=message.chat.id,
            text=INTRO_PAGE_1_TEXT,
            reply_markup=get_intro_kb_1()
        )
        await state.set_state(IntroState.page_1)
        await state.update_data(intro_message_id=intro_message.message_id)

    async def next_page_1(self, callback_query: CallbackQuery, state: FSMContext):
        """Перехід до другої сторінки інтро"""
        try:
            await callback_query.answer()
            data = await state.get_data()
            intro_message_id = data.get('intro_message_id')

            if not intro_message_id:
                logger.error("No intro_message_id in state data")
                return

            await callback_query.bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=intro_message_id,
                text=INTRO_PAGE_2_TEXT,
                reply_markup=get_intro_kb_2()
            )
            await state.set_state(IntroState.page_2)
            logger.info(f"User {callback_query.from_user.id} moved to intro page 2")
        except Exception as e:
            logger.error(f"Error in next_page_1: {e}")
            await callback_query.answer("Виникла помилка. Спробуйте /start")

    async def next_page_2(self, callback_query: CallbackQuery, state: FSMContext):
        """Перехід до третьої сторінки інтро"""
        try:
            await callback_query.answer()
            data = await state.get_data()
            intro_message_id = data.get('intro_message_id')

            if not intro_message_id:
                logger.error("No intro_message_id in state data")
                return

            await callback_query.bot.edit_message_text(
                chat_id=callback_query.message.chat.id,
                message_id=intro_message_id,
                text=INTRO_PAGE_3_TEXT,
                reply_markup=get_intro_kb_3()
            )
            await state.set_state(IntroState.page_3)
            logger.info(f"User {callback_query.from_user.id} moved to intro page 3")
        except Exception as e:
            logger.error(f"Error in next_page_2: {e}")
            await callback_query.answer("Виникла помилка. Спробуйте /start")

    async def finish_intro(self, callback_query: CallbackQuery, state: FSMContext):
        """Завершення інтро і перехід до головного меню"""
        try:
            await callback_query.answer()
            await self.goto_main_menu(callback_query.message, state)
        except Exception as e:
            logger.error(f"Error in finish_intro: {e}")

    async def goto_main_menu(self, message: Message, state: FSMContext):
        """Перехід до головного меню"""
        try:
            await state.clear()
            # Тут потрібно викликати головний хендлер для меню
            from handlers.main_menu import MainMenuHandler
            main_menu_handler = MainMenuHandler()
            await main_menu_handler.cmd_start(message, state)
        except Exception as e:
            logger.error(f"Error in goto_main_menu: {e}")
