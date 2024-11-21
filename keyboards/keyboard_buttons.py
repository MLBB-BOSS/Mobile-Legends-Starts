# keyboards/keyboard_buttons.py
from enum import Enum, auto

class MenuLevel(Enum):
    MAIN = auto()
    NAVIGATION = auto()
    HEROES = auto()
    TOURNAMENTS = auto()
    PROFILE = auto()

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
    
    # Меню героїв (HEROES)
    TANK = "🛡️ Танки"
    FIGHTER = "⚔️ Файтери"
    ASSASSIN = "🗡️ Асасіни"
    MAGE = "🔮 Маги"
    MARKSMAN = "🏹 Стрільці"
    SUPPORT = "🛠️ Підтримка"
    
    # Меню турнірів (TOURNAMENTS)
    ACTIVE = "🎮 Активні турніри"
    UPCOMING = "📅 Майбутні турніри"
    PAST = "📜 Минулі турніри"
    CREATE = "➕ Створити турнір"
    
    # Меню профілю (PROFILE)
    STATS = "📊 Статистика"
    ACHIEVEMENTS = "🏆 Досягнення"
    INVENTORY = "🎒 Інвентар"
    
    # Навігаційні кнопки
    BACK = "🔙 Назад"
    MAIN_MENU = "🏠 Головне меню"
