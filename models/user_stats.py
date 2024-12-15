from sqlalchemy import Column, Integer, ForeignKey
from models.base import Base

class UserStats(Base):
    __tablename__ = 'user_stats'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    rating = Column(Integer, nullable=False)
    # Додайте інші поля за необхідності