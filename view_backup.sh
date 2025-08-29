#!/bin/bash

# Скрипт для просмотра резервной копии сайта carnagemusic.com
# Дата: 8 августа 2025

echo "🔍 Анализ резервной копии carnagemusic.com"
echo "=========================================="

BACKUP_DIR="carnage_website_backup_full"

if [ ! -d "$BACKUP_DIR" ]; then
    echo "❌ Папка $BACKUP_DIR не найдена!"
    exit 1
fi

echo "📊 ОБЩАЯ СТАТИСТИКА:"
echo "   📁 Общий размер: $(du -sh $BACKUP_DIR | cut -f1)"
echo "   📄 Всего файлов: $(find $BACKUP_DIR -type f | wc -l | tr -d ' ')"
echo "   📂 Всего папок: $(find $BACKUP_DIR -type d | wc -l | tr -d ' ')"
echo ""

echo "🎵 МЕДИАФАЙЛЫ:"
MEDIA_COUNT=$(find $BACKUP_DIR -name "*.mp3" -o -name "*.mp4" -o -name "*.wav" -o -name "*.ogg" -o -name "*.jpg" -o -name "*.png" -o -name "*.gif" -o -name "*.webp" -o -name "*.svg" | wc -l | tr -d ' ')
echo "   🖼️  Медиафайлов: $MEDIA_COUNT"

echo "   🎨 Изображения и анимации:"
find $BACKUP_DIR -name "*.png" -o -name "*.jpg" -o -name "*.gif" -o -name "*.webp" -o -name "*.svg" | while read file; do
    size=$(du -h "$file" | cut -f1)
    name=$(basename "$file")
    echo "      • $name ($size)"
done

echo ""
echo "✏️ ШРИФТЫ:"
find $BACKUP_DIR -name "*.ttf" -o -name "*.woff" -o -name "*.woff2" -o -name "*.eot" | while read file; do
    size=$(du -h "$file" | cut -f1)
    name=$(basename "$file")
    echo "   📝 $name ($size)"
done

echo ""
echo "🌐 ОСНОВНЫЕ СТРАНИЦЫ:"
find $BACKUP_DIR -name "index.html" | while read file; do
    dir=$(dirname "$file" | sed "s|$BACKUP_DIR/||")
    size=$(du -h "$file" | cut -f1)
    echo "   🏠 $dir ($size)"
done

echo ""
echo "🔧 WORDPRESS СТРУКТУРА:"
if [ -d "$BACKUP_DIR/carnagemusic.com/wp-content" ]; then
    echo "   ✅ wp-content/ скачан"
    echo "      📁 uploads: $(find $BACKUP_DIR/carnagemusic.com/wp-content/uploads -type f 2>/dev/null | wc -l | tr -d ' ') файлов"
    echo "      📁 themes: $(find $BACKUP_DIR/carnagemusic.com/wp-content/themes -type f 2>/dev/null | wc -l | tr -d ' ') файлов"
    echo "      📁 plugins: $(find $BACKUP_DIR/carnagemusic.com/wp-content/plugins -type f 2>/dev/null | wc -l | tr -d ' ') файлов"
else
    echo "   ❌ wp-content/ не найден"
fi

echo ""
echo "🎯 ELEMENTOR КОНТЕНТ:"
ELEMENTOR_COUNT=$(find $BACKUP_DIR -path "*/elementor/*" -type f | wc -l | tr -d ' ')
echo "   🎨 Elementor файлов: $ELEMENTOR_COUNT"

echo ""
echo "📦 АРХИВ:"
if ls carnage_website_backup_*.tar.gz 1> /dev/null 2>&1; then
    archive=$(ls carnage_website_backup_*.tar.gz | head -1)
    echo "   ✅ Создан архив: $archive"
    echo "   📁 Размер архива: $(du -sh $archive | cut -f1)"
else
    echo "   ❌ Архив не создан"
fi

echo ""
echo "✅ Анализ завершен!" 