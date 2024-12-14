# models/user.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
# models/base.py
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    level = Column(Integer, default=1)
    screenshot_count = Column(Integer, default=0)
    mission_count = Column(Integer, default=0)
    quiz_count = Column(Integer, default=0)

    # Відношення до статистики
    stats = relationship('UserStats', back_populates='user', uselist=False)

    # Відношення до бейджів
    badges = relationship('Badge', secondary='user_badges', back_populates='users')
