#!/bin/bash

# Скрипт деплоя на SSH сервер
# Использование: ./deploy.sh user@server.com

if [ $# -eq 0 ]; then
    echo "❌ Укажи SSH сервер: ./deploy.sh user@server.com"
    exit 1
fi

SERVER=$1
PROJECT_NAME="carnage-music"

echo "🚀 ДЕПЛОИМ НА $SERVER"

# 1. Создаем архив проекта
echo "📦 Создаем архив проекта..."
tar -czf $PROJECT_NAME.tar.gz \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.DS_Store' \
    --exclude='staticfiles' \
    --exclude='db.sqlite3' \
    .

# 2. Копируем на сервер
echo "📤 Копируем на сервер..."
scp $PROJECT_NAME.tar.gz $SERVER:~/

# 3. Подключаемся и разворачиваем
echo "🔧 Разворачиваем на сервере..."
ssh $SERVER << 'EOF'
    # Создаем директорию проекта
    mkdir -p ~/$PROJECT_NAME
    cd ~/$PROJECT_NAME
    
    # Распаковываем архив
    tar -xzf ~/$PROJECT_NAME.tar.gz
    
    # Устанавливаем Docker если нет
    if ! command -v docker &> /dev/null; then
        echo "🐳 Устанавливаем Docker..."
        curl -fsSL https://get.docker.com -o get-docker.sh
        sh get-docker.sh
        sudo usermod -aG docker $USER
    fi
    
    # Устанавливаем Docker Compose если нет
    if ! command -v docker-compose &> /dev/null; then
        echo "📦 Устанавливаем Docker Compose..."
        sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
        sudo chmod +x /usr/local/bin/docker-compose
    fi
    
    # Останавливаем старые контейнеры
    docker-compose down || true
    
    # Собираем и запускаем
    docker-compose up --build -d
    
    # Очищаем
    rm ~/$PROJECT_NAME.tar.gz
    
    echo "✅ Деплой завершен!"
    echo "🌐 Сайт доступен по адресу: http://$(hostname -I | awk '{print $1}')"
EOF

# 4. Очищаем локально
rm $PROJECT_NAME.tar.gz

echo "�� ДЕПЛОЙ ЗАВЕРШЕН!"

