# handlers/__init__.py
from .start import router as start_router
from .heroes import router as heroes_router
from .tank import router as tank_router
from .fighter import router as fighter_router
from .guides import router as guides_router
from .back import router as back_router

all_routers = [
    start_router,
    heroes_router,
    tank_router,
    fighter_router,
    guides_router,
    back_router,
    # Додайте інші маршрутизатори
]
