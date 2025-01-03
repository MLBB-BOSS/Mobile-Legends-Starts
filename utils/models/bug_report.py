# utils/models/bug_report.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class BugReport(Base):
    __tablename__ = 'bug_reports'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # Відповідь на 'users.id'
    description = Column(String, nullable=False)

    user = relationship("User", back_populates="bug_reports")