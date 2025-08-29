from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class Artist(models.Model):
    """Модель артиста"""
    name = models.CharField(max_length=200, unique=True, verbose_name="Имя артиста")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")
    real_name = models.CharField(max_length=200, blank=True, verbose_name="Настоящее имя")
    bio = models.TextField(blank=True, verbose_name="Биография")
    slogan = models.CharField(max_length=500, blank=True, verbose_name="Слоган")
    
    # Изображения
    photo = models.ImageField(upload_to='artists/', blank=True, null=True, verbose_name="Фото")
    banner = models.ImageField(upload_to='artists/banners/', blank=True, null=True, verbose_name="Баннер")
    
    # Контактная информация
    email = models.EmailField(blank=True, verbose_name="Email")
    website = models.URLField(blank=True, verbose_name="Веб-сайт")
    
    # Социальные сети
    instagram_url = models.URLField(blank=True, verbose_name="Instagram")
    facebook_url = models.URLField(blank=True, verbose_name="Facebook")
    twitter_url = models.URLField(blank=True, verbose_name="Twitter")
    tiktok_url = models.URLField(blank=True, verbose_name="TikTok")
    soundcloud_url = models.URLField(blank=True, verbose_name="SoundCloud")
    spotify_url = models.URLField(blank=True, verbose_name="Spotify")
    youtube_url = models.URLField(blank=True, verbose_name="YouTube")
    bandcamp_url = models.URLField(blank=True, verbose_name="Bandcamp")
    beatport_url = models.URLField(blank=True, verbose_name="Beatport")
    
    # Географическая информация
    country = models.CharField(max_length=100, blank=True, verbose_name="Страна")
    city = models.CharField(max_length=100, blank=True, verbose_name="Город")
    
    # Последний релиз
    latest_album = models.ForeignKey('music.Album', on_delete=models.SET_NULL, null=True, blank=True, 
                                   related_name='featured_artist', verbose_name="Последний релиз")
    
    # Информация о релизе (для отображения в админке)
    album_info = models.TextField(blank=True, verbose_name="Информация о релизе", 
                                 help_text="Автоматически заполняется при выборе релиза")
    
    # Настройки
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемый")
    is_active = models.BooleanField(default=True, verbose_name="Активный")
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, 
                               verbose_name="Пользователь")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Артист"
        verbose_name_plural = "Артисты"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('artists:artist_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Оптимизация фото
        if self.photo:
            img = Image.open(self.photo.path)
            if img.height > 500 or img.width > 500:
                img.thumbnail((500, 500))
                img.save(self.photo.path)
        
        # Оптимизация баннера
        if self.banner:
            img = Image.open(self.banner.path)
            if img.height > 400 or img.width > 1200:
                img.thumbnail((1200, 400))
                img.save(self.banner.path)
    
    @property
    def track_count(self):
        """Количество треков артиста"""
        return self.track_set.filter(is_published=True).count()
    
    @property
    def album_count(self):
        """Количество релизов артиста"""
        return self.album_set.count()
    
    @property
    def latest_releases(self):
        """Последние релизы артиста"""
        return self.track_set.filter(is_published=True).order_by('-release_date')[:5]

    def get_latest_album(self):
        """Получить последний релиз - сначала проверяем выбранный вручную, потом автоматически"""
        if self.latest_album:
            return self.latest_album
        # Если нет выбранного релиза, возвращаем последний по дате релиза
        return self.album_set.all().order_by('-release_date').first()
