# database/repositories/hero_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from models import Hero, HeroRole
from ..base_repository import BaseRepository

class HeroRepository(BaseRepository[Hero]):
    def __init__(self):
        super().__init__(Hero)
    
    def get_by_name(self, session: Session, name: str) -> Optional[Hero]:
        return session.query(self.model).filter(self.model.name == name).first()
    
    def get_by_role(self, session: Session, role: HeroRole) -> List[Hero]:
        return session.query(self.model).filter(self.model.role == role).all()
    
    def get_with_media(self, session: Session, hero_id: int) -> Optional[Hero]:
        return session.query(self.model)\
            .filter(self.model.id == hero_id)\
            .options(joinedload(self.model.media))\
            .first()
