# keyboards/keyboard_buttons.py

from enum import Enum

class Buttons(Enum):
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Профіль"

class MenuLevel(Enum):
    MAIN = "main"
    PROFILE = "profile"
