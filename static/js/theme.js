// theme.js – dark/light + style switcher

(function () {
    const html = document.documentElement;

    // Lees bestaande voorkeuren
    const savedMode = localStorage.getItem("tg-mode") || "light";
    const savedTheme = localStorage.getItem("tg-theme") || "zen";

    // Pas toe op <html>
    html.classList.remove("light", "dark");
    html.classList.add(savedMode);
    html.setAttribute("data-theme", savedTheme);

    // Pak elementen
    const btnDesktop = document.getElementById("themeToggle");
    const btnMobile  = document.getElementById("themeToggleMobile");
    const selectDesktop = document.getElementById("themeSelect");
    const selectMobile  = document.getElementById("themeSelectMobile");

    // Init selects met huidige waarde
    if (selectDesktop) selectDesktop.value = savedTheme;
    if (selectMobile)  selectMobile.value  = savedTheme;

    // Helper: mode toggelen
    function toggleMode() {
        const current = html.classList.contains("dark") ? "dark" : "light";
        const next = current === "dark" ? "light" : "dark";

        html.classList.remove("light", "dark");
        html.classList.add(next);
        localStorage.setItem("tg-mode", next);
    }

    // Helper: theme zetten
    function setTheme(name) {
        html.setAttribute("data-theme", name);
        localStorage.setItem("tg-theme", name);

        if (selectDesktop && selectDesktop.value !== name) {
            selectDesktop.value = name;
        }
        if (selectMobile && selectMobile.value !== name) {
            selectMobile.value = name;
        }
    }

    // Events: dark/light
    if (btnDesktop) btnDesktop.addEventListener("click", toggleMode);
    if (btnMobile)  btnMobile.addEventListener("click", toggleMode);

    // Events: theme select
    if (selectDesktop) {
        selectDesktop.addEventListener("change", (e) => setTheme(e.target.value));
    }
    if (selectMobile) {
        selectMobile.addEventListener("change", (e) => setTheme(e.target.value));
    }
})();
