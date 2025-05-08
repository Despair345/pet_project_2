# Dockerfile
FROM python:3.11-slim

# Установка зависимостей
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Создание рабочей директории
WORKDIR /app

# Установка pip и зависимостей
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем код проекта
COPY . /app/