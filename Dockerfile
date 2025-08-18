# Базовый образ с Python
FROM python:3.13-slim

# Рабочая директория в контейнере
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Установка зависимостей c кэшированием на проекте (выносим отдельно)
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install --no-cache-dir -r requirements.txt

# Клонирование репозитория
COPY . .

# Команда запуска тестов
CMD ["pytest"]
