# utils/models/feedback.py
from sqlalchemy import Column, Integer, String, Text
from utils.db_base import Base

class Feedback(Base):
    __tablename__ = 'feedback'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    feedback_text = Column(Text, nullable=False)

    def __repr__(self):
        return f"<Feedback(id={self.id}, user_id={self.user_id}, feedback_text={self.feedback_text})>"
