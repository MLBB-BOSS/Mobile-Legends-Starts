from enum import Enum, auto

class MenuLevel(Enum):
    MAIN = auto()
    NAVIGATION = auto()
    HEROES = auto()
    TOURNAMENTS = auto()
    PROFILE = auto()
    SETTINGS = auto()

class Buttons(str, Enum):
    # Головне меню (MAIN)
    NAVIGATION = "🧭 Навігація"
    HEROES = "🎯 Герої"
    TOURNAMENTS = "🏆 Турніри"
    PROFILE = "👤 Профіль"
    SETTINGS = "⚙️ Налаштування"
    
    # Меню навігації (NAVIGATION)
    CHARACTERS = "👥 Персонажі"
    MAPS = "🗺 Мапи"
    GUIDES = "📖 Гайди"
    
    # Навігаційні кнопки
    BACK = "🔙 Назад"
    MAIN_MENU = "🏠 Головне меню"
