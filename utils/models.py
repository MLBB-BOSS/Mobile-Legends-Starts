from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float, ForeignKey, Text
from sqlalchemy.orm import relationship, DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    rating = Column(Float, default=0.0)
    tournaments_count = Column(Integer, default=0)
    wins = Column(Integer, default=0)
    matches_count = Column(Integer, default=0)
    
    # Relationships
    stats = relationship("UserStats", back_populates="user", uselist=False)
    feedbacks = relationship("Feedback", back_populates="user")
    bug_reports = relationship("BugReport", back_populates="user")

class UserStats(Base):
    __tablename__ = 'user_stats'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    tournaments_played = Column(Integer, default=0)
    tournaments_won = Column(Integer, default=0)
    matches_played = Column(Integer, default=0)
    matches_won = Column(Integer, default=0)
    rating = Column(Float, default=0.0)
    total_screenshots = Column(Integer, default=0)
    achievements_count = Column(Integer, default=0)
    last_activity = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="stats")

class Feedback(Base):
    __tablename__ = 'feedbacks'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    text = Column(Text)
    rating = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    user = relationship("User", back_populates="feedbacks")

class BugReport(Base):
    __tablename__ = 'bug_reports'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(200))
    description = Column(Text)
    status = Column(String(50), default='new')
    created_at = Column(DateTime, default=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)
    
    # Relationship
    user = relationship("User", back_populates="bug_reports")
