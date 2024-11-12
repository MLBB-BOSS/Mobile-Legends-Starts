from typing import Dict, Optional
from datetime import datetime
from .base import BaseModel

class MediaType:
    SCREENSHOT = 'screenshot'
    SKIN = 'skin'
    GAMEPLAY = 'gameplay'
    BUILD = 'build'

class HeroMedia(BaseModel):
    def __init__(self, 
                 hero_id: str,
                 media_type: str,
                 url: str,
                 author_id: str,
                 author_nickname: str,
                 metadata: Optional[Dict] = None):
        super().__init__()
        self.hero_id: str = hero_id
        self.media_type: str = media_type
        self.url: str = url
        self.author_id: str = author_id
        self.author_nickname: str = author_nickname
        self.metadata: Dict = metadata or {}
        self.approved: bool = False
        self.votes: int = 0
        self.approver_id: Optional[str] = None
        self.approved_at: Optional[datetime] = None
        self.reports: List[Dict] = []

    def approve(self, approver_id: str) -> None:
        """Approve the media content"""
        self.approved = True
        self.approver_id = approver_id
        self.approved_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def add_vote(self, user_id: str) -> bool:
        """Add a vote to the media"""
        if user_id not in self.metadata.get('voters', []):
            voters = self.metadata.get('voters', [])
            voters.append(user_id)
            self.metadata['voters'] = voters
            self.votes += 1
            self.updated_at = datetime.utcnow()
            return True
        return False
