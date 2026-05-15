import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore
import re
import os

# --- CONFIGURAZIONE ---
SERVICE_ACCOUNT_PATH = 'backend/config/log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json'
CLIENTI_XLSX = 'g:/Il mio Drive/App/AppLogSolutionLocale/dati/PROGRAMMA/mappatura_destinazioni.xlsx'
RIENTRI_XLSX = 'g:/Il mio Drive/App/AppLogSolutionLocale/dati/rientri_ddt.xlsx'
ARTICOLI_PY = 'g:/Il mio Drive/App/AppLogSolutionLocale/dati/PROGRAMMA/9_genera_distinte_da_viaggi.py'

if not os.path.exists(SERVICE_ACCOUNT_PATH):
    print(f"❌ Errore: File service account non trovato in {SERVICE_ACCOUNT_PATH}")
    exit(1)

# Inizializza Firebase
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred)
db = firestore.client()

ARTICOLI_XLSX = 'g:/Il mio Drive/App/AppLogSolutionLocale/dati/tabella_aggiornamento_articoli.xlsx'

def sync_articoli():
    print("📦 Sincronizzazione Articoli (da Excel)...")
    df = pd.read_excel(ARTICOLI_XLSX)
    df = df.where(pd.notnull(df), None)
    
    # Leggi anche il consolidamento dal file Python per le regole
    with open(ARTICOLI_PY, 'r', encoding='utf-8') as f:
        content = f.read()
    match_cons = re.search(r'CONSOLIDAMENTO = \{(.*?)\}', content, re.S)
    consolidamento = {}
    if match_cons:
        items = re.findall(r'"(.*?)":\s*\("(.*?)",\s*"(.*?)",\s*(\d+)\)', match_cons.group(1))
        for cod, p, s, r in items:
            consolidamento[cod] = {"unita_principale": p, "unita_secondaria": s, "ratio": int(r)}

    batch = db.batch()
    count = 0
    for _, row in df.iterrows():
        art = str(row.get('Codice') or '').strip()
        if not art: continue
        
        # Pulisci eventuale newline
        art = art.replace('\n', ' ')
        
        doc_ref = db.collection('customers').document('DNR').collection('anagrafica_articoli').document(art)
        data = consolidamento.get(art, {})
        data['descrizione'] = row.get('Descrizione') or ''
        data['is_articolo_noto'] = True
        if art.endswith('-'):
            data['is_wildcard_prefix'] = True
        
        batch.set(doc_ref, data, merge=True)
        count += 1
    
    batch.commit()
    print(f"✅ Sincronizzati {count} articoli.")

def sync_clienti():
    print("👥 Sincronizzazione Clienti...")
    df = pd.read_excel(CLIENTI_XLSX)
    df = df.where(pd.notnull(df), None) # Sostituisce NaN con None
    
    batch = db.batch()
    count = 0
    for _, row in df.iterrows():
        cod_f = str(row.get('Codice Frutta') or '').strip().lower()
        cod_l = str(row.get('Codice Latte') or '').strip().lower()
        
        if not cod_f and not cod_l: continue
        
        # ID documento: codice_frutta se esiste, altrimenti codice_latte
        doc_id = cod_f if cod_f and cod_f != 'p00000' else (cod_l if cod_l else 'p00000_gen_' + str(count))
        
        doc_ref = db.collection('customers').document('DNR').collection('clienti').document(doc_id)
        
        data = {
            "codice_frutta": row.get('Codice Frutta'),
            "codice_latte": row.get('Codice Latte'),
            "cliente": row.get('A chi va consegnato'),
            "indirizzo": row.get('Indirizzo'),
            "cap": str(row.get('CAP') or ''),
            "citta": row.get('Città'),
            "provincia": row.get('Provincia'),
            "lat": row.get('Latitudine'),
            "lon": row.get('Longitudine'),
            "orario_min_frutta": row.get('Orario min Frutta'),
            "orario_max_frutta": row.get('Orario max Frutta'),
            "orario_min_latte": row.get('Orario min Latte'),
            "orario_max_latte": row.get('Orario max Latte'),
        }
        
        batch.set(doc_ref, data, merge=True)
        count += 1
        
        if count % 400 == 0:
            batch.commit()
            batch = db.batch()

    batch.commit()
    print(f"✅ Sincronizzati {count} clienti.")

def sync_rientri():
    print("🔄 Sincronizzazione Rientri...")
    if not os.path.exists(RIENTRI_XLSX):
        print("⚠️ File rientri non trovato.")
        return
        
    df = pd.read_excel(RIENTRI_XLSX)
    df = df.where(pd.notnull(df), None)
    
    batch = db.batch()
    count = 0
    for _, row in df.iterrows():
        cod = str(row.get('Codice consegna') or '').strip()
        if not cod: continue
        
        doc_id = f"{cod}_{row.get('Data DDT')}".replace(" ", "_").replace("/", "-")
        doc_ref = db.collection('customers').document('DNR').collection('rientri_ddt').document(doc_id)
        
        data = {
            "codice_consegna": cod,
            "data_ddt": row.get('Data DDT'),
            "stato": row.get('Stato'),
            "note": row.get('Note')
        }
        
        batch.set(doc_ref, data, merge=True)
        count += 1

    batch.commit()
    print(f"✅ Sincronizzati {count} rientri.")

if __name__ == "__main__":
    sync_articoli()
    sync_clienti()
    sync_rientri()
    print("\n🚀 SINCRONIZZAZIONE COMPLETATA!")
