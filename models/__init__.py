"""
models/__init__.py
-------------------
Menginisialisasi instance SQLAlchemy yang dipakai bersama
oleh seluruh model di package ini, dan mengimpor model
agar dikenali saat db.create_all() dipanggil.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import model di bawah agar terdaftar ke SQLAlchemy metadata.
# Diletakkan setelah pembuatan `db` untuk menghindari circular import.
from models.contact_model import ContactMessage  # noqa: E402,F401
from models.history_model import ValidationHistory  # noqa: E402,F401
