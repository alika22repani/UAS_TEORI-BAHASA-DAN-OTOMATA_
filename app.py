"""
app.py
------
Entry point utama aplikasi Flask.
Menggunakan pola "Application Factory" agar aplikasi mudah dites,
mudah dikembangkan, dan siap di-deploy ke Railway (via Procfile + gunicorn).
"""

import os
from flask import Flask, render_template

from config import get_config
from models import db


def create_app():
    """Membuat dan mengonfigurasi instance aplikasi Flask."""

    app = Flask(__name__)
    app.config.from_object(get_config())

    # Pastikan folder instance/ tersedia untuk menyimpan file SQLite
    os.makedirs(os.path.join(app.root_path, "instance"), exist_ok=True)

    # Inisialisasi database
    db.init_app(app)

    # Registrasi blueprint (routes)
    from routes.main_routes import main_bp
    from routes.pda_routes import pda_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(pda_bp)

    # Membuat tabel database jika belum ada (aman dipanggil berkali-kali)
    with app.app_context():
        db.create_all()

    # Handler untuk halaman 404 agar tetap konsisten dengan desain aplikasi
    @app.errorhandler(404)
    def not_found(_error):
        return render_template("errors/404.html"), 404

    # Handler untuk error server (500) dengan tampilan yang rapi
    @app.errorhandler(500)
    def server_error(_error):
        return render_template("errors/500.html"), 500

    return app


# Instance global yang dipakai oleh gunicorn saat production (lihat Procfile)
app = create_app()

if __name__ == "__main__":
    # Port dibaca dari environment variable untuk kompatibilitas dengan Railway
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=app.config.get("DEBUG", False))
