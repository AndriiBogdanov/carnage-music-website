#!/bin/bash

# Скрипт для сжатия резервной копии сайта carnagemusic.com
# Дата: 8 августа 2025

echo "🚀 Создание архива резервной копии carnagemusic.com..."

# Переменные
BACKUP_DIR="carnage_website_backup_full"
ARCHIVE_NAME="carnage_website_backup_$(date +%Y%m%d_%H%M%S).tar.gz"

# Проверяем существование папки с резервной копией
if [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ Ошибка: Папка $BACKUP_DIR не найдена!"
    exit 1
fi

echo "📁 Папка резервной копии найдена: $BACKUP_DIR"

# Показываем статистику
echo "📊 Статистика резервной копии:"
echo "   Размер: $(du -sh $BACKUP_DIR | cut -f1)"
echo "   Файлов: $(find $BACKUP_DIR -type f | wc -l | tr -d ' ')"

# Создаем архив
echo "🗜️  Создание сжатого архива..."
tar -czf "$ARCHIVE_NAME" "$BACKUP_DIR"

if [ $? -eq 0 ]; then
    echo "✅ Архив успешно создан: $ARCHIVE_NAME"
    echo "📁 Размер архива: $(du -sh $ARCHIVE_NAME | cut -f1)"
    
    # Проверяем целостность архива
    echo "🔍 Проверка целостности архива..."
    tar -tzf "$ARCHIVE_NAME" > /dev/null
    
    if [ $? -eq 0 ]; then
        echo "✅ Архив прошел проверку целостности"
        echo ""
        echo "🎉 Резервное копирование завершено успешно!"
        echo "📦 Файл архива: $ARCHIVE_NAME"
    else
        echo "❌ Ошибка: Архив поврежден!"
        exit 1
    fi
else
    echo "❌ Ошибка при создании архива!"
    exit 1
fi 