/**
 * main.js
 * -------
 * Script umum yang dipakai di seluruh halaman:
 * 1. Animasi mini "stack demo" pada hero halaman Home (signature element).
 * 2. Perilaku kecil navbar (menutup menu mobile setelah klik link).
 */

document.addEventListener("DOMContentLoaded", () => {
    initStackDemo();
    initNavbarAutoClose();
});

/**
 * Menutup navbar collapse otomatis di mobile setelah pengguna memilih menu.
 */
function initNavbarAutoClose() {
    const navLinks = document.querySelectorAll(".navbar-nav .nav-link");
    const navCollapse = document.getElementById("navMain");
    if (!navCollapse) return;

    navLinks.forEach((link) => {
        link.addEventListener("click", () => {
            const bsCollapse = bootstrap.Collapse.getInstance(navCollapse);
            if (bsCollapse && navCollapse.classList.contains("show")) {
                bsCollapse.hide();
            }
        });
    });
}

/**
 * Menjalankan simulasi PUSH/POP sederhana secara otomatis pada hero,
 * merepresentasikan bagaimana PDA memproses urutan tag HTML:
 *     <div> <p> </p> </div>
 * Animasi ini murni ilustratif (bukan mesin PDA sungguhan),
 * mesin PDA yang sebenarnya berjalan di halaman /validator.
 */
function initStackDemo() {
    const body = document.getElementById("stackDemoBody");
    const log = document.getElementById("stackDemoLog");
    if (!body || !log) return;

    // Skenario tetap: urutan token beserta aksinya
    const sequence = [
        { tag: "div", action: "PUSH" },
        { tag: "section", action: "PUSH" },
        { tag: "p", action: "PUSH" },
        { tag: "p", action: "POP" },
        { tag: "section", action: "POP" },
        { tag: "div", action: "POP" },
    ];

    let stack = [];
    let stepIndex = 0;

    function render() {
        body.innerHTML = '<div class="stack-chip base"><span>Z0</span><span>bottom</span></div>';
        stack.forEach((tag) => {
            const chip = document.createElement("div");
            chip.className = "stack-chip";
            chip.innerHTML = `<span>&lt;${tag}&gt;</span><span>tag</span>`;
            body.appendChild(chip);
        });
    }

    function step() {
        const current = sequence[stepIndex % sequence.length];

        if (current.action === "PUSH") {
            stack.push(current.tag);
            log.innerHTML = `<span class="tag-push">PUSH</span> &lt;${current.tag}&gt; ke stack`;
        } else {
            stack.pop();
            log.innerHTML = `<span class="tag-pop">POP</span> &lt;${current.tag}&gt; dari stack`;
        }

        render();
        stepIndex += 1;

        // Jeda sedikit lebih lama saat stack kembali kosong agar siklus terlihat jelas
        const delay = stack.length === 0 ? 1400 : 750;
        setTimeout(step, delay);
    }

    render();
    setTimeout(step, 900);
}
