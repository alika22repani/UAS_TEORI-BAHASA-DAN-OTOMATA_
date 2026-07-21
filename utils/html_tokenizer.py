"""
utils/html_tokenizer.py
------------------------
Modul ini bertugas memecah (tokenize) kode HTML menjadi daftar token tag
yang nantinya akan "dibaca" satu per satu oleh mesin Pushdown Automata (PDA).

Kita hanya tertarik pada tag (bukan teks biasa), karena PDA yang dibangun
di sini bertujuan memvalidasi *keseimbangan struktur tag* HTML,
sama seperti PDA klasik yang memvalidasi keseimbangan kurung "( )" atau "{ }".

Setiap token menyimpan informasi posisi (baris & kolom) agar ketika terjadi
kesalahan, aplikasi bisa menunjukkan lokasi persis kesalahan tersebut.
"""

import re

# Daftar elemen HTML "void" yang tidak memiliki tag penutup,
# meskipun ditulis tanpa garis miring penutup "/>"
VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

# Pola regex untuk menangkap komentar, doctype, dan tag pembuka/penutup
TAG_PATTERN = re.compile(
    r"""
    (?P<comment><!--.*?-->)                     |  # komentar HTML
    (?P<doctype><!DOCTYPE[^>]*>)                |  # deklarasi doctype
    (?P<closing></\s*(?P<close_name>[a-zA-Z][a-zA-Z0-9-]*)\s*>) |  # tag penutup
    (?P<opening><\s*(?P<open_name>[a-zA-Z][a-zA-Z0-9-]*)(?P<attrs>[^<>]*)>)  # tag pembuka
    """,
    re.VERBOSE | re.DOTALL,
)


class Token:
    """Merepresentasikan satu token tag hasil tokenisasi."""

    def __init__(self, kind, name, raw, line, col, index):
        self.kind = kind          # 'open' | 'close' | 'self-close' | 'comment' | 'doctype'
        self.name = name          # nama tag, lowercase (None untuk comment/doctype)
        self.raw = raw            # teks asli token, mis. '<div class="a">'
        self.line = line          # nomor baris (mulai dari 1)
        self.col = col            # nomor kolom (mulai dari 1)
        self.index = index        # urutan token ke berapa (mulai dari 0)

    def to_dict(self):
        return {
            "kind": self.kind,
            "name": self.name,
            "raw": self.raw,
            "line": self.line,
            "col": self.col,
            "index": self.index,
        }


def _position_of(text, offset):
    """Menghitung nomor baris & kolom dari sebuah offset karakter dalam teks."""
    before = text[:offset]
    line = before.count("\n") + 1
    last_newline = before.rfind("\n")
    col = offset - last_newline if last_newline != -1 else offset + 1
    return line, col


def tokenize(html_source):
    """
    Mengubah string HTML menjadi list of Token.

    Parameter:
        html_source (str): kode HTML mentah dari input pengguna

    Return:
        list[Token]
    """
    tokens = []
    index = 0

    for match in TAG_PATTERN.finditer(html_source):
        line, col = _position_of(html_source, match.start())
        raw = match.group(0)

        if match.group("comment"):
            tokens.append(Token("comment", None, raw, line, col, index))

        elif match.group("doctype"):
            tokens.append(Token("doctype", None, raw, line, col, index))

        elif match.group("closing"):
            name = match.group("close_name").lower()
            tokens.append(Token("close", name, raw, line, col, index))

        else:
            name = match.group("open_name").lower()
            attrs = match.group("attrs") or ""
            is_self_closed = attrs.strip().endswith("/")
            if is_self_closed or name in VOID_ELEMENTS:
                tokens.append(Token("self-close", name, raw, line, col, index))
            else:
                tokens.append(Token("open", name, raw, line, col, index))

        index += 1

    return tokens
