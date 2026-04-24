import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import math
from pathlib import Path

# --- CONFIGURAZIONE ---
EXCEL_PATH = Path(r"g:\Il mio Drive\App\AppLogSolutionLocale\dati\PROGRAMMA\mappatura_destinazioni.xlsx")
CRED_PATH  = Path(r"g:\Il mio Drive\App\AppLogSolutionsWeb\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(str(CRED_PATH))
    firebase_admin.initialize_app(cred)

db = firestore.client()

def clean(v):
    if pd.isna(v): return ""
    return str(v).strip()

def to_float(v):
    try:
        if pd.isna(v): return None
        x = float(str(v).replace(",", "."))
        return x
    except:
        return None

def reset():
    col = db.collection("mappatura")
    deleted = 0
    while True:
        docs = list(col.limit(500).stream())
        if not docs:
            break
        batch = db.batch()
        for d in docs:
            batch.delete(d.reference)
        batch.commit()
        deleted += len(docs)
        print(f"   ...deleted {deleted} documents")
    return deleted

def rebuild():
    print(f"READING EXCEL: {EXCEL_PATH}")
    df = pd.read_excel(EXCEL_PATH, dtype=str)

    print("RESETTING COLLECTION 'mappatura'...")
    deleted = reset()

    print("REBUILDING COLLECTION...")
    batch = db.batch()
    seen = set()
    inserted = 0
    skipped = 0

    for _, r in df.iterrows():
        cf = clean(r.get("Codice Frutta", "p00000"))
        cl = clean(r.get("Codice Latte", "p00000"))
        uid = f"{cf}_{cl}"

        if uid in seen:
            skipped += 1
            continue
        seen.add(uid)

        lat = to_float(r.get("Latitudine"))
        lon = to_float(r.get("Longitudine"))

        if lat is None or lon is None:
            skipped += 1
            continue

        if not (35 < lat < 48 and 6 < lon < 19):
            skipped += 1
            continue

        doc = {
            "codice_univoco": uid,
            "codice_frutta": cf,
            "codice_latte": cl,
            "cliente": clean(row_val(r, ['Mensa / Sede', 'A chi va consegnato', 'Cliente'])),
            "indirizzo": clean(r.get("Indirizzo")),
            "citta": clean(row_val(r, ['Località', 'Città', 'Citta'])),
            "lat": lat,
            "lon": lon,
            "rebuilt_at": firestore.SERVER_TIMESTAMP
        }

        ref = db.collection("mappatura").document(uid)
        batch.set(ref, doc)
        inserted += 1

        if inserted % 400 == 0:
            batch.commit()
            batch = db.batch()
            print(f"   ...inserted {inserted} documents")

    batch.commit()
    return {
        "deleted": deleted,
        "inserted": inserted,
        "skipped": skipped
    }

def row_val(row, keys):
    for k in keys:
        if k in row and pd.notna(row[k]):
            return row[k]
    return ""

if __name__ == "__main__":
    result = rebuild()
    print("\nOPERATION COMPLETED")
    print(result)
