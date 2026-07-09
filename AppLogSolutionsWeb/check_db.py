import firebase_admin
from firebase_admin import credentials, firestore

def check_db(key_path, env_name):
    print(f"\n--- CONTROLLO {env_name} ---")
    try:
        cred = credentials.Certificate(key_path)
        app = firebase_admin.initialize_app(cred, name=env_name)
        db = firestore.client(app=app)
        
        docs = db.collection('clienti').document('CATTEL').collection('raccolta clienti').where('cliente', '==', 'DALIE E FAGIOLI IL FUNGO').stream()
        found = False
        for doc in docs:
            found = True
            data = doc.to_dict()
            print(f"ID: {doc.id}")
            print(f"Nome: {data.get('cliente')}")
            print(f"Codice Frutta: {data.get('codice_frutta')}")
            print(f"Codice Latte: {data.get('codice_latte')}")
        
        if not found:
            print("Cliente non trovato con campo 'cliente'. Cerco in tutti...")
            all_docs = db.collection('clienti').document('CATTEL').collection('raccolta clienti').stream()
            for doc in all_docs:
                d = doc.to_dict()
                name = d.get('cliente') or d.get('nome_consegna') or ''
                if 'DALIE E FAGIOLI IL FUNGO' in name.upper():
                    print(f"ID: {doc.id}")
                    print(f"Nome Trovato: {name}")
                    print(f"Codice Frutta: {d.get('codice_frutta')}")
                    print(f"Codice Latte: {d.get('codice_latte')}")
    except Exception as e:
        print(f"Errore: {e}")

check_db('prod_key.json', 'PRODUZIONE')
check_db('dev_key.json', 'SVILUPPO')
