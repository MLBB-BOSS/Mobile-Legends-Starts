from aiogram.fsm.state import State, StatesGroup

# Головне меню
class MainMenuState(StatesGroup):
    """Стан головного меню"""
    MAIN_MENU = State()
    SETTINGS = State()
    PROFILE = State()
    TOURNAMENTS = State()
    SCREENSHOTS = State()

# Меню користувача
class MenuStates(StatesGroup):
    """Станів для меню користувача"""
    MAIN_MENU = State()
    PROFILE = State()
    STATS = State()
    TEAM = State()
    TOURNAMENT = State()

# Інтро
class IntroState(StatesGroup):
    """Станів для інтро"""
    INTRO_PAGE_1 = State()
    INTRO_PAGE_2 = State()
    INTRO_PAGE_3 = State()

# Додайте __all__ для зручного імпорту
__all__ = ['MainMenuState', 'MenuStates', 'IntroState']
