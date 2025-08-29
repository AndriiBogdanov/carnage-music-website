#!/usr/bin/env python
"""
Скрипт для настройки базы данных и создания тестовых данных
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'carnage_music_project.settings')
django.setup()

from django.contrib.auth.models import User
from artists.models import Artist
from music.models import Album, Track
from django.utils.text import slugify

def setup_database():
    """Настраивает базу данных и создает тестовые данные"""
    
    # Создаем суперпользователя
    username = 'carnage_admin'
    email = 'admin@carnagemusic.com'
    password = 'carnage2024!'
    
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f"✅ Суперпользователь {username} создан успешно!")
    else:
        print(f"ℹ️ Суперпользователь {username} уже существует")
    
    # Создаем тестового артиста если нет артистов
    if not Artist.objects.exists():
        artist = Artist.objects.create(
            name="Test Artist",
            slug="test-artist",
            bio="Тестовый артист для демонстрации",
            photo="artists/test_artist.jpg",
            is_active=True
        )
        print(f"✅ Тестовый артист создан: {artist.name}")
        
        # Создаем тестовый альбом
        album = Album.objects.create(
            title="Test Album",
            artist=artist,
            release_date="2024-01-01",
            cover="albums/test_album.jpg"
        )
        print(f"✅ Тестовый альбом создан: {album.title}")
        
        # Создаем тестовый трек
        track = Track.objects.create(
            title="Test Track",
            album=album,
            track_number=1,
            audio_file="tracks/test_track.mp3"
        )
        print(f"✅ Тестовый трек создан: {track.title}")
    else:
        print(f"ℹ️ Артисты уже существуют ({Artist.objects.count()} артистов)")

if __name__ == '__main__':
    setup_database()
