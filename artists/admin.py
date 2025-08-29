from django.contrib import admin
from django.utils.html import format_html
from django import forms
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from .models import Artist
from music.models import Album, Track


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['name', 'real_name', 'country', 'city', 'is_featured', 
                   'is_active', 'selected_album', 'photo_preview']
    list_filter = ['is_featured', 'is_active', 'country', 'created_at']
    search_fields = ['name', 'real_name', 'bio']
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'real_name', 'bio', 'slogan')
        }),
        ('Медиа', {
            'fields': ('photo', 'banner')
        }),
        ('Контакты', {
            'fields': ('email', 'website'),
        }),
        ('Социальные сети', {
            'fields': ('instagram_url', 'facebook_url', 'twitter_url', 'tiktok_url',
                      'soundcloud_url', 'spotify_url', 'youtube_url', 
                      'bandcamp_url', 'beatport_url'),
            'classes': ('collapse',)
        }),
        ('География', {
            'fields': ('country', 'city')
        }),
        ('Настройки', {
            'fields': ('is_featured', 'is_active', 'user')
        }),
        ('Музыка', {
            'fields': ('latest_album',),
            'description': '🎵 Выберите любой релиз для отображения на странице артиста. Можно выбрать любой существующий релиз из списка.'
        }),
        ('Информация о релизе', {
            'fields': ('album_info',),
            'classes': ('collapse',)
        }),
        ('Статистика', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "latest_album":
            # Показываем все релизы для выбора
            if hasattr(request, '_obj_') and request._obj_:
                # Если редактируем существующего артиста, показываем все релизы
                kwargs["queryset"] = Album.objects.all().order_by('-release_date')
            else:
                # Если создаем нового артиста, показываем все релизы
                kwargs["queryset"] = Album.objects.all().order_by('-release_date')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    
    def get_form(self, request, obj=None, **kwargs):
        # Сохраняем объект в request для использования в formfield_for_foreignkey
        request._obj_ = obj
        return super().get_form(request, obj, **kwargs)
    
    def save_model(self, request, obj, form, change):
        """При сохранении артиста обновляем информацию о выбранном релизе"""
        super().save_model(request, obj, form, change)
        
        # Обновляем информацию о выбранном релизе
        if obj.latest_album:
            album = obj.latest_album
            obj.album_info = f"🎵 {album.title}\n📅 Дата релиза: {album.release_date}\n🎵 Треков: {album.tracks.count()}"
            if album.description:
                obj.album_info += f"\n📝 Описание: {album.description[:200]}..."
            obj.save(update_fields=['album_info'])
    
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;">',
                obj.photo.url
            )
        return "Нет фото"
    photo_preview.short_description = 'Фото'
    
    def selected_album(self, obj):
        """Показывает выбранный релиз артиста"""
        if obj.latest_album:
            return format_html(
                '<span style="color: #4caf50; font-weight: 500;">🎵 {}</span>',
                obj.latest_album.title
            )
        return format_html('<span style="color: #999;">—</span>')
    selected_album.short_description = 'Выбранный релиз'
    
    class Media:
        js = ('admin/js/artist_admin.js',)
