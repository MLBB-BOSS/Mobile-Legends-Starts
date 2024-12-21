# models/bug_report.py

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .user import User, Base

class BugReport(Base):
    __tablename__ = 'bug_reports'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    report = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="bug_reports")
    
    def __repr__(self):
        return f"<BugReport(user_id={self.user_id}, report='{self.report[:20]}...')>"