import os
import re

root = 'functions'
main_path = os.path.join(root, 'main.py')

if not os.path.exists(main_path):
    print(f"Errore: {main_path} non trovato.")
    exit(1)

with open(main_path, 'r', encoding='utf-8') as f:
    c_main = f.read()

# Cerchiamo la riga che restituisce la versione nel backend
# Esempio: return {"version": "1.0.0"}
match = re.search(r'return\s*\{\s*"version"\s*:\s*"([\d\.]+)"\s*\}', c_main)

if match:
    v_old_str = match.group(1)
    try:
        parts = v_old_str.split('.')
        if len(parts) == 3:
            major, minor, patch = parts
            patch_int = int(patch) + 1
            if patch_int >= 100:
                minor = str(int(minor) + 1)
                patch_int = 0
            v_new = f"{major}.{minor}.{patch_int}"
        elif len(parts) == 2:
            major, minor = parts
            minor_int = int(minor) + 1
            v_new = f"{major}.{minor_int}.0"
        else:
            v_new = '1.0.1'
    except Exception:
        v_new = '1.0.1'
else:
    print("Non sono riuscito a trovare la versione nel file main.py. Assicurati che get_backend_version esista.")
    v_new = '1.0.1'

print(f"Versione backend precedente: {v_old_str if match else 'Sconosciuta'}")
print(f"Nuova versione backend calcolata: {v_new}")

# Sostituiamo la versione vecchia con la nuova
c_main_new = re.sub(
    r'(return\s*\{\s*"version"\s*:\s*")[\d\.]+("\s*\})',
    rf'\g<1>{v_new}\g<2>',
    c_main
)

with open(main_path, 'w', encoding='utf-8') as f:
    f.write(c_main_new)

print(f"✅ Backend bumpato a {v_new}.")
print("💡 Ricorda di fare il deploy della funzione get_backend_version (o di tutto il backend) per rendere effettiva la modifica!")
