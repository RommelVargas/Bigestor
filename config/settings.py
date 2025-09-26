# config/settings.py
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- CORE SETTINGS ---
# SECURITY WARNING: keep the secret key used in production secret!
# Lee la clave de la Variable de Entorno de Render. NO PEGUES LA CLAVE AQUÍ.
SECRET_KEY = os.environ.get('SECRET_KEY', default='django-insecure-tu-clave-de-respaldo')

# SECURITY WARNING: don't run with debug turned on in production!
# Si la variable 'DEBUG' existe en el entorno y es 'False', la desactiva.
DEBUG = os.environ.get('DEBUG', 'True') == 'True' 

ALLOWED_HOSTS = []

# Configuración de Hosts para Render
RENDER_EXTERNA_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNA_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNA_HOSTNAME)
# Añadir el comodín de Render y localhost
ALLOWED_HOSTS.append('.onrender.com') 
ALLOWED_HOSTS.append('127.0.0.1')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gestion', # Tu aplicación
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # CRÍTICO para servir estáticos en Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# --- DATABASE ---
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --- VALIDATION AND INTERNATIONALIZATION (STANDARD) ---
AUTH_PASSWORD_VALIDATORS = [
    # ... (Lista de validadores por defecto)
]

LANGUAGE_CODE = 'es-mx'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# --- ARCHIVOS ESTÁTICOS (SOLUCIÓN DEL ERROR EN RENDER) ---

STATIC_URL = 'static/'

# CRÍTICO: Folder donde Django recolectará todos los archivos estáticos.
# Esta línea faltaba y causaba el error 'ImproperlyConfigured'.
STATIC_ROOT = BASE_DIR / 'staticfiles' 

# Opcional: Directorios adicionales donde buscar estáticos
STATICFILES_DIRS = [
    # BASE_DIR / 'static', 
]

# CRÍTICO: Configuración de WhiteNoise para producción
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    # Usa WhiteNoise para servir los archivos estáticos con compresión y hash.
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'