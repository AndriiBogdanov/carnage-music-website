#!/bin/bash

echo "=== НАЧАЛО СБОРКИ ==="

# Устанавливаем зависимости
echo "Устанавливаем зависимости..."
pip install -r requirements.txt

# Выполняем миграции
echo "Выполняем миграции..."
python manage.py migrate

# Собираем статические файлы
echo "Собираем статические файлы..."
python manage.py collectstatic --noinput

# Создаем суперпользователя и тестовые данные
echo "Создаем суперпользователя и тестовые данные..."
python setup_database.py

echo "=== СБОРКА ЗАВЕРШЕНА ==="
