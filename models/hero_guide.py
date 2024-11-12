from typing import List, Optional
from datetime import datetime
from .base import BaseModel

class HeroGuide(BaseModel):
    def __init__(self,
                 hero_id: str,
                 content: str,
                 author_id: str,
                 author_nickname: str,
                 title: str,
                 tags: List[str] = None):
        super().__init__()
        self.hero_id: str = hero_id
        self.title: str = title
        self.content: str = content
        self.author_id: str = author_id
        self.author_nickname: str = author_nickname
        self.tags: List[str] = tags or []
        self.approved: bool = False
        self.votes: int = 0
        self.views: int = 0
        self.approver_id: Optional[str] = None
        self.approved_at: Optional[datetime] = None
        self.comments: List[Dict] = []

    def increment_view(self) -> None:
        """Increment guide view count"""
        self.views += 1
        self.updated_at = datetime.utcnow()

    def add_comment(self, user_id: str, username: str, content: str) -> Dict:
        """Add comment to the guide"""
        comment = {
            'id': str(uuid4()),
            'user_id': user_id,
            'username': username,
            'content': content,
            'created_at': datetime.utcnow()
        }
        self.comments.append(comment)
        self.updated_at = datetime.utcnow()
        return comment
