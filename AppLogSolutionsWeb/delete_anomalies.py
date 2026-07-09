import firebase_admin
from firebase_admin import credentials, firestore

def count_and_delete(project_id, cred_path):
    print(f"\n--- Project: {project_id} ---")
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_path)
            app = firebase_admin.initialize_app(cred)
        elif len(firebase_admin._apps) == 1 and list(firebase_admin._apps.keys())[0] != '[DEFAULT]':
            cred = credentials.Certificate(cred_path)
            app = firebase_admin.initialize_app(cred, name=project_id)
        else:
            app = firebase_admin.get_app() # if it's the same or we need to manage multiple apps better
            # To be safe, just delete and re-init
            firebase_admin.delete_app(app)
            cred = credentials.Certificate(cred_path)
            app = firebase_admin.initialize_app(cred)
            
        db = firestore.client(app=app)
        
        # Check DNR
        docs = db.collection('clienti').document('DNR').collection('nuovi codici consegna').where("tipo", "==", "CATTEL").stream()
        count = 0
        batch = db.batch()
        
        for doc in docs:
            count += 1
            batch.delete(doc.reference)
            
        print(f"Found {count} anomalies for CATTEL in DNR. Committing delete...")
        if count > 0:
            batch.commit()
            print("Deleted successfully.")
            
    except Exception as e:
        print(f"Error: {e}")

count_and_delete('log-solutions-sviluppo', r'C:\Users\Diego\Documents\antigravity\elegant-goodall\backend\config\log-solutions-sviluppo-firebase-adminsdk-j679b-2abda85d7b.json')
count_and_delete('log-solution-60007', r'C:\Users\Diego\Documents\antigravity\elegant-goodall\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json')
