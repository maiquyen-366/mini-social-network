"""Tầng cấu hình: cài đặt Django, DRF, PostgreSQL, CORS và Channels."""

import os
from pathlib import Path
from datetime import timedelta

from django.core.exceptions import ImproperlyConfigured


BASE_DIR = Path(__file__).resolve().parent.parent


def load_local_env():
    """Đọc file .env đơn giản để project chạy được ngay sau khi copy mẫu."""
    env_path = BASE_DIR / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_local_env()


def get_bool_env(name, default=False):
    """Đọc biến môi trường kiểu boolean."""
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


def get_list_env(name, default):
    """Đọc danh sách phân tách bằng dấu phẩy và bỏ phần tử rỗng."""
    raw_value = os.getenv(name)
    if raw_value is None:
        return default
    return [item.strip() for item in raw_value.split(",") if item.strip()]


SECRET_KEY = os.getenv("SECRET_KEY", "local-only-secret-key")
DEBUG = get_bool_env("DEBUG", True)
if not DEBUG and SECRET_KEY in {"", "local-only-secret-key", "change-me-in-local"}:
    raise ImproperlyConfigured("SECRET_KEY phải được cấu hình bằng giá trị mạnh khi DEBUG=False.")

ALLOWED_HOSTS = get_list_env("ALLOWED_HOSTS", ["localhost", "127.0.0.1"])

INSTALLED_APPS = [
    "daphne",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "accounts.apps.AccountsConfig",
    "posts.apps.PostsConfig",
    "chat.apps.ChatConfig",
    "notifications.apps.NotificationsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
TEMPLATES = [{
    "BACKEND": "django.template.backends.django.DjangoTemplates",
    "DIRS": [],
    "APP_DIRS": True,
    "OPTIONS": {"context_processors": [
        "django.template.context_processors.request",
        "django.contrib.auth.context_processors.auth",
        "django.contrib.messages.context_processors.messages",
    ]},
}]
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

DB_SSLMODE = os.getenv("DB_SSLMODE", "disable" if DEBUG else "require").strip()
DATABASE_OPTIONS = {"sslmode": DB_SSLMODE} if DB_SSLMODE else {}

DATABASES = {"default": {
    "ENGINE": "django.db.backends.postgresql",
    "NAME": os.getenv("DB_NAME", "mini_social"),
    "USER": os.getenv("DB_USER", "postgres"),
    "PASSWORD": os.getenv("DB_PASSWORD", "postgres"),
    "HOST": os.getenv("DB_HOST", "127.0.0.1"),
    "PORT": os.getenv("DB_PORT", "5432"),
    "OPTIONS": DATABASE_OPTIONS,
}}

AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = "vi"
TIME_ZONE = "Asia/Ho_Chi_Minh"
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"},
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.User"

CORS_ALLOWED_ORIGINS = get_list_env("CORS_ALLOWED_ORIGINS", ["http://localhost:5173"])
CSRF_TRUSTED_ORIGINS = get_list_env("CSRF_TRUSTED_ORIGINS", ["http://localhost:5173"])

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG

CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME", "")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY", "")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET", "")

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "EXCEPTION_HANDLER": "core.exception_handler.custom_exception_handler",
    "DEFAULT_PAGINATION_CLASS": "core.pagination.SimplePagePagination",
    "PAGE_SIZE": 10,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

CHANNEL_LAYERS = {"default": {"BACKEND": "channels.layers.InMemoryChannelLayer"}}

REDIS_HOST = os.getenv("REDIS_HOST", "").strip()
REDIS_PORT = os.getenv("REDIS_PORT", "6379").strip()
REDIS_URL = os.getenv("REDIS_URL", "").strip()

if REDIS_URL or REDIS_HOST:
    try:
        import channels_redis  # noqa: F401
        redis_hosts = [REDIS_URL] if REDIS_URL else [(REDIS_HOST, int(REDIS_PORT))]
        CHANNEL_LAYERS = {
            "default": {
                "BACKEND": "channels_redis.core.RedisChannelLayer",
                "CONFIG": {"hosts": redis_hosts},
            },
        }
        redis_cache_url = REDIS_URL or f"redis://{REDIS_HOST}:{REDIS_PORT}/1"
        CACHES = {
            "default": {
                "BACKEND": "django.core.cache.backends.redis.RedisCache",
                "LOCATION": redis_cache_url,
            }
        }
    except ImportError:
        pass
