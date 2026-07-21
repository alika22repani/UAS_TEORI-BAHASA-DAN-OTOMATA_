"""
routes/pda_routes.py
----------------------
Blueprint untuk modul inti aplikasi: validasi tag HTML menggunakan
Pushdown Automata (PDA).

Berisi:
- Halaman /validator (UI interaktif)
- API POST /api/validate (menjalankan mesin PDA dan mengembalikan JSON)
- API GET  /api/examples (daftar contoh HTML)
"""

from flask import Blueprint, render_template, request, jsonify

from models import db
from models.history_model import ValidationHistory
from utils.pda_validator import validate_html
from utils.sample_data import get_all_examples, get_example_by_id

pda_bp = Blueprint("pda", __name__, url_prefix="")


@pda_bp.route("/validator")
def validator_page():
    """Menampilkan halaman utama alat validasi PDA beserta contoh HTML."""
    examples = get_all_examples()
    return render_template("validator.html", examples=examples)


@pda_bp.route("/api/validate", methods=["POST"])
def api_validate():
    """
    Endpoint utama: menerima kode HTML dari frontend (JSON),
    menjalankan simulasi PDA, lalu mengembalikan hasilnya sebagai JSON.

    Body request yang diharapkan:
        { "html": "<div>...</div>" }
    """
    payload = request.get_json(silent=True) or {}
    html_code = payload.get("html", "")

    if not html_code.strip():
        return jsonify({"error": "Kode HTML tidak boleh kosong."}), 400

    # Batasi ukuran input agar server tidak dibebani input yang terlalu besar
    if len(html_code) > 20000:
        return jsonify({"error": "Kode HTML terlalu panjang (maksimum 20.000 karakter)."}), 400

    result = validate_html(html_code)

    # Simpan ringkasan hasil validasi ke database sebagai riwayat sederhana
    try:
        history = ValidationHistory(
            is_valid=result.is_valid,
            total_tags=result.total_tags,
            error_message=result.error,
        )
        db.session.add(history)
        db.session.commit()
    except Exception:
        # Kegagalan menyimpan riwayat tidak boleh menggagalkan proses validasi
        db.session.rollback()

    return jsonify(result.to_dict())


@pda_bp.route("/api/examples")
def api_examples():
    """Mengembalikan seluruh contoh HTML dalam format JSON."""
    return jsonify(get_all_examples())


@pda_bp.route("/api/examples/<example_id>")
def api_example_detail(example_id):
    """Mengembalikan satu contoh HTML berdasarkan id."""
    example = get_example_by_id(example_id)
    if example is None:
        return jsonify({"error": "Contoh tidak ditemukan."}), 404
    return jsonify(example)
