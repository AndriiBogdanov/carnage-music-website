# Carnage Music Website

Музыкальный лейбл Carnage Music - официальный сайт.

## 🚀 Деплой на PythonAnywhere

### 1. Создайте аккаунт на PythonAnywhere
- Зайдите на [www.pythonanywhere.com](https://www.pythonanywhere.com)
- Зарегистрируйтесь (бесплатный план)

### 2. Загрузите код
- В консоли PythonAnywhere выполните:
```bash
git clone https://github.com/your-username/carnage-music-website.git
cd carnage-music-website
```

### 3. Создайте виртуальное окружение
```bash
mkvirtualenv --python=/usr/bin/python3.11 carnage-music
pip install -r requirements.txt
```

### 4. Настройте базу данных
```bash
python manage.py migrate
python manage.py collectstatic
```

### 5. Создайте суперпользователя
```bash
python manage.py createsuperuser
```

### 6. Настройте веб-приложение
- Перейдите в раздел "Web"
- Создайте новое веб-приложение
- Выберите "Manual configuration"
- Python версия: 3.11
- Source code: /home/yourusername/carnage-music-website
- Working directory: /home/yourusername/carnage-music-website

### 7. Настройте WSGI файл
Замените содержимое WSGI файла на:
```python
import os
import sys

path = '/home/yourusername/carnage-music-website'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'carnage_music_project.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 8. Перезапустите веб-приложение
- Нажмите "Reload" в разделе Web

## 📁 Структура проекта

```
carnage-music-website/
├── carnage_music_project/     # Основные настройки Django
├── artists/                   # Приложение артистов
├── music/                     # Приложение музыки
├── templates/                 # HTML шаблоны
├── static/                    # Статические файлы
├── requirements.txt           # Зависимости Python
└── manage.py                 # Django management
```

## 🎵 Функции сайта

- **Главная страница** - логотип и социальные сети
- **Артисты** - список артистов лейбла
- **Релизы** - музыкальные релизы
- **События** - предстоящие события
- **О нас** - информация о лейбле
- **Контакты** - контактная информация
- **Поддержка** - поддержка артистов

## 🔧 Технологии

- **Django 5.2.4** - веб-фреймворк
- **Python 3.11** - язык программирования
- **HTML5/CSS3** - фронтенд
- **JavaScript** - интерактивность
- **SQLite** - база данных (для разработки)

## 📱 Адаптивность

Сайт полностью адаптивен для:
- 📱 Смартфонов (iPhone, Android)
- 📱 Больших смартфонов (iPhone Pro Max)
- 📱 Планшетов
- 💻 Десктопов

## 🌐 Домен

После деплоя сайт будет доступен по адресу:
`yourusername.pythonanywhere.com` 