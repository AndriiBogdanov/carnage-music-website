document.addEventListener('DOMContentLoaded', function() {
    const albumSelect = document.getElementById('id_latest_album');
    const albumInfoContainer = document.querySelector('.field-album_info');
    
    if (albumSelect && albumInfoContainer) {
        // Функция для загрузки информации о релизе
        function loadAlbumInfo(albumId) {
            if (!albumId) {
                albumInfoContainer.innerHTML = '<p>Выберите релиз для отображения информации</p>';
                return;
            }
            
            // Показываем индикатор загрузки
            albumInfoContainer.innerHTML = '<p>Загрузка информации о релизе...</p>';
            
            // Здесь можно добавить AJAX запрос для получения данных о релизе
            // Пока что показываем статическую информацию
            fetch(`/admin/api/album/${albumId}/info/`)
                .then(response => response.json())
                .then(data => {
                    displayAlbumInfo(data);
                })
                .catch(error => {
                    console.error('Ошибка загрузки информации о релизе:', error);
                    displayAlbumInfo({
                        title: 'Ошибка загрузки',
                        tracks: []
                    });
                });
        }
        
        // Функция для отображения информации о релизе
        function displayAlbumInfo(data) {
            let html = `
                <div style="background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0;">
                    <h4 style="margin: 0 0 10px 0; color: #333;">📀 Информация о релизе</h4>
                    <p><strong>Название:</strong> ${data.title || 'Не указано'}</p>
                    <p><strong>Дата релиза:</strong> ${data.release_date || 'Не указано'}</p>
                    <p><strong>Описание:</strong> ${data.description || 'Не указано'}</p>
                    <p><strong>Каталожный номер:</strong> ${data.catalog_number || 'Не указано'}</p>
                    
                    <h5 style="margin: 15px 0 10px 0; color: #666;">🎵 Треки (${data.tracks ? data.tracks.length : 0})</h5>
            `;
            
            if (data.tracks && data.tracks.length > 0) {
                html += '<ul style="margin: 0; padding-left: 20px;">';
                data.tracks.forEach(track => {
                    html += `
                        <li style="margin: 5px 0;">
                            <strong>${track.track_number || '?'}. ${track.title}</strong>
                            ${track.genres ? `<br><small>Жанры: ${track.genres}</small>` : ''}
                            ${track.duration ? `<br><small>Длительность: ${track.duration}</small>` : ''}
                            ${track.bpm ? `<br><small>BPM: ${track.bpm}</small>` : ''}
                        </li>
                    `;
                });
                html += '</ul>';
            } else {
                html += '<p style="color: #999; font-style: italic;">Треки не добавлены</p>';
            }
            
            html += '</div>';
            albumInfoContainer.innerHTML = html;
        }
        
        // Обработчик изменения выбора релиза
        albumSelect.addEventListener('change', function() {
            loadAlbumInfo(this.value);
        });
        
        // Загружаем информацию при загрузке страницы, если релиз уже выбран
        if (albumSelect.value) {
            loadAlbumInfo(albumSelect.value);
        }
    }
    
    // Добавляем стили для улучшения внешнего вида
    const style = document.createElement('style');
    style.textContent = `
        .field-album_info {
            background: #fff;
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            margin: 10px 0;
        }
        
        .field-album_info h4 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 5px;
        }
        
        .field-album_info ul li {
            background: #ecf0f1;
            padding: 8px;
            border-radius: 3px;
            margin: 5px 0;
        }
    `;
    document.head.appendChild(style);
}); 