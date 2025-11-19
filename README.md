![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)
![Tests](https://img.shields.io/badge/Tests-Passing-green.svg)

# 🚀 FastAPI Асинхронный Бэкенд Проект

[English](#-fastapi-asynchronous-backend-project) | **Русский**

Полнофункциональное асинхронное бэкенд-приложение, построенное на современном стеке технологий.

## 🔥 Демо

**Живое демо:** [https://your-project.onrender.com](https://your-project.onrender.com)

**Доступные эндпоинты:**
- 📚 **Документация API:** [/docs](https://your-project.onrender.com/docs)
- 🔍 **Альтернативная документация:** [/redoc](https://your-project.onrender.com/redoc)
- 🏓 **Health Check:** [/health](https://your-project.onrender.com/health)

## 🛠 Технологический стек

**Бэкенд:**
- **Python 3.11+** - Основной язык программирования
- **FastAPI** - Современный асинхронный фреймворк
- **SQLAlchemy 2.0** - Асинхронный ORM
- **Alembic** - Миграции базы данных
- **Pydantic** - Валидация данных

**База данных:**
- **PostgreSQL** - Основная реляционная БД
- **AsyncPG** - Асинхронный драйвер PostgreSQL

**Инфраструктура:**
- **Docker** - Контейнеризация
- **Docker Compose** - Оркестрация
- **Pytest** - Тестирование
- **GitHub Actions** - CI/CD

## 🚀 Быстрый старт

### Предварительные требования
- Docker & Docker Compose
- Python 3.11+ (для локальной разработки)

### Запуск через Docker (Рекомендуется)
```bash
# Клонировать репозиторий
git clone https://github.com/yourusername/your-project.git
cd your-project

# Запустить все сервисы
docker-compose up --build

# Приложение будет доступно по http://localhost:8000
```

### Локальная разработка
```bash
# Создать виртуальное окружение
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements.txt

# Запустить базу данных
docker-compose up -d db

# Применить миграции
alembic upgrade head

# Запустить сервер
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📡 API Эндпоинты

### Основные endpoints:
- `GET /health` - Проверка работоспособности API
- `POST /api/v1/users` - Создание пользователя
- `GET /api/v1/users/{id}` - Получение пользователя
- `POST /api/v1/auth/login` - Аутентификация

### Особенности API:
- ✅ **Асинхронные операции**
- ✅ **JWT аутентификация**
- ✅ **Валидация данных Pydantic**
- ✅ **Пагинация и фильтрация**
- ✅ **Обработка ошибок**

## 🧪 Тестирование

Проект включает комплексные тесты:

```bash
# Запуск всех тестов
pytest

# Запуск с покрытием
pytest --cov=app --cov-report=html

# Запуск тестов в Docker
docker-compose -f docker-compose.test.yml up --build
```

**Покрытие тестами:**
- Модульные тесты (Unit tests)
- Интеграционные тесты
- Тесты API эндпоинтов

## 🗄 Структура проекта

```
project/
├── app/
│   ├── api/           # Роутеры и endpoints
│   ├── core/          # Конфигурация, security
│   ├── models/        # SQLAlchemy модели
│   ├── schemas/       # Pydantic схемы
│   ├── services/      # Бизнес-логика
│   └── tests/         # Тесты
├── migrations/        # Alembic миграции
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## 🔧 Настройка окружения

Создайте `.env` файл:
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 👨‍💻 Разработка

### Миграции базы данных:
```bash
# Создать новую миграцию
alembic revision --autogenerate -m "Description"

# Применить миграции
alembic upgrade head

# Откатить миграцию
alembic downgrade -1
```

### Code Style:
```bash
# Форматирование кода
black app/

# Проверка стиля
flake8 app/

# Сортировка импортов
isort app/
```

## 📈 Производительность

Благодаря асинхронной архитектуре и использованию:
- **FastAPI** для высокопроизводительных запросов
- **AsyncPG** для асинхронного доступа к БД
- **Pydantic** для быстрой валидации
- **Docker** для изоляции и масштабирования

---

# 🚀 FastAPI Asynchronous Backend Project

**Russian** | [English](#-fastapi-asynchronous-backend-project)

A fully-featured asynchronous backend application built with modern technology stack.

...