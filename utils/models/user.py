from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String)
    name = Column(String)
    email = Column(String, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    stats = relationship("UserStats", back_populates="user", uselist=False)
    bug_reports = relationship("BugReport", back_populates="user")
    feedbacks = relationship("Feedback", back_populates="user")
    screenshots = relationship("Screenshot", back_populates="user")
    achievements = relationship("Achievement", back_populates="user")
    tournament_participations = relationship("TournamentParticipation", back_populates="user")

    def __init__(self, telegram_id, username=None, name=None, email=None):
        self.telegram_id = telegram_id
        self.username = username
        self.name = name
        self.email = email

    def __repr__(self):
        return f"<User(telegram_id={self.telegram_id}, username={self.username})>"

    @property
    def total_matches(self):
        return self.stats.games_played if self.stats else 0

    @property
    def total_wins(self):
        return self.stats.wins if self.stats else 0

    @property
    def total_losses(self):
        return self.stats.losses if self.stats else 0

    @property
    def win_rate(self):
        if not self.total_matches:
            return 0
        return (self.total_wins / self.total_matches) * 100

    @property
    def achievements_count(self):
        return len(self.achievements) if self.achievements else 0

    @property
    def screenshots_count(self):
        return len(self.screenshots) if self.screenshots else 0

    @property
    def tournament_count(self):
        return len(self.tournament_participations) if self.tournament_participations else 0

    def to_dict(self):
        """Конвертує об'єкт користувача в словник для API відповідей"""
        return {
            'id': self.id,
            'telegram_id': self.telegram_id,
            'username': self.username,
            'name': self.name,
            'email': self.email,
            'stats': {
                'total_matches': self.total_matches,
                'wins': self.total_wins,
                'losses': self.total_losses,
                'win_rate': self.win_rate,
                'achievements_count': self.achievements_count,
                'screenshots_count': self.screenshots_count,
                'tournament_count': self.tournament_count
            },
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def update_from_dict(self, data):
        """Оновлює дані користувача з словника"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'telegram_id', 'created_at', 'updated_at']:
                setattr(self, key, value)