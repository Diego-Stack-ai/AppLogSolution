import os
import re
import json
from datetime import datetime
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# --- CONFIGURAZIONE ---
SERVICE_ACCOUNT_PATH = r'g:\Il mio Drive\App\AppLogSolutionsWeb\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json'
CARTELLA_AGGIORNAMENTi = r'g:\Il mio Drive\App\AppLogSolutionsWeb\Presenze\presenze_aggiornate'
# Fallback in caso la cartella abbia uno spazio o nome diverso
if not os.path.exists(CARTELLA_AGGIORNAMENTi):
    CARTELLA_AGGIORNAMENTi = r'g:\Il mio Drive\App\AppLogSolutionsWeb\Presenze\Presenze aggiornate'

if not os.path.exists(SERVICE_ACCOUNT_PATH):
    print(f"Errore: File service account non trovato in {SERVICE_ACCOUNT_PATH}")
    exit(1)

# Inizializza Firebase
try:
    cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
    firebase_admin.initialize_app(cred)
except ValueError:
    pass # Già inizializzato
db = firestore.client()

def normalizza_nome(nome):
    """Rimuove targhe, spazi extra e rende minuscolo per facilitare il match"""
    # Rimuove targhe tipo AA123BB o simili (2 lettere, 3 numeri, 2 lettere)
    nome = re.sub(r'[A-Z]{2}\d{3}[A-Z]{2}', '', nome, flags=re.IGNORECASE)
    # Rimuove .xlsx se presente
    nome = nome.replace('.xlsx', '')
    # Rimuove il prefisso o la targa se aggiunta
    # Sostituisce k con c per Viktor/Victor ecc.
    nome = nome.lower().replace('k', 'c')
    # Rimuove spazi doppi
    return ' '.join(nome.split())

def match_autista(nome_file, lista_autisti):
    """Cerca di abbinare il nome file all'ID dell'autista in Firebase."""
    nome_norm = normalizza_nome(nome_file)
    
    # Primo tentativo: match esatto sul nome normalizzato
    for autista in lista_autisti:
        if normalizza_nome(autista['nome']) == nome_norm:
            return autista['id'], autista['nome']
            
    # Secondo tentativo: partial match (tutte le parole del nome autista Firebase sono nel file)
    for autista in lista_autisti:
        nome_fb_norm = normalizza_nome(autista['nome'])
        parole_fb = nome_fb_norm.split()
        if all(p in nome_norm for p in parole_fb):
            return autista['id'], autista['nome']
            
    # Terzo tentativo: invertito (tutte le parole del file - tranne targa - sono nel nome FB)
    parole_file = nome_norm.split()
    for autista in lista_autisti:
        nome_fb_norm = normalizza_nome(autista['nome'])
        if all(p in nome_fb_norm for p in parole_file):
            return autista['id'], autista['nome']
            
    # Quarto: almeno una parola molto lunga (es cognome > 4) corrisponde
    parole_lunghe = [p for p in parole_file if len(p) > 4]
    for autista in lista_autisti:
        nome_fb_norm = normalizza_nome(autista['nome'])
        for p in parole_lunghe:
            if p in nome_fb_norm:
                return autista['id'], autista['nome']

    return None, None

def processa_aggiornamenti():
    print(f"--- INIZIO IMPORTAZIONE AGGIORNAMENTI DA {CARTELLA_AGGIORNAMENTi} ---")
    if not os.path.exists(CARTELLA_AGGIORNAMENTi):
        print(f"Errore: La cartella {CARTELLA_AGGIORNAMENTi} non esiste o non è ancora sincronizzata da Google Drive.")
        return
        
    files = [f for f in os.listdir(CARTELLA_AGGIORNAMENTi) if f.endswith(".xlsx") and not f.startswith("~$")]
    if not files:
        print("Nessun file Excel trovato nella cartella. Attendi la sincronizzazione di Google Drive.")
        return

    # 1. Scarica la lista autisti da Firebase per fare i match
    autisti_ref = db.collection('dipendenti').where('ruolo', '==', 'autista').stream()
    lista_autisti = []
    for doc in autisti_ref:
        data = doc.to_dict()
        lista_autisti.append({
            'id': doc.id,
            'nome': data.get('nome', '')
        })
    print(f"Scaricati {len(lista_autisti)} autisti da Firebase per il match.")

    batch = db.batch()
    operazioni_batch = 0
    totale_record = 0

    # 2. Elabora i file
    for file in files:
        percorso = os.path.join(CARTELLA_AGGIORNAMENTi, file)
        nome_base = file.replace(".xlsx", "").strip()
        print(f"\nElaborazione file: {nome_base}")
        
        autista_id, autista_nome = match_autista(nome_base, lista_autisti)
        if not autista_id:
            print(f"  [ATTENZIONE] Impossibile trovare un match in Firebase per: {nome_base}. Salto il file.")
            continue
            
        print(f"  --> Match trovato! Abbinato a: {autista_nome} (ID: {autista_id})")
        
        try:
            excel_file = pd.ExcelFile(percorso)
            for mese in excel_file.sheet_names:
                df = pd.read_excel(percorso, sheet_name=mese)
                
                for index, row in df.iterrows():
                    data_cella = row.iloc[0]
                    if pd.isna(data_cella) or not isinstance(data_cella, datetime):
                        continue
                        
                    try:
                        ore_totali = row.iloc[9] if not pd.isna(row.iloc[9]) else 0
                        km_delta = row.iloc[4] if not pd.isna(row.iloc[4]) else 0
                        cliente = str(row.iloc[1]) if not pd.isna(row.iloc[1]) else ""
                        ora_in = str(row.iloc[5]) if not pd.isna(row.iloc[5]) else ""
                        ora_out = str(row.iloc[6]) if not pd.isna(row.iloc[6]) else ""
                        note = str(row.iloc[12]) if len(row) > 12 and not pd.isna(row.iloc[12]) else ""
                        
                        if hasattr(row.iloc[5], 'strftime'): ora_in = row.iloc[5].strftime('%H:%M')
                        if hasattr(row.iloc[6], 'strftime'): ora_out = row.iloc[6].strftime('%H:%M')
                        
                        data_iso = data_cella.strftime("%Y-%m-%dT00:00:00.000Z")
                        doc_id = f"{autista_id}_{data_cella.strftime('%Y-%m-%d')}"
                        
                        doc_ref = db.collection('presenze').document(doc_id)
                        batch.set(doc_ref, {
                            "autistaId": autista_id,
                            "autista": autista_nome,
                            "mese": data_cella.strftime("%Y-%m"),
                            "data": data_iso,
                            "cliente": cliente,
                            "kmDelta": float(km_delta) if str(km_delta).replace('.','',1).isdigit() else 0,
                            "oraInizioM": ora_in,
                            "oraFineM": ora_out,
                            "oreTotali": float(ore_totali) if str(ore_totali).replace('.','',1).isdigit() else 0,
                            "note": note
                        }, merge=True)
                        
                        operazioni_batch += 1
                        totale_record += 1
                        
                        if operazioni_batch >= 400:
                            batch.commit()
                            batch = db.batch()
                            operazioni_batch = 0
                            
                    except Exception as e:
                        print(f"  [!] Errore riga {index} del mese {mese}: {e}")
                        
        except Exception as e:
            print(f"  [!] Errore lettura Excel {file}: {e}")

    if operazioni_batch > 0:
        batch.commit()
        
    print(f"\n--- IMPORTAZIONE COMPLETATA! ---")
    print(f"Record totali inviati a Firebase: {totale_record}")

if __name__ == "__main__":
    processa_aggiornamenti()
