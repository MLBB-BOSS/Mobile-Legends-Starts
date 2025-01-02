import logging
from aiogram import Router
from aiogram.fsm.context import FSMContext
from typing import Dict, Type, List

logger = logging.getLogger(__name__)

class BaseHandler:
    def __init__(self, name: str = "base_handler"):
        self.router = Router()
        self.name = name
        self._setup_router()

    def _setup_router(self):
        """Метод для налаштування роутера. Повинен перевизначатися."""
        pass

    @staticmethod
    async def get_state_data(state: FSMContext) -> Dict:
        """Отримати дані стану"""
        return await state.get_data()

    @staticmethod
    async def update_state_data(state: FSMContext, **kwargs):
        """Оновити дані стану"""
        await state.update_data(**kwargs)

    @staticmethod
    async def clear_state(state: FSMContext):
        """Очистити стан"""
        await state.clear()

def setup_handlers(dp):
    """Підключення всіх обробників"""
    from .intro_handler import IntroHandler
    from .menu_handler import MainMenuHandler

    handlers: List[BaseHandler]
