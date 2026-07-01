import firebase_admin
from firebase_admin import credentials, storage
import json

try:
    # Initialize firebase_admin if not already initialized
    if not firebase_admin._apps:
        firebase_admin.initialize_app(options={
            'storageBucket': 'log-solution-60007.appspot.com'
        })
    
    bucket = storage.bucket()
    blob = bucket.blob("REPORTS/30-06-2026/viaggi_giornalieri_Johnson.json")
    if blob.exists():
        data = json.loads(blob.download_as_string().decode('utf-8'))
        print("CLIENTE:", data.get('cliente') if isinstance(data, dict) else "LEGACY ARRAY")
        print("\nVIAGGI:")
        zone = data.get('zone', data) if isinstance(data, dict) else data
        for z in zone:
            print(f"- ID: {z.get('id_zona')}, Nome: {z.get('nome_giro')}, Has Stats: {z.get('_stats') is not None}, stats.is_gc: {z.get('_stats', {}).get('is_gc') if z.get('_stats') else 'No Stats'}, Punti: {len(z.get('lista_punti', []))}")
    else:
        print("File non trovato su Storage per il 30-06-2026.")
except Exception as e:
    print("Errore:", e)
