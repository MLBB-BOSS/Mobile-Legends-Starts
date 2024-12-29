# handlers/navigation/__init__.py
from aiogram import Router
from .menu import router as menu_router

# Створюємо головний роутер для навігації
router = Router()

# Підключаємо всі під-роутери
router.include_router(menu_router)

# Експортуємо роутер
__all__ = ["router"]
