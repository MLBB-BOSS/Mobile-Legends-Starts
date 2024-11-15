import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from config.settings import settings

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Ініціалізація бота та диспетчера
bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN, 
    parse_mode=ParseMode.HTML  # Змінено спосіб встановлення parse_mode
)

# Створення сховища для FSM
storage = MemoryStorage()

# Ініціалізація диспетчера
dp = Dispatcher(storage=storage)
