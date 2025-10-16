"""
Утилиты для аутентификации и хеширования паролей.

Этот модуль предоставляет функции для хеширования/проверки паролей
и создания/валидации JWT токенов с использованием passlib и python-jose.
"""

import os
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

# Контекст для хеширования паролей с использованием схемы sha256_crypt
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# Конфигурация JWT
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def hash_password(password: str) -> str:
    """
    Хеширует пароль с использованием sha256_crypt от passlib.

    Аргументы:
        password: Пароль в открытом виде для хеширования

    Возвращает:
        Хешированную строку пароля
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет пароль против его хеша.

    Аргументы:
        plain_password: Пароль в открытом виде для проверки
        hashed_password: Ранее хешированный пароль

    Возвращает:
        True если пароль совпадает, False в противном случае
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str) -> str:
    """
    Создает JWT токен доступа.

    Аргументы:
        subject: Идентификатор субъекта (обычно ID пользователя)

    Возвращает:
        Закодированную строку JWT токена
    """
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> str | None:
    """
    Декодирует и валидирует JWT токен.

    Аргументы:
        token: Строка JWT токена

    Возвращает:
        Субъект из payload токена или None если токен невалиден
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
