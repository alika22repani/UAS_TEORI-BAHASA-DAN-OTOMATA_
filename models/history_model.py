"""
models/history_model.py
------------------------
Model SQLAlchemy untuk menyimpan riwayat singkat setiap kali
pengguna melakukan validasi HTML lewat modul PDA.
Berguna untuk statistik sederhana pada halaman Documentation/About.
"""

from datetime import datetime, timezone
from models import db


class ValidationHistory(db.Model):
    """Merepresentasikan satu kali proses validasi HTML."""

    __tablename__ = "validation_history"

    id = db.Column(db.Integer, primary_key=True)
    is_valid = db.Column(db.Boolean, nullable=False)
    total_tags = db.Column(db.Integer, default=0)
    error_message = db.Column(db.String(300), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "is_valid": self.is_valid,
            "total_tags": self.total_tags,
            "error_message": self.error_message,
            "created_at": self.created_at.isoformat(),
        }
