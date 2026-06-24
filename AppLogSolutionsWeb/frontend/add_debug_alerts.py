import re

file_path = r"g:\Il mio Drive\App\AppLogSolutionsWeb\frontend\presenze.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add debug alerts
old_func = r"""        window.openDettagli = function(btn) {
            try {
                const tr = btn.closest('tr');"""

new_func = r"""        window.openDettagli = function(btn) {
            alert("DEBUG 1: Funzione openDettagli chiamata con successo!");
            try {
                const tr = btn.closest('tr');"""

if old_func in content:
    content = content.replace(old_func, new_func)

old_mod = r"""                const mod = document.getElementById('dettagliModal');
                if (mod) mod.style.display = 'flex';
                else throw new Error("Overlay modale non trovato");"""

new_mod = r"""                const mod = document.getElementById('dettagliModal');
                if (mod) {
                    alert("DEBUG 2: Trovato dettagliModal nel DOM! Imposto display a flex.");
                    mod.style.display = 'flex';
                    mod.style.visibility = 'visible';
                    mod.style.opacity = '1';
                    alert("DEBUG 3: display impostato a " + mod.style.display);
                }
                else throw new Error("Overlay modale non trovato");"""

if old_mod in content:
    content = content.replace(old_mod, new_mod)

# Fix possible quotes issue in hidden inputs
old_hidden = r"""                        <input type="hidden" data-field="note" value="${record.note || ''}">"""
new_hidden = r"""                        <input type="hidden" data-field="note" value="${(record.note || '').replace(/"/g, '&quot;')}">"""

if old_hidden in content:
    content = content.replace(old_hidden, new_hidden)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Added debug alerts!")
