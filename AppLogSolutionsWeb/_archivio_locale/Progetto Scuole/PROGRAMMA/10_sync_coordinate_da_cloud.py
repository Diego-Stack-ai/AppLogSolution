import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path

# --- CONFIGURAZIONE ---
PROJECT_ID = "log-solution-60007"
PROG_DIR = Path(__file__).resolve().parent
BASE_DIR = PROG_DIR.parent
EXCEL_PATH = PROG_DIR / "mappatura_destinazioni.xlsx"

# Percorso fisico al JSON del Service Account
CRED_PATH = BASE_DIR.parent / "backend" / "config" / "log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json"

def get_real_coords(db):
    """Recupera le coordinate 'reali' inviate dagli autisti dallo Firestore Cloud."""
    print("  Recupero coordinate dal cloud Firebase (Autenticato)...")
    try:
        docs = db.collection("coordinate_reali").stream()
        results = []
        for doc in docs:
            d = doc.to_dict()
            results.append({
                "doc_id": doc.id,
                "p_frutta": str(d.get("codice_frutta", "")),
                "p_latte": str(d.get("codice_latte", "")),
                "nome": str(d.get("nome", "")),
                "lat": float(d.get("lat", 0)),
                "lon": float(d.get("lon", 0)),
                "v_id": str(d.get("v_id", ""))
            })
        print(f"  OK Trovate {len(results)} nuove coordinate.")
        return results
    except Exception as e:
        print(f"  ERR Errore durante il recupero: {e}")
        return []

def delete_from_cloud(db, doc_id):
    """Elimina il documento dal cloud una volta processato."""
    try:
        db.collection("coordinate_reali").document(doc_id).delete()
    except Exception as e:
        print(f"  WARN Impossibile cancellare doc {doc_id}: {e}")

def main():
    if not EXCEL_PATH.exists():
        print(f"  ERR Excel non trovato in {EXCEL_PATH}")
        return

    if not CRED_PATH.exists():
        print(f"  ERR Chiave Firebase non trovata: {CRED_PATH}")
        print("  Assicurati che la cartella backend/config contegna il file JSON.")
        return

    # Inizializziamo Firebase Admin
    if not firebase_admin._apps:
        cred = credentials.Certificate(str(CRED_PATH))
        firebase_admin.initialize_app(cred)
    db = firestore.client()

    new_coords = get_real_coords(db)
    if not new_coords:
        print("  Nessuna nuova coordinata da elaborare.")
        return

    print(f"  Caricamento {EXCEL_PATH.name}...")
    df = pd.read_excel(EXCEL_PATH)

    # Assicuriamoci che la colonna T (COORDINATE_REALI) esista
    # Se il DF ha meno di 20 colonne, le creiamo
    while len(df.columns) < 20:
        df[f"Unnamed: {len(df.columns)}"] = None
    
    # Ridenominiamo la colonna T (indice 19)
    cols = list(df.columns)
    cols[19] = "COORDINATE_REALI_GPS"
    df.columns = cols

    applied_count = 0
    for c in new_coords:
        # Cerchiamo la riga per Codice Frutta o Codice Latte (non vuoto)
        mask = pd.Series([False]*len(df))
        if c['p_frutta'] and c['p_frutta'] != "p00000" and c['p_frutta'] != "None":
            mask = mask | (df['Codice Frutta'].astype(str) == c['p_frutta'])
        if c['p_latte'] and c['p_latte'] != "p00000" and c['p_latte'] != "None":
            mask = mask | (df['Codice Latte'].astype(str) == c['p_latte'])
        
        if mask.any():
            coord_str = f"{c['lat']}, {c['lon']}"
            df.loc[mask, 'COORDINATE_REALI_GPS'] = coord_str
            print(f"  Aggiornata: {c['nome'][:30]} -> {coord_str}")
            delete_from_cloud(db, c['doc_id'])
            applied_count += 1
        else:
            print(f"  WARN Non trovata: {c['nome'][:30]} ({c['p_frutta']}/{c['p_latte']})")

    if applied_count > 0:
        df.to_excel(EXCEL_PATH, index=False)
        print(f"\n  Operazione completata! {applied_count} record salvati nella colonna T.")
    else:
        print("\n  Nessun dato applicato all'Excel.")

if __name__ == "__main__":
    main()
