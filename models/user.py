from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

# Таблиця для реферальних зв'язків
referrals = Table(
    'referrals',
    Base.metadata,
    Column('referrer_id', Integer, ForeignKey('users.id')),
    Column('invitee_id', Integer, ForeignKey('users.id'))
)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String, nullable=True)
    player_id = Column(String, nullable=True)
    screenshot_count = Column(Integer, default=0)
    mission_count = Column(Integer, default=0)
    quiz_count = Column(Integer, default=0)
    tournament_participation = Column(Integer, default=0)
    tournament_top3 = Column(Integer, default=0)
    seasonal_participation = Column(Integer, default=0)
    multitask_completed = Column(Integer, default=0)
    referrals = Column(Integer, default=0)
    guides_created = Column(Integer, default=0)
    rating_rank = Column(Integer, default=0)
    active_months = Column(Integer, default=0)  # Лояльність
    spells_viewed = Column(Integer, default=0)  # Спели
    spells_applied = Column(Integer, default=0)  # Спели
    builds_created = Column(Integer, default=0)  # Білди
    builds_shared = Column(Integer, default=0)  # Білди
    builds_rated = Column(Integer, default=0)    # Білди
    characters_viewed = Column(Integer, default=0)  # Персонажі
    players_added = Column(Integer, default=0)  # Гравці
    events_participated = Column(Integer, default=0)  # Події
    discussions_participated = Column(Integer, default=0)  # Спільнота
    helped_users = Column(Integer, default=0)  # Спільнота
    level = Column(String, default="Новачок")
    is_active = Column(Boolean, default=True)  # Активний користувач
    badges = relationship("Badge", back_populates="user")
    invited_users = relationship(
        "User",
        secondary=referrals,
        primaryjoin=id == referrals.c.referrer_id,
        secondaryjoin=id == referrals.c.invitee_id,
        backref="referrer"
    )

class Badge(Base):
    __tablename__ = 'badges'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)  # Назва бейджа
    category = Column(String, nullable=False)  # Категорія бейджа
    level = Column(String, nullable=False)  # Рівень бейджа
    description = Column(String, nullable=False)  # Опис бейджа
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="badges")
    date_awarded = Column(DateTime, default=datetime.utcnow)