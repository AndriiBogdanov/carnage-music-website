# 🚀 БЫСТРЫЙ ДЕПЛОЙ НА PYTHONANYWHERE

## 📋 **ЧТО НУЖНО СДЕЛАТЬ:**

### 1. **Регистрация на PythonAnywhere**
- Зайдите на [www.pythonanywhere.com](https://www.pythonanywhere.com)
- Создайте бесплатный аккаунт

### 2. **Клонирование репозитория**
В консоли PythonAnywhere выполните:
```bash
git clone https://github.com/AndriiBogdanov/carnage-music-website.git
cd carnage-music-website
```

### 3. **Создание виртуального окружения**
```bash
mkvirtualenv --python=/usr/bin/python3.11 carnage-music
pip install -r requirements.txt
```

### 4. **Настройка базы данных**
```bash
python manage.py migrate
python manage.py collectstatic
```

### 5. **Создание суперпользователя**
```bash
python manage.py createsuperuser
# Логин: carnage_admin
# Пароль: carnage2024!
```

### 6. **Настройка веб-приложения**
- Перейдите в раздел "Web"
- Создайте новое веб-приложение
- Выберите "Manual configuration"
- Python версия: 3.11
- Source code: `/home/yourusername/carnage-music-website`
- Working directory: `/home/yourusername/carnage-music-website`

### 7. **Настройка WSGI файла**
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

### 8. **Перезапуск**
- Нажмите "Reload" в разделе Web

## 🎯 **РЕЗУЛЬТАТ:**
Сайт будет доступен по адресу: `yourusername.pythonanywhere.com`

## 📱 **ФЕЙТУРЫ:**
- ✅ Полностью адаптивный дизайн
- ✅ Мобильная версия оптимизирована
- ✅ Админка для управления контентом
- ✅ Аудиоплеер для треков
- ✅ Галерея артистов и релизов

---
**Время деплоя: ~10-15 минут**
