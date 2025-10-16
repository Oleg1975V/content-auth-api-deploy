"""
Конфигурация базы данных и управление сессиями.

Этот модуль настраивает SQLAlchemy engine, фабрику сессий и базовый класс
для операций с базой данных.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase, scoped_session
from dotenv import load_dotenv

load_dotenv()

# URL базы данных из переменных окружения или SQLite по умолчанию
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# Создание engine базы данных
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite") else {},
)


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy."""
    pass


# Фабрика сессий для dependency injection
SessionLocal = scoped_session(
    sessionmaker(bind=engine, autoflush=False, autocommit=False)
)
