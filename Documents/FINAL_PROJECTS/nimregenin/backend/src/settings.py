import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# Initialize environ
env = environ.Env()
env.read_env(BASE_DIR / ".env")

# Security
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'nimregenin',  # <-- Add this line
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # This line is important
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

WSGI_APPLICATION = 'src.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_URL = 'login'  # Default redirect for LoginRequiredMixin
LOGIN_REDIRECT_URL = '/'  # Redirect after login (to home)
LOGOUT_REDIRECT_URL = '/login/'  # Optional: Redirect after logout


# Email configuration (use your SMTP or test with console for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # For development, prints emails to console
# For production, configure SMTP settings like below:
#
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # or 'django.core.mail.backends.console.EmailBackend' for testing

EMAIL_HOST = 'smtp.gmail.com'  # Example for Gmail
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-study-email@gmail.com'  # Change this
EMAIL_HOST_PASSWORD = 'your-app-password'       # Use App Password if 2FA enabled

# Default from email
DEFAULT_FROM_EMAIL = 'NIM Regenin Study <your-study-email@gmail.com>'

# Recipients for reminders
OVERDUE_REMINDER_RECIPIENTS = [
    'coordinator1@example.com',
    'coordinator2@example.com',
    # Add real emails
]


# Site-specific reminder recipients
SITE_REMINDER_EMAILS = {
    'SITE001': ['site001_coordinator@hospital.com', 'pi_site001@hospital.com'],
    'SITE002': ['site002_monitor@university.edu'],
    'SITE003': ['coordinator@regionalclinic.org'],
    'SITE004': ['dr.smith@privatepractice.com'],
    # Add all your sites
}

# Fallback: central team if site has no email configured
CENTRAL_OVERDUE_RECIPIENTS = ['central_monitor@example.com']
