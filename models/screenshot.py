from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from .base import BaseModel

class Screenshot(BaseModel):
    __tablename__ = 'screenshots'

    user_id = Column(Integer, nullable=False, index=True)
    file_id = Column(String, nullable=False)
    file_unique_id = Column(String, nullable=False, unique=True)
    width = Column(Integer)
    height = Column(Integer)
    file_path = Column(String)

    def __repr__(self):
        return f"<Screenshot(id={self.id}, user_id={self.user_id}, file_id={self.file_id})>"

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'file_id': self.file_id,
            'file_unique_id': self.file_unique_id,
            'width': self.width,
            'height': self.height,
            'file_path': self.file_path,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
