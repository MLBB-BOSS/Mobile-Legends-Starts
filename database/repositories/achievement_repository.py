# database/repositories/achievement_repository.py
from typing import Optional, List
from sqlalchemy.orm import Session
from models import Achievement, User
from ..base_repository import BaseRepository

class AchievementRepository(BaseRepository[Achievement]):
    def __init__(self):
        super().__init__(Achievement)
    
    def award_to_user(self, session: Session, achievement_id: int, user_id: int) -> bool:
        achievement = self.get_by_id(session, achievement_id)
        user = session.query(User).get(user_id)
        
        if achievement and user:
            if achievement not in user.achievements:
                user.achievements.append(achievement)
                session.flush()
                return True
        return False
    
    def get_user_achievements(self, session: Session, user_id: int) -> List[Achievement]:
        user = session.query(User).get(user_id)
        return user.achievements if user else []
