# keyboards/keyboard_buttons.py
from enum import Enum

class Buttons(str, Enum):  # Повертаємо назву класу до Buttons
    # Головне меню
    NAVIGATION = "🧭 Навігація"
    HEROES = "🎯 Герої"
    PROFILE = "🪪 Профіль"
    SETTINGS = "⚙️ Налаштування"
    
    # Навігаційне меню
    CHARACTERS = "👥 Персонажі"
    MAPS = "🗺 Мапи"
    TOURNAMENTS = "🏆 Турніри"
    GUIDES = "📖 Гайди"
    
    # Загальні кнопки
    BACK = "🔙 Назад"
    MAIN_MENU = "🏠 Головне меню"
