#!/usr/bin/env python
"""
Скрипт для инициализации новой базы данных на Render
"""
import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carnage_music_project.settings_render')
django.setup()

from django.core.management import execute_from_command_line
from django.db import connection

def init_database():
    """Инициализация базы данных"""
    print("🗄️ Инициализация базы данных...")
    
    # Создаем таблицы
    print("📋 Создаем таблицы...")
    execute_from_command_line(['manage.py', 'migrate', '--run-syncdb'])
    
    # Создаем суперпользователя
    print("👤 Создаем суперпользователя...")
    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@carnagemusic.com', 'admin123')
        print("✅ Суперпользователь создан: admin / admin123")
    else:
        print("ℹ️ Суперпользователь уже существует")
    
    print("🎉 База данных инициализирована!")

if __name__ == '__main__':
    init_database()
