# utils/models/base.py
from sqlalchemy.ext.declarative import as_declarative, declared_attr

@as_declarative()
class Base:
    """
    Базовий клас для всіх моделей SQLAlchemy.
    """
    id: int
    __name__: str

    # Автоматично генерує ім'я таблиці на основі назви класу
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
