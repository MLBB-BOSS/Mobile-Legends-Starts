# handlers/__init__.py
from .start_command import router as start_router
from .navigation_handlers import router as navigation_router
from .profile_handlers import router as profile_router
from .statistics_handlers import router as statistics_router
from .achievements_handlers import router as achievements_router
from .settings_handlers import router as settings_router
from .feedback_handlers import router as feedback_router
from .help_handlers import router as help_router
from .heroes_handlers import router as heroes_router
from .guides_handlers import router as guides_router
from .counter_picks_handlers import router as counter_picks_router
from .builds_handlers import router as builds_router
from .voting_handlers import router as voting_router
from .map_handlers import router as map_router
from .game_modes_handlers import router as game_modes_router
# Додайте інші хендлери тут

__all__ = [
    'start_router',
    'navigation_router',
    'profile_router',
    'characters_router',
    'statistics_router',
    'achievements_router',
    'settings_router',
    'feedback_router',
    'help_router',
    'heroes_router',
    'guides_router',
    'counter_picks_router',
    'builds_router',
    'voting_router',
    'map_router',
    'game_modes_router',
    # Додайте інші хендлери тут
]
