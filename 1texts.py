# 1texts.py

# Імпорти та конфігурація
from typing import Dict, Any

# Загальні налаштування
DEFAULT_LANGUAGE = 'uk'

# Імпортуємо всі групи констант
from .text_constants.profile import PROFILE_TEXTS
from .text_constants.network import NETWORK_TEXTS
from .text_constants.menu import MENU_TEXTS
from .text_constants.team import TEAM_TEXTS
from .text_constants.interactive import INTERACTIVE_TEXTS
from .text_constants.system import SYSTEM_MESSAGES
from .text_constants.statistics import STATISTICS_TEXTS

# Функції форматування
def format_text(text: str, **kwargs) -> str:
    try:
        return text.format(**kwargs)
    except KeyError as e:
        logger.error(f"Missing key in format: {e}")
        return text
