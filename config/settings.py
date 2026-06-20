"""
Django settings for the Playonix project.

This file is intentionally heavily commented so it's easy to pick up
in Cursor without prior Django experience.
"""

import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from a local .env file (if present) BEFORE any
# os.environ.get(...) calls below. The .env file is git-ignored and used for
# local development only; in production (Render) the real env vars are set
# in the dashboard, so the missing .env is simply a no-op.
load_dotenv(BASE_DIR / '.env')


# ──────────────────────────────────────────────────────────────────
# SECURITY
# ──────────────────────────────────────────────────────────────────
# In production, move SECRET_KEY to an environment variable and
# never commit the real value to git. For local dev this is fine.
SECRET_KEY = os.environ.get(
    'DJANGO_SECRET_KEY',
    'django-insecure-CHANGE-ME-before-deploying-7)$jryjq$plo_eaulnfc'
)

# Set DEBUG = False before deploying live. While True, Django shows
# full error pages with code — great for development, unsafe for prod.
DEBUG = os.environ.get('DJANGO_DEBUG', 'True') == 'True'

# Add your real domain(s) here once you deploy, e.g. ['playonix.in', 'www.playonix.in']
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '*').split(',')


# ──────────────────────────────────────────────────────────────────
# APPS
# ──────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Our app — homepage, about, contact, blog, packages, catalogue, etc.
    'marketing',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise serves static files in production. Must come right after
    # SecurityMiddleware and before everything else.
    'whitenoise.middleware.WhiteNoiseMiddleware',
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
        # Project-level templates (base.html lives here, shared by all apps)
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# ──────────────────────────────────────────────────────────────────
# DATABASE
# ──────────────────────────────────────────────────────────────────
# In production we use a hosted PostgreSQL database (Neon) via the
# DATABASE_URL environment variable. Locally, when DATABASE_URL is not
# set, we fall back to SQLite so dev needs zero setup.
# Models, admin, and views stay exactly the same either way.
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            env='DATABASE_URL',
            conn_max_age=600,        # reuse connections for 10 min (Neon-friendly)
            ssl_require=True,        # Neon requires SSL
        ),
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# ──────────────────────────────────────────────────────────────────
# PASSWORD VALIDATION (for admin login)
# ──────────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ──────────────────────────────────────────────────────────────────
# INTERNATIONALIZATION
# ──────────────────────────────────────────────────────────────────
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = True


# ──────────────────────────────────────────────────────────────────
# STATIC & MEDIA FILES
# ──────────────────────────────────────────────────────────────────
# STATIC = CSS/JS/site-design images that ship with the code (logo, icons).
# MEDIA  = files uploaded later through the admin (e.g. real event photos).
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'  # used by `collectstatic` in production

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Static file storage backend.
# In production (DEBUG=False) WhiteNoise serves compressed, hashed
# (cache-busted) static files. In dev we keep Django's default so
# `runserver` works without needing to run collectstatic first.
STORAGES = {
    'default': {
        'BACKEND': 'django.core.files.storage.FileSystemStorage',
    },
    'staticfiles': {
        'BACKEND': (
            'config.storage.NonStrictManifestStaticFilesStorage'
            if not DEBUG
            else 'django.contrib.staticfiles.storage.StaticFilesStorage'
        ),
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ──────────────────────────────────────────────────────────────────
# EMAIL (for the Contact form)
# ──────────────────────────────────────────────────────────────────
# Fill these in with your real SMTP details (Gmail, Zoho Mail,
# or whatever you use for hello@playonix.in) before going live.
# Until then, EMAIL_BACKEND defaults to printing emails to the
# console so you can still test the form locally.
if os.environ.get('EMAIL_HOST_USER'):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
else:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    DEFAULT_FROM_EMAIL = 'hello@playonix.in'

# Where contact-form notifications get sent. Change this to your real inbox.
CONTACT_NOTIFICATION_EMAIL = os.environ.get('CONTACT_NOTIFICATION_EMAIL', 'hello@playonix.in')
