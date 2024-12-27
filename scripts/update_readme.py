import os
from datetime import datetime
import json
import requests

class ReadmeGenerator:
    def __init__(self):
        self.current_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        self.author = "MLBB-BOSS"
        self.bot_name = "@MLBB_MLS_BOT"
        
        # ASCII арт для лого (можна замінити на свій)
        self.ascii_art = """
╔═══╗─────╔╗──────────╔═══╗────────╔╗
║╔═╗║─────║║──────────║╔═╗║────────║║
║║─║╠══╦══╣║╔══╦══╦══╗║╚══╦╗╔╦══╦══╣║╔══╗
║║─║║╔╗║╔═╣║║╔╗║║═╣║═╣╠══╗║║║║╔═╣╔═╣║║══╣
║╚═╝║╚╝║╚═╣╚╣╚╝║║═╣║═╣║╚═╝║╚╝║╚═╣╚═╣╚╬══║
╚═══╩══╩══╩═╩══╩══╩══╝╚═══╩══╩══╩══╩═╩══╝
        """
        
        # Статистика (можна підключити реальні дані з API)
        self.stats = {
            "users": "1000+",
            "commands": "10000+",
            "languages": 3,
            "states": 99
        }

    def generate_readme(self):
        readme = f"""
<div align="center">
