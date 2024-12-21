# models/user.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=True)

    # Зв'язок з таблицею user_stats (один-к-одному)
    stats = relationship("UserStats", back_populates="user", uselist=False)
    
    # ДОДАТИ ЦЮ ЧАСТИНУ:
    # Зв'язок з таблицею feedbacks (один-ко-багатьох)
    feedbacks = relationship("Feedback", back_populates="user")

    def __repr__(self):
        return f"<User id={self.id} telegram_id={self.telegram_id} username={self.username}>"
