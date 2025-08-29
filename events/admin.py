from django.contrib import admin
from django.utils.html import format_html
from .models import EventType, Venue, Event, EventArtist, EventAttendance


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color', 'color_preview']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    
    def color_preview(self, obj):
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc;"></div>',
            obj.color
        )
    color_preview.short_description = 'Цвет'


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'country', 'capacity', 'event_count']
    list_filter = ['country', 'city']
    search_fields = ['name', 'address', 'city']
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'description')
        }),
        ('Адрес', {
            'fields': ('address', 'city', 'country', 'postal_code')
        }),
        ('Координаты', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',)
        }),
        ('Контакты', {
            'fields': ('website', 'phone', 'email')
        }),
        ('Дополнительно', {
            'fields': ('capacity',)
        })
    )
    
    def event_count(self, obj):
        return obj.event_set.count()
    event_count.short_description = 'События'


class EventArtistInline(admin.TabularInline):
    model = EventArtist
    extra = 0
    fields = ['artist', 'role', 'performance_order', 'performance_time', 'set_duration']
    ordering = ['performance_order']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'venue', 'start_datetime', 'status', 'is_featured', 
                   'is_published', 'attendance_count', 'poster_preview']
    list_filter = ['status', 'is_featured', 'is_published', 'event_type', 
                  'start_datetime', 'venue__city']
    search_fields = ['title', 'description', 'venue__name']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_datetime'
    inlines = [EventArtistInline]
    filter_horizontal = []
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'description', 'short_description')
        }),
        ('Событие', {
            'fields': ('event_type', 'venue', 'headliner')
        }),
        ('Даты и время', {
            'fields': ('start_datetime', 'end_datetime', 'doors_open')
        }),
        ('Медиа', {
            'fields': ('poster', 'banner')
        }),
        ('Билеты', {
            'fields': ('is_free', 'ticket_price_min', 'ticket_price_max', 
                      'ticket_url', 'age_limit'),
            'classes': ('collapse',)
        }),
        ('Социальные сети', {
            'fields': ('facebook_url', 'instagram_url'),
            'classes': ('collapse',)
        }),
        ('Настройки', {
            'fields': ('status', 'is_featured', 'is_published', 'created_by')
        }),
        ('Метаданные', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def poster_preview(self, obj):
        if obj.poster:
            return format_html(
                '<img src="{}" style="width: 50px; height: 70px; object-fit: cover;">',
                obj.poster.url
            )
        return "Нет постера"
    poster_preview.short_description = 'Постер'
    
    def attendance_count(self, obj):
        return obj.eventattendance_set.filter(status='going').count()
    attendance_count.short_description = 'Идут'


@admin.register(EventArtist)
class EventArtistAdmin(admin.ModelAdmin):
    list_display = ['event', 'artist', 'role', 'performance_order', 'performance_time']
    list_filter = ['role', 'event__start_datetime']
    search_fields = ['event__title', 'artist__name']
    ordering = ['event__start_datetime', 'performance_order']


@admin.register(EventAttendance)
class EventAttendanceAdmin(admin.ModelAdmin):
    list_display = ['event', 'user', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'event__start_datetime']
    search_fields = ['event__title', 'user__username']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
