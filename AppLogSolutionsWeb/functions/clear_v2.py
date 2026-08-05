import os
import sys
# Aggiungi il path corrente al sys.path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from infrastructure import firebase_setup

# Svuoto il dizionario in memoria
firebase_setup._LOCAL_STORAGE_CACHES["directions_cache_v2.json"] = {}
firebase_setup._INITIAL_CACHE_COUNTS["directions_cache_v2.json"] = 0

# Salvo sul cloud (sovrascrivendo con file vuoto)
try:
    firebase_setup.save_storage_cache("directions_cache_v2.json")
    print("Cache directions_cache_v2.json svuotata con successo sul cloud!")
except Exception as e:
    print(f"Errore durante lo svuotamento: {e}")
