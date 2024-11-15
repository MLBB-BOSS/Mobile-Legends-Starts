from datetime import datetime
from typing import Any, Dict
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.declarative import declared_attr

class Base(DeclarativeBase):
    """Базовий клас для всіх моделей з корисними методами та полями"""
    
    # Автоматично додаємо назву таблиці на основі імені класу
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
    # Загальні поля для всіх таблиць
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def to_dict(self) -> Dict[str, Any]:
        """Конвертує модель в словник"""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Base":
        """Створює екземпляр моделі з словника"""
        return cls(**{
            k: v for k, v in data.items() 
            if k in cls.__table__.columns
        })

    def update(self, **kwargs: Any) -> None:
        """Оновлює поля моделі"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self) -> str:
        """Представлення моделі у вигляді рядка"""
        attrs = []
        for column in self.__table__.columns:
            value = getattr(self, column.name)
            attrs.append(f"{column.name}={value!r}")
        return f"{self.__class__.__name__}({', '.join(attrs)})"
