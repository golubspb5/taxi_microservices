# Taxi Service

Простой бэкенд для сервиса заказа такси на сетке N×M.  
Использует FastAPI, PostgreSQL и Redis (по желанию).

## Структура проекта

- `app/` – код приложения (API, модели, схемы, сервисы, задачи)
- `alembic/` – миграции базы данных
- `tests/` – unit и интеграционные тесты
- `Dockerfile` и `docker-compose.yml` – для контейнеризации

## Запуск проекта

1. Сборка и запуск через Docker:

```bash
docker-compose build
docker-compose up
