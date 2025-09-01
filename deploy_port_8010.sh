#!/bin/bash

# Автоматический деплой на SSH сервер на порт 8010
SERVER="adminuser@217.154.120.187"
PROJECT_NAME="carnage-music"
PORT="8010"

echo "🚀 АВТОМАТИЧЕСКИЙ ДЕПЛОЙ НА СЕРВЕР НА ПОРТ $PORT!"

# 1. Создаем архив проекта
echo "📦 Создаем архив проекта..."
tar -czf $PROJECT_NAME.tar.gz \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.DS_Store' \
    --exclude='staticfiles' \
    --exclude='db.sqlite3' \
    --exclude='*.tar.gz' \
    .

# 2. Копируем на сервер
echo "📤 Копируем на сервер..."
scp $PROJECT_NAME.tar.gz $SERVER:~/

# 3. Выполняем деплой на сервере
echo "🔧 Настраиваем сервер на порт $PORT..."
ssh $SERVER << EOF
    # Создаем директорию проекта
    mkdir -p ~/$PROJECT_NAME
    cd ~/$PROJECT_NAME
    
    # Распаковываем архив
    tar -xzf ~/carnage-music.tar.gz
    
    # Проверяем что файлы есть
    ls -la
    
    # Устанавливаем Python и зависимости
    if ! command -v python3 &> /dev/null; then
        echo "🐍 Устанавливаем Python3..."
        sudo apt update -y
        sudo apt install -y python3 python3-pip python3-venv
    fi
    
    # Создаем виртуальное окружение
    python3 -m venv venv
    source venv/bin/activate
    
    # Устанавливаем зависимости
    pip install -r requirements.txt
    
    # Останавливаем старые процессы на порту $PORT
    sudo pkill -f "manage.py runserver.*:$PORT" || true
    sudo fuser -k $PORT/tcp || true
    
    # Запускаем Django на порту $PORT
    echo "🚀 Запускаем Django на порту $PORT..."
    nohup python3 manage.py runserver 0.0.0.0:$PORT > django.log 2>&1 &
    
    # Проверяем что сервер запустился
    sleep 3
    if curl -s http://localhost:$PORT/ > /dev/null; then
        echo "✅ Сервер успешно запущен на порту $PORT!"
    else
        echo "❌ Ошибка запуска сервера"
        cat django.log
    fi
    
    # Очищаем
    rm ~/carnage-music.tar.gz
    
    echo "✅ ДЕПЛОЙ ЗАВЕРШЕН!"
    echo "🌐 Сайт доступен по адресу: http://217.154.120.187:$PORT"
EOF

# 4. Очищаем локально
rm $PROJECT_NAME.tar.gz

echo "🎉 АВТОМАТИЧЕСКИЙ ДЕПЛОЙ НА ПОРТ $PORT ЗАВЕРШЕН!"
echo "🌐 Сайт: http://217.154.120.187:$PORT"
