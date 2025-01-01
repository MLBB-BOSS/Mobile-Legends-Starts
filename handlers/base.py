# handlers/base.py
import logging
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from typing import Dict, Type

logger = logging.getLogger(__name__)

class BaseHandler:
    def __init__(self):
        self.router = Router()
        self._setup_router()

    async def _setup_router(self):
        """Метод для налаштування роутера. Перевизначається в дочірніх класах"""
        pass

    @classmethod
    async def get_state_data(cls, state: FSMContext) -> Dict:
        """Отримати дані стану"""
        return await state.get_data()

    @classmethod
    async def update_state_data(cls, state: FSMContext, **kwargs):
        """Оновити дані стану"""
        await state.update_data(**kwargs)

    @classmethod
    async def clear_state(cls, state: FSMContext):
        """Очистити стан"""
        await state.clear()

def setup_handlers(dp):
    """Підключаємо всі хендлери"""
    from .intro_handler import IntroHandler
    from .main_menu_handler import MainMenuHandler
    # Додайте інші хендлери тут

    handlers = [
        IntroHandler(),
        MainMenuHandler(),
        # Додайте інші хендлери тут
    ]

    for handler in handlers:
        dp.include_router(handler.router)

    logger.info("All handlers successfully set up.")
