# handlers/profile/__init__.py
from aiogram import Router
from .menu import router as profile_menu_router

router = Router()
router.include_router(profile_menu_router)

# Якщо потім буде profile/statistics.py, achievements.py, settings.py:
# from .statistics import router as statistics_router
# router.include_router(statistics_router)
