from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class EventType(models.Model):
    """Модель типа события"""
    name = models.CharField(max_length=100, unique=True, verbose_name="Название")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    color = models.CharField(max_length=7, default="#000000", verbose_name="Цвет")
    
    class Meta:
        verbose_name = "Тип события"
        verbose_name_plural = "Типы событий"
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Venue(models.Model):
    """Модель места проведения"""
    name = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    # Адрес
    address = models.CharField(max_length=300, verbose_name="Адрес")
    city = models.CharField(max_length=100, verbose_name="Город")
    country = models.CharField(max_length=100, verbose_name="Страна")
    postal_code = models.CharField(max_length=20, blank=True, verbose_name="Почтовый индекс")
    
    # Координаты
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Широта")
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True, verbose_name="Долгота")
    
    # Контакты
    website = models.URLField(blank=True, verbose_name="Веб-сайт")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    email = models.EmailField(blank=True, verbose_name="Email")
    
    # Вместимость
    capacity = models.PositiveIntegerField(blank=True, null=True, verbose_name="Вместимость")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Место проведения"
        verbose_name_plural = "Места проведения"
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name}, {self.city}"
    
    def get_absolute_url(self):
        return reverse('events:venue_detail', kwargs={'slug': self.slug})


class Event(models.Model):
    """Модель события"""
    
    STATUS_CHOICES = [
        ('upcoming', 'Предстоящее'),
        ('ongoing', 'Происходит сейчас'),
        ('completed', 'Завершено'),
        ('cancelled', 'Отменено'),
        ('postponed', 'Перенесено'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")
    description = models.TextField(verbose_name="Описание")
    short_description = models.CharField(max_length=300, blank=True, verbose_name="Краткое описание")
    
    # Основная информация
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, verbose_name="Тип события")
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE, verbose_name="Место проведения")
    
    # Даты и время
    start_datetime = models.DateTimeField(verbose_name="Дата и время начала")
    end_datetime = models.DateTimeField(blank=True, null=True, verbose_name="Дата и время окончания")
    doors_open = models.TimeField(blank=True, null=True, verbose_name="Время открытия дверей")
    
    # Участники
    artists = models.ManyToManyField('artists.Artist', through='EventArtist', verbose_name="Артисты")
    headliner = models.ForeignKey('artists.Artist', on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='headlined_events', verbose_name="Хедлайнер")
    
    # Медиа
    poster = models.ImageField(upload_to='events/', blank=True, null=True, verbose_name="Постер")
    banner = models.ImageField(upload_to='events/banners/', blank=True, null=True, verbose_name="Баннер")
    
    # Билеты и цены
    ticket_price_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                          verbose_name="Минимальная цена билета")
    ticket_price_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True,
                                          verbose_name="Максимальная цена билета")
    ticket_url = models.URLField(blank=True, verbose_name="Ссылка на билеты")
    is_free = models.BooleanField(default=False, verbose_name="Бесплатное")
    
    # Возрастные ограничения
    age_limit = models.PositiveIntegerField(blank=True, null=True, verbose_name="Возрастное ограничение")
    
    # Статус и настройки
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming', verbose_name="Статус")
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемое")
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    
    # Социальные сети
    facebook_url = models.URLField(blank=True, verbose_name="Facebook Event")
    instagram_url = models.URLField(blank=True, verbose_name="Instagram")
    
    # Метаданные
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Создатель")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"
        ordering = ['-start_datetime']
    
    def __str__(self):
        return f"{self.title} - {self.start_datetime.strftime('%d.%m.%Y')}"
    
    def get_absolute_url(self):
        return reverse('events:event_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Оптимизация постера
        if self.poster:
            img = Image.open(self.poster.path)
            if img.height > 800 or img.width > 600:
                img.thumbnail((600, 800))
                img.save(self.poster.path)
        
        # Оптимизация баннера
        if self.banner:
            img = Image.open(self.banner.path)
            if img.height > 400 or img.width > 1200:
                img.thumbnail((1200, 400))
                img.save(self.banner.path)
    
    @property
    def is_upcoming(self):
        """Проверяет, предстоящее ли событие"""
        from django.utils import timezone
        return self.start_datetime > timezone.now()
    
    @property
    def is_today(self):
        """Проверяет, происходит ли событие сегодня"""
        from django.utils import timezone
        today = timezone.now().date()
        return self.start_datetime.date() == today
    
    @property
    def duration_hours(self):
        """Длительность события в часах"""
        if self.end_datetime:
            duration = self.end_datetime - self.start_datetime
            return duration.total_seconds() / 3600
        return None


class EventArtist(models.Model):
    """Промежуточная модель для артистов события"""
    
    ROLE_CHOICES = [
        ('headliner', 'Хедлайнер'),
        ('support', 'Саппорт'),
        ('opener', 'Открывающий'),
        ('special_guest', 'Специальный гость'),
        ('dj_set', 'DJ Set'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    artist = models.ForeignKey('artists.Artist', on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='support', verbose_name="Роль")
    performance_order = models.PositiveIntegerField(default=1, verbose_name="Порядок выступления")
    performance_time = models.TimeField(blank=True, null=True, verbose_name="Время выступления")
    set_duration = models.DurationField(blank=True, null=True, verbose_name="Длительность сета")
    
    class Meta:
        verbose_name = "Артист события"
        verbose_name_plural = "Артисты событий"
        ordering = ['performance_order']
        unique_together = ['event', 'artist']
    
    def __str__(self):
        return f"{self.event.title} - {self.artist.name} ({self.role})"


class EventAttendance(models.Model):
    """Модель посещения события"""
    
    STATUS_CHOICES = [
        ('going', 'Пойду'),
        ('maybe', 'Возможно'),
        ('not_going', 'Не пойду'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, verbose_name="Событие")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Посещение события"
        verbose_name_plural = "Посещения событий"
        unique_together = ['user', 'event']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title} ({self.status})"
