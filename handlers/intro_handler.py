# handlers/intro_handler.py
from datetime import datetime
import logging
from typing import Optional

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError

from states.menu_states import IntroState, MainMenuState
from keyboards.intro_kb import get_intro_kb_1, get_intro_kb_2, get_intro_kb_3
from keyboards.main_menu import get_main_menu_keyboard, get_main_menu_inline_keyboard
from constants.intro_texts import (
    INTRO_PAGE_1_TEXT, 
    INTRO_PAGE_2_TEXT, 
    INTRO_PAGE_3_TEXT,
    WELCOME_BACK_TEXT
)
from utils.interface_manager import (
    safe_delete_message, 
    update_interface_state, 
    InterfaceState
)
from models.user import User
from models.user_stats import UserStats

logger = logging.getLogger(__name__)

class IntroHandler:
    def __init__(self):
        self.router = Router(name="intro_handler")
        self.register_handlers()

    def register_handlers(self):
        """Реєстрація обробників інтро"""
        # Command handlers
        self.router.message.register(self.cmd_start, CommandStart())
        
        # Callback handlers for intro navigation
        self.router.callback_query.register(
            self.handle_intro_next_1, 
            F.data == "intro_next_1"
        )
        self.router.callback_query.register(
            self.handle_intro_next_2, 
            F.data == "intro_next_2"
        )
        self.router.callback_query.register(
            self.handle_intro_finish, 
            F.data == "intro_finish"
        )

    async def get_user_from_db(
        self, 
        session: AsyncSession, 
        telegram_id: int
    ) -> Optional[User]:
        """Отримання користувача з бази даних"""
        try:
            result = await session.execute(
                select(User).where(User.telegram_id == telegram_id)
            )
            return result.scalars().first()
        except SQLAlchemyError as e:
            logger.error(f"Database error while getting user {telegram_id}: {e}")
            return None

    async def create_new_user(
        self, 
        session: AsyncSession, 
        telegram_id: int, 
        username: str,
        first_name: str,
        last_name: str
    ) -> Optional[User]:
        """Створення нового користувача"""
        try:
            # Create new user
            new_user = User(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name,
                registration_date=datetime.utcnow(),
                last_activity=datetime.utcnow(),
                is_active=True
            )
            session.add(new_user)
            await session.flush()  # Flush to get the user.id

            # Create initial stats for the user
            new_stats = UserStats(
                user_id=new_user.id,
                total_games=0,
                wins=0,
                losses=0,
                win_streak=0,
                current_rating=1000,
                highest_rating=1000
            )
            session.add(new_stats)
            
            await session.commit()
            return new_user
            
        except SQLAlchemyError as e:
            logger.error(f"Database error while creating user {telegram_id}: {e}")
            await session.rollback()
            return None

    async def cmd_start(
        self, 
        message: Message, 
        state: FSMContext, 
        session: AsyncSession
    ):
        """Обробка команди /start"""
        try:
            # Видаляємо команду користувача
            await safe_delete_message(
                message.bot, 
                message.chat.id, 
                message.message_id
            )

            user = await self.get_user_from_db(session, message.from_user.id)

            if user:
                logger.info(f"Existing user {user.telegram_id} - redirecting to main menu")
                # Оновлюємо last_activity
                user.last_activity = datetime.utcnow()
                await session.commit()
                
                await self.goto_main_menu(message, state, user)
            else:
                logger.info(f"New user {message.from_user.id} - starting intro")
                user = await self.create_new_user(
                    session,
                    message.from_user.id,
                    message.from_user.username,
                    message.from_user.first_name,
                    message.from_user.last_name
                )
                if user:
                    await self.start_intro(message, state)
                else:
                    await message.answer("Помилка при реєстрації. Спробуйте пізніше.")

        except Exception as e:
            logger.error(f"Error in cmd_start: {e}")
            await message.answer("Виникла помилка. Спробуйте ще раз.")

    async def start_intro(self, message: Message, state: FSMContext):
        """Початок інтро-послідовності"""
        try:
            # Створюємо новий інтерфейс
            interface_state = InterfaceState(
                text=INTRO_PAGE_1_TEXT,
                markup=get_intro_kb_1()
            )
            
            # Оновлюємо інтерфейс
            message_ids = await update_interface_state(
                bot=message.bot,
                chat_id=message.chat.id,
                state=state,
                interface_state=interface_state
            )
            
            # Встановлюємо стан і зберігаємо ID повідомлень
            await state.set_state(IntroState.page_1)
            await state.update_data(
                current_page=1,
                message_ids=message_ids
            )
            
            logger.info(f"Started intro for user {message.from_user.id}")
            
        except Exception as e:
            logger.error(f"Error in start_intro: {e}")
            await message.answer("Виникла помилка. Спробуйте /start")

    async def handle_intro_next_1(
        self, 
        callback: CallbackQuery, 
        state: FSMContext
    ):
        """Обробка переходу до другої сторінки інтро"""
        await self._handle_intro_navigation(
            callback=callback,
            state=state,
            next_text=INTRO_PAGE_2_TEXT,
            next_markup=get_intro_kb_2(),
            next_state=IntroState.page_2,
            page_number=2
        )

    async def handle_intro_next_2(
        self, 
        callback: CallbackQuery, 
        state: FSMContext
    ):
        """Обробка переходу до третьої сторінки інтро"""
        await self._handle_intro_navigation(
            callback=callback,
            state=state,
            next_text=INTRO_PAGE_3_TEXT,
            next_markup=get_intro_kb_3(),
            next_state=IntroState.page_3,
            page_number=3
        )

    async def _handle_intro_navigation(
        self,
        callback: CallbackQuery,
        state: FSMContext,
        next_text: str,
        next_markup,
        next_state: IntroState,
        page_number: int
    ):
        """Загальна логіка навігації по інтро"""
        try:
            await callback.answer()
            
            # Оновлюємо інтерфейс
            interface_state = InterfaceState(
                text=next_text,
                markup=next_markup
            )
            
            await update_interface_state(
                bot=callback.bot,
                chat_id=callback.message.chat.id,
                state=state,
                interface_state=interface_state
            )
            
            # Оновлюємо стан
            await state.set_state(next_state)
            await state.update_data(current_page=page_number)
            
        except Exception as e:
            logger.error(f"Error in intro navigation: {e}")
            await callback.message.answer("Виникла помилка. Спробуйте /start")

    async def handle_intro_finish(
        self, 
        callback: CallbackQuery, 
        state: FSMContext
    ):
        """Завершення інтро і перехід до головного меню"""
        try:
            await callback.answer()
            await self.goto_main_menu(callback.message, state)
        except Exception as e:
            logger.error(f"Error in intro_finish: {e}")
            await callback.message.answer("Виникла помилка. Спробуйте /start")

    async def goto_main_menu(
        self, 
        message: Message, 
        state: FSMContext,
        user: Optional[User] = None
    ):
        """Перехід до головного меню"""
        try:
            # Створюємо стан інтерфейсу для головного меню
            welcome_text = WELCOME_BACK_TEXT.format(
                username=user.username if user else "користувач"
            )
            
            interface_state = InterfaceState(
                control_text=welcome_text,
                control_markup=get_main_menu_keyboard(),
                screen_text="Головне меню",
                screen_markup=get_main_menu_inline_keyboard()
            )
            
            # Оновлюємо інтерфейс
            await update_interface_state(
                bot=message.bot,
                chat_id=message.chat.id,
                state=state,
                interface_state=interface_state
            )
            
            # Встановлюємо стан головного меню
            await state.set_state(MainMenuState.main)
            
            logger.info(f"User {message.chat.id} moved to main menu")
            
        except Exception as e:
            logger.error(f"Error in goto_main_menu: {e}")
            await message.answer("Виникла помилка. Спробуйте /start")
