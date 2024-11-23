# handlers/router.py

from aiogram import Router
from handlers.menu import menu_router
from handlers.navigation import navigation_router
from handlers.heroes import heroes_router

router = Router()

router.include_router(menu_router)
router.include_router(navigation_router)
router.include_router(heroes_router)  # Зареєструвати новий роутер
