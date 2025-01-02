# utils/models/user.py
from sqlalchemy import Column, Integer, String

class User:
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    # Інші поля...

    def some_method(self):
        from utils.db import Base
        # Використання Base тут
