from typing import List, Optional
from .base import BaseModel

class Hero(BaseModel):
    def __init__(self, 
                 name: str, 
                 role: str, 
                 description: str,
                 difficulty: str = "Normal",
                 speciality: List[str] = None,
                 recommended_spells: List[str] = None,
                 recommended_emblems: List[str] = None):
        super().__init__()
        self.name: str = name
        self.role: str = role
        self.description: str = description
        self.difficulty: str = difficulty
        self.speciality: List[str] = speciality or []
        self.recommended_spells: List[str] = recommended_spells or []
        self.recommended_emblems: List[str] = recommended_emblems or []
        self.media_count: int = 0
        self.guide_count: int = 0
        self.popularity: int = 0

    @property
    def search_text(self) -> str:
        """Generate searchable text for the hero"""
        return f"{self.name} {self.role} {self.description}".lower()
