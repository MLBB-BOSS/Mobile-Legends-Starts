# UTC:22:42
# 2024-11-24
# models/user.py
# Author: MLBB-BOSS
# Description: User model
# The era of artificial intelligence.

from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: int
    user_id: int
    username: Optional[str]
    first_name: str
    last_name: Optional[str]
    ml_id: Optional[str]
    ml_server: Optional[str]
    ml_nickname: Optional[str]
    favorite_heroes: Optional[str]
    main_role: Optional[str]
    matches_played: int
    wins: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
