from aiogram import Router

from handlers.menu_handlers import menu_router
from handlers.navigation_handlers import navigation_router
from handlers.profile_handlers import profile_router
from handlers.hero_class_handlers import hero_class_router
from handlers.heroes_handlers import heroes_router
from handlers.message_handlers import message_router
from handlers.error_handler import error_router
from handlers.start_command import start_router

router = Router()

# Додаємо всі обробники
router.include_router(menu_router)
router.include_router(navigation_router)
router.include_router(profile_router)
router.include_router(hero_class_router)
router.include_router(heroes_router)
router.include_router(message_router)
router.include_router(error_router)
router.include_router(start_router)
