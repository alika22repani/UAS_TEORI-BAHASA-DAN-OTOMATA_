"""
utils/sample_data.py
----------------------
Kumpulan contoh kode HTML (valid maupun tidak valid) yang ditampilkan
pada halaman validator sebagai referensi cepat bagi pengguna.
Setiap contoh memiliki id unik agar bisa dimuat via tombol "Coba contoh ini".
"""

SAMPLE_EXAMPLES = [
    {
        "id": "valid-basic",
        "title": "Struktur Dasar Valid",
        "category": "valid",
        "description": "Dokumen HTML sederhana dengan tag yang tertutup rapi.",
        "code": (
            "<!DOCTYPE html>\n"
            "<html>\n"
            "  <head>\n"
            "    <title>Halaman Contoh</title>\n"
            "  </head>\n"
            "  <body>\n"
            "    <h1>Selamat Datang</h1>\n"
            "    <p>Ini adalah paragraf yang <strong>valid</strong>.</p>\n"
            "  </body>\n"
            "</html>"
        ),
    },
    {
        "id": "valid-void",
        "title": "Valid dengan Void Element",
        "category": "valid",
        "description": "Menggunakan tag mandiri seperti <br>, <img>, dan <input> yang tidak memerlukan penutup.",
        "code": (
            "<div class=\"card\">\n"
            "  <img src=\"foto.jpg\">\n"
            "  <p>Baris pertama<br>Baris kedua</p>\n"
            "  <input type=\"text\" placeholder=\"Nama\">\n"
            "</div>"
        ),
    },
    {
        "id": "invalid-mismatch",
        "title": "Tag Tertukar (Mismatch)",
        "category": "invalid",
        "description": "Urutan penutupan tag tertukar antara <p> dan <div>.",
        "code": (
            "<div>\n"
            "  <p>Paragraf ini tidak ditutup dengan benar.\n"
            "</div>\n"
            "</p>"
        ),
    },
    {
        "id": "invalid-unclosed",
        "title": "Tag Tidak Ditutup",
        "category": "invalid",
        "description": "Tag <section> dibuka tetapi tidak pernah ditutup hingga akhir dokumen.",
        "code": (
            "<section>\n"
            "  <h2>Judul Bagian</h2>\n"
            "  <p>Konten di dalam section ini.</p>\n"
        ),
    },
    {
        "id": "invalid-extra-closing",
        "title": "Tag Penutup Berlebih",
        "category": "invalid",
        "description": "Terdapat tag penutup </span> tanpa tag pembuka yang sesuai.",
        "code": (
            "<p>Halo dunia</span></p>"
        ),
    },
]


def get_all_examples():
    """Mengembalikan seluruh contoh HTML yang tersedia."""
    return SAMPLE_EXAMPLES


def get_example_by_id(example_id):
    """Mencari satu contoh berdasarkan id-nya."""
    for example in SAMPLE_EXAMPLES:
        if example["id"] == example_id:
            return example
    return None
