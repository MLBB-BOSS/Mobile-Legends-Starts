# database/repositories/user_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from models import User
from ..base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    def __init__(self):
        super().__init__(User)
    
    def get_by_telegram_id(self, session: Session, telegram_id: int) -> Optional[User]:
        return session.query(self.model).filter(self.model.telegram_id == telegram_id).first()
    
    def get_admins(self, session: Session) -> List[User]:
        return session.query(self.model).filter(self.model.is_admin == True).all()
    
    def update_experience(self, session: Session, user_id: int, exp_amount: int) -> Optional[User]:
        user = self.get_by_id(session, user_id)
        if user:
            user.experience += exp_amount
            # Логіка підвищення рівня
            user.level = user.experience // 1000 + 1
            session.flush()
        return user
