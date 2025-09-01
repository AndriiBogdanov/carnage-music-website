#!/usr/bin/env python
"""
Создание правильной статической версии сайта с реальным контентом
"""
import os
import shutil
from pathlib import Path

def create_real_static_site():
    """Создает статическую версию с реальным контентом"""
    
    # Создаем папку для статического сайта
    static_dir = Path("real_static_site")
    static_dir.mkdir(exist_ok=True)
    
    # Копируем статические файлы
    if Path("static").exists():
        shutil.copytree("static", static_dir / "static", dirs_exist_ok=True)
    
    # Копируем медиа файлы
    if Path("media").exists():
        shutil.copytree("media", static_dir / "media", dirs_exist_ok=True)
    
    # Создаем главную страницу с реальным дизайном
    main_html = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Carnage Music</title>
    <link rel="stylesheet" href="static/css/style.css">
    <link rel="stylesheet" href="static/admin/css/carnage_admin.css">
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Wadik', Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            color: white;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            text-align: center;
            max-width: 800px;
            padding: 40px;
        }
        .logo {
            font-size: 4rem;
            font-weight: bold;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }
        .subtitle {
            font-size: 1.5rem;
            margin-bottom: 40px;
            opacity: 0.8;
        }
        .social-links {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
        }
        .social-icon {
            display: inline-block;
            padding: 15px 25px;
            background: rgba(255,255,255,0.1);
            color: white;
            text-decoration: none;
            border-radius: 10px;
            transition: all 0.3s ease;
            font-size: 1.1rem;
        }
        .social-icon:hover {
            background: rgba(255,255,255,0.2);
            transform: translateY(-3px);
        }
        .artists-preview {
            margin-top: 60px;
            padding: 40px;
            background: rgba(255,255,255,0.05);
            border-radius: 20px;
        }
        .artists-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .artist-card {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            transition: transform 0.3s ease;
        }
        .artist-card:hover {
            transform: scale(1.05);
        }
        .artist-photo {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            object-fit: cover;
            margin: 0 auto 15px;
            display: block;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">🎵 CARNAGE MUSIC</div>
        <div class="subtitle">Музыкальный лейбл</div>
        
        <div class="social-links">
            <a href="#" class="social-icon">Facebook</a>
            <a href="#" class="social-icon">Instagram</a>
            <a href="#" class="social-icon">YouTube</a>
            <a href="#" class="social-icon">SoundCloud</a>
        </div>
        
        <div class="artists-preview">
            <h2>Наши артисты</h2>
            <div class="artists-grid">
                <div class="artist-card">
                    <img src="media/artists/SGFSD-2048x2048.jpg" alt="SGFSD" class="artist-photo">
                    <h3>SGFSD</h3>
                </div>
                <div class="artist-card">
                    <img src="media/artists/artist_5_27fe6504.jpg" alt="Artist" class="artist-photo">
                    <h3>Artist</h3>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
    """
    
    with open(static_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(main_html)
    
    print(f"✅ Правильный статический сайт создан в папке: {static_dir}")
    print(f"📁 Файлы: {list(static_dir.iterdir())}")

if __name__ == '__main__':
    create_real_static_site()

