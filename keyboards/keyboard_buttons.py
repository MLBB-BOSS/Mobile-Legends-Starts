# keyboards/keyboard_buttons.py
from enum import Enum

class Buttons(str, Enum):
    NAVIGATION = "🧭 Навігація"
    CHARACTERS = "👥 Персонажі"
    MAPS = "🗺 Мапи"
    TOURNAMENTS = "🏆 Турніри"
    GUIDES = "📖 Гайди"
    BACK_TO_MAIN = "🔙 Назад до Головного меню"
