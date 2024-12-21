# models/__init__.py

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .user import User
from .user_stats import UserStats
from .feedback import Feedback
from .bug_report import BugReport
# Import other models here