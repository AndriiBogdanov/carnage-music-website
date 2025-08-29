# 🚀 ДЕПЛОЙ НА VERCEL.COM

## 📋 **ПОШАГОВАЯ ИНСТРУКЦИЯ:**

### **1. Регистрация на Vercel**
- Зайдите на [vercel.com](https://vercel.com)
- Создайте аккаунт (можно через GitHub)

### **2. Подключение GitHub репозитория**
- Нажмите "New Project"
- Выберите "Import Git Repository"
- Подключите: `AndriiBogdanov/carnage-music-website`

### **3. Настройка проекта**
```
Framework Preset: Other
Root Directory: ./
Build Command: pip install -r requirements_vercel.txt
Output Directory: staticfiles
Install Command: pip install -r requirements_vercel.txt
```

### **4. Переменные окружения**
Добавьте в Environment Variables:
```
DJANGO_SETTINGS_MODULE=carnage_music_project.settings
DEBUG=False
ALLOWED_HOSTS=.vercel.app
SECRET_KEY=z=8tocloi$044d@koqiwi9!a=u77ya1-b%=$lk77$p8$vp&3)&
```

### **5. Деплой**
- Нажмите "Deploy"
- Ждите завершения сборки

## 🎯 **РЕЗУЛЬТАТ:**
Сайт будет доступен по адресу: `carnage-music-website.vercel.app`

## 📱 **ПРЕИМУЩЕСТВА VERCEL:**
- ✅ Автоматический деплой из GitHub
- ✅ Неограниченный бесплатный план
- ✅ SSL сертификат включен
- ✅ Глобальный CDN
- ✅ Простая настройка

## ⚡ **ВРЕМЯ ДЕПЛОЯ: ~3-5 минут**

---
**Vercel автоматически перезапускает сайт при каждом push в GitHub!**
