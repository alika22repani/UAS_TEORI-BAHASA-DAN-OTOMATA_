# PDA HTML Validator

Capstone Project mata kuliah **Teori Bahasa dan Otomata** &mdash; aplikasi web
untuk memvalidasi struktur tag HTML menggunakan konsep **Pushdown Automata (PDA)**.

## Fitur

- Validasi struktur tag HTML (valid / tidak valid) menggunakan PDA.
- Deteksi lokasi kesalahan (baris & kolom) saat struktur tidak valid.
- Simulasi stack (push & pop) langkah demi langkah.
- Jejak state (`q_scan`, `q_accept`, `q_reject`) selama proses validasi.
- Penjelasan konsep teori PDA (halaman Documentation).
- Contoh HTML valid dan tidak valid siap pakai.
- Halaman Home, About, Documentation, dan Contact (dengan penyimpanan pesan ke SQLite).

## Struktur Proyek

```
pda-capstone/
├── app.py                  # Entry point aplikasi (application factory)
├── config.py                # Konfigurasi environment (dev/prod/testing)
├── requirements.txt
├── Procfile                 # Perintah start untuk Railway/Heroku
├── runtime.txt               # Versi Python
├── routes/
│   ├── main_routes.py       # Home, About, Documentation, Contact
│   └── pda_routes.py         # Halaman & API validator PDA
├── models/
│   ├── contact_model.py      # Model pesan Contact
│   └── history_model.py      # Model riwayat validasi
├── utils/
│   ├── html_tokenizer.py     # Tokenisasi kode HTML menjadi token tag
│   ├── pda_validator.py       # Mesin Pushdown Automata
│   └── sample_data.py         # Contoh HTML valid/tidak valid
├── templates/                # Jinja2 templates + Bootstrap 5
└── static/                   # CSS & JavaScript kustom
```

## Menjalankan Secara Lokal

```bash
# 1. Buat virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependency
pip install -r requirements.txt

# 3. Salin file environment
cp .env.example .env

# 4. Jalankan aplikasi
python app.py
```

Aplikasi akan berjalan di `http://localhost:5000`.

## Deploy ke Railway

1. Push proyek ini ke repository GitHub.
2. Buat project baru di [Railway](https://railway.app) dan hubungkan ke repository tersebut.
3. Railway akan otomatis mendeteksi `requirements.txt`, `Procfile`, dan `runtime.txt`.
4. Tambahkan environment variable berikut di tab **Variables**:
   - `SECRET_KEY` (nilai bebas, rahasia)
   - `FLASK_ENV=production`
5. Deploy. Railway akan menjalankan `web: gunicorn app:app --bind 0.0.0.0:$PORT` sesuai `Procfile`.

> Catatan: database SQLite pada Railway bersifat *ephemeral* (dapat ter-reset saat redeploy)
> kecuali menambahkan Railway Volume. Untuk kebutuhan capstone/demo hal ini tidak menjadi masalah.

## Lisensi

Proyek ini dibuat untuk keperluan akademik (tugas kuliah/capstone).
