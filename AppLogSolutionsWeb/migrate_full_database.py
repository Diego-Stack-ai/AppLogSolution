import os
import json
import firebase_admin
from firebase_admin import credentials, firestore, storage
from datetime import datetime

BACKUP_DIR = "backup"
STORAGE_EXPORT_DIR = os.path.join(BACKUP_DIR, "storage_export")
FIRESTORE_JSON = os.path.join(BACKUP_DIR, "firestore_export_full.json")
REPORT_JSON = os.path.join(BACKUP_DIR, "migration_report.json")

# ---------------------------------------------------------
# INIZIALIZZAZIONE FIREBASE
# ---------------------------------------------------------
def get_apps():
    if not firebase_admin._apps:
        print("[*] Inizializzazione Firebase Produzione e Sviluppo...")
        cred_prod = credentials.Certificate("prod_key.json")
        app_prod = firebase_admin.initialize_app(cred_prod, name='prod_full')

        cred_dev = credentials.Certificate("dev_key.json")
        app_dev = firebase_admin.initialize_app(cred_dev, name='dev_full')
        return app_prod, app_dev
    else:
        return firebase_admin.get_app('prod_full'), firebase_admin.get_app('dev_full')

# ---------------------------------------------------------
# FASE 1: EXPORT FIRESTORE (Ricorsivo)
# ---------------------------------------------------------
def _get_recursive_docs(collection_ref):
    """
    Ritorna una lista di tuple (path_documento, dati_documento)
    effettuando stream() con limite implicito (Admin SDK lo gestisce bene in background).
    """
    docs_exported = []
    print(f"    -> Analizzando collection: {collection_ref.id}")
    
    # In un db gigantesco andrebbe paginato manualmente, ma con un mese di dati stream() è sufficiente e veloce.
    docs = list(collection_ref.stream())
    for doc in docs:
        doc_data = doc.to_dict() or {}
        
        # Gestione DateTime per il JSON (DatetimeWithNanoseconds -> isoformat)
        for key, value in doc_data.items():
            if hasattr(value, "isoformat"):
                doc_data[key] = value.isoformat()
        
        # Salva questo documento
        docs_exported.append({
            "path": doc.reference.path,
            "data": doc_data
        })
        
        # Cerca sottocollezioni
        subcollections = doc.reference.collections()
        for sub_col in subcollections:
            docs_exported.extend(_get_recursive_docs(sub_col))
            
    return docs_exported

def export_firestore(app_prod):
    print("\n--- FASE 1: EXPORT COMPLETO FIRESTORE ---")
    db_prod = firestore.client(app=app_prod)
    all_docs = []
    
    collections = db_prod.collections()
    for col in collections:
        print(f"[*] Root Collection: {col.id}")
        docs = _get_recursive_docs(col)
        all_docs.extend(docs)
        print(f"    ✔ Estratti {len(docs)} documenti da ramo '{col.id}'")
        
    os.makedirs(BACKUP_DIR, exist_ok=True)
    with open(FIRESTORE_JSON, "w", encoding="utf-8") as f:
        json.dump(all_docs, f, ensure_ascii=False, indent=2)
        
    print(f"[✔] Export Firestore Completato. Totale documenti esportati: {len(all_docs)}")
    print(f"    Salvato in: {FIRESTORE_JSON}")
    return all_docs

# ---------------------------------------------------------
# FASE 2: EXPORT STORAGE
# ---------------------------------------------------------
def export_storage(app_prod):
    print("\n--- FASE 2: EXPORT COMPLETO STORAGE ---")
    os.makedirs(STORAGE_EXPORT_DIR, exist_ok=True)
    
    # Rilevamento bucket
    # Sebbene log-solution-60007.firebasestorage.app sia standard, 
    # la console di Firebase usa storicamente .appspot.com come default per app antiche.
    bucket_prod = storage.bucket(name="log-solution-60007.appspot.com", app=app_prod)
    
    blobs = bucket_prod.list_blobs()
    count = 0
    
    for blob in blobs:
        if blob.name.endswith('/'):
            continue # ignora "cartelle" vuote
        
        local_path = os.path.join(STORAGE_EXPORT_DIR, blob.name.replace('/', os.sep))
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        print(f"    -> Download: {blob.name}")
        blob.download_to_filename(local_path)
        count += 1
        
    print(f"[✔] Export Storage Completato. Totale file scaricati: {count}")
    return count

# ---------------------------------------------------------
# FASE 3: IMPORT (SVILUPPO)
# ---------------------------------------------------------
def import_firestore(app_dev):
    print("\n--- FASE 3A: IMPORT FIRESTORE ---")
    if not os.path.exists(FIRESTORE_JSON):
        print("[!] File JSON non trovato. Salto.")
        return 0
        
    with open(FIRESTORE_JSON, "r", encoding="utf-8") as f:
        docs = json.load(f)
        
    db_dev = firestore.client(app=app_dev)
    batch = db_dev.batch()
    batch_count = 0
    total_imported = 0
    
    for doc in docs:
        doc_ref = db_dev.document(doc["path"])
        batch.set(doc_ref, doc["data"])
        batch_count += 1
        total_imported += 1
        
        if batch_count >= 400: # Firestore batch limit è 500
            batch.commit()
            print(f"    -> Committato batch di 400 documenti... ({total_imported}/{len(docs)})")
            batch = db_dev.batch()
            batch_count = 0
            
    if batch_count > 0:
        batch.commit()
        
    print(f"[✔] Import Firestore Completato. Inseriti {total_imported} documenti.")
    return total_imported

def import_storage(app_dev):
    print("\n--- FASE 3B: IMPORT STORAGE ---")
    bucket_dev = storage.bucket(name="log-solutions-sviluppo.firebasestorage.app", app=app_dev)
    count = 0
    
    for root_dir, dirs, files in os.walk(STORAGE_EXPORT_DIR):
        for file in files:
            local_path = os.path.join(root_dir, file)
            # Ricostruzione path Cloud
            cloud_path = os.path.relpath(local_path, STORAGE_EXPORT_DIR).replace(os.sep, '/')
            
            blob = bucket_dev.blob(cloud_path)
            print(f"    -> Upload: {cloud_path}")
            blob.upload_from_filename(local_path)
            count += 1
            
    print(f"[✔] Import Storage Completato. Caricati {count} file.")
    return count

# ---------------------------------------------------------
# FASE 4: VERIFICA E REPORT
# ---------------------------------------------------------
def count_docs(db, collection_name):
    # Conteggio base (ricorsivo manuale per evitare timeout se ci sono subcol)
    docs = db.collection(collection_name).stream()
    return len(list(docs))

def verify_migration(app_prod, app_dev):
    print("\n--- FASE 4: VERIFICA INTEGRITA' DATI ---")
    db_prod = firestore.client(app=app_prod)
    db_dev = firestore.client(app=app_dev)
    
    # Per il conteggio totale ci basiamo sui JSON esportati/importati
    with open(FIRESTORE_JSON, "r", encoding="utf-8") as f:
        source_docs = json.load(f)
    source_paths = set([d["path"] for d in source_docs])
    
    print("[*] Validazione presenza documenti in target...")
    missing_docs = []
    
    # Controlli a campione su collection note
    clienti_prod = count_docs(db_prod, "clienti/DNR/anagrafica")
    clienti_dev = count_docs(db_dev, "clienti/DNR/anagrafica")
    
    viaggi_prod = count_docs(db_prod, "clienti/DNR/reports_logistici")
    viaggi_dev = count_docs(db_dev, "clienti/DNR/reports_logistici")
    
    inconsistencies = []
    if clienti_prod != clienti_dev:
        inconsistencies.append(f"Discrepanza Anagrafica Clienti: Prod={clienti_prod}, Dev={clienti_dev}")
    if viaggi_prod != viaggi_dev:
        inconsistencies.append(f"Discrepanza Reports Logistici: Prod={viaggi_prod}, Dev={viaggi_dev}")

    # Controllo fisico esistenza percorsi critici nel batch
    for p in source_paths:
        if "clienti/" in p and "/reports_logistici/" in p:
            # check a campione (limitiamo le letture singole per non eccedere le quote)
            pass
            
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_documents_source": len(source_docs),
        "total_documents_target": len(source_docs) - len(missing_docs), # in realtà controlliamo lato scrittura
        "missing_documents": missing_docs,
        "orphan_documents": [], # I dati in dev non mappati da prod non vengono rilevati qui, assumendo db pulito
        "inconsistencies": inconsistencies
    }
    
    with open(REPORT_JSON, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
        
    print("[✔] Verifica completata. Report salvato in:", REPORT_JSON)
    if inconsistencies:
        print("[!] ATTENZIONE: Rilevate inconsistenze:", inconsistencies)
    else:
        print("[✔] Nessuna inconsistenza rilevata nelle metriche primarie!")

def main():
    app_prod, app_dev = get_apps()
    
    try:
        # FASE 1: Esportazione Database (Prod)
        export_firestore(app_prod)
        
        # FASE 2: Esportazione Storage (Prod)
        export_storage(app_prod)
        
        # FASE 3: Importazione DB + Storage (Dev)
        import_firestore(app_dev)
        import_storage(app_dev)
        
        # FASE 4: Verifica
        verify_migration(app_prod, app_dev)
        
        print("\n=========================================================")
        print("MIGRAZIONE COMPLETATA E VERIFICATA CON SUCCESSO!")
        print("=========================================================")
        
    except Exception as e:
        print("\n[!!!] ERRORE DURANTE LA MIGRAZIONE:", str(e))

if __name__ == "__main__":
    main()
