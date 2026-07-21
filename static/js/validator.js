/**
 * validator.js
 * ------------
 * Logika frontend untuk halaman /validator:
 * - Mengirim kode HTML ke endpoint POST /api/validate
 * - Menampilkan status valid/tidak valid
 * - Menampilkan tabel jejak langkah PDA (state, aksi, stack)
 * - Memuat contoh HTML ke dalam editor saat tombol contoh diklik
 */

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("validatorForm");
    const input = document.getElementById("htmlInput");
    const statusArea = document.getElementById("statusArea");
    const traceBody = document.getElementById("traceBody");
    const traceWrapper = document.getElementById("traceWrapper");
    const emptyState = document.getElementById("emptyState");
    const summaryArea = document.getElementById("summaryArea");
    const submitBtn = document.getElementById("submitBtn");

    if (!form) return; // Guard: script ini hanya dipakai di halaman validator

    // Klik salah satu chip contoh -> isi textarea dengan kode contoh tersebut
    document.querySelectorAll(".example-chip").forEach((chip) => {
        chip.addEventListener("click", () => {
            const code = chip.getAttribute("data-code");
            input.value = decodeHtmlEntities(code);
            input.focus();
            window.scrollTo({ top: form.getBoundingClientRect().top + window.scrollY - 90, behavior: "smooth" });
        });
    });

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const htmlCode = input.value;

        if (!htmlCode.trim()) {
            renderError("Silakan masukkan kode HTML terlebih dahulu.");
            return;
        }

        setLoading(true);

        try {
            const response = await fetch("/api/validate", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ html: htmlCode }),
            });

            const data = await response.json();

            if (!response.ok) {
                renderError(data.error || "Terjadi kesalahan saat memproses permintaan.");
                return;
            }

            renderResult(data);
        } catch (err) {
            renderError("Tidak dapat terhubung ke server. Silakan coba lagi.");
        } finally {
            setLoading(false);
        }
    });

    function setLoading(isLoading) {
        submitBtn.disabled = isLoading;
        submitBtn.innerHTML = isLoading
            ? '<span class="spinner-border spinner-border-sm me-2"></span>Memvalidasi...'
            : '<i class="bi bi-play-fill me-1"></i>Jalankan Validasi';
    }

    function renderError(message) {
        emptyState.classList.add("d-none");
        summaryArea.classList.remove("d-none");
        traceWrapper.classList.add("d-none");
        statusArea.innerHTML = `
            <span class="status-badge invalid">
                <i class="bi bi-exclamation-triangle-fill"></i> Tidak dapat diproses
            </span>
            <p class="mt-3 mb-0 text-danger-emphasis">${escapeHtml(message)}</p>
        `;
    }

    function renderResult(data) {
        emptyState.classList.add("d-none");
        summaryArea.classList.remove("d-none");
        traceWrapper.classList.remove("d-none");

        // ---- Status utama ----
        if (data.is_valid) {
            statusArea.innerHTML = `
                <span class="status-badge valid">
                    <i class="bi bi-check-circle-fill"></i> Struktur Tag Valid
                </span>
                <p class="mt-3 mb-0 text-secondary">
                    PDA menerima input ini &mdash; seluruh ${data.total_tags} tag berhasil dipasangkan
                    dengan benar dan stack kembali ke simbol dasar <code>Z0</code>.
                </p>
            `;
        } else {
            statusArea.innerHTML = `
                <span class="status-badge invalid">
                    <i class="bi bi-x-circle-fill"></i> Struktur Tag Tidak Valid
                </span>
                <p class="mt-3 mb-0 text-danger-emphasis">${escapeHtml(data.error)}</p>
            `;
        }

        // ---- Tabel jejak simulasi (step by step) ----
        traceBody.innerHTML = "";
        data.steps.forEach((step) => {
            const row = document.createElement("tr");
            if (step.action === "REJECT") row.classList.add("table-danger");
            if (step.action === "ACCEPT") row.classList.add("table-success");

            const stackHtml = step.stack_after
                .map((item) => `<span>${escapeHtml(item)}</span>`)
                .join("");

            row.innerHTML = `
                <td>${step.step_no}</td>
                <td>${step.token ? escapeHtml(step.token) : "&mdash;"}</td>
                <td><span class="action-pill ${step.action}">${step.action}</span></td>
                <td>${step.state}</td>
                <td>${step.line ? `Baris ${step.line}, Kol ${step.col}` : "&mdash;"}</td>
                <td><div class="stack-visual">${stackHtml}</div></td>
                <td class="text-secondary">${escapeHtml(step.detail)}</td>
            `;
            traceBody.appendChild(row);
        });
    }

    function escapeHtml(str) {
        if (str === null || str === undefined) return "";
        const div = document.createElement("div");
        div.textContent = str;
        return div.innerHTML;
    }

    function decodeHtmlEntities(str) {
        const textarea = document.createElement("textarea");
        textarea.innerHTML = str;
        return textarea.value;
    }
});
