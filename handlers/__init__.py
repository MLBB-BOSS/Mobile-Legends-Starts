# handlers/__init__.py
from .start_command import router as start_router
from .navigation_handlers import router as navigation_router
from .profile_handlers import router as profile_router
from .characters_handlers import router as characters_router
from .statistics_handlers import router as statistics_router
# Додайте інші хендлери тут

__all__ = [
    'start_router',
    'navigation_router',
    'profile_router',
    'characters_router',
    'statistics_router',
    # Додайте інші хендлери тут
]
