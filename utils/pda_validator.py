"""
utils/pda_validator.py
------------------------
Implementasi konsep Pushdown Automata (PDA) untuk memvalidasi
keseimbangan struktur tag HTML.

============================================================
KONSEP TEORI YANG DITERAPKAN
============================================================
Sebuah PDA didefinisikan secara formal sebagai 7-tuple:

    M = (Q, Sigma, Gamma, delta, q0, Z0, F)

    Q      : himpunan state         -> {q_scan, q_reject}
    Sigma  : alfabet input          -> token tag HTML (open/close/self-close)
    Gamma  : alfabet stack          -> nama tag HTML + simbol dasar Z0
    delta  : fungsi transisi        -> lihat method `_step()`
    q0     : state awal             -> q_scan
    Z0     : simbol awal stack      -> "Z0" (penanda dasar stack)
    F      : himpunan state akhir   -> {q_accept} (diturunkan jika stack == [Z0])

Cara kerja PDA di sini persis seperti PDA klasik untuk bahasa
"kurung berpasangan" (balanced parentheses):
    - Tag pembuka (<tag>)  ==  PUSH tag ke stack   (analog membuka kurung)
    - Tag penutup (</tag>) ==  POP tag dari stack   (analog menutup kurung)
    - Jika tag yang di-pop tidak sama dengan tag penutup -> tidak valid (mismatch)
    - Jika stack tidak kosong (kembali ke Z0) di akhir input -> tidak valid (ada tag yang belum ditutup)
    - Jika ingin pop tapi stack sudah kosong (hanya Z0) -> tidak valid (tag penutup tanpa pasangan)

Tag self-closing / void element (mis. <br>, <img>, <input/>) tidak
mempengaruhi stack sama sekali karena tidak memerlukan pasangan penutup.
"""

from utils.html_tokenizer import tokenize

BOTTOM_MARKER = "Z0"        # simbol dasar stack (Gamma awal)
STATE_SCAN = "q_scan"       # state ketika PDA sedang membaca token
STATE_ACCEPT = "q_accept"   # state akhir jika seluruh input valid
STATE_REJECT = "q_reject"   # state jebakan (dead state) jika ditemukan kesalahan


class PDAResult:
    """Struktur hasil akhir validasi, siap dikirim sebagai JSON ke frontend."""

    def __init__(self):
        self.is_valid = True
        self.error = None                # pesan kesalahan (jika ada)
        self.error_token = None           # token yang menyebabkan error
        self.steps = []                   # riwayat langkah demi langkah
        self.total_tags = 0
        self.final_stack = []

    def to_dict(self):
        return {
            "is_valid": self.is_valid,
            "error": self.error,
            "error_token": self.error_token,
            "steps": self.steps,
            "total_tags": self.total_tags,
            "final_stack": self.final_stack,
        }


def validate_html(html_source):
    """
    Fungsi utama: menjalankan simulasi PDA terhadap kode HTML yang diberikan.

    Parameter:
        html_source (str): kode HTML mentah dari input pengguna

    Return:
        PDAResult: objek berisi status valid/tidak valid beserta jejak simulasi
    """
    result = PDAResult()
    tokens = tokenize(html_source)

    stack = [BOTTOM_MARKER]     # inisialisasi stack dengan simbol dasar Z0
    current_state = STATE_SCAN

    def record_step(token, action, detail):
        """Mencatat satu baris riwayat simulasi (dipakai untuk visualisasi stack)."""
        result.steps.append({
            "step_no": len(result.steps) + 1,
            "token": token.raw if token else None,
            "token_kind": token.kind if token else None,
            "tag_name": token.name if token else None,
            "line": token.line if token else None,
            "col": token.col if token else None,
            "action": action,               # PUSH | POP | SKIP | REJECT | ACCEPT
            "stack_after": list(stack),
            "state": current_state,
            "detail": detail,
        })

    for token in tokens:
        # Komentar & doctype diabaikan oleh PDA (tidak mengubah stack)
        if token.kind in ("comment", "doctype"):
            record_step(token, "SKIP", f"'{token.raw.strip()}' diabaikan (bukan bagian dari struktur tag)")
            continue

        # Tag self-closing / void element: tidak mempengaruhi stack
        if token.kind == "self-close":
            result.total_tags += 1
            record_step(token, "SKIP", f"<{token.name}> adalah tag mandiri (self-closing/void), stack tidak berubah")
            continue

        # Tag pembuka -> PUSH ke stack
        if token.kind == "open":
            result.total_tags += 1
            stack.append(token.name)
            record_step(token, "PUSH", f"Tag pembuka <{token.name}> di-push ke stack")
            continue

        # Tag penutup -> harus POP dan cocok dengan puncak stack
        if token.kind == "close":
            result.total_tags += 1

            # Kasus 1: stack sudah kosong (hanya tersisa Z0) -> tag penutup tanpa pasangan
            if len(stack) <= 1:
                current_state = STATE_REJECT
                record_step(
                    token, "REJECT",
                    f"Ditemukan tag penutup </{token.name}> tanpa tag pembuka yang sesuai"
                )
                result.is_valid = False
                result.error = (
                    f"Tag penutup </{token.name}> pada baris {token.line}, kolom {token.col} "
                    f"tidak memiliki tag pembuka yang sesuai (stack kosong)."
                )
                result.error_token = token.to_dict()
                result.final_stack = list(stack)
                return result

            top = stack[-1]

            # Kasus 2: tag di puncak stack cocok -> POP normal
            if top == token.name:
                stack.pop()
                record_step(token, "POP", f"Tag penutup </{token.name}> cocok dengan puncak stack, POP berhasil")
                continue

            # Kasus 3: tidak cocok -> kesalahan nesting (mismatch)
            current_state = STATE_REJECT
            record_step(
                token, "REJECT",
                f"Tag penutup </{token.name}> tidak cocok dengan puncak stack <{top}>"
            )
            result.is_valid = False
            result.error = (
                f"Struktur tidak valid pada baris {token.line}, kolom {token.col}: "
                f"menemukan </{token.name}> tetapi tag yang seharusnya ditutup adalah <{top}>."
            )
            result.error_token = token.to_dict()
            result.final_stack = list(stack)
            return result

    # Setelah seluruh token diproses, PDA hanya menerima (accept)
    # jika stack kembali ke kondisi awal (hanya berisi Z0)
    result.final_stack = list(stack)

    if len(stack) == 1:
        current_state = STATE_ACCEPT
        record_step(None, "ACCEPT", "Seluruh token telah diproses dan stack kembali ke Z0. Input DITERIMA.")
        result.is_valid = True
    else:
        current_state = STATE_REJECT
        unclosed = stack[1:]
        record_step(
            None, "REJECT",
            f"Input berakhir tetapi stack belum kembali ke Z0. Tag belum ditutup: {', '.join(unclosed)}"
        )
        result.is_valid = False
        result.error = (
            "Terdapat tag yang belum ditutup hingga akhir dokumen: "
            f"{', '.join(f'<{name}>' for name in unclosed)}."
        )

    return result
