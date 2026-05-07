# Configurações adicionais para produção no PythonAnywhere
# Adicione ao settings.py: from .settings_prod import * (apenas em produção)

import os
from pathlib import Path

# ====== SEGURANÇA ======
DEBUG = False
ALLOWED_HOSTS = [
    os.getenv('PYTHONANYWHERE_USER', 'seu-usuario') + '.pythonanywhere.com',
    'localhost',
    '127.0.0.1',
]

# Use variáveis de ambiente em produção
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-me')

# ====== SSL ======
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ====== HEADERS ======
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# ====== BANCO DE DADOS ======
# Descomente para usar PostgreSQL
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('DB_NAME'),
#         'USER': os.getenv('DB_USER'),
#         'PASSWORD': os.getenv('DB_PASSWORD'),
#         'HOST': os.getenv('DB_HOST'),
#         'PORT': os.getenv('DB_PORT', '5432'),
#     }
# }

# ====== LOGGING ======
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/tmp/django_errors.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# ====== EMAIL ======
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# ====== CACHE ======
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
