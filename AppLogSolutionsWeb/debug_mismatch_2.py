import sys
import json
import firebase_admin
from firebase_admin import credentials, storage, firestore

if not firebase_admin._apps:
    cred = credentials.Certificate("log-solutions-sviluppo-firebase-adminsdk.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()
bucket = storage.bucket(name="log-solutions-sviluppo.appspot.com")
data_consegna = "2026-07-09"

# Load old zones
blob_old = bucket.blob(f"REPORTS/{data_consegna}/viaggi_giornalieri_Johnson.json")
old_data = json.loads(blob_old.download_as_string().decode('utf-8'))
old_zones = old_data.get("zone", [])

# Load db_mappati
db_mappati = {}
for current_tenant in ['DNR', 'GRAN CHEF', 'CATTEL']:
    clienti_ref = db.collection('clienti').document(current_tenant).collection('raccolta clienti')
    for doc in clienti_ref.stream():
        d = doc.to_dict()
        cf = str(d.get('codice_frutta') or '').strip().lower()
        cl = str(d.get('codice_latte') or '').strip().lower()
        if cf and cf != 'p00000' and cf != 'nan': db_mappati[cf] = d
        if cl and cl != 'p00000' and cl != 'nan': db_mappati[cl] = d

# Load ddt_list
ddt_list = []
prefix_search = f"split_ddt/{data_consegna}/"
blobs = bucket.list_blobs(prefix=prefix_search)
for blob in blobs:
    if "ddt_estratti" in blob.name and blob.name.endswith(".json"):
        meta_data = json.loads(blob.download_as_string())
        job_competenza = meta_data.get("competenza") or meta_data.get("tipo", "FRUTTA").upper()
        if job_competenza in ("GRAND_CHEF", "GRAND CHEF", "GRAN CHEF"):
            job_competenza = "GRAN_CHEF"
        for ddt in meta_data.get("deliveries", []):
            cod = ddt.get("codice_consegna")
            cod_l = str(cod).strip().lower()
            cliente_info = db_mappati.get(cod_l)
            if cliente_info:
                ddt["nome"] = cliente_info.get('cliente') or cliente_info.get('nome_consegna') or cod
            else:
                ddt["nome"] = cod
            ddt_list.append(ddt)

def _build_tripla_chiave(cod_f: str, cod_l: str, nome: str) -> str:
    cf = str(cod_f).strip().lower()
    cl = str(cod_l).strip().lower()
    n  = str(nome).strip().lower()
    return f"{cf}|{cl}|{n}"

punti_map_keys = set()
for ddt in ddt_list:
    cod = ddt.get('codice_consegna')
    cod_l = str(cod).strip().lower()
    cliente_info = db_mappati.get(cod_l)
    nome = ddt.get('nome', cod)
    if cliente_info:
        cf_key = str(cliente_info.get('codice_frutta') or 'p00000').strip().lower()
        cl_key = str(cliente_info.get('codice_latte') or 'p00000').strip().lower()
        nome_key = cliente_info.get('cliente') or cliente_info.get('nome_consegna') or nome
        chiave = _build_tripla_chiave(cf_key, cl_key, nome_key)
    else:
        chiave = ddt.get('tripla_chiave') or cod
    punti_map_keys.add(chiave)

print(f"Totale chiavi in punti_da_assegnare: {len(punti_map_keys)}")

unmatched = []
matched = []
for z in old_zones:
    if z.get("id_zona") in ("DDT_DA_INSERIRE", "0000", "SENZA_ZONA"): continue
    for old_p in z.get("lista_punti", []):
        cf_key = str(old_p.get("codice_frutta") or "p00000").strip().lower()
        cl_key = str(old_p.get("codice_latte") or "p00000").strip().lower()
        nome_key = old_p.get("nome") or ""
        p_key = _build_tripla_chiave(cf_key, cl_key, nome_key)
        
        if p_key in punti_map_keys:
            matched.append(p_key)
        else:
            unmatched.append((z.get("id_zona"), old_p.get("nome"), p_key))

print(f"Matched: {len(matched)}")
print(f"Unmatched: {len(unmatched)}")
if unmatched:
    print("Primi 5 unmatched:")
    for u in unmatched[:5]: print(u)
