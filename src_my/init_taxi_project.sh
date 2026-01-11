#!/bin/bash

# Корневая папка проекта
mkdir -p taxi_service
cd taxi_service || exit

# Основные файлы
touch .gitignore README.md requirements.txt Dockerfile docker-compose.yml pyproject.toml

# Alembic
mkdir -p alembic/versions
touch alembic/env.py

# App
mkdir -p app/{api,core,models,schemas,services,tasks}
touch app/main.py app/database.py app/config.py app/deps.py app/events.py
touch app/core/security.py app/core/exceptions.py app/core/utils.py

# Models
touch app/models/{user.py,driver_status.py,trip.py,assignment.py,tariff.py}

# Schemas
touch app/schemas/{auth.py,driver.py,passenger.py,trip.py,common.py,tariff.py}

# Services
touch app/services/{matching_service.py,eta_service.py,pricing_service.py,driver_service.py,trip_service.py,stats_service.py,distance.py,tariff_service.py,user_service.py}

# Tasks
touch app/tasks/{assignment_timeout.py,queue_processor.py}

# API endpoints
touch app/api/{auth.py,passenger.py,driver.py,trips.py}

# Tests
mkdir -p tests
touch tests/{test_smoke.py,__init__.py}

# Инициализация git
git init

echo "Структура проекта taxi_service создана!"
