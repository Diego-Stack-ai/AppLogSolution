import os
import firebase_admin
from firebase_admin import credentials, storage

def sync_caches():
    print("==================================================")
    print("   SINCRONIZZATORE CACHE (PRODUZIONE -> SVILUPPO)")
    print("==================================================")

    # 1. Inizializzazione Firebase
    if not firebase_admin._apps:
        print("[*] Connessione a Firebase (Produzione)...")
        cred_prod = credentials.Certificate("prod_key.json")
        app_prod = firebase_admin.initialize_app(cred_prod, name='prod_sync')

        print("[*] Connessione a Firebase (Sviluppo)...")
        cred_dev = credentials.Certificate("dev_key.json")
        app_dev = firebase_admin.initialize_app(cred_dev, name='dev_sync')
    else:
        app_prod = firebase_admin.get_app('prod_sync')
        app_dev = firebase_admin.get_app('dev_sync')

    bucket_prod = storage.bucket(name="log-solution-60007.firebasestorage.app", app=app_prod)
    bucket_dev = storage.bucket(name="log-solutions-sviluppo.firebasestorage.app", app=app_dev)

    # 2. Sincronizzazione cartella 'caches/'
    print("\n[*] Ricerca file di cache nel server di Produzione...")
    blobs = bucket_prod.list_blobs(prefix="caches/")
    
    count = 0
    temp_dir = "temp_cache_sync"
    os.makedirs(temp_dir, exist_ok=True)

    for blob in blobs:
        if blob.name.endswith('/'):
            continue # Salta le cartelle vuote

        local_path = os.path.join(temp_dir, os.path.basename(blob.name))
        
        print(f"    -> Copia in corso: {blob.name}")
        
        # Download da Produzione
        blob.download_to_filename(local_path)
        
        # Upload su Sviluppo
        blob_dev = bucket_dev.blob(blob.name)
        blob_dev.upload_from_filename(local_path)
        count += 1

    # Pulizia temporanea
    for file in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, file))
    os.rmdir(temp_dir)

    print("\n==================================================")
    print(f"[✔] Sincronizzazione completata! Copiati {count} file.")
    print("Ora l'app di Sviluppo ha le stesse distanze dell'app Ufficiale.")
    print("==================================================")

if __name__ == "__main__":
    try:
        sync_caches()
    except Exception as e:
        print("\n[!!!] ERRORE DURANTE LA SINCRONIZZAZIONE:", str(e))
