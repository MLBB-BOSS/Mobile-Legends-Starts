# models/achievement.py
from sqlalchemy import Column, String, Text, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

# Таблиця зв'язку між користувачами та досягненнями
user_achievements = Table('user_achievements',
    BaseModel.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('achievement_id', Integer, ForeignKey('achievements.id')),
)

class Achievement(BaseModel):
    __tablename__ = 'achievements'

    name = Column(String(64), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    points = Column(Integer, default=0)
    icon_url = Column(String(512))
    
    # Відносини
    users = relationship("User", secondary=user_achievements, backref="achievements")

    def __repr__(self):
        return f"<Achievement(name={self.name}, points={self.points})>"
