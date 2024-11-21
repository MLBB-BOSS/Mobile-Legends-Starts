# models/character.py

from pydantic import BaseModel, Field
from typing import List, Optional

class Character(BaseModel):
    name: str = Field(..., description="Ім'я персонажа")
    role: str = Field(..., description="Роль персонажа")
    skills: List[str] = Field(..., description="Список навичок")
    builds: List[str] = Field(..., description="Список білдів")
    counter_picks: List[str] = Field(..., description="Список контр-піків")

class Characters(BaseModel):
    Assassin: Optional[dict] = None
    Fighter: Optional[dict] = None
    Mage: Optional[dict] = None
    Marksman: Optional[dict] = None
    Support: Optional[dict] = None
    Tank: Optional[dict] = None
