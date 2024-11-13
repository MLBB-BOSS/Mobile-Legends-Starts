import logging
from core.bot_runner import run_bot  # Оновлений імпорт

logger = logging.getLogger(__name__)

class S3Service:
    def __init__(self):
        pass

    async def some_method(self, session_factory):
        # Використання run_bot асинхронно
        await run_bot(session_factory)
