import firebase_admin
from firebase_admin import credentials, firestore

key_path = r'g:\Il mio Drive\AppLogSolution\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json'
if not firebase_admin._apps:
    firebase_admin.initialize_app(credentials.Certificate(key_path))

db = firestore.client()

def list_and_reset_viaggi():
    viaggi_ref = db.collection('viaggi')
    docs = viaggi_ref.stream()
    
    count = 0
    for doc in docs:
        count += 1
        print(f"Eliminando viaggio: {doc.id}")
        
        # Elimina sottocollezione logs
        logs_ref = doc.reference.collection('logs')
        logs = logs_ref.stream()
        for log in logs:
            log.reference.delete()
            
        # Elimina documento principale
        doc.reference.delete()
        
    print(f"Reset completato. Eliminati {count} viaggi.")

if __name__ == "__main__":
    list_and_reset_viaggi()
