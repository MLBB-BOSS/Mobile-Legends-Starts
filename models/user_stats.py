from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.base import Base

class UserStats(Base):
    __tablename__ = "user_stats"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    points = Column(Integer, default=0)
    level = Column(Integer, default=1)  # Поле рівня користувача

    # Зв’язок з User
    user = relationship("User", back_populates="stats")

    def __repr__(self):
        return f"<UserStats(id={self.id}, user_id={self.user_id}, level={self.level})>"