"""
Модели базы данных SQLAlchemy.

Этот модуль определяет схему базы данных с использованием SQLAlchemy ORM.
"""

from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class User(Base):
    """
    Модель пользователя для хранения данных аутентификации.

    Атрибуты:
        id: Первичный ключ
        email: Уникальный email пользователя
        full_name: Полное имя пользователя
        hashed_password: Хешированный пароль
        is_active: Статус активации аккаунта
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
