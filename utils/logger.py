# utils/logger.py

from rich.console import Console
from rich.logging import RichHandler
import logging

# Ініціалізація Rich для логування
console = Console()
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(console=console)]
)

logger = logging.getLogger("rich")
