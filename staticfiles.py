# Настройки для статических файлов в продакшене
import os
from django.conf import settings

# Настройка статических файлов
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(settings.BASE_DIR, 'staticfiles')

# Дополнительные директории для статических файлов
STATICFILES_DIRS = [
    os.path.join(settings.BASE_DIR, 'static'),
]

# Настройка для whitenoise (для продакшена)
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... остальные middleware
]

# Сжатие статических файлов
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
