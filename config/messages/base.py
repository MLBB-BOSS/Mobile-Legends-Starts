from pydantic import BaseModel, Field
from pathlib import Path
from functools import lru_cache

class NavigationMessages(BaseModel):
    main: str 
    guides: str
    characters: str
    counter_picks: str
    builds: str
    voting: str
    back_to_main: str

class ProfileMessages(BaseModel):
    main: str
    statistics: str
    achievements: str
    settings: str

class Messages(BaseModel):
    welcome_message: str
    navigation: NavigationMessages
    profile: ProfileMessages

    @classmethod
    def load_messages(cls, lang: str = "uk") -> "Messages":
        messages_path = Path("config/messages/locales") / f"{lang}.json"
        return cls.parse_file(messages_path)

@lru_cache()
def get_messages(lang: str = "uk") -> Messages:
    return Messages.load_messages(lang)
