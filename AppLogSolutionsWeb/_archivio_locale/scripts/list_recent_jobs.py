import sys
sys.path.append('g:\\Il mio Drive\\App\\AppLogSolutionsWeb\\functions')
import main
import datetime

def list_jobs():
    db = main.get_db()
    for t in ['DNR', 'GRAN CHEF', 'CATTEL']:
        print(f"--- TENANT {t} ---")
        docs = db.collection('clienti').document(t).collection('processing_jobs').order_by('created_at', direction=main.firestore.Query.DESCENDING).limit(3).stream()
        for d in docs:
            jd = d.to_dict()
            print(f"Job ID: {d.id}")
            print(f" - Created At: {jd.get('created_at')}")
            print(f" - Status: {jd.get('status')}")
            print(f" - Message: {jd.get('message')}")
            print(f" - Error: {jd.get('error_message')}")
            print(f" - Storage Path: {jd.get('storage_path')}")
            print(f" - PDF Generati: {jd.get('pdf_generati')}")
            print(f" - Tipo: {jd.get('type')}")
            print("-----------------------")

if __name__ == "__main__":
    list_jobs()
