# 🚀 ДЕПЛОЙ НА RENDER.COM

## 📋 **ПОШАГОВАЯ ИНСТРУКЦИЯ:**

### **1. Регистрация на Render**
- Зайдите на [render.com](https://render.com)
- Создайте аккаунт (можно через GitHub)

### **2. Создание нового Web Service**
- Нажмите "New +" → "Web Service"
- Выберите "Connect a repository"
- Подключите GitHub репозиторий: `AndriiBogdanov/carnage-music-website`

### **3. Настройка Web Service**
```
Name: carnage-music-website
Environment: Python 3
Region: Frankfurt (EU Central)
Branch: main
Root Directory: (оставьте пустым)
Build Command: pip install -r requirements.txt
Start Command: gunicorn carnage_music_project.wsgi:application
```

### **4. Переменные окружения**
Добавьте в Environment Variables:
```
PYTHON_VERSION=3.11.0
DJANGO_SETTINGS_MODULE=carnage_music_project.settings
DEBUG=False
ALLOWED_HOSTS=.onrender.com
SECRET_KEY=your-secret-key-here
```

### **5. Создание суперпользователя**
После деплоя в консоли Render выполните:
```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
# Логин: carnage_admin
# Пароль: carnage2024!
```

## 🎯 **РЕЗУЛЬТАТ:**
Сайт будет доступен по адресу: `carnage-music-website.onrender.com`

## 📱 **ПРЕИМУЩЕСТВА RENDER:**
- ✅ Автоматический деплой из GitHub
- ✅ 750 бесплатных часов/месяц
- ✅ SSL сертификат включен
- ✅ Простая настройка
- ✅ Мониторинг и логи

## ⚡ **ВРЕМЯ ДЕПЛОЯ: ~5-10 минут**

---
**Render автоматически перезапускает сайт при каждом push в GitHub!**
