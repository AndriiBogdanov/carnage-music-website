#!/usr/bin/env python
"""
Скрипт для автоматического создания суперпользователя Django
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carnage_music_project.settings')
django.setup()

from django.contrib.auth.models import User

def create_superuser():
    """Создает суперпользователя если его нет"""
    username = 'carnage_admin'
    email = 'admin@carnagemusic.com'
    password = 'carnage2024!'
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"✅ Суперпользователь {username} создан успешно!")
    else:
        print(f"ℹ️ Суперпользователь {username} уже существует")

if __name__ == '__main__':
    create_superuser()
