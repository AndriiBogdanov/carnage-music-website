from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
import os
from django.core.exceptions import ValidationError


class Genre(models.Model):
    """Модель жанра музыки"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Album(models.Model):
    """Модель релиза"""
    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")
    artist = models.ForeignKey('artists.Artist', on_delete=models.CASCADE, verbose_name="Артист", null=True, blank=True)
    cover = models.ImageField(upload_to='albums/', blank=True, null=True, verbose_name="Обложка")
    release_date = models.DateField(verbose_name="Дата релиза")
    description = models.TextField(blank=True, verbose_name="Описание релиза", 
                                 help_text="Подробное описание релиза, включая описание каждого трека")
    catalog_number = models.CharField(max_length=50, blank=True, verbose_name="Каталожный номер", 
                                    help_text="Необязательно. Например: CARNAGE001, EP001")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Релиз"
        verbose_name_plural = "Релизы"
        ordering = ['-release_date']
    
    def __str__(self):
        if self.artist:
            return f"{self.artist.name} - {self.title}"
        return self.title
    
    def get_absolute_url(self):
        return reverse('music:album_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.cover:
            img = Image.open(self.cover.path)
            if img.height > 800 or img.width > 800:
                img.thumbnail((800, 800))
                img.save(self.cover.path)


class Track(models.Model):
    """Модель трека"""
    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=200, verbose_name="URL")
    artist = models.ForeignKey('artists.Artist', on_delete=models.CASCADE, verbose_name="Артист", null=True, blank=True)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True, 
                             related_name='tracks', verbose_name="Релиз")
    
    # Файлы
    audio_file = models.FileField(upload_to='tracks/', blank=True, null=True, verbose_name="Аудио файл")
    cover = models.ImageField(upload_to='tracks/', blank=True, null=True, verbose_name="Обложка")
    
    # Метаданные
    duration = models.DurationField(blank=True, null=True, verbose_name="Длительность")
    bpm = models.PositiveIntegerField(blank=True, null=True, verbose_name="BPM")
    key = models.CharField(max_length=5, blank=True, verbose_name="Тональность")
    track_number = models.PositiveIntegerField(blank=True, null=True, verbose_name="Номер трека")
    genres = models.CharField(max_length=500, blank=True, verbose_name="Жанры", 
                            help_text="Введите жанры через запятую (например: Techno, Industrial, EBM)")
    
    # Ссылки на стриминговые платформы
    spotify_url = models.URLField(blank=True, verbose_name="Spotify")
    apple_music_url = models.URLField(blank=True, verbose_name="Apple Music")
    youtube_url = models.URLField(blank=True, verbose_name="YouTube")
    soundcloud_url = models.URLField(blank=True, verbose_name="SoundCloud")
    bandcamp_url = models.URLField(blank=True, verbose_name="Bandcamp")
    beatport_url = models.URLField(blank=True, verbose_name="Beatport")
    
    # Статистика
    play_count = models.PositiveIntegerField(default=0, verbose_name="Количество прослушиваний")
    download_count = models.PositiveIntegerField(default=0, verbose_name="Количество скачиваний")
    
    # Настройки
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемый")
    is_free_download = models.BooleanField(default=False, verbose_name="Бесплатное скачивание")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    
    release_date = models.DateField(blank=True, null=True, verbose_name="Дата релиза")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Трек"
        verbose_name_plural = "Треки"
        ordering = ['-release_date', 'track_number']
    
    def __str__(self):
        if self.artist:
            return f"{self.artist.name} - {self.title}"
        return self.title
    
    def get_absolute_url(self):
        if self.artist:
            return reverse('music:track_detail', kwargs={'slug': self.slug, 'artist_slug': self.artist.slug})
        return reverse('music:track_detail', kwargs={'slug': self.slug, 'artist_slug': 'unknown'})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.cover:
            img = Image.open(self.cover.path)
            if img.height > 800 or img.width > 800:
                img.thumbnail((800, 800))
                img.save(self.cover.path)


