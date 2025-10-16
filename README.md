# Content Auth API

Простой REST API для аутентификации пользователей с JWT токенами на FastAPI.

## Быстрый старт

### Установка и запуск

1. **Клонируйте репозиторий:**
git clone https://github.com/yourusername/content-auth-api.git
cd content-auth-api

2. **Создай виртуальное окружение:**
python -m venv venv
source venv/bin/activate  # Linux/Mac
#### или
venv\Scripts\activate     # Windows

2. **Установите зависимости:**
pip install -r requirements.txt

3. **Запустите сервер:**
python run.py
#### или 
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

4. **Откройте в браузере:**
API документация: http://127.0.0.1:8000/docs

5. **Откройте в браузере:**
frontend/index.html

### Онлайн демо
***API доступно по ссылке:*** 
https://content-auth-api.onrender.com

***Документация:*** 
https://content-auth-api.onrender.com/docs

***Health check:*** 
https://content-auth-api.onrender.com/health


### API Endpoints
POST /api/v1/register - Регистрация пользователя

POST /api/v1/login - Вход и получение JWT токена

GET /api/v1/me - Получение профиля пользователя

POST /api/v1/logout - Выход

GET /health - Проверка здоровья сервиса

### Технологии
Backend: FastAPI, SQLAlchemy, JWT

Database: SQLite (можно переключить на PostgreSQL)

Frontend: HTML, JavaScript

Auth: JWT tokens, password hashing

### Тестирование
**Запустите тесты:**
python test_api.py

**В ручную**
через http://127.0.0.1:8000/docs

