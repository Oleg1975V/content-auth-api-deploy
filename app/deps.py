"""
Утилиты dependency injection для FastAPI.

Этот модуль предоставляет зависимости для сессий базы данных и
аутентификации, которые могут использоваться в обработчиках маршрутов.
"""

from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app import models
from app.auth import decode_token

# OAuth2 схема для аутентификации по токену
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")


def get_db() -> Generator[Session, None, None]:
    """
    Зависимость для сессии базы данных.

    Yields:
        Сессия базы данных

    Гарантирует:
        Сессия закрывается после завершения запроса
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    """
    Зависимость для получения текущего аутентифицированного пользователя.

    Аргументы:
        token: JWT токен из заголовка Authorization
        db: Сессия базы данных

    Возвращает:
        Объект аутентифицированного пользователя

    Вызывает:
        HTTPException: Если токен невалиден или пользователь не найден
    """
    user_id = decode_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный токен",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return user
