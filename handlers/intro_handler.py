from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from states.menu_states import IntroState, MainMenuState
from keyboards.intro_kb import get_intro_kb_1, get_intro_kb_2, get_intro_kb_3
from constants.intro_texts import INTRO_PAGE_1_TEXT, INTRO_PAGE_2_TEXT, INTRO_PAGE_3_TEXT
from utils.interface_manager import safe_delete_message
from models.user import User  # Add this import

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

    async def cmd_start(self, message: Message, state: FSMContext, db: AsyncSession):
        """Обробка команди /start"""
        # Перевірка, чи користувач новий
        user_id = message.from_user.id
        user = await db.get(User, user_id)
        if user:
            # Користувач вже існує, переходимо до головного меню
            await self.goto_main_menu(message, state)
        else:
            # Новий користувач, починаємо інтро
            await self.start_intro(message, state)

    # Rest of the code remains the same...

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
        await callback_query.answer()
        data = await state.get_data()
        intro_message_id = data.get('intro_message_id')
        await callback_query.bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=intro_message_id,
            text=INTRO_PAGE_2_TEXT,
            reply_markup=get_intro_kb_2()
        )
        await state.set_state(IntroState.page_2)

    async def next_page_2(self, callback_query: CallbackQuery, state: FSMContext):
        """Перехід до третьої сторінки інтро"""
        await callback_query.answer()
        data = await state.get_data()
        intro_message_id = data.get('intro_message_id')
        await callback_query.bot.edit_message_text(
            chat_id=callback_query.message.chat.id,
            message_id=intro_message_id,
            text=INTRO_PAGE_3_TEXT,
            reply_markup=get_intro_kb_3()
        )
        await state.set_state(IntroState.page_3)

    async def finish_intro(self, callback_query: CallbackQuery, state: FSMContext):
        """Завершення інтро і перехід до головного меню"""
        await callback_query.answer()
        await self.goto_main_menu(callback_query.message, state)

    async def goto_main_menu(self, message: Message, state: FSMContext):
        """Перехід до головного меню"""
        from handlers.main_menu import MainMenuHandler
        await state.clear()
        main_menu_handler = MainMenuHandler()
        await main_menu_handler.cmd_start(message, state)
