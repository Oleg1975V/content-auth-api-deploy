"""
FastAPI приложение с эндпоинтами аутентификации пользователей.

Этот модуль определяет основное FastAPI приложение и API маршруты
для регистрации, входа и управления профилем пользователя.
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import Base, engine
from app import models
from app.schemas import UserCreate, UserOut, Token
from app.auth import hash_password, verify_password, create_access_token
from app.deps import get_db, get_current_user

# Создание таблиц базы данных
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Content Auth API",
    description="Простой API для аутентификации пользователей с JWT токенами",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware для продакшена
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://your-frontend-domain.vercel.app"  # замените на ваш фронтенд
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(
    "/api/v1/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Регистрация нового пользователя",
    description="Создает новый аккаунт пользователя с email и паролем"
)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):
    """
    Регистрирует нового пользователя.

    Аргументы:
        payload: Данные для регистрации пользователя
        db: Сессия базы данных

    Возвращает:
        Данные нового пользователя

    Вызывает:
        HTTPException: Если email уже существует или регистрация не удалась
    """
    # Проверяем существование пользователя
    existing_user = db.query(models.User).filter(
        models.User.email == payload.email
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email уже зарегистрирован"
        )

    # Создаем нового пользователя
    user = models.User(
        email=payload.email,
        full_name=payload.full_name,
        hashed_password=hash_password(payload.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


@app.post(
    "/api/v1/login",
    response_model=Token,
    summary="Вход пользователя",
    description="Аутентифицирует пользователя и возвращает JWT токен"
)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Аутентифицирует пользователя и возвращает токен доступа.

    Аргументы:
        form_data: OAuth2 форма с username и password
        db: Сессия базы данных

    Возвращает:
        JWT токен доступа

    Вызывает:
        HTTPException: Если учетные данные неверны
    """
    user = db.query(models.User).filter(
        models.User.email == form_data.username
    ).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверные учетные данные",
        )

    token = create_access_token(str(user.id))
    return Token(access_token=token)


@app.get(
    "/api/v1/me",
    response_model=UserOut,
    summary="Получить текущего пользователя",
    description="Получает данные профиля текущего аутентифицированного пользователя"
)
def read_me(current_user: models.User = Depends(get_current_user)):
    """
    Получает профиль текущего пользователя.

    Аргументы:
        current_user: Аутентифицированный пользователь из зависимости

    Возвращает:
        Данные текущего пользователя
    """
    return current_user


@app.post(
    "/api/v1/logout",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Выход пользователя",
    description="Клиентская инвалидация токена (JWT является stateless)"
)
def logout():
    """
    Эндпоинт выхода.

    Примечание: JWT является stateless, поэтому выход обрабатывается
    на клиентской стороне путем удаления токена.
    """
    return None


@app.get("/health")
def health_check():
    """Эндпоинт проверки здоровья для мониторинга сервиса."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
