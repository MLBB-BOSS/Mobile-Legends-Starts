# keyboards/keyboard_buttons.py
from enum import Enum

class Buttons(str, Enum):
    # Головне меню
    NAVIGATION = "🧭 Навігація"
    HEROES = "🎯 Герої"
    PROFILE = "🪪 Профіль"
    SETTINGS = "⚙️ Налаштування"
    BUY_TICKETS = "🎫 Купити білети"
    STATISTICS = "📊 Статистика"
    
    # Навігаційне меню
    CHARACTERS = "👥 Персонажі"
    MAPS = "🗺 Мапи"
    TOURNAMENTS = "🏆 Турніри"
    GUIDES = "📖 Гайди"
    
    # Меню персонажів
    TANK = "🛡️ Танк"
    MAGE = "🔮 Маг"
    MARKSMAN = "🏹 Стрілець"
    ASSASSIN = "🗡️ Асасін"
    SUPPORT = "🛠️ Підтримка"
    
    # Загальні кнопки
    BACK_TO_MAIN = "🔙 Назад до Головного меню"
    SEARCH = "🔍 Пошук"
