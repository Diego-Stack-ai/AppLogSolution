import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import sys
import io

def cleanup_and_test(env_name, key_path):
    print(f"\n=================================")
    print(f"=== ESECUZIONE SU {env_name} ===")
    print(f"=================================\n")
    
    # Inizializza l'app se non lo è già
    try:
        app = firebase_admin.get_app(env_name)
    except ValueError:
        cred = credentials.Certificate(key_path)
        app = firebase_admin.initialize_app(cred, name=env_name)
        
    db = firestore.client(app=app)
    
    print("1. Pulizia Anomalie (processing_jobs con status da_mappare)...")
    jobs_ref = db.collection('clienti').document('CATTEL').collection('processing_jobs')
    docs = jobs_ref.where('status', '==', 'da_mappare').stream()
    deleted = 0
    for doc in docs:
        doc.reference.delete()
        deleted += 1
    print(f"-> Cancellati {deleted} job in anomalia/da mappare.")
    
    # Controllo collection 'anomalie' se esiste (a volte usata nel front-end)
    anom_ref = db.collection('clienti').document('CATTEL').collection('anomalie')
    anom_docs = anom_ref.stream()
    anom_deleted = 0
    for d in anom_docs:
        d.reference.delete()
        anom_deleted += 1
    if anom_deleted > 0:
        print(f"-> Cancellati {anom_deleted} documenti dalla collection 'anomalie'.")
        
    print("\n2. Preparazione Test di Importazione...")
    print("-> Caricamento anagrafica CATTEL dal DB...")
    clienti_ref = db.collection('clienti').document('CATTEL').collection('raccolta clienti')
    db_docs = clienti_ref.stream()
    db_mappati = {}
    for doc in db_docs:
        data = doc.to_dict()
        codice = data.get('codice_frutta', '').lower().strip()
        if codice:
            db_mappati[codice] = data
            
    print(f"-> Trovati {len(db_mappati)} clienti CATTEL indicizzati.")
    
    print("\n3. Esecuzione Simulazione Parser (ReportPianificazione.xlsx)...")
    excel_path = 'ReportPianificazione.xlsx'
    with open(excel_path, 'rb') as f:
        excel_bytes = f.read()
        
    # Importiamo la funzione aggiornata da main.py
    sys.path.append('.')
    try:
        from functions.main import _processa_excel_cattel_core_logic
        risultato = _processa_excel_cattel_core_logic(excel_bytes, db_mappati, '2026-07-08', 'test_job_123')
        
        nuovi = risultato.get('nuovi_dati', {})
        deliveries = risultato.get('deliveries', [])
        
        print(f"\n=== RISULTATO IMPORTAZIONE ({env_name}) ===")
        print(f"Clienti Trovati e Abbinati (Deliveries): {len(deliveries)}")
        print(f"Clienti NON Trovati (Nuovi da mappare): {len(nuovi)}")
        
        if len(nuovi) > 0:
            print("\nELENCO CLIENTI DA MAPPARE TROVATI:")
            for code, info in nuovi.items():
                print(f" - Codice estratto: {code} | Nome: {info.get('dest')} | Indirizzo: {info.get('ind')}")
        else:
            print("\nNessuna anomalia! Tutti i clienti del file sono stati riconosciuti automaticamente.")
            
    except Exception as e:
        print(f"Errore durante l'esecuzione del parser: {e}")
        import traceback
        traceback.print_exc()

# Esegui per entrambi gli ambienti
cleanup_and_test('SVILUPPO', 'dev_key.json')
cleanup_and_test('PRODUZIONE', 'prod_key.json')
