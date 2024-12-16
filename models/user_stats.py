from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Float
from sqlalchemy.orm import relationship, Session
from datetime import datetime
from models.base import Base
from models.user import User


# Модель UserStats для зберігання статистики користувача
class UserStats(Base):
    __tablename__ = 'user_stats'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    rating = Column(Integer, default=0)
    achievements_count = Column(Integer, default=0)
    total_matches = Column(Integer, default=0)
    total_wins = Column(Integer, default=0)
    total_losses = Column(Integer, default=0)
    last_update = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="stats")
    
    def __repr__(self):
        return (f"<UserStats(user_id={self.user_id}, rating={self.rating}, "
                f"achievements_count={self.achievements_count}, total_matches={self.total_matches})>")


# Функція для отримання тексту профілю користувача
async def get_user_profile_text(db: Session, telegram_id: int):
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        return "Користувач не знайдений. Будь ласка, зареєструйтесь."

    profile_text = f"""
    🆔 MLBB ID: {user.mlbb_id or "Невказано"}
    🎯 **Рейтинг:** {user.rating}
    """
    return profile_text


# Функція для оновлення MLBB ID
async def update_mlbb_id(db: Session, telegram_id: int, mlbb_id: str):
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        return "Користувач не знайдений. Реєструйтесь спочатку."
    
    user.mlbb_id = mlbb_id
    db.commit()
    return f"Ваш MLBB ID успішно оновлено на: {mlbb_id}"
