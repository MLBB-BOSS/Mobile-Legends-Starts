# File: utils/localization.py
from typing import Dict

class Localization:
    def __init__(self):
        self.messages: Dict[str, str] = {
            "welcome": "Вітаємо у MLBB-BOSS! Оберіть опцію з меню:",
            "navigation_menu": "Оберіть розділ навігації:",
            "profile_menu": "Ваш профіль - оберіть розділ:",
            "characters_menu": "Оберіть категорію персонажів:",
            "guides_menu": "Оберіть розділ гайдів:",
            "counter_picks_menu": "Оберіть опцію контр-піків:",
            "builds_menu": "Оберіть опцію білдів:",
            "voting_menu": "Оберіть опцію голосування:",
            "statistics_menu": "Оберіть тип статистики:",
            "achievements_menu": "Оберіть розділ досягнень:",
            "settings_menu": "Оберіть налаштування:",
            "feedback_menu": "Оберіть тип зворотного зв'язку:",
            "help_menu": "Оберіть розділ допомоги:",
            # Add other messages...
        }
    
    def get_message(self, key: str, default: str = None) -> str:
        return self.messages.get(key, default or key)

loc = Localization()
