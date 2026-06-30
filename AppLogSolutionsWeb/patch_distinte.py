import os
import json
import firebase_admin
from firebase_admin import credentials, firestore, storage
from urllib.request import urlopen

if not firebase_admin._apps:
    cred = credentials.Certificate(r"C:\Users\Diego\Documents\antigravity\elegant-goodall\log-solution-60007-firebase-adminsdk-h4g9o-c46fa673eb.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket': 'log-solution-60007.firebasestorage.app'
    })

db = firestore.client()
bucket = storage.bucket()

def patch_distinta_urls():
    # Trova tutti i viaggi
    viaggi_ref = db.collection('clienti').document('DNR').collection('viaggi ddt')
    docs = viaggi_ref.stream()
    
    for doc in docs:
        data = doc.to_dict()
        if not data.get("distinta_light"):
            # try to find it in storage manifest
            date_str = data.get("data")
            if not date_str: continue
            
            date_formatted = date_str.replace("/", "-")
            manifest_blob = bucket.blob(f"REPORTS/{date_formatted}/manifest_link_viaggi.json")
            if manifest_blob.exists():
                manifest_json = manifest_blob.download_as_text()
                try:
                    manifest = json.loads(manifest_json)
                    for m in manifest:
                        if m.get("v_id") == doc.id:
                            d_light = m.get("distinta_light")
                            d_comp = m.get("distinta_completa")
                            if d_light:
                                doc.reference.update({
                                    "distinta_light": d_light,
                                    "distinta_completa": d_comp
                                })
                                print(f"Patched {doc.id} with distinta_light")
                except:
                    pass

if __name__ == "__main__":
    patch_distinta_urls()
    print("Done")
