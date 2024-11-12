from datetime import datetime
from typing import Optional, Dict, Any
from uuid import uuid4

class BaseModel:
    def __init__(self):
        self.id: str = str(uuid4())
        self.created_at: datetime = datetime.utcnow()
        self.updated_at: datetime = datetime.utcnow()
        self.is_active: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return {
            key: value for key, value in self.__dict__.items()
            if not key.startswith('_')
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BaseModel':
        """Create model instance from dictionary"""
        instance = cls()
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        return instance
