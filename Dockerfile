FROM python:3.11-slim

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Создаем пользователя для безопасности
RUN useradd --create-home --shell /bin/bash app

# Создаем директорию для статических файлов
RUN mkdir -p /app/staticfiles && chown -R app:app /app

# Переключаемся на пользователя app
USER app

# Открываем порт
EXPOSE 8000

# Запускаем Django
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "carnage_music_project.wsgi:application"]
