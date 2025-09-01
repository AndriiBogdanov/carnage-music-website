#!/usr/bin/env python
"""
Создание статической версии сайта для GitHub Pages
"""
import os
import shutil
from pathlib import Path

def create_static_site():
    """Создает статическую версию сайта"""
    
    # Создаем папку для статического сайта
    static_dir = Path("static_site")
    static_dir.mkdir(exist_ok=True)
    
    # Копируем статические файлы
    if Path("static").exists():
        shutil.copytree("static", static_dir / "static", dirs_exist_ok=True)
    
    # Копируем медиа файлы
    if Path("media").exists():
        shutil.copytree("media", static_dir / "media", dirs_exist_ok=True)
    
    # Создаем главную страницу
    main_html = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Carnage Music</title>
    <link rel="stylesheet" href="static/css/style.css">
</head>
<body>
    <div class="container">
        <h1>🎵 Carnage Music</h1>
        <p>Музыкальный лейбл</p>
        <div class="social-links">
            <a href="#" class="social-icon">Facebook</a>
            <a href="#" class="social-icon">Instagram</a>
            <a href="#" class="social-icon">YouTube</a>
        </div>
    </div>
</body>
</html>
    """
    
    with open(static_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(main_html)
    
    print(f"✅ Статический сайт создан в папке: {static_dir}")
    print(f"📁 Файлы: {list(static_dir.iterdir())}")

if __name__ == '__main__':
    create_static_site()

