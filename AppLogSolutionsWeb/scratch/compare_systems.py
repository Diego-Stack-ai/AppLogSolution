import os
import sys
import json
import time
from pathlib import Path
from collections import defaultdict

# Setup paths
CLOUD_FUNCTIONS_DIR = os.path.abspath(r'g:\Il mio Drive\App\AppLogSolutionsWeb\functions')
LOCAL_PROG_DIR = os.path.abspath(r'g:\Il mio Drive\App\AppLogSolutionLocale\dati\PROGRAMMA')

sys.path.append(CLOUD_FUNCTIONS_DIR)
sys.path.append(LOCAL_PROG_DIR)

import firebase_admin
from firebase_admin import credentials

try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(r'g:\Il mio Drive\App\AppLogSolutionsWeb\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json')
        firebase_admin.initialize_app(cred)
except Exception as e:
    pass

import main as cloud_main

try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("locale_distinte", os.path.join(LOCAL_PROG_DIR, "9_genera_distinte_da_viaggi.py"))
    locale_mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(locale_mod)
except Exception as e:
    print(f"Errore import locale: {e}")

# ---------------- CONFIG ----------------
pdf_frutta_locale = Path(r"G:\Il mio Drive\App\AppLogSolutionLocale\dati\ddt frutta 22-04.pdf")
pdf_latte_locale = Path(r"G:\Il mio Drive\App\AppLogSolutionLocale\dati\ddt latte 22-04.pdf")
# ----------------------------------------

print("=== START COMPARATIVE TEST ===")

# FASE 2: ESECUZIONE SISTEMA CLOUD (Simulato, ma usando il db/storage vero)
print("\n--- FASE 2: CLOUD ---")
db = cloud_main.get_db()
bucket = cloud_main.storage.bucket(name=cloud_main.BUCKET_NAME)

# Carico in input_pdf_fornitore (Gia' caricato e stratto)
# blob_frutta = bucket.blob("input_pdf_fornitore/ddt frutta 22-04.pdf")
# blob_frutta.upload_from_filename(str(pdf_frutta_locale))
# blob_latte = bucket.blob("input_pdf_fornitore/ddt latte 22-04.pdf")
# blob_latte.upload_from_filename(str(pdf_latte_locale))

# Elabora
# print("Elaborazione PDF (Estrazione / Taglio)...")
# res_estrazione = cloud_main.core_elabora_pdf_estrazione("test_uid")
# print(f"DDT Estratti Cloud: {res_estrazione['data'].get('ddt_estratti')}")

# Trova i DDT estratti per la data 22-04-2026
ddts = list(db.collection('customers').document('DNR').collection('ddt').where('data', '==', '22-04-2026').stream())
ddt_ids = [d.id for d in ddts]
print(f"Trovati {len(ddt_ids)} DDT per il 22-04-2026")

# Crea Viaggio Test
viaggio_id = "viaggio_comparativo_123"
db.collection('customers').document('DNR').collection('Viaggi_DNR').document(viaggio_id).set({
    "ddt_ids": ddt_ids,
    "stato": "bozza",
    "magazzino": {"lat": 45.438515, "lon": 11.697479}
})

print("Ottimizzazione viaggio...")
cloud_main.core_ottimizza_viaggio(viaggio_id)

print("Generazione distinta cloud...")
# Patchiamo temporaneamente la distinta per non scrivere il PDF ma ritornare i report items
original_core_genera = cloud_main.core_genera_distinta_viaggio

# Per catturare l'output, analizziamo il codice o la accumulatore
import inspect
codice_genera = inspect.getsource(cloud_main.core_genera_distinta_viaggio)

# Invece di patchare, eseguiamo e poi estraiamo dal cloud_output.json? 
# Il cloud_main.core_genera_distinta_viaggio non restituisce gli articoli nel JSON, restituisce solo "articoli_totali".
# Quindi devo eseguire io la logica di aggregazione Cloud qui copiandola per salvare il JSON:
articoli_noti, config_cons = cloud_main.get_config_app()
accumulatore_cloud = defaultdict(lambda: {"qty": [], "desc": ""})
import pdfplumber, io, re
for d_id in ddt_ids:
    doc = db.collection('customers').document('DNR').collection('ddt').document(d_id).get().to_dict()
    blob = bucket.blob(doc['storage_path'])
    pdf_bytes = blob.download_as_bytes()
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            if not tables: continue
            tab = next((t for t in tables if t and "Cod. Articolo" in str(t[0])), None)
            if not tab: continue
            for row in tab[1:]:
                if not row or not row[0]: continue
                base, var = cloud_main.normalize_code(row[0], articoli_noti)
                desc = str(row[1] or "").replace('\n', ' ').strip()
                qty_raw = str(row[3] or "")
                qty_parsed = [(int(m.group(1)), m.group(2).title()) for m in re.finditer(r"(\d+)\s+([A-Za-z]+)", qty_raw)]
                if qty_parsed:
                    key = (base, var)
                    accumulatore_cloud[key]["qty"].extend(qty_parsed)
                    if not accumulatore_cloud[key]["desc"]: accumulatore_cloud[key]["desc"] = desc

report_cloud = []
for (codice, variante), dati in sorted(accumulatore_cloud.items()):
    report_cloud.append({
        "codice": codice,
        "variante": variante,
        "descrizione": dati["desc"],
        "display_qty": cloud_main.consolidate_qty(codice, dati["qty"], config_cons)
    })

with open('cloud_output.json', 'w') as f:
    json.dump(report_cloud, f, indent=2)

print(f"Cloud completato. {len(report_cloud)} articoli raggruppati.")


# FASE 1: ESECUZIONE SISTEMA LOCALE
print("\n--- FASE 1: LOCALE ---")
# Useremo _raccogli_articoli_da_pdf di locale_mod sui PDF SCARICATI (già splittati)
accumulatore_locale = []
for d_id in ddt_ids:
    doc = db.collection('customers').document('DNR').collection('ddt').document(d_id).get().to_dict()
    # Scarichiamo localmente in scratch
    local_path = Path(f"scratch_ddt_{d_id}.pdf")
    bucket.blob(doc['storage_path']).download_to_filename(str(local_path))
    tipo = "FRUTTA" if "FRUTTA" in doc['storage_path'] else "LATTE"
    try:
        arts = locale_mod._raccogli_articoli_da_pdf(local_path, tipo)
        if arts:
            accumulatore_locale.extend(arts)
    except Exception as e:
        print(f"Errore parsing locale su {d_id}: {e}")
    finally:
        if local_path.exists():
            try:
                local_path.unlink()
            except:
                pass

aggr_loc = locale_mod._aggrega_articoli(accumulatore_locale)
report_locale = []
for k, v in aggr_loc.items():
    cod, var = k
    desc = v['descrizione']
    raw_qty = locale_mod._consolida_quantita(cod, v['quantita'])
    qty = raw_qty[1] if isinstance(raw_qty, tuple) and len(raw_qty) > 1 else str(raw_qty)
    report_locale.append({
        "codice": cod,
        "variante": var,
        "descrizione": desc,
        "display_qty": qty
    })

with open('local_output.json', 'w') as f:
    json.dump(report_locale, f, indent=2)

print(f"Locale completato. {len(report_locale)} articoli raggruppati.")

# FASE 3 E 4: NORMALIZZAZIONE E CONFRONTO
print("\n--- FASE 4: CONFRONTO ---")
dict_cloud = { (r['codice'].lower().strip(), r['variante'].lower().strip()): r for r in report_cloud }
dict_locale = { (r['codice'].lower().strip(), r['variante'].lower().strip()): r for r in report_locale }

differenze = []

# Check keys
all_keys = set(dict_cloud.keys()).union(set(dict_locale.keys()))
for k in all_keys:
    if k not in dict_cloud:
        differenze.append({"codice": f"{k[0]} {k[1]}", "tipo": "missing_cloud", "locale": "presente", "cloud": "mancante"})
        continue
    if k not in dict_locale:
        differenze.append({"codice": f"{k[0]} {k[1]}", "tipo": "missing_locale", "locale": "mancante", "cloud": "presente"})
        continue
    
    c_data = dict_cloud[k]
    l_data = dict_locale[k]
    
    # Compare Qty (case insensitive space normalized)
    q_cloud = re.sub(r'\s+', ' ', c_data['display_qty'].lower().strip())
    q_locale = re.sub(r'\s+', ' ', l_data['display_qty'].lower().strip())
    
    if q_cloud != q_locale:
        differenze.append({
            "codice": f"{k[0]} {k[1]}",
            "tipo": "quantita",
            "locale": l_data['display_qty'],
            "cloud": c_data['display_qty']
        })

if differenze:
    esito = "errore" if any(d['tipo'] in ['quantita', 'missing_cloud', 'missing_locale'] for d in differenze) else "warning"
else:
    esito = "match"

final_report = {
    "esito": esito,
    "differenze": differenze,
    "totale_articoli_locale": len(report_locale),
    "totale_articoli_cloud": len(report_cloud)
}

with open('report_confronto.json', 'w') as f:
    json.dump(final_report, f, indent=2)

print(f"\nESITO FINALE: {esito.upper()}")
if differenze:
    for d in differenze[:10]:
        print(d)
