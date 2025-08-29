"""
URL configuration for carnage_music_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.shortcuts import render

# Основные views
from artists.views import home_view, admin_view
from events.views import events_view

def support_view(request):
    """Страница поддержки"""
    return render(request, 'support.html')

def contact_view(request):
    """Страница контактов"""
    return render(request, 'contact.html')

def about_view(request):
    """Страница About"""
    return render(request, 'about.html')

urlpatterns = [
    # Django админка
    path('django-admin/', admin.site.urls),
    
    # Основные страницы
    path('', home_view, name='home'),
    path('artists/', include('artists.urls')),  # Веб-страницы с namespace
    path('music/', include('music.urls')),  # Страницы музыки
    path('events/', events_view, name='events'),  # Страница событий
    path('support/', support_view, name='support'),  # Страница поддержки
    path('contact/', contact_view, name='contact'),  # Страница контактов
    path('about/', about_view, name='about'),  # Страница About
    path('admin/', admin_view, name='admin'),
    
    # API без namespace
    path('api/', include('artists.api_urls')),
    
    # Админский API
    path('admin/api/', include('artists.api_urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Настройка админки
admin.site.site_header = "🎵 Carnage Music Administration"
admin.site.site_title = "Carnage Music Admin"
admin.site.index_title = "Добро пожаловать в админку Carnage Music"

# Кастомизация админки
admin.site.site_url = "/"  # Ссылка на главную страницу
