"""
routes/main_routes.py
------------------------
Blueprint untuk halaman-halaman umum aplikasi:
Home, About, Documentation, dan Contact.
"""

from flask import Blueprint, render_template, request, flash, redirect, url_for

from models import db
from models.contact_model import ContactMessage

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    """Halaman Home: landing page yang memperkenalkan aplikasi."""
    return render_template("index.html")


@main_bp.route("/about")
def about():
    """Halaman About: penjelasan tentang capstone project dan tujuannya."""
    return render_template("about.html")


@main_bp.route("/documentation")
def documentation():
    """Halaman Documentation: penjelasan teori PDA dan cara pakai aplikasi."""
    return render_template("documentation.html")


@main_bp.route("/contact", methods=["GET", "POST"])
def contact():
    """Halaman Contact: menampilkan form dan menyimpan pesan ke database."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()

        # Validasi sederhana di sisi server
        if not name or not email or not message:
            flash("Nama, email, dan pesan wajib diisi.", "danger")
            return redirect(url_for("main.contact"))

        new_message = ContactMessage(
            name=name, email=email, subject=subject or "(Tanpa subjek)", message=message
        )
        db.session.add(new_message)
        db.session.commit()

        flash("Pesan Anda berhasil dikirim. Terima kasih!", "success")
        return redirect(url_for("main.contact"))

    return render_template("contact.html")
