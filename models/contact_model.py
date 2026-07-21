"""
models/contact_model.py
------------------------
Model SQLAlchemy untuk menyimpan pesan yang dikirim
pengguna melalui halaman Contact.
"""

from datetime import datetime, timezone
from models import db


class ContactMessage(db.Model):
    """Merepresentasikan satu pesan yang dikirim lewat form Contact."""

    __tablename__ = "contact_messages"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        """Mengubah objek menjadi dictionary, berguna untuk response JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "subject": self.subject,
            "message": self.message,
            "created_at": self.created_at.isoformat(),
        }
