"""
config.py
---------
Berisi konfigurasi terpusat untuk aplikasi Flask.
Menggunakan pola class-based config agar mudah dikembangkan
(Development, Production, Testing) dan mudah di-deploy ke Railway.

Environment variable yang didukung:
- SECRET_KEY      : kunci rahasia Flask (session, CSRF, dsb)
- DATABASE_URL    : lokasi database SQLite (opsional, default file lokal)
- PORT            : port yang digunakan Railway saat runtime
"""

import os
from pathlib import Path

# Direktori root proyek, dipakai untuk menentukan path database SQLite
BASE_DIR = Path(__file__).resolve().parent


class BaseConfig:
    """Konfigurasi dasar yang dipakai oleh semua environment."""

    # Kunci rahasia Flask, wajib diganti lewat environment variable saat produksi
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-ganti-saat-produksi")

    # Konfigurasi SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Lokasi database SQLite default, disimpan di folder instance/
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'instance' / 'app.db'}"
    )

    # Nama aplikasi, ditampilkan di beberapa bagian UI
    APP_NAME = "PDA HTML Validator"
    APP_AUTHOR = "Capstone Project - Teori Bahasa dan Otomata"


class DevelopmentConfig(BaseConfig):
    """Konfigurasi untuk pengembangan lokal."""

    DEBUG = True
    ENV = "development"


class ProductionConfig(BaseConfig):
    """Konfigurasi untuk produksi (Railway)."""

    DEBUG = False
    ENV = "production"


class TestingConfig(BaseConfig):
    """Konfigurasi untuk automated testing."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


# Mapping nama string ke class config, dipakai di app.py
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config():
    """Mengambil class config sesuai environment variable FLASK_ENV."""
    env_name = os.environ.get("FLASK_ENV", "production")
    return config_by_name.get(env_name, ProductionConfig)
