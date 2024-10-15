# 2. Установка зависимостей:
    pip install -r requirements.txt

# 3. Настройка окружения:

    Создайте (будет в проекте) файл .env в корне проекта и добавьте необходимые переменные окружения (например, секретный ключ для JWT, настройки базы данных и т.д.).

# 4 Миграции базы данных:
    alembic upgrade head

# 5. Запуск сервера:
    uvicorn app.main:app --reload

# 6. Доступ к документации:
    Swagger: http://127.0.0.1:8000/docs

    ReDoc: http://127.0.0.1:8000/redoc

# 7. Примеры использования API
     
    # Регистрация пользователя:
        curl -X POST "http://127.0.0.1:8000/api/auth/register" -H "Content-Type: application/json" -d '{"email": "user@example.com", "password": "password"}'
    
    # Создание реферального кода:
        curl -X POST "http://127.0.0.1:8000/api/referral/create" -H "Authorization: Bearer <your_token>" -H "Content-Type: application/json" -d '{"expiration_date": "2024-10-15"}'
    
    # Получение реферального кода по email:
        curl -X GET "http://127.0.0.1:8000/api/referral/get_by_email?email=referrer@example.com"
    
    # Регистрация по реферальному коду:
        curl -X POST "http://127.0.0.1:8000/api/auth/register_with_referral" -H "Content-Type: application/json" -d '{"email": "newuser@example.com", "password": "password", "referral_code": "ABC123"}'