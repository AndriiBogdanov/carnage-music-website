# 🚀 БЫСТРЫЙ ДЕПЛОЙ НА PYTHONANYWHERE (512 МБ)

## 📋 **ЧТО НУЖНО СДЕЛАТЬ:**

### 1. **Регистрация на PythonAnywhere**
- Зайдите на [www.pythonanywhere.com](https://www.pythonanywhere.com)
- Создайте бесплатный аккаунт

### 2. **Очистка пространства (ВАЖНО!)**
```bash
# Удалите ненужные файлы
rm -rf ~/.cache/pip
rm -rf ~/.local/lib/python*
rm -rf ~/.local/bin
rm -rf /tmp/*
```

### 3. **Клонирование репозитория**
```bash
git clone https://github.com/AndriiBogdanov/carnage-music-website.git
cd carnage-music-website
```

### 4. **Создание виртуального окружения**
```bash
mkvirtualenv --python=/usr/bin/python3.11 carnage-music
```

### 5. **Установка минимальных зависимостей**
```bash
# Создайте временную директорию
mkdir -p /tmp/pip_temp
export TMPDIR=/tmp/pip_temp

# Установите минимальные зависимости
pip install Django==5.2.4
pip install gunicorn==21.2.0
pip install whitenoise==6.6.0
pip install python-decouple==3.8
pip install pillow==11.0.0
pip install djangorestframework==3.16.1
pip install django-cors-headers==4.7.0
```

### 6. **Настройка базы данных**
```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 7. **Создание суперпользователя**
```bash
python manage.py createsuperuser
# Логин: carnage_admin
# Пароль: carnage2024!
```

### 8. **Настройка веб-приложения**
- Перейдите в раздел "Web"
- Создайте новое веб-приложение
- Выберите "Manual configuration"
- Python версия: 3.11
- Source code: `/home/yourusername/carnage-music-website`
- Working directory: `/home/yourusername/carnage-music-website`

### 9. **Настройка WSGI файла**
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

### 10. **Перезапуск**
- Нажмите "Reload" в разделе Web

## 🎯 **РЕЗУЛЬТАТ:**
Сайт будет доступен по адресу: `yourusername.pythonanywhere.com`

## 📱 **ФЕЙТУРЫ:**
- ✅ Полностью адаптивный дизайн
- ✅ Мобильная версия оптимизирована
- ✅ Админка для управления контентом
- ✅ Аудиоплеер для треков
- ✅ Галерея артистов и релизов

## ⚠️ **ВАЖНО:**
- Используйте только минимальные зависимости
- Очищайте кэш после установки
- Мониторьте использование диска

---
**Время деплоя: ~15-20 минут**
