from django.urls import path
from . import views

# API URLs без namespace чтобы избежать конфликта
urlpatterns = [
    path('artists/', views.artists_api, name='artists_api'),
    path('artists/<int:artist_id>/', views.artist_detail_api, name='artist_detail_api'),
    path('album/<int:album_id>/info/', views.album_info_api, name='album_info_api'),
] 