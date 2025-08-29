from django.urls import path
from . import views

app_name = 'artists'

urlpatterns = [
    # Веб-страницы
    path('', views.artists_list_view, name='artists_list'),
    path('<slug:slug>/', views.artist_detail_view, name='artist_detail'),
] 