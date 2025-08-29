# 🎵 Перенос жанров с релизов на треки

## ✅ Изменение структуры

### 🔄 Что изменилось:
- ❌ **Раньше:** Жанры выбирались на уровне релиза (Album)
- ✅ **Теперь:** Жанры выбираются для каждого трека отдельно (Track)

### 🎯 Новая логика работы:

#### 1. **Модель Album (Релиз)**:
- ✅ **Убрано поле genres** - жанры больше не на уровне релиза
- ✅ **Упрощенная структура** - только основные данные релиза
- ✅ **Фокус на треки** - релиз теперь контейнер для треков

#### 2. **Модель Track (Трек)**:
- ✅ **Добавлено поле genres** - выбор жанров для каждого трека
- ✅ **Уменьшено поле key** - с 10 до 5 символов
- ✅ **Гибкость** - каждый трек может иметь свои жанры

## 🚀 Техническая реализация

### Модель Album (music/models.py):
```python
class Album(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL")
    artist = models.ForeignKey('artists.Artist', on_delete=models.CASCADE, 
                             verbose_name="Артист", null=True, blank=True)
    cover = models.ImageField(upload_to='albums/', blank=True, null=True, verbose_name="Обложка")
    release_date = models.DateField(verbose_name="Дата релиза")
    description = models.TextField(blank=True, verbose_name="Описание")
    catalog_number = models.CharField(max_length=50, blank=True, verbose_name="Каталожный номер")
    is_featured = models.BooleanField(default=False, verbose_name="Рекомендуемый")
    # Убрано поле genres
```

### Модель Track (music/models.py):
```python
class Track(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    # ... другие поля ...
    key = models.CharField(max_length=5, blank=True, verbose_name="Тональность")  # Уменьшено
    genres = models.ManyToManyField(Genre, blank=True, verbose_name="Жанры")  # Добавлено
    # ... остальные поля ...
```

### Админка релизов (music/admin.py):
```python
fieldsets = (
    ('Основная информация', {
        'fields': ('title', 'slug', 'release_date', 'catalog_number'),
        'description': 'Основные данные о релизе. Артист будет выбран при создании артиста.'
    }),
    ('Медиа', {
        'fields': ('cover', 'description'),
        'description': 'Обложка и описание релиза'
    }),
    ('Настройки', {
        'fields': ('is_featured',),  # Убрано genres
        'description': 'Настройки отображения релиза'
    }),
    ('🎵 Треки релиза', {
        'fields': (),
        'description': 'Здесь добавляются треки к релизу. Жанры выбираются для каждого трека отдельно.',
        'classes': ('wide',)
    })
)
```

### TrackInline (music/admin.py):
```python
class TrackInline(admin.TabularInline):
    model = Track
    extra = 3
    fields = ['track_number', 'title', 'audio_file', 'duration', 'bpm', 'key', 'genres', 'is_published']
    # Добавлено поле genres
```

## 🎵 Пошаговая инструкция

### Создание релиза с треками:
1. Перейдите в **Releases** → **Добавить релиз**
2. Заполните основные данные релиза:
   - **Title:** название релиза
   - **Slug:** URL (автозаполняется)
   - **Release Date:** дата релиза
   - **Cover:** обложка
   - **Description:** описание
3. В разделе **"🎵 Треки релиза"** добавьте треки:
   - **Track Number:** номер трека
   - **Title:** название трека
   - **Audio File:** аудиофайл
   - **Duration:** длительность
   - **BPM:** темп
   - **Key:** тональность (5 символов)
   - **Genres:** выберите жанры для этого трека
   - **Is Published:** опубликовано
4. **Сохраните релиз**

## 🎯 Преимущества новой структуры

### ✅ Гибкость:
- **Разные жанры** - каждый трек может иметь свои жанры
- **Точная классификация** - более точное описание музыки
- **Гибкие релизы** - релиз может содержать треки разных жанров

### ✅ Простота:
- **Упрощенная структура** - жанры на уровне трека
- **Интуитивно понятно** - как в реальной жизни
- **Меньше путаницы** - четкое разделение

### ✅ Функциональность:
- **Точный поиск** - можно искать по жанрам треков
- **Рекомендации** - более точные рекомендации
- **Статистика** - детальная статистика по жанрам

## 🎵 Статус

**✅ ГОТОВО:** Жанры перенесены с релизов на треки
**🎵 Релизы:** Упрощенная структура без жанров
**🎶 Треки:** Выбор жанров для каждого трека
**🚀 Сервер:** Запущен на порту 8005

### Доступ к админке:
- **URL:** http://localhost:8005/django-admin/
- **Логин:** carnage
- **Пароль:** (установлен вами)

---

**Carnage Music - Underground Music Label 2025**
*Теперь жанры выбираются для каждого трека отдельно!* 🎵✨ 