import os
import firebase_admin
from firebase_admin import credentials, firestore, storage

def copia_collezione(db_prod, db_dev, tenant, coll_name):
    print(f"[{tenant}] Sincronizzazione collezione: {coll_name}")
    docs = db_prod.collection('clienti').document(tenant).collection(coll_name).stream()
    
    # Pulizia Sviluppo prima di inserire per evitare dati sporchi
    old_docs = db_dev.collection('clienti').document(tenant).collection(coll_name).stream()
    cancellati = 0
    for old_d in old_docs:
        old_d.reference.delete()
        cancellati += 1
    if cancellati > 0:
        print(f"  - Puliti {cancellati} vecchi documenti da {coll_name} (Sviluppo)")
        
    copiati = 0
    for doc in docs:
        data = doc.to_dict() or {}
        db_dev.collection('clienti').document(tenant).collection(coll_name).document(doc.id).set(data)
        copiati += 1
        
    print(f"  - Copiati {copiati} documenti da Produzione a Sviluppo in {coll_name}")

def main():
    if not os.path.exists("prod_key.json") or not os.path.exists("dev_key.json"):
        print("ERRORE: Mancano i file delle chiavi (prod_key.json o dev_key.json).")
        return

    print("Inizializzazione Produzione (log-solution-60007)...")
    cred_prod = credentials.Certificate("prod_key.json")
    app_prod = firebase_admin.initialize_app(cred_prod, name='prod_mirata_2', options={
        'storageBucket': 'log-solution-60007.firebasestorage.app'
    })
    db_prod = firestore.client(app=app_prod)
    bucket_prod = storage.bucket(app=app_prod)

    print("Inizializzazione Sviluppo (log-solutions-sviluppo)...")
    cred_dev = credentials.Certificate("dev_key.json")
    app_dev = firebase_admin.initialize_app(cred_dev, name='dev_mirata_2', options={
        'storageBucket': 'log-solutions-sviluppo.firebasestorage.app'
    })
    db_dev = firestore.client(app=app_dev)
    bucket_dev = storage.bucket(app=app_dev)
    
    tenants = ["DNR", "CATTEL", "GRAN CHEF", "BAUER"]
    collezioni = ["raccolta clienti", "viaggi ddt", "reports_logistici"]
    
    print("\n=====================================================")
    print("INIZIO SINCRONIZZAZIONE MIRATA (FIRESTORE)")
    print("=====================================================")
    
    for t in tenants:
        for c in collezioni:
            copia_collezione(db_prod, db_dev, t, c)
            
    print("\n=====================================================")
    print("INIZIO SINCRONIZZAZIONE STORAGE (REPORTS / split_ddt)")
    print("=====================================================")
    
    # Raccogliamo tutte le date dai reports logistici appena copiati
    date_con_viaggi = set()
    for t in tenants:
        docs = db_prod.collection('clienti').document(t).collection('reports_logistici').stream()
        for d in docs:
            date_con_viaggi.add(d.id)
            
    print(f"Date rilevate con dati logistici: {date_con_viaggi}")
    
    for date_str in date_con_viaggi:
        prefixes = [f"REPORTS/{date_str}/", f"split_ddt/{date_str}/"]
        for prefix in prefixes:
            print(f"Analisi Storage Prefix Produzione: {prefix}")
            try:
                blobs_prod = bucket_prod.list_blobs(prefix=prefix)
                copiati = 0
                for blob in blobs_prod:
                    data = blob.download_as_bytes()
                    dev_blob = bucket_dev.blob(blob.name)
                    dev_blob.upload_from_string(data, content_type=blob.content_type)
                    copiati += 1
                if copiati > 0:
                    print(f"  - Copiati {copiati} file da {prefix}")
            except Exception as e:
                print(f"  - ERRORE in {prefix}: {e}")

    print("\n=====================================================")
    print("MIGRAZIONE COMPLETATA CON SUCCESSO")
    print("=====================================================")

if __name__ == "__main__":
    main()
