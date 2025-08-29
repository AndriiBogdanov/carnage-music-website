from django.urls import path
from . import views

app_name = 'music'

urlpatterns = [
    path('releases/', views.releases_view, name='releases'),
    path('release/<slug:slug>/', views.release_detail_view, name='release_detail'),
] 