#!/bin/bash

# Автоматический деплой на SSH сервер
SERVER="adminuser@217.154.120.187"
PROJECT_NAME="carnage-music"

echo "🚀 АВТОМАТИЧЕСКИЙ ДЕПЛОЙ НА СЕРВЕР!"

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
echo "🔧 Настраиваем сервер..."
ssh $SERVER << 'EOF'
    # Создаем директорию проекта
    mkdir -p ~/$PROJECT_NAME
    cd ~/$PROJECT_NAME
    
    # Распаковываем архив
    tar -xzf ~/carnage-music.tar.gz
    
    # Проверяем что файлы есть
    ls -la
    
    # Устанавливаем Docker (если нет)
    if ! command -v docker &> /dev/null; then
        echo "🐳 Устанавливаем Docker..."
        sudo apt update -y
        sudo apt install -y docker.io docker-compose
        sudo usermod -aG docker $USER
    fi
    
    # Останавливаем старые контейнеры
    docker-compose down || true
    
    # Собираем и запускаем
    echo "🏗️ Собираем и запускаем..."
    docker-compose up --build -d
    
    # Очищаем
    rm ~/carnage-music.tar.gz
    
    echo "✅ ДЕПЛОЙ ЗАВЕРШЕН!"
    echo "🌐 Сайт доступен по адресу: http://217.154.120.187"
EOF

# 4. Очищаем локально
rm $PROJECT_NAME.tar.gz

echo "🎉 АВТОМАТИЧЕСКИЙ ДЕПЛОЙ ЗАВЕРШЕН!"
echo "🌐 Сайт: http://217.154.120.187"
