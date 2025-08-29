from django.shortcuts import render, get_object_or_404
from .models import Album, Track

# Create your views here.

def releases_view(request):
    """Страница всех релизов"""
    # Получаем все релизы, отсортированные по дате выпуска (новые сначала)
    # Это обеспечит отображение самого нового релиза в левом верхнем углу
    releases = Album.objects.filter(is_active=True).order_by('-release_date', '-created_at')
    
    context = {
        'releases': releases,
    }
    
    return render(request, 'releases.html', context)

def release_detail_view(request, slug):
    """Страница описания релиза"""
    release = get_object_or_404(Album, slug=slug, is_active=True)
    
    # Получаем треки релиза, фильтруем по album и убираем дубликаты по title
    all_tracks = Track.objects.filter(album=release).order_by('track_number', 'id')
    
    seen_titles = set()
    tracks = []
    
    for track in all_tracks:
        if track.title not in seen_titles:
            tracks.append(track)
            seen_titles.add(track.title)
    
    context = {
        'release': release,
        'tracks': tracks,
    }
    
    return render(request, 'release_detail.html', context)
