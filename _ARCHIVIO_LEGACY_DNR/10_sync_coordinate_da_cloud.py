import pandas as pd
import requests
import json
from pathlib import Path

# --- CONFIGURAZIONE ---
PROJECT_ID = "log-solution-60007"
EXCEL_PATH = Path(__file__).resolve().parent / "mappatura_destinazioni.xlsx"

# NOTE: Firestore REST API non richiede autenticazione se le regole sono aperte (test mode)
# In produzione dovresti usare un Service Account Key (JSON).
STORE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/coordinate_reali"

def get_real_coords():
    """Recupera le coordinate 'reali' inviate dagli autisti dallo Firestore Cloud."""
    print("📡 Recupero coordinate dal cloud Firebase...")
    try:
        resp = requests.get(STORE_URL)
        if resp.status_code != 200:
            print(f"❌ Errore API Firestore: {resp.status_code}")
            return []
        
        data = resp.json()
        docs = data.get("documents", [])
        results = []
        for d in docs:
            fields = d.get("fields", {})
            results.append({
                "doc_name": d["name"],
                "p_frutta": fields.get("codice_frutta", {}).get("stringValue", ""),
                "p_latte": fields.get("codice_latte", {}).get("stringValue", ""),
                "nome": fields.get("nome", {}).get("stringValue", ""),
                "lat": float(fields.get("lat", {}).get("doubleValue", 0)),
                "lon": float(fields.get("lon", {}).get("doubleValue", 0)),
                "v_id": fields.get("v_id", {}).get("stringValue", "")
            })
        print(f"✅ Trovate {len(results)} nuove coordinate.")
        return results
    except Exception as e:
        print(f"❌ Errore durante il recupero: {e}")
        return []

def delete_from_cloud(doc_name):
    """Elimina il documento dal cloud una volta processato."""
    try:
        requests.delete(f"https://firestore.googleapis.com/v1/{doc_name}")
    except: pass

def main():
    if not EXCEL_PATH.exists():
        print(f"❌ Excel non trovato in {EXCEL_PATH}")
        return

    new_coords = get_real_coords()
    if not new_coords:
        print("☕ Nessuna nuova coordinata da elaborare.")
        return

    print(f"📂 Caricamento {EXCEL_PATH.name}...")
    df = pd.read_excel(EXCEL_PATH)

    # Assicuriamoci che la colonna COORDINATE_REALI_GPS esista — ricerca per NOME,
    # non per indice. Elimina la dipendenza dalle 4 colonne "Unnamed" di padding.
    COL_GPS = "COORDINATE_REALI_GPS"
    if COL_GPS not in df.columns:
        df[COL_GPS] = None
        print(f"  ℹ️ Colonna '{COL_GPS}' creata.")

    applied_count = 0
    for c in new_coords:
        # Cerchiamo la riga per Codice Frutta o Codice Latte
        mask = (df['Codice Frutta'].astype(str) == str(c['p_frutta'])) | \
               (df['Codice Latte'].astype(str) == str(c['p_latte']))
        
        if mask.any():
            coord_str = f"{c['lat']}, {c['lon']}"
            df.loc[mask, COL_GPS] = coord_str
            print(f"📍 Aggiornata: {c['nome']} -> {coord_str}")
            delete_from_cloud(c['doc_name'])
            applied_count += 1
        else:
            print(f"⚠️ Non trovata in Excel: {c['nome']} ({c['p_frutta']}/{c['p_latte']})")

    if applied_count > 0:
        df.to_excel(EXCEL_PATH, index=False)
        print(f"\n✨ Operazione completata! {applied_count} record salvati nella colonna T.")
    else:
        print("\nℹ️ Nessun dato applicato all'Excel.")

if __name__ == "__main__":
    main()
