from utils.db_base import Base
from .user import User, UserStats
from .bug_report import BugReport
from .feedback import Feedback  # Додайте цей рядок

__all__ = ["Base", "User", "UserStats", "Feedback", "BugReport"]
