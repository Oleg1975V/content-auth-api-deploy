"""
Скрипт для тестирования API аутентификации.
"""

import requests


def test_api():
    """Тестирует все эндпоинты API."""
    BASE_URL = "http://127.0.0.1:8000/api/v1"

    print("=== ТЕСТИРОВАНИЕ CONTENT AUTH API ===")
    print()

    # Тест регистрации
    print("1. 📝 Тест регистрации пользователя...")
    try:
        response = requests.post(f"{BASE_URL}/register", json={
            "email": "testuser@example.com",
            "full_name": "Test User",
            "password": "testpassword123"
        })
        print(f"   Статус: {response.status_code}")
        if response.status_code == 201:
            user_data = response.json()
            print("   ✅ Успех: Пользователь создан")
            print(f"      ID: {user_data['id']}")
        else:
            error_detail = response.json().get('detail', 'Неизвестная ошибка')
            print(f"   ❌ Ошибка: {error_detail}")
    except requests.exceptions.ConnectionError:
        print("   ❌ Ошибка: Не удалось подключиться к серверу")
        print("   Убедитесь, что сервер запущен на http://127.0.0.1:8000")
        return

    # Тест входа
    print("\n2. 🔑 Тест входа пользователя...")
    response = requests.post(f"{BASE_URL}/login", data={
        "username": "testuser@example.com",
        "password": "testpassword123"
    })
    print(f"   Статус: {response.status_code}")

    token = None
    if response.status_code == 200:
        token_data = response.json()
        token = token_data["access_token"]
        print("   ✅ Успех: Токен получен")
        print(f"      Токен: {token[:20]}...")
    else:
        error_detail = response.json().get('detail', 'Неизвестная ошибка')
        print(f"   ❌ Ошибка: {error_detail}")
        return

    # Тест получения профиля
    print("\n3. 👤 Тест получения профиля...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/me", headers=headers)
    print(f"   Статус: {response.status_code}")

    if response.status_code == 200:
        user_info = response.json()
        print("   ✅ Успех: Профиль получен")
        print(f"      ID: {user_info['id']}")
        print(f"      Email: {user_info['email']}")
        print(f"      Имя: {user_info['full_name']}")
    else:
        error_detail = response.json().get('detail', 'Неизвестная ошибка')
        print(f"   ❌ Ошибка: {error_detail}")

    # Тест проверки здоровья
    print("\n4. 🏥 Тест проверки здоровья...")
    response = requests.get("http://127.0.0.1:8000/health")
    print(f"   Статус: {response.status_code}")
    if response.status_code == 200:
        health_data = response.json()
        print(f"   ✅ Успех: {health_data['status']}")
    else:
        print("   ❌ Ошибка: Сервис не здоров")

    print("\n=== ТЕСТИРОВАНИЕ ЗАВЕРШЕНО ===")


if __name__ == "__main__":
    test_api()
