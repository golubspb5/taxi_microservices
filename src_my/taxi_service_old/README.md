# Taxi Service (skeleton)

Структура проекта и скелет файлов для сервиса заказа такси (N x M grid).
Запуск:
1. Создать виртуальное окружение и установить зависимости:
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
2. Доработать config.py (DATABASE_URL, REDIS_DSN)
3. Запустить uvicorn:
   uvicorn app.main:app --reload
