# File: config/messages/base.py
from pydantic import BaseModel, Field
from typing import Dict
from pathlib import Path
from functools import lru_cache

class NavigationMessages(BaseModel):
    main: str = Field(..., description="Main navigation message")
    guides: str = Field(..., description="Guides section message")
    characters: str = Field(..., description="Characters section message")
    counter_picks: str = Field(..., description="Counter picks section message")
    builds: str = Field(..., description="Builds section message")
    voting: str = Field(..., description="Voting section message")
    back_to_main_menu: str = Field(..., description="Back to main menu message")

class ProfileMessages(BaseModel):
    main: str = Field(..., description="Main profile message")
    statistics: str = Field(..., description="Statistics section message")
    achievements: str = Field(..., description="Achievements section message")
    settings: str = Field(..., description="Settings section message")

class Messages(BaseModel):
    welcome_message: str = Field(..., description="Welcome message for new users")
    navigation: NavigationMessages
    profile: ProfileMessages

    @classmethod
    def load_messages(cls, lang: str = "uk") -> "Messages":
        """Load messages for specified language"""
        messages_path = Path("config/messages/locales") / f"{lang}.json"
        return cls.parse_file(messages_path)

@lru_cache()
def get_messages(lang: str = "uk") -> Messages:
    """Get cached messages instance"""
    return Messages.load_messages(lang)
