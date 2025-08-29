from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import json
import base64
import uuid
import os
from .models import Artist
from music.models import Album, Track

# Web Views
def home_view(request):
    """Главная страница"""
    return render(request, 'index.html')

def admin_view(request):
    """Страница с информацией о Django админке"""
    context = {
        'title': 'Django Админка - Carnage Music',
        'admin_url': '/django-admin/',
    }
    return render(request, 'admin_info.html', context)

def artists_list_view(request):
    """Страница списка артистов"""
    artists = Artist.objects.all()
    return render(request, 'artists.html', {'artists': artists})

def artist_detail_view(request, slug):
    """Страница детального просмотра артиста"""
    artist = get_object_or_404(Artist, slug=slug)
    
    # Используем новый метод для получения последнего релиза
    latest_album = artist.get_latest_album()
    
    # Получаем все релизы артиста для отображения
    all_releases = []
    if latest_album:
        all_releases.append(latest_album)
    
    # Также добавляем все остальные релизы артиста
    other_releases = artist.album_set.exclude(id=latest_album.id if latest_album else None).order_by('-release_date')
    all_releases.extend(other_releases)
    
    # Получаем всех артистов для навигации
    all_artists = Artist.objects.filter(is_active=True).order_by('name')
    
    # Находим предыдущего и следующего артиста
    artist_list = list(all_artists)
    current_index = next((i for i, a in enumerate(artist_list) if a.slug == slug), None)
    
    prev_artist = None
    next_artist = None
    
    if current_index is not None:
        if current_index > 0:
            prev_artist = artist_list[current_index - 1]
        if current_index < len(artist_list) - 1:
            next_artist = artist_list[current_index + 1]
    
    # Дедупликация треков для каждого релиза
    for release in all_releases:
        all_tracks = Track.objects.filter(album=release).order_by('track_number', 'id')
        seen_titles = set()
        unique_tracks = []
        for track in all_tracks:
            if track.title not in seen_titles:
                unique_tracks.append(track)
                seen_titles.add(track.title)
        release.unique_tracks = unique_tracks
    
    context = {
        'artist': artist,
        'latest_album': latest_album,
        'all_releases': all_releases,  # Добавляем все релизы
        'prev_artist': prev_artist,
        'next_artist': next_artist,
    }
    
    return render(request, 'artist_detail.html', context)

# API Views (существующие)
@require_http_methods(["GET", "POST"])
@csrf_exempt
def artists_api(request):
    """API для работы с артистами"""
    
    if request.method == 'GET':
        # Получить список всех артистов
        artists = Artist.objects.all()
        artists_data = []
        
        for artist in artists:
            artist_data = {
                'id': artist.id,
                'name': artist.name,
                'slogan': artist.slogan if artist.slogan else artist.bio[:100] if artist.bio else '',
                'avatar': artist.photo.url if artist.photo else '',
                'social_links': {
                    'facebook': artist.facebook_url,
                    'instagram': artist.instagram_url,
                    'twitter': artist.twitter_url,
                    'tiktok': artist.tiktok_url,
                    'soundcloud': artist.soundcloud_url,
                    'spotify': artist.spotify_url,
                    'youtube': artist.youtube_url,
                    'beatport': artist.beatport_url,
                    'bandcamp': artist.bandcamp_url,
                },
                'tracks': [],  # TODO: добавить треки если нужно
                'featured': artist.is_featured,
                'date_added': artist.created_at.isoformat()
            }
            artists_data.append(artist_data)
        
        return JsonResponse({'artists': artists_data})
    
    elif request.method == 'POST':
        # Создать нового артиста
        try:
            # Проверяем размер запроса
            content_length = request.META.get('CONTENT_LENGTH')
            if content_length:
                content_length = int(content_length)
                max_size = 4 * 1024 * 1024 * 1024  # 4 ГБ
                if content_length > max_size:
                    return JsonResponse({
                        'success': False,
                        'error': f'Размер данных слишком велик: {content_length / (1024*1024):.1f} МБ. Максимум: {max_size / (1024*1024*1024)} ГБ'
                    }, status=413)
            
            # Логируем входящие данные
            print(f"Request size: {content_length} bytes" if content_length else "No content length")
            print(f"Content-Type: {request.content_type}")
            
            # Проверяем формат данных
            if not request.body:
                return JsonResponse({
                    'success': False,
                    'error': 'Пустой запрос'
                }, status=400)
            
            try:
                data = json.loads(request.body)
                print(f"Data parsed successfully, keys: {list(data.keys())}")
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                return JsonResponse({
                    'success': False,
                    'error': f'Некорректный JSON: {str(e)}'
                }, status=400)
            except MemoryError:
                return JsonResponse({
                    'success': False,
                    'error': 'Недостаточно памяти для обработки запроса. Попробуйте уменьшить размер файлов.'
                }, status=413)
            
            # Проверяем обязательные поля
            name = data.get('name', '').strip()
            if not name:
                return JsonResponse({
                    'success': False,
                    'error': 'Поле "name" обязательно для заполнения'
                }, status=400)
            
            # Автоматически создаем slug из имени
            slug = slugify(name)
            if not slug:
                slug = f'artist-{Artist.objects.count() + 1}'
            
            # Проверяем уникальность имени
            if Artist.objects.filter(name__iexact=name).exists():
                return JsonResponse({
                    'success': False,
                    'error': f'Артист с именем "{name}" уже существует'
                }, status=400)
            
            # Создаем базовый объект артиста
            artist_data = {
                'name': name,
                'slug': slug,
                'slogan': data.get('slogan', ''),
                'bio': data.get('description', ''),
                'facebook_url': data.get('social_links', {}).get('facebook', ''),
                'instagram_url': data.get('social_links', {}).get('instagram', ''),
                'twitter_url': data.get('social_links', {}).get('twitter', ''),
                'tiktok_url': data.get('social_links', {}).get('tiktok', ''),
                'soundcloud_url': data.get('social_links', {}).get('soundcloud', ''),
                'spotify_url': data.get('social_links', {}).get('spotify', ''),
                'youtube_url': data.get('social_links', {}).get('youtube', ''),
                'beatport_url': data.get('social_links', {}).get('beatport', ''),
                'bandcamp_url': data.get('social_links', {}).get('bandcamp', ''),
                'is_featured': data.get('featured', False)
            }
            
            print(f"Creating artist with basic data")
            
            # Создаем артиста сначала без аватара
            artist = Artist.objects.create(**artist_data)
            print(f"Artist created with ID: {artist.id}")
            
            # Обрабатываем avatar/photo отдельно для экономии памяти
            avatar_url = data.get('avatar', '')
            if avatar_url and avatar_url.startswith('data:'):
                try:
                    print("Processing base64 avatar...")
                    # Извлекаем base64 данные
                    header, base64_data = avatar_url.split(',', 1)
                    
                    # Определяем расширение файла
                    if 'jpeg' in header or 'jpg' in header:
                        ext = 'jpg'
                    elif 'png' in header:
                        ext = 'png'
                    elif 'gif' in header:
                        ext = 'gif'
                    else:
                        ext = 'jpg'  # По умолчанию
                    
                    # Генерируем уникальное имя файла
                    filename = f"artist_{artist.id}_{uuid.uuid4().hex[:8]}.{ext}"
                    
                    # Декодируем и сохраняем файл
                    file_data = base64.b64decode(base64_data)
                    file_path = f"artists/{filename}"
                    
                    # Сохраняем файл
                    saved_path = default_storage.save(file_path, ContentFile(file_data))
                    artist.photo = saved_path
                    artist.save()
                    
                    print(f"Avatar saved successfully: {saved_path}")
                    
                except Exception as e:
                    print(f"Error processing avatar: {e}")
                    # Не прерываем создание артиста из-за ошибки с аватаром
            
            return JsonResponse({
                'success': True,
                'artist_id': artist.id,
                'message': 'Артист успешно создан'
            })
            
        except MemoryError:
            return JsonResponse({
                'success': False,
                'error': 'Недостаточно памяти для обработки запроса. Попробуйте уменьшить размер файлов.'
            }, status=413)
        except Exception as e:
            print(f"Unexpected error: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({
                'success': False,
                'error': f'Внутренняя ошибка сервера: {str(e)}'
            }, status=500)

@require_http_methods(["GET", "PUT", "DELETE"])
@csrf_exempt
def artist_detail_api(request, artist_id):
    """API для работы с конкретным артистом"""
    
    artist = get_object_or_404(Artist, id=artist_id)
    
    if request.method == 'GET':
        artist_data = {
            'id': artist.id,
            'name': artist.name,
            'slogan': artist.slogan if artist.slogan else artist.bio[:100] if artist.bio else '',
            'avatar': artist.photo.url if artist.photo else '',
            'social_links': {
                'facebook': artist.facebook_url,
                'instagram': artist.instagram_url,
                'twitter': artist.twitter_url,
                'tiktok': artist.tiktok_url,
                'soundcloud': artist.soundcloud_url,
                'spotify': artist.spotify_url,
                'youtube': artist.youtube_url,
                'beatport': artist.beatport_url,
                'bandcamp': artist.bandcamp_url,
            },
            'featured': artist.is_featured,
            'date_added': artist.created_at.isoformat()
        }
        return JsonResponse(artist_data)
    
    elif request.method == 'PUT':
        # Обновить артиста
        try:
            data = json.loads(request.body)
            
            artist.name = data.get('name', artist.name)
            artist.slogan = data.get('slogan', artist.slogan)
            artist.bio = data.get('description', artist.bio)
            
            # Обновляем slug если изменилось имя
            if 'name' in data:
                artist.slug = slugify(data['name'])
            
            social_links = data.get('social_links', {})
            artist.facebook_url = social_links.get('facebook', artist.facebook_url)
            artist.instagram_url = social_links.get('instagram', artist.instagram_url)
            artist.twitter_url = social_links.get('twitter', artist.twitter_url)
            artist.tiktok_url = social_links.get('tiktok', artist.tiktok_url)
            artist.soundcloud_url = social_links.get('soundcloud', artist.soundcloud_url)
            artist.spotify_url = social_links.get('spotify', artist.spotify_url)
            artist.youtube_url = social_links.get('youtube', artist.youtube_url)
            artist.beatport_url = social_links.get('beatport', artist.beatport_url)
            artist.bandcamp_url = social_links.get('bandcamp', artist.bandcamp_url)
            
            artist.is_featured = data.get('featured', artist.is_featured)
            artist.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Артист успешно обновлен'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)
    
    elif request.method == 'DELETE':
        # Удалить артиста
        try:
            artist.delete()
            return JsonResponse({
                'success': True,
                'message': 'Артист успешно удален'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=400)

@require_http_methods(["GET"])
@csrf_exempt
def album_info_api(request, album_id):
    """API для получения информации о релизе и его треках"""
    
    try:
        album = get_object_or_404(Album, id=album_id)
        
        # Получаем треки релиза
        tracks = album.tracks.all().order_by('track_number')
        tracks_data = []
        
        for track in tracks:
            track_data = {
                'id': track.id,
                'title': track.title,
                'track_number': track.track_number,
                'genres': track.genres,
                'duration': str(track.duration) if track.duration else None,
                'bpm': track.bpm,
                'key': track.key,
                'is_published': track.is_published
            }
            tracks_data.append(track_data)
        
        # Формируем данные о релизе
        album_data = {
            'id': album.id,
            'title': album.title,
            'release_date': album.release_date.strftime('%Y-%m-%d') if album.release_date else None,
            'description': album.description,
            'catalog_number': album.catalog_number,
            'cover_url': album.cover.url if album.cover else None,
            'tracks': tracks_data,
            'track_count': len(tracks_data)
        }
        
        return JsonResponse(album_data)
        
    except Exception as e:
        return JsonResponse({
            'error': f'Ошибка получения информации о релизе: {str(e)}'
        }, status=500)
