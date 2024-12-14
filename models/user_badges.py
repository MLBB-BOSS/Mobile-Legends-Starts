# models/user_badges.py
from sqlalchemy import Table, Column, Integer, ForeignKey
from .base import Base

user_badges = Table(
    'user_badges',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('badge_id', Integer, ForeignKey('badges.id'), primary_key=True)
)
