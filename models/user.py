from sqlalchemy import Column, BigInteger, String
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(100), nullable=True)

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username={self.username})>"
