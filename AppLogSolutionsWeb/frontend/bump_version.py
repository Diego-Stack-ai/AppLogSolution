import os
import re
import glob

frontend_dir = "G:/Il mio Drive/App/AppLogSolutionsWeb/frontend"
sw_path = os.path.join(frontend_dir, "sw.js")
script_path = os.path.join(frontend_dir, "script.js")

# 1. Legge la versione corrente da script.js
with open(script_path, "r", encoding="utf-8") as f:
    script_content = f.read()

version_match = re.search(r'const APP_VERSION\s*=\s*"([^"]+)"', script_content)
if not version_match:
    print("Errore: impossibile trovare APP_VERSION in script.js")
    exit(1)

old_version = version_match.group(1)
# Calcola la nuova versione (incremento decimale, es. 2.90 -> 2.91)
major, minor = old_version.split(".")
new_version = f"{major}.{int(minor) + 1:02d}"
print(f"Versione corrente: {old_version} -> Nuova versione: {new_version}")

# 2. Aggiorna script.js
new_script_content = script_content.replace(
    f'const APP_VERSION = "{old_version}";',
    f'const APP_VERSION = "{new_version}";'
)
with open(script_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(new_script_content)
print("✓ script.js aggiornato.")

# 3. Aggiorna sw.js
with open(sw_path, "r", encoding="utf-8") as f:
    sw_content = f.read()

new_sw_content = sw_content.replace(
    f"const CACHE_NAME = 'log-solution-v{old_version}';",
    f"const CACHE_NAME = 'log-solution-v{new_version}';"
)
with open(sw_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(new_sw_content)
print("✓ sw.js aggiornato.")

# 4. Aggiorna tutti i file HTML (sostituisce qualsiasi ?v=X.XX con la nuova versione)
html_files = glob.glob(os.path.join(frontend_dir, "*.html"))
updated_html_count = 0

for h_file in html_files:
    with open(h_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Sostituisce ?v=X.XX con la nuova versione
    # Riconosce ?v=1.23, ?v=2.90, ?v=2.25 ecc.
    new_content = re.sub(r'\?v=\d+\.\d+', f'?v={new_version}', content)
    
    if new_content != content:
        with open(h_file, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_content)
        updated_html_count += 1
        print(f"  - Aggiornato ?v= in: {os.path.basename(h_file)}")

print(f"✓ Allineamento completato. Aggiornati {updated_html_count} file HTML.")
