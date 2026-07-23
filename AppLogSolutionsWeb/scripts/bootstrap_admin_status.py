import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import sys
import os

def main():
    if '--confirm' not in sys.argv:
        print("MODALITA' DRY-RUN (aggiungi --confirm per scrivere sul database)")
        dry_run = True
    else:
        dry_run = False

    try:
        cred = credentials.Certificate('../functions/serviceAccountKey.json')
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Errore caricamento serviceAccountKey: {e}. Provo con credenziali default GCP...")
        try:
            firebase_admin.initialize_app()
        except ValueError:
            pass # already initialized

    # Sicurezza: Deve operare solo su sviluppo
    try:
        project_id = firebase_admin.get_app().project_id
    except Exception:
        # Se non riesce a leggerlo, assicura che lo chieda.
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    if project_id != 'log-solutions-sviluppo':
        print(f"ERRORE CRITICO: Sei connesso a {project_id}. Questo script PUO' ESSERE ESEGUITO SOLO SU log-solutions-sviluppo.")
        sys.exit(1)
        
    print(f"Connesso al progetto: {project_id}")

    db = firestore.client()
    
    print("Ricerca amministratori attuali...")
    docs = db.collection('dipendenti').where('ruolo', '==', 'amministratore').stream()
    
    admin_uids = []
    print("\n--- Amministratori Rilevati ---")
    for doc in docs:
        data = doc.to_dict()
        uid = doc.id
        nome = data.get('nome', 'Sconosciuto')
        cognome = data.get('cognome', '')
        email = data.get('email', '')
        masked_email = email.split('@')[0][:3] + "***@" + email.split('@')[-1] if '@' in email else email
        print(f"- UID: {uid} | Nome: {nome} {cognome} | Email: {masked_email}")
        admin_uids.append(uid)
        
    if len(admin_uids) == 0:
        print("\nERRORE: Nessun amministratore rilevato nel database! Impossibile creare un registro vuoto.")
        sys.exit(1)
        
    print(f"\nTotale amministratori: {len(admin_uids)}")
    
    if dry_run:
        print("\n[DRY-RUN] Nessuna modifica apportata. Esegui 'python bootstrap_admin_status.py --confirm' per salvare.")
    else:
        print("\nSalvataggio registro in config/system_status...")
        db.collection('config').document('system_status').set({
            'admins': admin_uids
        }, merge=True)
        print("FATTO! Registro amministratori creato con successo.")

if __name__ == "__main__":
    main()
