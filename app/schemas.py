"""
Pydantic схемы для валидации запросов и ответов.

Этот модуль определяет модели данных для валидации ввода/вывода API
с использованием Pydantic.
"""

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Базовая схема пользователя с общими полями."""
    email: EmailStr
    full_name: str | None = None


class UserCreate(UserBase):
    """Схема для регистрации пользователя."""
    password: str


class UserOut(UserBase):
    """Схема для вывода данных пользователя."""
    id: int
    is_active: bool

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Схема для ответа с JWT токеном."""
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    """Схема для запроса входа (альтернатива OAuth2 форме)."""
    email: EmailStr
    password: str
