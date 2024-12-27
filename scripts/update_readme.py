import os
from datetime import datetime
import sys

class ReadmeGenerator:
    def __init__(self, current_time=None, current_user=None):
        # Використовуємо передані параметри або значення за замовчуванням
        self.current_date = current_time or datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        self.author = current_user or "MLBB-BOSS"
        self.bot_name = "@MLBB_MLS_BOT"
        
        self.ascii_art = """
████████╗██╗   ██╗    ████████╗██╗   ██╗████████╗
╚══██╔══╝╚██╗ ██╔╝    ╚══██╔══╝██║   ██║╚══██╔══╝
   ██║    ╚████╔╝        ██║   ██║   ██║   ██║   
   ██║     ╚██╔╝         ██║   ██║   ██║   ██║   
   ██║      ██║          ██║   ╚██████╔╝   ██║   
   ╚═╝      ╚═╝          ╚═╝    ╚═════╝    ╚═╝   
                                                  
███╗   ███╗██╗     ███████╗    ██████╗  ██████╗ ████████╗
████╗ ████║██║     ██╔════╝    ██╔══██╗██╔═══██╗╚══██╔══╝
██╔████╔██║██║     ███████╗    ██████╔╝██║   ██║   ██║   
██║╚██╔╝██║██║     ╚════██║    ██╔══██╗██║   ██║   ██║   
██║ ╚═╝ ██║███████╗███████║    ██████╔╝╚██████╔╝   ██║   
╚═╝     ╚═╝╚══════╝╚══════╝    ╚═════╝  ╚═════╝    ╚═╝"""
        
        self.stats = {
            "users": "1000+",
            "commands": "10000+",
            "languages": 3,
            "states": 99
        }

    # ... (rest of the code remains the same)

if __name__ == "__main__":
    # Отримуємо параметри з командного рядка
    current_time = sys.argv[1] if len(sys.argv) > 1 else None
    current_user = sys.argv[2] if len(sys.argv) > 2 else None
    
    # Створюємо генератор з отриманими параметрами
    generator = ReadmeGenerator(current_time, current_user)
    generator.save_readme()
