// JavaScript для улучшения работы TrackInline

document.addEventListener('DOMContentLoaded', function() {
    // Функция для инициализации полей загрузки аудио
    function initializeAudioFields() {
        const audioInputs = document.querySelectorAll('input[type="file"][accept*="audio"]');
        
        audioInputs.forEach(function(input) {
            // Добавляем класс для стилизации
            input.classList.add('audio-file-input');
            
            // Добавляем обработчик изменения файла
            input.addEventListener('change', function(e) {
                const file = e.target.files[0];
                if (file) {
                    // Проверяем тип файла
                    if (!file.type.startsWith('audio/')) {
                        alert('Пожалуйста, выберите аудиофайл (MP3, WAV, OGG и т.д.)');
                        input.value = '';
                        return;
                    }
                    
                    // Проверяем размер файла (максимум 50MB)
                    const maxSize = 50 * 1024 * 1024; // 50MB в байтах
                    if (file.size > maxSize) {
                        alert('Размер файла не должен превышать 50MB');
                        input.value = '';
                        return;
                    }
                    
                    // Показываем информацию о загруженном файле
                    const fileName = file.name;
                    const fileSize = (file.size / (1024 * 1024)).toFixed(2);
                    
                    // Создаем или обновляем элемент с информацией о файле
                    let fileInfo = input.parentNode.querySelector('.file-info');
                    if (!fileInfo) {
                        fileInfo = document.createElement('div');
                        fileInfo.className = 'file-info';
                        fileInfo.style.cssText = 'margin-top: 5px; font-size: 12px; color: #4caf50; font-weight: 500;';
                        input.parentNode.appendChild(fileInfo);
                    }
                    
                    fileInfo.innerHTML = `✅ ${fileName} (${fileSize} MB)`;
                    
                    // Добавляем визуальную обратную связь
                    input.style.borderColor = '#4caf50';
                    input.style.backgroundColor = '#e8f5e8';
                }
            });
            
            // Добавляем обработчик для drag and drop
            input.addEventListener('dragover', function(e) {
                e.preventDefault();
                input.style.borderColor = '#ff6b35';
                input.style.backgroundColor = '#ffe0b2';
            });
            
            input.addEventListener('dragleave', function(e) {
                e.preventDefault();
                input.style.borderColor = '#ff6b35';
                input.style.backgroundColor = '#fff3e0';
            });
            
            input.addEventListener('drop', function(e) {
                e.preventDefault();
                const files = e.dataTransfer.files;
                if (files.length > 0) {
                    input.files = files;
                    input.dispatchEvent(new Event('change'));
                }
            });
        });
    }
    
    // Инициализируем поля при загрузке страницы
    initializeAudioFields();
    
    // Обработчик для динамически добавляемых полей
    document.addEventListener('click', function(e) {
        if (e.target && e.target.classList.contains('add-row')) {
            // Ждем немного, чтобы новые поля появились в DOM
            setTimeout(function() {
                initializeAudioFields();
            }, 100);
        }
    });
    
    // Обработчик для кнопки "Добавить ещё один Трек"
    const addRowLinks = document.querySelectorAll('.add-row a');
    addRowLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            // Добавляем небольшую задержку для инициализации новых полей
            setTimeout(function() {
                initializeAudioFields();
            }, 200);
        });
    });
    
    // Улучшенная обработка формы
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(e) {
            const audioInputs = form.querySelectorAll('input[type="file"][accept*="audio"]');
            let hasErrors = false;
            
            audioInputs.forEach(function(input) {
                if (input.files.length > 0) {
                    const file = input.files[0];
                    
                    // Проверяем тип файла
                    if (!file.type.startsWith('audio/')) {
                        alert('Один из файлов не является аудиофайлом. Пожалуйста, проверьте все загруженные файлы.');
                        hasErrors = true;
                        return;
                    }
                    
                    // Проверяем размер файла
                    const maxSize = 50 * 1024 * 1024;
                    if (file.size > maxSize) {
                        alert(`Файл "${file.name}" слишком большой. Максимальный размер: 50MB`);
                        hasErrors = true;
                        return;
                    }
                }
            });
            
            if (hasErrors) {
                e.preventDefault();
            }
        });
    }
    
    // Добавляем подсказки для полей
    const trackNumberInputs = document.querySelectorAll('input[name*="track_number"]');
    trackNumberInputs.forEach(function(input) {
        input.placeholder = '1, 2, 3...';
        input.title = 'Номер трека в альбоме';
    });
    
    const titleInputs = document.querySelectorAll('input[name*="title"]');
    titleInputs.forEach(function(input) {
        input.placeholder = 'Название трека';
        input.title = 'Введите название трека';
    });
    
    const durationInputs = document.querySelectorAll('input[name*="duration"]');
    durationInputs.forEach(function(input) {
        input.placeholder = '3:45';
        input.title = 'Длительность в формате MM:SS или HH:MM:SS';
    });
    
    const bpmInputs = document.querySelectorAll('input[name*="bpm"]');
    bpmInputs.forEach(function(input) {
        input.placeholder = '128';
        input.title = 'Темп в ударах в минуту';
    });
    
    const keyInputs = document.querySelectorAll('input[name*="key"]');
    keyInputs.forEach(function(input) {
        input.placeholder = 'Am, C, F#m...';
        input.title = 'Тональность трека';
    });
    
    const genresInputs = document.querySelectorAll('input[name*="genres"]');
    genresInputs.forEach(function(input) {
        input.placeholder = 'Techno, Industrial, EBM';
        input.title = 'Введите жанры через запятую';
    });
});

// Функция для добавления анимации загрузки
function showLoadingAnimation(input) {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'loading-animation';
    loadingDiv.innerHTML = '⏳ Загрузка...';
    loadingDiv.style.cssText = 'position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); color: #ff6b35; font-weight: 600;';
    
    input.parentNode.style.position = 'relative';
    input.parentNode.appendChild(loadingDiv);
    
    setTimeout(function() {
        if (loadingDiv.parentNode) {
            loadingDiv.parentNode.removeChild(loadingDiv);
        }
    }, 2000);
} 