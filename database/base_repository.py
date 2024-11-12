# database/base_repository.py
from typing import Generic, TypeVar, Type, List, Optional, Any
from sqlalchemy.orm import Session
from models.base import BaseModel

T = TypeVar('T', bound=BaseModel)

class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T]):
        self.model = model
    
    def create(self, session: Session, **kwargs) -> T:
        instance = self.model(**kwargs)
        session.add(instance)
        session.flush()  # Отримуємо ID без коміту
        return instance
    
    def get_by_id(self, session: Session, id: int) -> Optional[T]:
        return session.query(self.model).filter(self.model.id == id).first()
    
    def get_all(self, session: Session) -> List[T]:
        return session.query(self.model).all()
    
    def update(self, session: Session, id: int, **kwargs) -> Optional[T]:
        instance = self.get_by_id(session, id)
        if instance:
            for key, value in kwargs.items():
                setattr(instance, key, value)
            session.flush()
        return instance
    
    def delete(self, session: Session, id: int) -> bool:
        instance = self.get_by_id(session, id)
        if instance:
            session.delete(instance)
            session.flush()
            return True
        return False
