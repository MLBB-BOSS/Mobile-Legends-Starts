# File: keyboards/menu_states.py
from enum import Enum, auto

class MenuState(Enum):
    MAIN = auto()
    NAVIGATION = auto()
    PROFILE = auto()
    
    # Navigation submenu states
    CHARACTERS = auto()
    GUIDES = auto()
    COUNTER_PICKS = auto()
    BUILDS = auto()
    VOTING = auto()
    
    # Profile submenu states
    STATISTICS = auto()
    ACHIEVEMENTS = auto()
    SETTINGS = auto()
    FEEDBACK = auto()
    HELP = auto()
