from enum import Enum

class Buttons(Enum):
    NAVIGATION = "🧭 Навігація"
    HEROES = "🛡️ Герої"
    TOURNAMENTS = "📊 Турніри"
    PROFILE = "👤 Профіль"
    SETTINGS = "⚙️ Налаштування"

    def __str__(self):
        return self.value
