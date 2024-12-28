from aiogram import Router
from .menu import router as navigation_menu_router
from .heroes import router as heroes_router
# from .builds import router as builds_router
# from .guides import router as guides_router
# ...

router = Router()
router.include_router(navigation_menu_router)
router.include_router(heroes_router)
# router.include_router(builds_router)
# router.include_router(guides_router)
