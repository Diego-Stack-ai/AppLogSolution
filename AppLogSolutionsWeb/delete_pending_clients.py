import firebase_admin
from firebase_admin import credentials, firestore

def pulisci_anomalie(env_name, key_path):
    print(f"\n=================================")
    print(f"=== ESECUZIONE SU {env_name} ===")
    print(f"=================================\n")
    
    try:
        app = firebase_admin.get_app(env_name)
    except ValueError:
        cred = credentials.Certificate(key_path)
        app = firebase_admin.initialize_app(cred, name=env_name)
        
    db = firestore.client(app=app)
    
    print("Cancellazione 'nuovi codici consegna' (clienti in attesa dati)...")
    nuovi_ref = db.collection('clienti').document('CATTEL').collection('nuovi codici consegna')
    docs = nuovi_ref.stream()
    deleted = 0
    for doc in docs:
        doc.reference.delete()
        deleted += 1
    print(f"-> Cancellati {deleted} clienti in attesa di mappatura.")
    
    print("Cancellazione eventuali 'nuovi orari mancanti'...")
    orari_ref = db.collection('clienti').document('CATTEL').collection('nuovi orari mancanti')
    docs_o = orari_ref.stream()
    deleted_o = 0
    for doc in docs_o:
        doc.reference.delete()
        deleted_o += 1
    print(f"-> Cancellati {deleted_o} record di orari in attesa.")
    
    # Cancelliamo anche eventuali pending processing_jobs per essere totalmente puliti
    print("Cancellazione processing_jobs residui...")
    jobs_ref = db.collection('clienti').document('CATTEL').collection('processing_jobs')
    docs_j = jobs_ref.stream()
    deleted_j = 0
    for doc in docs_j:
        doc.reference.delete()
        deleted_j += 1
    print(f"-> Cancellati {deleted_j} processing jobs.")

# Eseguiamo per Sviluppo
pulisci_anomalie('SVILUPPO', 'dev_key.json')

# Eseguiamo per Produzione
pulisci_anomalie('PRODUZIONE', 'prod_key.json')

