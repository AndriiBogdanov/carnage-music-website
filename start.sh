#!/bin/bash

# Выполняем миграции
echo "Выполняем миграции..."
python manage.py migrate

# Собираем статические файлы
echo "Собираем статические файлы..."
python manage.py collectstatic --noinput

# Создаем суперпользователя
echo "Создаем суперпользователя..."
python create_superuser.py

# Запускаем сервер
echo "Запускаем сервер..."
gunicorn carnage_music_project.wsgi:application
