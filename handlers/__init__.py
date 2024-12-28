
from aiogram import Dispatcher
from .base import router as base_router
from .missing_handlers import router as missing_handlers_router
from .base import router as base_router
from .hero_handlers import router as hero_router

__all__ = ['base_router', 'hero_router']

def setup_handlers(dp: Dispatcher):
    # Список роутерів для підключення
    routers = [base_router, missing_handlers_router]

    # Підключення всіх роутерів до диспетчера
    for router in routers:
        dp.include_router(router)
