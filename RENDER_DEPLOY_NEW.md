# 🚀 Деплой Carnage Music на Render (NEW)

## 📋 Что настроено:

✅ **render.yaml** - конфигурация для Render  
✅ **settings_render.py** - настройки Django для продакшена  
✅ **build.sh** - автоматические миграции и сборка  
✅ **PostgreSQL** - база данных  
✅ **HTTPS** - SSL сертификат из коробки  

## 🌐 Новый проект:

**Название**: `carnage-music-website-new`  
**URL**: `https://carnage-music-website-new.onrender.com`  
**База данных**: `carnage-music-db-new`  

## 📱 Пошаговый деплой:

### 1. Создание аккаунта на Render
- Зайти на [render.com](https://render.com)
- Зарегистрироваться через GitHub

### 2. Подключение репозитория
- Нажать "New +" → "Blueprint"
- Выбрать GitHub репозиторий: `carnage-music-website`
- Render автоматически найдет `render.yaml`

### 3. Настройка проекта
- **Name**: `carnage-music-website-new`
- **Branch**: `main`
- **Root Directory**: оставить пустым
- Нажать "Apply"

### 4. Автоматический деплой
Render автоматически:
- Создаст PostgreSQL базу данных
- Установит зависимости
- Выполнит миграции
- Соберет статические файлы
- Запустит Django приложение

## 🔧 Что происходит при деплое:

1. **Установка зависимостей**: `pip install -r requirements.txt`
2. **Миграции БД**: `python manage.py migrate`
3. **Сборка статики**: `python manage.py collectstatic --noinput`
4. **Запуск**: `gunicorn carnage_music_project.wsgi:application`

## 📊 Мониторинг:

- **Logs**: доступны в реальном времени
- **Health Check**: автоматическая проверка `/`
- **Auto-deploy**: при каждом push в `main` ветку

## 💰 Стоимость:

- **Starter план**: $7/месяц
- **PostgreSQL**: включен в план
- **SSL**: бесплатно
- **CDN**: включен

## 🎯 Результат:

Сайт будет доступен по адресу:
**https://carnage-music-website-new.onrender.com**

---

**Готово для SEO + SMM раскрутки! 🎵**
