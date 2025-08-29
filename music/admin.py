from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Genre, Album, Track
from django import forms


class TrackInline(admin.TabularInline):
    model = Track
    extra = 3  # Показываем 3 пустые формы для добавления новых треков
    fields = ['track_number', 'title', 'audio_file', 'duration', 'bpm', 'key', 'genres', 'is_published']
    readonly_fields = ['play_count']
    
    # Кастомные заголовки для полей
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        form = formset.form
        
        # Автоматически заполняем artist из релиза
        if obj and obj.artist and 'artist' in form.base_fields:
            form.base_fields['artist'].initial = obj.artist
            form.base_fields['artist'].widget = forms.HiddenInput()
        
        # Добавляем кастомные стили для поля audio_file
        if 'audio_file' in form.base_fields:
            form.base_fields['audio_file'].widget.attrs.update({
                'style': 'border: 2px solid #ff6b35; border-radius: 4px; padding: 8px; background-color: #fff3e0;',
                'accept': 'audio/*',
                'class': 'audio-file-input'
            })
            form.base_fields['audio_file'].help_text = '🎵 Загрузите аудиофайл (MP3, WAV, OGG)'
        
        return formset
    
    class Media:
        css = {
            'all': ('admin/css/track_inline.css',)
        }
        js = ('admin/js/track_inline.js',)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'release_date', 'track_count', 'is_active', 'cover_preview']
    list_filter = ['release_date', 'artist', 'is_active']
    search_fields = ['title', 'artist__name', 'catalog_number']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'release_date'
    inlines = [TrackInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'release_date', 'catalog_number', 'is_active'),
            'description': 'Основные данные о релизе. Артист будет выбран при создании артиста.'
        }),
        ('Медиа', {
            'fields': ('cover', 'description'),
            'description': 'Обложка и описание релиза'
        }),
        ('🎵 Треки релиза', {
            'fields': (),
            'description': 'Здесь добавляются треки к релизу.',
            'classes': ('wide',)
        })
    )
    
    def get_form(self, request, obj=None, **kwargs):
        """Скрываем поле artist из формы"""
        form = super().get_form(request, obj, **kwargs)
        
        # Скрываем поле artist - оно будет заполняться через артиста
        if 'artist' in form.base_fields:
            form.base_fields['artist'].widget = forms.HiddenInput()
            form.base_fields['artist'].required = False
        
        return form
    
    def track_count(self, obj):
        return obj.tracks.count()
    track_count.short_description = 'Треков'
    
    def cover_preview(self, obj):
        if obj.cover:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 8px; object-fit: cover;">',
                obj.cover.url
            )
        return "Нет обложки"
    cover_preview.short_description = 'Обложка'
    
    # Добавляем кастомные действия для релизов
    actions = ['publish_all_tracks']
    
    def publish_all_tracks(self, request, queryset):
        """Публикует все треки в выбранных релизах"""
        total_tracks = 0
        for album in queryset:
            tracks_updated = album.tracks.update(is_published=True)
            total_tracks += tracks_updated
        self.message_user(request, f'Опубликовано {total_tracks} треков в {queryset.count()} релизах.')
    publish_all_tracks.short_description = "Опубликовать все треки в релизах"


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'album', 'track_number', 'is_published', 'streaming_links']
    list_filter = ['is_published', 'artist', 'album', 'genres']
    search_fields = ['title', 'artist__name', 'album__title']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['play_count', 'download_count']
    
    def get_form(self, request, obj=None, **kwargs):
        """Добавляем кастомные стили для полей"""
        form = super().get_form(request, obj, **kwargs)
        
        # Улучшаем поле audio_file
        if 'audio_file' in form.base_fields:
            form.base_fields['audio_file'].widget.attrs.update({
                'style': 'border: 2px solid #ff6b35; border-radius: 6px; padding: 12px; background-color: #fff3e0; font-weight: 500;',
                'accept': 'audio/*',
                'class': 'audio-file-input'
            })
            form.base_fields['audio_file'].help_text = '🎵 Загрузите аудиофайл (MP3, WAV, OGG). Максимальный размер: 50MB'
        
        # Добавляем подсказки для других полей
        if 'track_number' in form.base_fields:
            form.base_fields['track_number'].widget.attrs['placeholder'] = '1, 2, 3...'
            form.base_fields['track_number'].help_text = 'Номер трека в альбоме'
        
        if 'duration' in form.base_fields:
            form.base_fields['duration'].widget.attrs['placeholder'] = '3:45'
            form.base_fields['duration'].help_text = 'Длительность в формате MM:SS или HH:MM:SS'
        
        if 'bpm' in form.base_fields:
            form.base_fields['bpm'].widget.attrs['placeholder'] = '128'
            form.base_fields['bpm'].help_text = 'Темп в ударах в минуту'
        
        if 'key' in form.base_fields:
            form.base_fields['key'].widget.attrs['placeholder'] = 'Am, C, F#m...'
            form.base_fields['key'].help_text = 'Тональность трека'
        
        if 'genres' in form.base_fields:
            form.base_fields['genres'].widget.attrs['placeholder'] = 'Techno, Industrial, EBM'
            form.base_fields['genres'].help_text = 'Введите жанры через запятую'
        
        return form
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'artist', 'album', 'track_number')
        }),
        ('Метаданные', {
            'fields': ('duration', 'bpm', 'key', 'genres'),
            'classes': ('collapse',)
        }),
        ('🎵 Аудио файл', {
            'fields': ('audio_file', 'cover'),
            'description': 'Загрузите аудиофайл и обложку трека',
            'classes': ('wide',)
        }),
        ('🎵 Ссылки на стриминговые платформы', {
            'fields': ('spotify_url', 'apple_music_url', 'youtube_url', 'beatport_url', 'soundcloud_url', 'bandcamp_url'),
            'description': 'Добавьте ссылки на трек в различных стриминговых сервисах',
            'classes': ('wide',)
        }),
        ('Настройки', {
            'fields': ('is_published', 'is_featured', 'is_free_download', 'release_date'),
            'classes': ('collapse',)
        }),
        ('Статистика', {
            'fields': ('play_count', 'download_count'),
            'classes': ('collapse',)
        })
    )
    
    class Media:
        css = {
            'all': ('admin/css/track_inline.css',)
        }
        js = ('admin/js/track_inline.js',)
    
    def streaming_links(self, obj):
        """Показывает иконки доступных стриминговых ссылок"""
        links = []
        
        if obj.spotify_url:
            links.append('<span title="Spotify">🎵</span>')
        if obj.apple_music_url:
            links.append('<span title="Apple Music">🍎</span>')
        if obj.youtube_url:
            links.append('<span title="YouTube">📺</span>')
        if obj.beatport_url:
            links.append('<span title="Beatport">🎧</span>')
        if obj.soundcloud_url:
            links.append('<span title="SoundCloud">☁️</span>')
        if obj.bandcamp_url:
            links.append('<span title="Bandcamp">🏪</span>')
            
        return mark_safe(' '.join(links)) if links else '—'
    streaming_links.short_description = 'Платформы'
