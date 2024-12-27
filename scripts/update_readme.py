# scripts/update_readme.py
import os
from datetime import datetime

class ReadmeGenerator:
    def __init__(self):
        self.current_date = "2024-12-27 20:38:40 UTC"  # Ваш точний час
        self.author = "MLBB-BOSS"
        self.bot_name = "@MLBB_MLS_BOT"
        
        # Креативний ASCII-арт з часом
        self.ascii_art = f"""
╔════════════════════ CURRENT TIME ══════════════════════╗
║                                                        ║
║  ████████╗██╗   ██╗    ████████╗██╗   ██╗████████╗    ║
║  ╚══██╔══╝╚██╗ ██╔╝    ╚══██╔══╝██║   ██║╚══██╔══╝    ║
║     ██║    ╚████╔╝        ██║   ██║   ██║   ██║       ║
║     ██║     ╚██╔╝         ██║   ██║   ██║   ██║       ║
║     ██║      ██║          ██║   ╚██████╔╝   ██║       ║
║     ╚═╝      ╚═╝          ╚═╝    ╚═════╝    ╚═╝       ║
║                                                        ║
║          {self.current_date}           ║
║                                                        ║
╚════════════════════════════════════════════════════════╝
"""

        # Оновлена статистика з часовою міткою
        self.stats = {
            "users": "1000+",
            "commands": "10000+",
            "languages": 3,
            "states": 99,
            "last_update": self.current_date
        }

        # Додаткова інформація про оновлення
        self.update_info = {
            "author": self.author,
            "bot": self.bot_name,
            "time": self.current_date,
            "branch": "aiogram-3x"
        }

    def generate_readme(self):
        return f'''<div align="center">
